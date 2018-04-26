import numpy as np
from sklearn.metrics import precision_recall_fscore_support

class Predictor():
    """
    Binary predictor for candidate evaluation
    """

    def __init__(self, classifier):
        self.classifier = classifier

    def fit(self, features, labels):
        self.classifier.fit(features, labels)
        return self

    def predict(self, group_ix, features):
        """
        The whole data set should already be sorted by group_ix
        predict by select just one canonical form for each group_ix
        When labels are identical, default use the first column of training data to break tie
        """
        assert (all(group_ix[i] >= group_ix[i - 1] for i in range(1, len(group_ix))))

        predicted = self.classifier.predict(features)
        # choose best based on group id next
        diff_ixs = [0]+[i for i in range(1,len(group_ix)) if group_ix[i]!=group_ix[i-1]]+[len(group_ix)]
        result = np.zeros(predicted.shape, dtype=bool)
        for i in range(1, len(diff_ixs)):
            best_ix, _ = max(enumerate([(predicted[j], features[j][0]) for j in range(diff_ixs[i - 1], diff_ixs[i])]),
                             key=lambda x: x[1])
            result[best_ix+diff_ixs[i-1]] = 1
        return result

    def score(self, group_ix, features, labels):
        """
        The whole data set should already be sorted by group_ix
        return precision recall and f1_score for testing_data
        """
        res = self.predict(group_ix, features)
        return precision_recall_fscore_support(y_true=labels, y_pred=res, average='binary', pos_label=1)[:3]