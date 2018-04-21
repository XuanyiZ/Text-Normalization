import numpy as np

def generateTrainingCandidates(mappedTweets, maps, includeSelf=False):
    # (before_mean, before_conf, support, confidence, sim_index, len_ti, len_c, diff_len)
    static_map, support_map, confidence_map, index_map = maps
    candidates = []
    tweet_idx = 0
    for tweet in mappedTweets:
        idx = 0
        for token in tweet['input']:
            token = token.lower()
            right = ''
            if 'output' in tweet:
                right = tweet['output'][idx].lower()
            if includeSelf:
                tmp_support = 0
                tmp_confidence = 0
                if token in static_map:
                    tmp_support = support_map[token]
                    sum_canonical_occurence = np.sum([v for k, v in confidence_map[token].items()])
                    tmp_confidence = 1 - sum_canonical_occurence / support_map[token]
                else:
                    if token in support_map:
                        tmp_support = support_map[token]
                        tmp_confidence = 1.0
                    else:
                        tmp_support = 0.0
                        tmp_confidence = 1.0
                candidates.append({
                    'tweet_idx': tweet_idx,
                    'idx': idx,
                    'category': 'self',
                    'token': token,
                    'feature': [tmp_support, 
                                tmp_confidence, 
                                1.0, 
                                len(token), 
                                len(token), 
                                0.0,
                                tweet['mean'], 
                                tweet['prob'][idx],
                                '',
                                ''], 
                    'input': [t for t in tweet['input']], 
                    'label': 1 if token == right else 0})
            if token in static_map:
                for canonical in static_map[token]:
                    candidates.append({
                        'tweet_idx': tweet_idx,
                        'idx': idx, 
                        'category': 'canonical',
                        'token': canonical,
                        'feature': [support_map[token], 
                                    confidence_map[token][canonical] / support_map[token], 
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
        tweet_idx += 1
    return candidates

def isRepetitive(token):
    for i in range(len(token) - 2):
        if token[i] == token[i + 1] and token[i + 1] == token[i + 2]:
            return True
    return False

def generateCandidates(mappedTweets, maps, includeSelf=True, constrained=True):
    # (before_mean, before_conf, support, confidence, sim_index, len_ti, len_c, diff_len)
    static_map, support_map, confidence_map, index_map = maps
    candidates = []
    tweet_idx = 0
    for tweet in mappedTweets:
        idx = 0
        for token in tweet['input']:
            token = token.lower()
            right = ''
            if 'output' in tweet:
                right = tweet['output'][idx].lower()
            if includeSelf:
                tmp_support = 0
                tmp_confidence = 0
                if token in static_map:
                    tmp_support = support_map[token]
                    sum_canonical_occurence = np.sum([v for k, v in confidence_map[token].items()])
                    tmp_confidence = 1 - sum_canonical_occurence / support_map[token]
                else:
                    if token in support_map:
                        tmp_support = support_map[token]
                        tmp_confidence = 1.0
                    else:
                        tmp_support = 0.0
                        tmp_confidence = 1.0
                candidates.append({
                    'tweet_idx': tweet_idx,
                    'idx': idx, 
                    'category': 'self',
                    'token': token,
                    'feature': [tmp_support, 
                                tmp_confidence, 
                                1.0, 
                                len(token), 
                                len(token), 
                                0.0,
                                tweet['mean'], 
                                tweet['prob'][idx],
                                '',
                                ''], 
                    'input': [t for t in tweet['input']],
                    'label': 1 if token == right else 0})
            if token in static_map:
                sorted_index = sorted(((v, k) for k, v in index_map[token].items()), reverse=True)
                if constrained:
                    for canonical in static_map[token]:
                        if len(canonical.split()) > 1:
                            candidates.append({
                                'tweet_idx': tweet_idx,
                                'idx': idx, 
                                'category': 'split',
                                'token': canonical,
                                'feature': [support_map[token], 
                                            confidence_map[token][canonical] / support_map[token], 
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
                    if isRepetitive(token):
                        candidates.append({
                            'tweet_idx': tweet_idx,
                            'idx': idx, 
                            'category': 'canonical',
                            'token': sorted_index[0][1],
                            'feature': [support_map[token], 
                                        confidence_map[token][sorted_index[0][1]] / support_map[token], 
                                        index_map[token][sorted_index[0][1]], 
                                        len(token), 
                                        len(canonical), 
                                        len(canonical) - len(token),
                                        tweet['mean'], 
                                        tweet['prob'][idx],
                                        '',
                                        ''], 
                            'input': [t if i != idx else sorted_index[0][1] for (i, t) in enumerate(tweet['input'])],
                            'label': 1 if sorted_index[0][1] == right else 0})
                else:
                    for i in range(min(len(sorted_index), 3)):
                        sim, canonical = sorted_index[i]
                        candidates.append({
                            'tweet_idx': tweet_idx,
                            'idx': idx, 
                            'category': 'canonical',
                            'token': canonical,
                            'feature': [support_map[token], 
                                        confidence_map[token][canonical] / support_map[token], 
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
        tweet_idx += 1
    return candidates
