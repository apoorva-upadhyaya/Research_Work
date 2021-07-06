########## cognitive features : Sentiments, EMotions, LIWC #############

translateEnglish.py: translates the tweet text to english if other language and outputs a dictionary with tweet id as key and tweet text as value.

Sentiments: We use IBM WATSON Natural Language Understanding classifier API that returns the probabilistic value and a label for the sentiment as a json object. The output is a csv file that contains tweet id, text, label and score provided by IBM API.

Emotions: We use the IBM WATSON Natural Language Understanding classifier API to detect anger, disgust, fear, joy, or sadness that is conveyed in the tweet. The scores of each emotion are provided by the API. The output is a csv file that contains tweet id, text, dictionary with each emotions and its score.
