import subprocess
import os
import csv
from collections import defaultdict
import numpy as np
from similarity_index import JaccardIndex

def generateMap(tweets):
    static_map = defaultdict(set)
    support_map = defaultdict(int)
    confidence_map = defaultdict(lambda: defaultdict(float))
    index_map = defaultdict(lambda: defaultdict(float))
    for tweet in tweets:
        for (input_word, output_word) in zip(tweet['input'], tweet['output']):
            input_word = input_word.lower()
            output_word = output_word.lower()
            if input_word != output_word and output_word != '':
                static_map[input_word].add(output_word)
                confidence_map[input_word][output_word] += 1
            support_map[input_word] += 1
    for key, values in static_map.items():
        confidence_map[key] = {k: v / support_map[key] for k, v in confidence_map[key].items()}
        index_map[key] = {k: JaccardIndex(k, key) for k in values}
        print(("%d %s: %s ; " % (support_map[key], key, values)) + str(confidence_map[key].items()) + str(index_map[key]))
    return static_map, support_map, confidence_map, index_map

def generatePOSConfidence(tweets, containOutput=False):
    serialized = '\n'.join([' '.join(words['input']) for words in tweets])
    file = open('tmp.txt', 'w')
    file.write(serialized)
    file.close()
    result = subprocess.check_output(('./ark-tweet-nlp-0.3.2/runTagger.sh', './tmp.txt')).decode('utf-8')
    os.remove('tmp.txt')
    file = open('tagged.txt', 'w')
    file.write(result)
    file.close()
    tsv = csv.reader(open('tagged.txt', 'r'), delimiter='\t')
    idx = 0
    drop = 0
    mappedTweets = []
    for row in tsv:
        if (len(row) < 4):
            row = row[0].split('\t')
        tag = row[1].split()
        prob = np.array(list(map(float, row[2].split())))
        tweet = list(map(str.lower, tweets[idx]['input']))
        norm_tweet = None
        if containOutput:
            norm_tweet = tweets[idx]['output']
        idx += 1
        if not (len(tag) == len(prob) and len(tag) == len(tweet)):
            print(tweet)
            print(row)
            drop += 1
            continue
        assert len(tag) == len(prob) and len(tag) == len(tweet), 'Wrong length'
        newtweet = {'mean': np.mean(prob), 'tag': tag, 'prob': prob, 'input': tweet,}
        if containOutput:
            newtweet['output'] = norm_tweet
        mappedTweets.append(newtweet)
    os.remove('tagged.txt')
    print('Dropped %d' % drop)
    return mappedTweets

def generateCandidates(mappedTweets, maps):
    # (before_mean, before_conf, support, confidence, sim_index, len_ti, len_c, diff_len)
    static_map, support_map, confidence_map, index_map = maps

def generateModifiedTweet(tweets, maps):
    static_map, support_map, confidence_map, index_map = maps
