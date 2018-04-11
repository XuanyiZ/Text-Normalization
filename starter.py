import json
from generate_feature import generateMap, generateInitialPOSConfidence

jsonfile = open('lexnorm2015/train_data.json', 'r')
tweets = json.load(jsonfile)
jsonfile.close()

generateInitialPOSConfidence(tweets)