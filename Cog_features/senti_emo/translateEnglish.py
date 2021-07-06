
import json
import langid
import googletrans

from googletrans import Translator
# from googletrans.translate import Translator
translator = Translator()
import re
import nltk
from scipy import stats
import emoji

tweets1={}
tweets={}
list_text=[]
dic={}
ccc=0

file_ob=open("../../identify_viralTweets/viral/dict_600_info.json",'r')
dict_600_info=json.load(file_ob)

print("length",len(dict_600_info))

for key in dict_600_info:
	result=langid.classify(dict_600_info[key]["text"])
	if (result[0]=="en"):
		dic[key]=dict_600_info[key]["text"]
	else:
		ccc=ccc+1
		# print("text:",dict_600_info[key]["text"])
		# print("code:::",result[0])
		translator = Translator()
		str_demoji = emoji.demojize((dict_600_info[key]["text"]))
		# print("change",str_demoji)
		try:
			dt1 = translator.translate(str(str_demoji))
			# print("trans",dt1.text)
			dic[key]=dt1.text
		except Exception as e:
			dic[key]=dict_600_info[key]["text"]
			print("Exception **************",e)
			continue
						
				
print("translated text:",ccc)
print("len of list_text:",len(dic))
with open("sigma_viral_tweet_text.json", "w+") as f4:
	f4.write(json.dumps(dic))
