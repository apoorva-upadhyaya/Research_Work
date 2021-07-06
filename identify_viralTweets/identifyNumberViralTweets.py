

import json
import os

dic_cas={}
dic_org={}
set_tweet=set()
set_retweet=set()
c=0
corig=0
set_user=set()
tweets={}

##### if the tweets are kept in different files placed at files_path folder location 
files_path="data/data/"
for filename in os.listdir(files_path):
		print(filename)
		filename=files_path+"/"+filename
		f=open(filename,'r')
		for line in f:
			tweet=json.loads(line)
			u_id=tweet['user']['id_str']
			tid=tweet['id_str']
			set_user.add(u_id)
			if tid not in tweets:
				tweets[tid]=tweet["retweet_count"]
			if "retweeted_status" in tweet:
				c=c+1
				set_retweet.add(tid)
				x=tweet['retweeted_status']
				orig=x["id_str"]
				if orig not in dic_cas:
					dic_cas[orig]=1
				else:
					dic_cas[orig]=dic_cas[orig] +1
			else:
				set_tweet.add(tid)
				dic_org[tid]=tweet["retweet_count"]

#### if all tweets are kept in single JSON file ################
# with open("25/product_1.json","r") as f:
# 	for line in f:
# 			tweet=json.loads(line)
# 			u_id=tweet['user']['id_str']
# 			tid=tweet['id_str']
# 			set_user.add(u_id)
# 			if tid not in tweets:
# 				tweets[tid]=tweet["retweet_count"]
# 			if "retweeted_status" in tweet:
# 				c=c+1
# 				set_retweet.add(tid)
# 				x=tweet['retweeted_status']
# 				orig=x["id_str"]
# 				if orig not in dic_cas:
# 					dic_cas[orig]=1
# 				else:
# 					dic_cas[orig]=dic_cas[orig] +1
# 			else:
# 				set_tweet.add(tid)
# 				dic_org[tid]=tweet["retweet_count"]

import operator
######### sorting tweets with descending order of their retweets ###########
sorted_x = sorted(tweets.items(), key=operator.itemgetter(1),reverse=True)
set_tweet=list(set_tweet)
set_retweet=list(set_retweet)
set_user=list(set_user)

print("len of tweets",len(tweets))
print("len of orig",len(set_tweet))
print("len of rt",len(set_retweet))
print("len of users",len(set_user))
print("sorted tweets ",sorted_x[:20])

#### sorted_x
len_=len(sorted_x)
top=int(.02 * len_)
refer_rt=sorted_x[top]
xx=int(refer_rt[1])
print(refer_rt[1])
viral=0

l=1
for key,data in sorted_x:
	l=l+1
	# if retweet count >=1000, then viral :
	if data >= 1000 :
		viral=viral+1
		#### select top 2% of the tweets ########
		if(l>top):
			print("donee")
			break


print("viral tweets/retweets with retweet count>=1000",viral)


############ same is repeated with original tweets with retweet count >=1000 #############

sorted_dic_org = sorted(dic_org.items(), key=operator.itemgetter(1),reverse=True)

len_=len(sorted_dic_org)
top=int(.02 * len_)
refer_rt=sorted_dic_org[top]
xx=int(refer_rt[1])
print(refer_rt[1])
viral=0

l=1
for key,data in sorted_dic_org:
	l=l+1
	if data > 600 :
		# print(key,data)
		viral=viral+1
	if(l>top):
		print("donee")
		break
print("dic_org ############")	
print("top",top)
print("xx",xx)
print("viral",viral)
