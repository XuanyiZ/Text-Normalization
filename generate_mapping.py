from collections import defaultdict
from similarity_index import JaccardIndex
import re, os

path = os.path.dirname(os.path.abspath(__file__))

"""
Create mapping from training data. Static map is all the mappings 
from token to its normalized form. Support map counts the times a 
token appears. Confidence map is the frequency counting for each 
normalized form when a token appears. Index map is the Jaccard index 
between token and the normalized form.
"""
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
    return static_map, support_map, confidence_map, index_map

"""
Augment the mappings with EMNLP dataset.
"""
def augmentMapUsingEMNLP(maps):
    static_map, support_map, confidence_map, index_map = maps
    file = open(path + '/emnlp2012-lexnorm/emnlp_dict.txt', 'r')
    pairs = file.read().split()
    file.close()
    for i in range(int(len(pairs) / 2)):
        input_word = pairs[i * 2].lower()
        output_word = pairs[i * 2 + 1].lower()
        static_map[input_word].add(output_word)
        support_map[input_word] += 1
        confidence_map[input_word][output_word] += 1
        index_map[input_word][output_word] = JaccardIndex(input_word, output_word)
    return static_map, support_map, confidence_map, index_map

"""
Augment the mappings with Fei Liu's dataset.
"""
def augmentMapUsingFeiLiu(maps):
    static_map, support_map, confidence_map, index_map = maps
    lines = [line.rstrip('\n') for line in open('Text_Norm_Data_Release_Fei_Liu/Test_Set_3802_Pairs.txt')]
    tokens = [list(map(str.strip, re.split(r'[\t\|]', l))) for l in lines]
    for token in tokens:
        input_word = token[1]
        support_map[input_word] += int(token[0])
        for output_word in token[2:]:
            static_map[input_word].add(output_word)
            confidence_map[input_word][output_word] += 1
            index_map[input_word][output_word] = JaccardIndex(input_word, output_word)
    return static_map, support_map, confidence_map, index_map

"""
Convert to normal dictionary in Python for saving later.
"""
def consolidateMap(maps):
    static_map, support_map, confidence_map, index_map = maps
    return dict(static_map), dict(support_map), {k: dict(v) for k, v in confidence_map.items()}, {k: dict(v) for k, v in index_map.items()}
