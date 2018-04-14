import json
from generate_feature import generateMap, generatePOSConfidence, generateCandidates, generateFeatureVectors

jsonfile = open('lexnorm2015/dummy_data.json', 'r')
rawtweets = json.load(jsonfile)
jsonfile.close()

maps = generateMap(rawtweets)
tweets = generatePOSConfidence(rawtweets, True)
candidateTweets = generateCandidates(tweets, maps)
# for vec in candidateTweets:
#     print(str(vec))
featureTweets = generatePOSConfidence(candidateTweets)
t, l = generateFeatureVectors(candidateTweets, featureTweets)
for (tt, ll) in zip(t, l):
    print(str(tt) + '   ' + str(ll))