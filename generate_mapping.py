from collections import defaultdict
from similarity_index import JaccardIndex
import re

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

def augmentMapUsingEMNLP(maps):
    static_map, support_map, confidence_map, index_map = maps
    file = open('emnlp2012-lexnorm/emnlp_dict.txt', 'r')
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

def consolidateMap(maps):
    static_map, support_map, confidence_map, index_map = maps
    return dict(static_map), dict(support_map), {k: dict(v) for k, v in confidence_map.items()}, {k: dict(v) for k, v in index_map.items()}
