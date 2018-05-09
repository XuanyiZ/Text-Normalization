import os, sys, tempfile
import subprocess
import csv
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

"""
Invoke ark-tweet POS tagger and extend each Tweet object with field 
 - mean (Mean POS tagging confidence)
 - prob (Array of POS tagging confidence for each token)
 - tag (Array of POS tags)
"""
def initWithPOS(tweets):
    serialized = '\n'.join(tweets)
    (tmp_fd, tmp_name) = tempfile.mkstemp()
    file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    file.write(serialized)
    file.close()
    result = subprocess.check_output((path + '/ark-tweet-nlp-0.3.2/runTagger.sh', file.name)).decode('utf-8')
    os.remove(file.name)
    (tmp_fd, tmp_name) = tempfile.mkstemp()
    file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    file.write(result.replace('"', '"""'))
    file.close()
    file = open(file.name)
    tsv = csv.reader(file, delimiter='\t')
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
    file.close()
    os.remove(file.name)
    return mappedTweets

"""
Invoke ark-tweet POS tagger and extend each Tweet object with field 
 - mean (Mean POS tagging confidence)
 - prob (Array of POS tagging confidence for each token)
 - tag (Array of POS tags)

Work only for tweets that normalize to equal or longer in length. 
If normalized tweet is shorter in token count, it is dropped. 
originalTweet contains all legal tweets and mappedTweets is its mapped version.
"""
def generatePOSConfidence(tweets):
    serialized = '\n'.join([' '.join(words['input']) for words in tweets])
    (tmp_fd, tmp_name) = tempfile.mkstemp()
    file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    file.write(serialized)
    file.close()
    result = subprocess.check_output((path + '/ark-tweet-nlp-0.3.2/runTagger.sh', file.name)).decode('utf-8')
    os.remove(file.name)
    (tmp_fd, tmp_name) = tempfile.mkstemp()
    file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    file.write(result.replace('"', '"""'))
    file.close()
    file = open(file.name)
    tsv = csv.reader(file, delimiter='\t')
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
    file.close()
    os.remove(file.name)
    print('Dropped %d' % drop, file=sys.stderr)
    return originalTweets, mappedTweets