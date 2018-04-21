import json
import pickle
from collections import defaultdict
from generate_mapping import *
from generate_pos_info import *
from generate_candidate import *
from generate_feature import *

if __name__ == '__main__':
    tweet = input()
    with open('mapping_unconstrained', 'rb') as fp:
        maps = pickle.load(fp)
    mappedTweet = initWithPOS([tweet])
    candidateTweets = generateCandidates(mappedTweet, maps, True, False)
    notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
    categories, tokens, features, _ = generateFeatureVectors(notDroppedTweets, featureTweets)
    print('\n'.join([c + ' ' + t + ' ' + str(f) for (c, t, f) in zip(categories, tokens, features)]))
    # TODO using 'features' to classify, categories may help. Substitute the highest probability one with token
    #      and ' '.join them to form a new tweet.
