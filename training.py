from predictor import Predictor
from load_store_data import *
from sklearn.ensemble import RandomForestClassifier

if __name__ =='__main__':
    # update model_trained
    training_dataset = load_dataset('training')
    classifier = RandomForestClassifier(n_estimators=20, n_jobs=-1, class_weight="balanced")
    model = Predictor(classifier)
    model.fit(training_dataset)
    save_model(model)

    # get prediction
    for test_file in ['testing_constrained', 'testing_unconstrained']:
        testing_dataset = load_dataset(test_file)
        stats = model.score(testing_dataset)
        print('precision: {}, recall: {}, f1-score: {}'.format(*stats))

