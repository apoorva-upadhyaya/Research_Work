
import json


########3 tweet_text contains tweet id as key and tweet text as value ########
file_ob=open("tweet_text.json",'r')
dic=json.load(file_ob)


from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import watson_developer_cloud as WDC
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions, CategoriesOptions, EmotionOptions, SentimentOptions
from watson_developer_cloud.personality_insights_v3 import *
import time


authenticator = IAMAuthenticator('API_KEY')
natural_language_understanding = NaturalLanguageUnderstandingV1(
	    version='2019-07-12',
	    authenticator=authenticator
	)

	

natural_language_understanding.set_service_url('https://gateway-lon.watsonplatform.net/natural-language-understanding/api')
natural_language_understanding.set_disable_ssl_verification(True)
	# # list_1=list_1[0:10]

list_0_emotions=[]
count=0
for key in dic :
		count=count+1
		try:
			response = natural_language_understanding.analyze(
			    text=str(dic[key]),
			    features=Features(emotion=EmotionOptions())).get_result()
		# 	# with open("pt/emotions.json","a") as f:
			obj=response["emotion"]["document"]["emotion"]
			# print(obj)
			x=sorted(obj, key=lambda k: (obj[k], k),reverse=True)
		# print(x)
		except:
			print("exception list_1::::::")
			print(key,dic[key])
			continue
		if(count==10):
			print("COUNT :    ",count)
			time.sleep(60)
			count=0
		list_0_emotions.append(x)
		with open("all_emotions.csv","a+") as f:	
			y=[]
			f.write(str(key))
			f.write(";")
			f.write(str(obj))
			f.write(';')
			f.write(str(x))
			f.write(';')
			f.write(str([dic[key]]))
			f.write("\n")
			f.flush()


sadness=[0,0,0,0,0]
joy=[0,0,0,0,0]
fear=[0,0,0,0,0]
disgust=[0,0,0,0,0]
anger=[0,0,0,0,0]

print("emotions length list_0",len(list_0_emotions))

for i in range(len(list_0_emotions)):
		x=list_0_emotions[i]
		exc=x.index("sadness")
		sadness[exc]=sadness[exc]+1
		exc=x.index("joy")
		joy[exc]=joy[exc]+1
		exc=x.index("fear")
		fear[exc]=fear[exc]+1
		exc=x.index("disgust")
		disgust[exc]=disgust[exc]+1
		exc=x.index("anger")
		anger[exc]=anger[exc]+1


		
print("All Emotions")
print("sadness : ",sadness)
print("joy ::",joy)
print("fear ::",fear)
print("disgust :: ",disgust)
print("anger :: ",anger)


count=0
list_senti_ibm=[]
for key in dic : 
		# print(list_1[i][0])
		count=count+1
		try:
			response = natural_language_understanding.analyze(
			    text=str(dic[key]),
			    features=Features(sentiment=SentimentOptions())).get_result()
		# 	# with open("pt/emotions.json","a") as f:
			
			obj=response["sentiment"]["document"]["score"]
			# print(obj)
			x=response["sentiment"]["document"]["label"]
		# print(x)
		except:
			print("exception list_1::::::")
			print(key,dic[key])
			continue
		if(count==20):
			print("COUNT :    ",count)
			time.sleep(60)
			count=0
		list_senti_ibm.append(x)
		with open("all_senti.csv","a+") as f:	
			f.write(str(key))
			f.write(";")
			f.write(str(obj))
			f.write(';')
			f.write(str(x))
			f.write(';')
			f.write(str([dic[key]]))
			f.write("\n")
			f.flush()

cn=0
cneg=0
cp=0
for i in range(len(list_senti_ibm)):
	if(list_senti_ibm[i]=="positive"):
		cp=cp+1
	elif(list_senti_ibm[i]=="negative"):
		cneg=cneg+1

	elif(list_senti_ibm[i]=="neutral"):
		cn=cn+1


print("positive",cp)
print("negative",cneg)
print("neutral",cn)

