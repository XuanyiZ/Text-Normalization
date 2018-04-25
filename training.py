from predictor import Predictor
from load_store_data import *
from sklearn.ensemble import RandomForestClassifier

if __name__ =='__main__':
    # update model_trained
    group_ix, tokens, features, labels= load_dataset_from_file('training')
    classifier = RandomForestClassifier(n_estimators=20, n_jobs=-1, class_weight="balanced")
    model = Predictor(classifier)
    model.fit(features, labels)
    save_model(model)

    # get prediction
    for test_file in ['testing_constrained', 'testing_unconstrained']:
        group_ix, tokens, features, labels = load_dataset_from_file(test_file)
        stats = model.score(group_ix, features, labels)
        print('precision: {}, recall: {}, f1-score: {}'.format(*stats))

    # get prediction from constrained mode for first 3 tweets:
    group_ix, tokens, features, labels = load_dataset_from_file('testing_constrained')
    predicted = model.predict(group_ix, features)
    new_tokens, new_group_ix = tokens[predicted], sorted(set(group_ix))
    for j in range(0, 3):
        print(' '.join(new_tokens[[ix for (ix,i) in enumerate(new_group_ix) if i[0] == j]]))