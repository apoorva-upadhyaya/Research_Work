

import json 
from datetime import datetime 
import time
datetimeFormat='%Y-%m-%d %H:%M:%S'


final=set()

file_ob=open("../Nw_features/dict_user_past_tweets.json",'r')
dict_user_past_tweets=json.load(file_ob)

print("len of dict_user_past_tweets",len(dict_user_past_tweets))

dict_10=dict_user_past_tweets

count=0
dic_profile={}
for key in dict_10:

	l_text,l_type,l_created,l_lang=[],[],[],[]
	list_=[]
	di={}
	value=dict_10[key]
	
	dd={}
		
	for li in value:

		di['content']=li[2]
		di['contenttype']="text/plain"
		di['created']=(datetime.strptime(str(li[1]), datetimeFormat)).timestamp()
		di['language']="en"
		list_.append(di)
			# print(di)


	dd["contentItems"]=list_
	dd=json.dumps(dd)
	dic_profile[key]=dd
	count=count+1

print("len of dic_profile",len(dic_profile))

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import watson_developer_cloud as WDC
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions, CategoriesOptions, EmotionOptions, SentimentOptions
from watson_developer_cloud.personality_insights_v3 import *

authenticator = IAMAuthenticator('PsArCR7IZU6ekX_M9JA1cF_BNbJu_pU9ov-s6p8faCFs')
natural_language_understanding = NaturalLanguageUnderstandingV1(
	    version='2019-07-12',
	    authenticator=authenticator
	)

import operator
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


from ibm_watson import PersonalityInsightsV3

authenticator1 = IAMAuthenticator('OnnFYs_z5Wwn7k2XeNbZL4TxcWqR8-HLxoEM7AEiPfvY')
personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    authenticator=authenticator1
)

personality_insights.set_service_url('https://api.eu-gb.personality-insights.watson.cloud.ibm.com/instances/b229525d-3bd4-49f8-84ec-13a2e926b1db')

personality_insights.set_disable_ssl_verification(True)
import watson_developer_cloud as WDC
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions, CategoriesOptions, EmotionOptions, SentimentOptions
from watson_developer_cloud.personality_insights_v3 import *
print(personality_insights)



personality_insights.set_default_headers({'x-watson-learning-opt-out': "true"})

list_big5_per=[]
list_big5_raw=[]
count=0
result_dic={}
for user in dic_profile:
	profile_json=(dic_profile[user])
	# profile_json=json.dumps(profile_json)
	try:
		profile = personality_insights.profile(
		        profile_json,
		        'application/json',
		        content_type='application/json',
		        raw_scores=True
		).get_result()
		# print(json.dumps(profile, indent=2))
		if user not in result_dic:
			result_dic[user]=profile
	except Exception as e:
		print("exception",e)
		continue
	x={}
	x['open']=profile['personality'][0]['percentile']
	x['cons']=profile['personality'][1]['percentile']
	x['extra']=profile['personality'][2]['percentile']
	x['agree']=profile['personality'][3]['percentile']
	x['neur']=profile['personality'][4]['percentile']
	sorted_x = sorted(x.items(), key=operator.itemgetter(1),reverse=True)
	y=[]
	for (w,k) in sorted_x:
		y.append(w)

	list_big5_per.append(y)

	x_raw={}
	x_raw['open']=profile['personality'][0]['raw_score']
	x_raw['cons']=profile['personality'][1]['raw_score']
	x_raw['extra']=profile['personality'][2]['raw_score']
	x_raw['agree']=profile['personality'][3]['raw_score']
	x_raw['neur']=profile['personality'][4]['raw_score']
	sorted_x_raw = sorted(x_raw.items(), key=operator.itemgetter(1),reverse=True)
	y_raw=[]
	for (w,k) in sorted_x_raw:
		y_raw.append(w)
	list_big5_raw.append(y_raw)

with open("result_user_profile.json", "w+") as f4:
			f4.write(json.dumps(result_dic))
			f4.flush()


big5_openness=[0,0,0,0,0]
big5_conscientiousness=[0,0,0,0,0]
big5_extraversion=[0,0,0,0,0]
big5_agreeableness=[0,0,0,0,0]
big5_neuroticism=[0,0,0,0,0]

print("len of list_big5_per",len(list_big5_per))

for i in range(len(list_big5_per)):
	x=list_big5_per[i]
	exc=x.index('open')
	big5_openness[exc]=big5_openness[exc]+1
	exc=x.index("cons")
	big5_conscientiousness[exc]=big5_conscientiousness[exc]+1
	exc=x.index("extra")
	big5_extraversion[exc]=big5_extraversion[exc]+1
	exc=x.index("agree")
	big5_agreeableness[exc]=big5_agreeableness[exc]+1
	exc=x.index("neur")
	big5_neuroticism[exc]=big5_neuroticism[exc]+1

print("NPT NEGATIVE ::::::::::::::::: ")
print("list_big5_per")
print("big5_openness :: ",big5_openness)
print("big5_conscientiousness :: ",big5_conscientiousness)
print("big5_extraversion :: ",big5_extraversion)
print("big5_agreeableness :: ",big5_agreeableness)
print("big5_neuroticism :: ",big5_neuroticism)


big5_openness=[0,0,0,0,0]
big5_conscientiousness=[0,0,0,0,0]
big5_extraversion=[0,0,0,0,0]
big5_agreeableness=[0,0,0,0,0]
big5_neuroticism=[0,0,0,0,0]


for i in range(len(list_big5_raw)):
	x=list_big5_raw[i]
	exc=x.index('open')
	big5_openness[exc]=big5_openness[exc]+1
	exc=x.index("cons")
	big5_conscientiousness[exc]=big5_conscientiousness[exc]+1
	exc=x.index("extra")
	big5_extraversion[exc]=big5_extraversion[exc]+1
	exc=x.index("agree")
	big5_agreeableness[exc]=big5_agreeableness[exc]+1
	exc=x.index("neur")
	big5_neuroticism[exc]=big5_neuroticism[exc]+1

print("list_big5_raw")
print("big5_openness :: ",big5_openness)
print("big5_conscientiousness :: ",big5_conscientiousness)
print("big5_extraversion :: ",big5_extraversion)
print("big5_agreeableness :: ",big5_agreeableness)
print("big5_neuroticism :: ",big5_neuroticism)
