import pickle
import numpy as np
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier

def load_dataset(f):
    with open(f, 'rb') as fp:
        features, labels = map(np.array, pickle.load(fp))
    features = features[:, :8].astype(float)
    print('Feature shape: {}, label shape: {}, #positive {}'.format(features.shape, labels.shape, sum(labels)))
    return features, labels


if __name__ == '__main__':
    features, labels = load_dataset('training')
    classifier = RandomForestClassifier(n_estimators=20, n_jobs=-1, class_weight="balanced")
    predicted = cross_val_predict(classifier, features, labels, cv=10, n_jobs=-1)
    stats = precision_recall_fscore_support(y_true=labels, y_pred=predicted, average='binary', pos_label=1)[:3]
    print('precision: {}, recall: {}, f1-score: {}'.format(*stats))

    # In case you would like a traditional training and testing
    tfeatures, tlabels = load_dataset('testing')
    classifier.fit(features, labels)
    predicted = classifier.predict(tfeatures)
    stats = precision_recall_fscore_support(y_true=tlabels, y_pred=predicted, average='binary', pos_label=1)[:3]
    print('precision: {}, recall: {}, f1-score: {}'.format(*stats))