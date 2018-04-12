import json
from generate_feature import generateMap, generatePOSConfidence

jsonfile = open('lexnorm2015/train_data.json', 'r')
rawtweets = json.load(jsonfile)
jsonfile.close()

tweets = generatePOSConfidence(rawtweets)
print(generateMap(tweets))