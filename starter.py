import json
import pickle
from generate_feature import generateMap, generatePOSConfidence, generateCandidates, generateFeatureVectors

jsonfile = open('lexnorm2015/train_data.json', 'r')
rawtweets = json.load(jsonfile)
jsonfile.close()

maps = generateMap(rawtweets)
print('Generated static map')
_, tweets = generatePOSConfidence(rawtweets, True)
print('Tagged primary tweets')
candidateTweets = generateCandidates(tweets, maps)
print('Candidates are enumerated')
notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
print('Tagged all candidate tweets')
training_set = generateFeatureVectors(notDroppedTweets, featureTweets)
print('Generated feature vectors')


with open('mapping', 'wb') as fp:
    static_map, support_map, confidence_map, index_map = maps
    pickle.dump((
        dict(static_map), 
        dict(support_map), 
        {k: dict(v) for k, v in confidence_map.items()}, 
        {k: dict(v) for k, v in index_map.items()}), fp)
    print('Saved mapping')
with open('training', 'wb') as fp:
    pickle.dump(training_set, fp)
    print('Saved dataset')
# with open('training', 'rb') as fp:
#     _ = pickle.load(fp)
