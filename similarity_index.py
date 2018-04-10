import itertools

def ngram(word, n):
    wordlist = list(word)
    k0gram = [''.join(gram) for gram in \
                zip(*[wordlist[i:] for i in range(n)])]
    if len(k0gram) == 1:
        k0gram.append(k0gram[0] + '$')
        k0gram[0] = '$' + k0gram[0]
    elif (len(k0gram) > 1):
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