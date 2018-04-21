import os
import subprocess
import csv
import numpy as np

def initWithPOS(tweets):
    serialized = '\n'.join(tweets)
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
        tweet = list(map(str.lower, row[0].split()))
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
        mappedTweets.append(newtweet)
        idx += 1
    os.remove('tagged.txt')
    return mappedTweets

def generatePOSConfidence(tweets):
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
        if 'output' in tweets[idx]:
            newtweet['output'] = tweets[idx]['output']
        mappedTweets.append(newtweet)
        originalTweets.append(tweets[idx])
        idx += 1
    os.remove('tagged.txt')
    print('Dropped %d' % drop)
    return originalTweets, mappedTweets