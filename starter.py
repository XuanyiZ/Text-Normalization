import json
import pickle
from generate_feature import generateMap, generatePOSConfidence, generateCandidates, generateFeatureVectors

jsonfile = open('lexnorm2015/dummy2_data.json', 'r')
rawtweets = json.load(jsonfile)
jsonfile.close()

maps = generateMap(rawtweets)
print('Generated static map')
# _, tweets = generatePOSConfidence(rawtweets, True)
# print('Tagged primary tweets')
# candidateTweets = generateCandidates(tweets, maps)
# print('Candidates are enumerated')
# notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
# print('Tagged all candidate tweets')
# training_set = generateFeatureVectors(notDroppedTweets, featureTweets)
# print('Generated feature vectors')

# with open('training', 'wb') as fp:
#     pickle.dump(training_set, fp)
#     print('Saved')
# with open('training', 'rb') as fp:
#     _ = pickle.load(fp)
