from collections import defaultdict
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

def generateInitialPOSConfidence(tweets):
    serialized = '\n'.join([' '.join(words['input']) for words in tweets])
    print(serialized)

def generateModifiedTweet(tweets, maps):
    static_map, support_map, confidence_map, index_map = maps
