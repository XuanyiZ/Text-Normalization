import json
import pickle
from collections import defaultdict
from generate_mapping import *
from generate_pos_info import *
from generate_candidate import *
from generate_feature import *

print('=============TRAINING SET GENERATION=============')
# Generate Training dataset
rawtweets = []
try:
    jsonfile = open('lexnorm2015/train_data.json', 'r')
    rawtweets.append(json.load(jsonfile))
finally:
    jsonfile.close()
try:
    jsonfile = open('twimalizer/augmentData.json', 'r')
    rawtweets.append(json.load(jsonfile))
except:
    pass
finally:
    jsonfile.close()

constrained_maps = generateMap(rawtweets)
maps = consolidateMap(constrained_maps)
print('Generated static map')
_, tweets = generatePOSConfidence(rawtweets)
print('Tagged primary tweets')
candidateTweets = generateTrainingCandidates(tweets, maps, False)
print('Candidates are enumerated')
notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
print('Tagged all candidate tweets')
training_set = generateFeatureVectors(notDroppedTweets, featureTweets)
print('Generated feature vectors')

with open('mapping_constrained', 'wb') as fp:
    pickle.dump(maps, fp)
    print('Saved mapping')
with open('training', 'wb') as fp:
    pickle.dump(training_set, fp)
    print('Saved dataset')
print('=======================DONE=======================\n')


print('=============CONSTRAINED TEST GENERATION=============')
# Generate constrained testing dataset
rawtweets = []
try:
    jsonfile = open('lexnorm2015/test_truth.json', 'r')
    rawtweets.append(json.load(jsonfile))
finally:
    jsonfile.close()

_, tweets = generatePOSConfidence(rawtweets)
print('Tagged primary tweets')
candidateTweets = generateCandidates(tweets, maps, True, True)
print('Candidates are enumerated')
notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
print('Tagged all candidate tweets')
training_set = generateFeatureVectors(notDroppedTweets, featureTweets)
print('Generated feature vectors')

with open('testing_constrained', 'wb') as fp:
    pickle.dump(training_set, fp)
    print('Saved dataset')
print('=========================DONE========================\n')

print('=============UNCONSTRAINED TEST GENERATION=============')
# Generate unconstrained testing dataset
candidateTweets = generateCandidates(tweets, maps, True, False)
print('Candidates are enumerated')
notDroppedTweets, featureTweets = generatePOSConfidence(candidateTweets)
print('Tagged all candidate tweets')
training_set = generateFeatureVectors(notDroppedTweets, featureTweets)
print('Generated feature vectors')

with open('testing_unconstrained', 'wb') as fp:
    pickle.dump(training_set, fp)
    print('Saved dataset')
print('=========================DONE==========================\n')

print('=============AUGMENT MAPPING=============')
# Generate unconstrained mapping
unconstrained_maps = consolidateMap(augmentMapUsingFeiLiu(augmentMapUsingEMNLP(constrained_maps)))
with open('mapping_unconstrained', 'wb') as fp:
    pickle.dump(unconstrained_maps, fp)
    print('Saved mapping')
print('==================DONE==================')
