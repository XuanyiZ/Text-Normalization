import pickle
import numpy as np
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier


if __name__ == '__main__':

    with open('training', 'rb') as fp:
        features, labels = map(np.array, pickle.load(fp))
    features = features[:, :8].astype(float)
    print('Receiving feature of shape: {}, label of shape: {}'.format(features.shape, labels.shape))

    classifier = RandomForestClassifier(n_estimators=20, n_jobs=-1)
    predicted = cross_val_predict(classifier, features, labels, cv=10, n_jobs=-1)
    stats = precision_recall_fscore_support(y_true=labels, y_pred=predicted, average='binary', pos_label=1)[:3]
    print('precision: {}, recall: {}, f1-score: {}'.format(*stats))
