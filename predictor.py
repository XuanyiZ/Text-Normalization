import numpy as np
from sklearn.metrics import precision_recall_fscore_support

class Predictor():
    """
    Binary predictor for candidate evaluation
    Input data should be consist of group_ix, features and labels of same length
    When labels are identical, default use the first column of training data to break tie
    """

    def __init__(self, classifier):
        self.classifier = classifier

    def fit(self, training_data):
        _, features, labels = training_data
        self.classifier.fit(features, labels)

    def predict(self, data):
        group_ix, features, _ = data
        order = group_ix.argsort()
        group_ix, features = group_ix[order], features[order]
        predicted = self.classifier.predict(features)
        # choose best based on group id next
        diff_ixs = [0]+[i for i in range(1,len(group_ix)) if group_ix[i]!=group_ix[i-1]]
        result = np.zeros(predicted.shape)
        for i in range(1, len(diff_ixs)):
            best_ix, _ = max(enumerate([(predicted[j], features[j][0]) for j in range(diff_ixs[i - 1], diff_ixs[i])]),
                             key=lambda x: x[1])
            result[best_ix+diff_ixs[i-1]] = 1
        return result

    def score(self, testing_data):
        """return precision recall and fscore for testing_data"""
        _,_,labels = testing_data
        res = self.predict(testing_data)
        return precision_recall_fscore_support(y_true=labels, y_pred=res, average='binary', pos_label=1)[:3]