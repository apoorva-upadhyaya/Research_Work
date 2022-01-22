import random
import pandas as pd

df=pd.read_csv("results/event.csv", delimiter=",")

### data for an event 
#Filename,Segment,WC,Analytic,Clout,Authentic,Tone,WPS,Sixltr,Dic,function,pronoun,ppron,i,we,you,shehe,they,ipron,article,prep,auxverb,adverb,conj,negate,verb,adj,compare,interrog,number,quant,affect,posemo,negemo,anx,anger,sad,social,family,friend,female,male,cogproc,insight,cause,discrep,tentat,certain,differ,percept,see,hear,feel,bio,body,health,sexual,ingest,drives,affiliation,achieve,power,reward,risk,focuspast,focuspresent,focusfuture,relativ,motion,space,time,work,leisure,home,money,relig,death,informal,swear,netspeak,assent,nonflu,filler,AllPunc,Period,Comma,Colon,SemiC,QMark,Exclam,Dash,Quote,Apostro,Parenth,OtherP
#apple_tweets.txt,1,11199,82.71,65.39,10.67,94.60,18.95,16.97,66.88,37.42,8.92,5.60,2.51,0.49,1.42,0.97,0.21,3.32,5.81,10.26,6.62,2.88,4.25,1.16,11.46,3.50,1.57,0.96,7.09,1.20,6.30,5.40,0.88,0.07,0.21,0.22,7.69,0.47,0.32,0.46,1.02,6.95,1.09,1.54,1.13,1.54,0.70,1.92,2.38,1.48,0.44,0.41,0.93,0.35,0.35,0.04,0.14,8.31,1.89,3.06,4.39,3.12,0.25,1.91,8.59,1.06,10.11,1.74,3.91,4.58,1.60,0.85,0.34,2.21,2.09,0.04,1.50,0.05,1.07,0.51,0.27,0.00,27.65,5.18,3.65,0.69,0.13,0.90,1.64,0.82,0.42,1.66,0.81,11.73


print(list(df))

print("posemo::",df["posemo"])
print("negemo::",df["negemo"])
print("anger::",df["anger"])
print("anger::",df["anger"])
print("anxious::",df["anx"])
print("sadness::",df["sad"])
