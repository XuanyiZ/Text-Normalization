"""
Generate feature vectors, and the corresponding properties and labels. 
See generateCandidates for explaination about properties.
"""
def generateFeatureVectors(candidateTweets, TaggedTweets):
    assert len(candidateTweets) == len(TaggedTweets), 'Not matching in length, cannot compose'
    tweet_id = []
    indices = []
    category = []
    token = []
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
        indices.append(idx)
        tweet_id.append(ctweet['tweet_idx'])
        training.append(feature)
        label.append(ctweet['label'])
        category.append(ctweet['category'])
        token.append(ctweet['token'])
    return tweet_id, indices, category, token, training, label
