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
        index_map[key] = {k: JaccardIndex(k, key) for k in values}
        # print(("%d %s: %s ; " % (support_map[key], key, values)) + str(confidence_map[key]) + str(index_map[key]))
    return dict(static_map), dict(support_map), {k: dict(v) for k, v in confidence_map.items()}, {k: dict(v) for k, v in index_map.items()}

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
    originalTweets = []
    mappedTweets = []
    for row in tsv:
        if (len(row) < 4):
            row = row[0].split('\t')
        tag = row[1].split()
        prob = np.array(list(map(float, row[2].split())))
        tweet = list(map(str.lower, tweets[idx]['input']))
        if len(' '.join(tweet).split()) != len(tag):
            drop += 1
            idx += 1
            continue
        inner_idx = 0
        newProb = []
        newTag = []
        for token in tweet:
            token_len = len(token.split())
            newProb.append(np.mean(prob[inner_idx:inner_idx + token_len]))
            newTag.append(tag[inner_idx])
            inner_idx += token_len
        newtweet = {'mean': np.mean(prob), 'prob': newProb, 'tag': newTag, 'input': tweet}
        if containOutput:
            newtweet['output'] = tweets[idx]['output']
        mappedTweets.append(newtweet)
        originalTweets.append(tweets[idx])
        idx += 1
    os.remove('tagged.txt')
    print('Dropped %d' % drop)
    return originalTweets, mappedTweets

def generateCandidates(mappedTweets, maps, isTraining=True):
    # (before_mean, before_conf, support, confidence, sim_index, len_ti, len_c, diff_len)
    static_map, support_map, confidence_map, index_map = maps
    candidates = []
    for tweet in mappedTweets:
        idx = 0
        for token in tweet['input']:
            token = token.lower()
            right = ''
            if isTraining:
                right = tweet['output'][idx].lower()
            # sum_canonical_occurence = np.sum([v for k, v in confidence_map[token].items()])
            # candidates.append({
            #     'idx': idx, 
            #     'feature': [support_map[token], 
            #                 1 - sum_canonical_occurence / support_map[token], 
            #                 1.0, 
            #                 len(token), 
            #                 len(token), 
            #                 0.0,
            #                 tweet['mean'], 
            #                 tweet['prob'][idx],
            #                 '',
            #                 ''], 
            #     'input': [t for t in tweet['input']], 
            #     'label': 1 if token == right else 0})
            if token in static_map:
                for canonical in static_map[token]:
                    candidates.append({
                        'idx': idx, 
                        'feature': [support_map[token], 
                                    confidence_map[token][canonical], 
                                    index_map[token][canonical], 
                                    len(token), 
                                    len(canonical), 
                                    len(canonical) - len(token),
                                    tweet['mean'], 
                                    tweet['prob'][idx],
                                    '',
                                    ''], 
                        'input': [t if i != idx else canonical for (i, t) in enumerate(tweet['input'])], 
                        'label': 1 if canonical == right else 0})
            idx += 1
    return candidates

def generateFeatureVectors(candidateTweets, TaggedTweets):
    assert len(candidateTweets) == len(TaggedTweets), 'Not matching in length, cannot compose'
    training = []
    label = []
    for (ctweet, ttweet) in zip(candidateTweets, TaggedTweets):
        idx = ctweet['idx']
        feature = ctweet['feature']
        feature[6] = ttweet['mean'] - feature[6]
        feature[7] = ttweet['prob'][idx] - feature[7]
        if idx > 0:
            feature[8] = ttweet['tag'][idx - 1]
        feature[9] = ttweet['tag'][idx]
        training.append(feature)
        label.append(ctweet['label'])
    return training, label
