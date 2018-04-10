import json
from collections import defaultdict
import itertools
import numpy as np

# jsonfile = open('lexnorm2015/train_data.json', 'r')
# tweets = json.load(jsonfile)
# jsonfile.close()

# static_map = defaultdict(set)
# for tweet in tweets:
#     for (input_word, output_word) in zip(tweet['input'], tweet['output']):
#         if input_word.lower() != output_word.lower() and output_word != '':
#             static_map[input_word].add(output_word)

# for key,values in static_map.items():
#     print("%s: %s" % (key, values))

# index = ngram.NGram(N=2, pad_len=1)
# print(list(index.ngrams(index.pad('abc'))))

def ngram(word, n):
    wordlist = list(word)
    k0gram = [''.join(gram) for gram in \
                zip(*[wordlist[i:] for i in range(n)])]
    if (len(k0gram) > 0):
        k0gram[0] = '$' + k0gram[0]
        k0gram[-1] = k0gram[-1] + '$'
    return set(k0gram)

def skipgram(word, n, k):
    wordlist = list(word)
    kngram = [list(set(['|'.join(gram) for gram in \
                zip(*[wordlist[(i * (skip + 1)):] for i in range(n)])])) \
                for skip in range(1, k + 1)]
    return set(itertools.chain.from_iterable(kngram))

def sim_feature(word, n=2, k=1):
    return set(itertools.chain.from_iterable([list(ngram(word, n))] + [list(skipgram(word, n, k))]))

def JaccardIndex(s1, s2, n=2, k=1, tailWeight=3):
    feature1 = sim_feature(s1, n, k)
    feature2 = sim_feature(s2, n, k)
    intersection = feature1.intersection(feature2)
    intersection_len = len(intersection)
    union = feature1.union(feature2)
    union_len = len(union)
    startWeight = 0
    endWeight = 0
    for gram in intersection:
        if gram.startswith('$'):
            startWeight = tailWeight - 1
            continue
        if gram.endswith('$'):
            endWeight = tailWeight - 1
            continue
    return (intersection_len + startWeight + endWeight) / (union_len + startWeight + endWeight)

print(JaccardIndex('love', 'looove'))