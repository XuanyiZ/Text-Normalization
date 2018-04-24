import pickle
import numpy as np

# in the format of ., confidence, 6., categorical, categorical
def load_dataset(file_name, categories=None):

    def one_hot_encode(data, ixs):
        assert(all(np.array(ixs)>=0))
        for i in ixs:
            records = np.zeros((len(data), len(categories)))
            for row_ix, elem in enumerate(data[:, i]):
                records[row_ix, np.where(categories == elem)] = 1
            data = np.concatenate((data, records), axis=1)
        return np.delete(data, ixs, axis=1).astype(float)

    with open(file_name,'rb') as f:
        tweet_ix, ix, _, token,  features, labels = map(np.array, pickle.load(f))
    features[:,1], features[:,0] = features[:,0], features[:,1].copy()

    if categories == None:
        # all the POS_taggings I can find
        categories = np.array(['','!','#','$','&',',','@','A','D','E','G','L','N','O','P','R','S','T','U','V','X','Y','Z','^','~'])
    features = one_hot_encode(features,[8,9])
    group_ix, features, labels = tweet_ix.astype(int), features.astype(float), labels.astype(int)

    print(group_ix[:10])
    print(len(np.unique(group_ix)), sum(labels), np.unique(labels))
    return group_ix, features, labels



def save_model(model, file_name='model_trained'):
    with open(file_name,'wb') as f:
        pickle.dump(model,f)

def load_model(file_name='model_trained'):
    with open(file_name, 'rb') as f:
        return pickle.load(f)
