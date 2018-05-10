# CS410 Final Project - Tweet Normalizer

## Introduction

The Tweet Normalizer is the implementation of the unconstrained mode of [this paper](http://www.aclweb.org/anthology/W15-4313): NCSU-SAS-Ning: Candidate Generation and Feature Engineering for Supervised Lexical Normalization. Tweets are retrieved by the Twitter API /statuses/filter on the account @TestNormalizer specifically registered for this application. With the training on dataset provided by [this competition](https://noisy-text.github.io/2015/norm-shared-task.html), and static mapping expanded by Lexical normalisation dictionary (found in Resource section in the competition). The application supplies the revision feature, which expand the dataset to enable better normalization.

- [CS410 Final Project - Tweet Normalizer](#cs410-final-project---tweet-normalizer)
    - [Introduction](#introduction)
    - [Setup](#setup)
        - [Set up Python 3 environment](#set-up-python-3-environment)
        - [Set up Electron](#set-up-electron)
        - [Start the application](#start-the-application)
    - [Architecture](#architecture)
        - [Feature Set](#feature-set)
        - [Similarity Index](#similarity-index)
        - [Candidate Generation](#candidate-generation)
            - [Constrained mode](#constrained-mode)
            - [Unconstrained mode](#unconstrained-mode)
        - [Candidate Evaluation](#candidate-evaluation)
    - [Implementation](#implementation)
        - [Normalizer Implementation](#normalizer-implementation)
            - [Dataset generation](#dataset-generation)
            - [Training & testing](#training-testing)
            - [Frontend](#frontend)
        - [GUI Implementation](#gui-implementation)
    - [Training & Testing](#training-testing)

## Setup

*The application only runs on MacOS or Linux.

### Set up Python 3 environment
Make sure Python 3 is installed by `which python3`, and install the required libraries
```
pip install -r requirements.txt
```

### Set up Electron

Install [Node.js and NPM](https://nodejs.org/en/), and install the packages:
```
cd twimalizer
npm install -g electron-forge
npm install --save
```

### Start the application

Stay in twimalizer folder, and run
```
electron-forge start
```

## Architecture

Two-step procedure including candidate generation and candidate evaluation is proposed in the paper.

### Feature Set

The feature set is generated for a token by calculating its n-gram and k-skip-n-gram (In this application the configuration is 2-gram and 1-skip-2 gram). '$' is prepended and appended before and after the first and last n-gram, and '|' is added between skips. For example:

```
love -> { $lo, ov, ve$, l|v, o|e }
```

### Similarity Index

The paper proposed to use Jaccard index as the similarity measure, which is the cardinality ratio of the intersection of two feature sets and their union.

### Candidate Generation

The following are considered possible candidates:
- The token itself
- Words in the mapping
    - Canonical form: transformed word, such as `ur -> your`
    - Split words: a token is split into multiple words, such as `lol -> laugh out loud`

*During testing, token itself is not included.

#### Constrained mode

The following candidates are generated for each token:
- Token itself
- Top scoring canonical form (for repetitive token only, which means the same letter appears three times consecutively)
- Split words (if exists)

#### Unconstrained mode

The following candidates are generated for each token:
- Token itself
- Top 3 scoring words in mapping (no differentiation between canonical form and splitting)

### Candidate Evaluation

#### Feature
For a token t<sub>i</sub> in the tweet T composed of "t<sub>1</sub> t<sub>2</sub> t<sub>3</sub> ... t<sub>i-1</sub> t<sub>i</sub> ... t<sub>n</sub>", candidates for it are associated with the following feature vectors for the classifier to determine if the candidate is the correct form to normalize to.

| Feature                  | Association | Definition                                                                               | Assumption                                                                                            |
| ------------------------ | ----------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Support                  | Token       | The number of times that the token appears during training                               | 0 if the token never appears during training                                                          |
| Confidence               | Candidate   | The probability that the token is normalized to this candidate form during training      | 1 if the corresponding token never appears during training                                            |
| Similarity               | Candidate   | Jaccard index calculated between the token and the candidate                             |                                                                                                       |
| Token Length             | Token       | The length of the token string                                                           |                                                                                                       |
| Candidate Length         | Candidate   | The length of the candidate string                                                       |                                                                                                       |
| Length Difference        | Candidate   | Difference of length between the token and the candidate                                 |                                                                                                       |
| Mean POS Confidence Diff | Candidate   | The change in the mean POS confidence for the whole tweet before and after normalization |                                                                                                       |
| POS Confidence Diff      | Candidate   | The change in POS confidence for the current token before and after normalization        | If the candidate is of multiple words, average POS confidence is used to calculate the change         |
| POS of t<sub>i-1</sub>   | Candidate   | The part-of-speech tagging of the previous token                                         | Empty for the first token                                                                             |
| POS of t<sub>i</sub>     | Candidate   | The part-of-speech tagging of the previous candidate                                     | If the candidate is of multiple words, the POS tagging for the first word is used                     |


#### Classifier

Random forest classifier is used for training. For fitting, simply pass the features and labels to the random forest classifier. For prediction, first, obtain a list of predictions using classifier. Then for each token, among candidates predicted to be correct canonical form, select the one with the highest confidence.

## Implementation

Training data is provided in JSON file, and the basic format for a tweet is the following:
```
{
    'input':  ['token1', 'token2', ...],
    'output': ['token1', 'token2', ...]
}
```
'input' is the original tweet tokenized, 'output' is the tokens normalized with correspondence to 'input'.

### Normalizer Implementation

#### Dataset generation

- `generate_mapping.py`

| Function              | Parameters                                                                                                            | Return                                                                                                                | Description                                                                                                                                                                                                                                                                                                           |
| --------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| generateMap           | tweets:List                                                                                                           | (static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict) | Create the mapping from training data. Static map is all the mappings from token to its normalized form. Support map counts the times a token appears. Confidence map is the frequency count for each normalized form when a token appears. Index map is the Jaccard index between the token and the normalized form. |
| augmentMapUsingEMNLP  | (static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict) | (static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict) | Augment the mappings with EMNLP dataset.                                                                                                                                                                                                                                                                              |
| augmentMapUsingFeiLiu | (static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict) | (static_map,<br> support_map,<br> confidence_map,<br> index_map):(defaultdict, defaultdict, defaultdict, defaultdict) | Augment the mappings with Fei Liu's dataset.                                                                                                                                                                                                                                                                          |
| consolidateMap        | (static_map(defaultdict),<br> support_map(defaultdict),<br> confidence_map(defaultdict),<br> index_map(defaultdict))  | (static_map,<br> support_map,<br> confidence_map,<br> index_map):(dict, dict, dict, dict)                             | Convert to normal dictionary in Python for saving later.                                                                                                                                                                                                                                                              |

- `generate_pos_info.py`


| Function              | Parameters  | Return                                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                    |
| --------------------- | ----------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| initWithPOS           | tweets:List | mappedTweets:List                           | Invoke ark-tweet POS tagger and extend each Tweet object with field `mean` (Mean POS tagging confidence), `prob` (Array of POS tagging confidence for each token), `tag` (Array of POS tags).                                                                                                                                                                                                                                  |
| generatePOSConfidence | tweets:List | (originalTweets, mappedTweets):(List, List) | Invoke ark-tweet POS tagger and extend each Tweet object with field `mean` (Mean POS tagging confidence), `prob` (Array of POS tagging confidence for each token), `tag` (Array of POS tags). Work only for tweets that normalize to equal or longer in length. If the normalized tweet is shorter in the number of tokens, it is dropped. `originalTweet` contains all legal tweets and `mappedTweets` is its mapped version. |

- `similarity_index.py`

| Function     | Parameters                                                                                              | Return       | Description                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------- | ------------ | -------------------------------------------------------------------------- |
| ngram        | word:string<br>ninteger                                                                                 | k0gram:set   | Generate n-gram set. With $ appended (prepended) at the end (beginning).   |
| skipgram     | word:string<br>n:integer<br>k:integer                                                                   | kngram:set   | Generate k-skip-n gram set. With &#124; to separate characters.            |
| sim_feature  | word:string<br>n:integer<br>k:integer(default=1)                                                        | features:set | Generate proposed feature set which combines n-gram and k-skip-n gram.     |
| JaccardIndex | s1:string<br>s2:string<br>n:integer(default=2)<br>k:integer(default=1)<br>tailWeight:integer(default=3) | score:float  | Calculate the Jaccard index between two words.                             |

- `generate_candidate.py`

| Function                   | Parameters                                                                                                     | Return          | Description                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| generateCandidates         | mappedTweets:List<br>maps:(4 dictionaries)<br>includeSelf:bool(default=True)<br>constrained:bool(default=True) | candidates:List | Return a list of mapped candidates, which contain fields original input `input`, whether this is correct form `label`, feature vector `feature`, normalizing token `token`, type of candidate `category` (either `self`, `canonical`, or `split`), tweet index `tweet_idx`, and word index `idx`. If `constrained` is set True, then similarity measure is used only when the word is repetitive, otherwise, top 3 tokens are used. |
| generateTrainingCandidates | mappedTweets:List<br>maps:(4 dictionaries)<br>includeSelf:bool(default=False)                                  | candidates:List | Same as `generateCandidates` except for all possible normalizing tokens are used.                                                                                                                                                                                                                                                                                                                                                   |
| isRepetitive               | token:string                                                                                                   | repetitive:bool | Check whether three same letters appear consecutively.                                                                                                                                                                                                                                                                                                                                                                              |

- `generate_feature.py`

| Function               | Parameters                                   | Return                                                                                     | Description                                                                                                                        |
| ---------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| generateFeatureVectors | (candidateTweets, TaggedTweets):(List, List) | (tweet_id, indices, category, token, training, label):(List, List, List ,List, List, List) | Generate feature vectors, and the corresponding properties and labels. See `generateCandidates` for explaination about properties. |

- `create_dataset.py`

The script that generates the training and testing dataset with all the mappings saved for future use.

#### Training & testing

- `predictor.py`

| Function          | Parameters                                                                            | Return                                                                  | Description                                                                                                                                                        |
| ----------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Predictor         | (classifier):<br>(sklearn.ensemble.RandomForestClassifier)                            | Predictor                                                               | __init__ the class                                                                                                                                                 |
| Predictor.fit     | (features,<br> labels):<br>(numpy.ndarray,<br> numpy.ndarray)                         | Predictor                                                               | Fit the features and labels to the predictor                                                                                                                       |
| Predictor.predict | (group_ix,<br> features):<br>(list,<br> numpy.ndarray)                                | (result):<br>(numpy.ndarray)                                            | predict the results by select just one canonical form for each group_ix. When labels are identical, default use the first column of training data to break the tie |
| Predictor.score   | (group_ix,<br> features,<br> labels):<br>(list,<br> numpy.ndarray,<br> numpy.ndarray) | (precision,<br> recall,<br> f1_score):<br>(float,<br> float,<br> float) | return precision recall and f1_score for testing_data                                                                                                              |

- `training.py`

training.py passed random forest classifier to the predictor class we create, fit the training data to it, and then save the model. It then evaluates the precision, recall, and f1-score on both the constrained and unconstrained datasets and prints out predictions to make sure result looks correct.

- `load_store_data.py`

| Function               | Parameters                                                                                                                                                                                  | Return                                                                                                               | Description                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| load_dataset_from_file | (filename,<br> categories):<br>(str, <br> numpy.ndarray)                                                                                                                                    | (group_ix,<br> tokens,<br> features,<br> labels):<br>(list,<br> numpy.ndarray,<br> numpy.ndarray,<br> numpy.ndarray) | load dataset from file to arrays needed for prediction         |
| load_dataset           | (tweet_ix,<br> ix,<br> tokens,<br> features,<br> labels,<br> categories):<br>(numpy.ndarray,<br> numpy.ndarray,<br> numpy.ndarray,<br> numpy.ndarray,<br> numpy.ndarray,<br> numpy.ndarray) | (group_ix,<br> tokens,<br> features,<br> labels):<br>(list,<br> numpy.ndarray,<br> numpy.ndarray,<br> numpy.ndarray) | load dataset from various part to arrays needed for prediction |
| save_model             | (model, <br> file_name):<br>(Predictor, <br> str)                                                                                                                                           | None                                                                                                                 | save model to file specified                                   |
| load_model             | (file_name):<br>(str)                                                                                                                                                                       | (model):<br>(Predictor)                                                                                              | load model from file specified                                 |


#### Frontend

- `normalize_tweets.py`

The script that spawns the unconstrained mode normalizer and read from `stdin` to get a tweet to normalize. The result is written to `stdout`.

| Function  | Parameters   | Return                                       | Description                                 |
| --------- | ------------ | -------------------------------------------- | ------------------------------------------- |
| mapATweet | tweet:string | (inputTokens, normalizedTokens):(List, List) | Normalize a single tweet and tokenize them. |

### GUI Implementation

The GUI is implemented using modern techniques with web development. The wrapper is Electron and the framework is Vue.js. Electron configuration is in `src/index.html` and `src/index.js`. Vue component `src/normalizer.vue` is using Semantic UI to create the feed list. A Twitter client is connected at the creation of the component, stream API is hooked to a function that continuously pushes new tweets to the array.

Normalizing process is achieved by using [Subprocess](https://www.npmjs.com/package/subprocess) to spawn a python instance to execute `normalize_tweets.py` with the input being the tweet and its output parsed to substitute the chosen tweet.

## Training & Testing

To train a new model, or, if new data are added and you would like to rebuild the dataset. Run
```
python3 create_dataset.py
python3 training.py
```

Now you have the model saved to a file, you can start the application in unconstrained mode following the instructions above.

For model evaluation, we obtained the following result (see training.py for more details):

| dataset       | precision          | recall             | f1-score           |
| ------------- | ------------------ | ------------------ | ------------------ |
| Constrained   | 0.9258239891267415 | 0.9989734188817598 | 0.9610087293889428 |
| Unconstrained | 0.972782874617737  | 0.9924084858569051 | 0.9824976835169361 |
