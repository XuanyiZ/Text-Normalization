import json
import pickle
from collections import defaultdict
from generate_mapping import *
from generate_pos_info import *
from generate_candidate import *
from generate_feature import *

with open('mapping_unconstrained', 'rb') as fp:
    maps = pickle.load(fp)

def mapATweet(tweet):
    mappedTweet = initWithPOS([tweet])
    candidateTweets = generateCandidates(mappedTweet, maps, True, False)
    notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
    tweet_idx, indices, categories, tokens, features, _ = generateFeatureVectors(notDroppedTweets, featureTweets)
    print('\n'.join([str(i) + ' ' + str(j) + ' ' + c + ' ' + t + ' ' + str(f) for (i, j, c, t, f) 
                        in zip(tweet_idx, indices, categories, tokens, features)]))
    # TODO using 'features' to classify, categories may help. Substitute the highest probability one with token
    #      and ' '.join them to form a new tweet.

if __name__ == '__main__':
    tweet = input()
    mapATweet(tweet)
