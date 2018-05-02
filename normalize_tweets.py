import json, sys, os
import pickle
from collections import defaultdict
from generate_mapping import *
from generate_pos_info import *
from generate_candidate import *
from generate_feature import *
from load_store_data import *
from predictor import *

path = os.path.dirname(os.path.abspath(__file__))

with open(path + '/mapping_unconstrained', 'rb') as fp:
    maps = pickle.load(fp)

def read_in():
    lines = sys.stdin.readlines()
    return lines[0]

def mapATweet(tweet):
    mappedTweet = initWithPOS([tweet])
    candidateTweets = generateCandidates(mappedTweet, maps, True, False)
    notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
    dataset = generateFeatureVectors(notDroppedTweets, featureTweets)
    tweet_idx, indices, categories, tokens, features, labels = map(np.array, dataset)

    group_ix, tokens, features, labels = load_dataset(tweet_idx, indices, tokens, features, labels)
    model = load_model()
    predicted = model.predict(group_ix, features)
    return mappedTweet[0]['input'], list(tokens[predicted])

if __name__ == '__main__':
    tweet = read_in()
    original, normalized = mapATweet(tweet)
    for t in original:
        print(t)
    for t in normalized:
        print(t)
