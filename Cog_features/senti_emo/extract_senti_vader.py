import json
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

########3 tweet_text contains tweet id as key and tweet text as value ########
file_ob=open("viral_tweet_text.json",'r')
dic=json.load(file_ob)

def sentiment_scores(sentence):
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
     
    
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
    	label="positive"
        # print("Positive")
 
    elif sentiment_dict['compound'] <= - 0.05 :
    	label="negative"
        # print("Negative")
 
    else :
    	label="neutral"
        # print("Neutral")

    return sentiment_dict['compound'],label
    
li_label=[]
li_score=[]
for key in dic:
        score,label=sentiment_scores(str(dic[key]))
        li_label.append(label)
        li_score.append(score)


li_label1=np.array(li_label)
print("np unique:::",np.unique(li_label1,return_counts=True))


dic_senti={}
keys=list(dic.keys())

for i in range(len(li_label)):
    label=li_label[i]
    score=li_score[i]
    li=[]
    li.append(label)
    li.append(score)
    key=keys[i]
    
    if key not in dic_senti:
        dic_senti[key]=li
        
print("len of label::",len(li_label),len(dic_senti))
   
with open("dic_senti.json", "w+") as f4:
    f4.write(json.dumps(dic_senti))
