import json
import matplotlib.pyplot as plt
import os
import io, pickle
import networkx as nx
from datetime import datetime 
import time
datetimeFormat='%a %b %d %H:%M:%S %z %Y'


########## dic_user_tweets contains key as user id and value as all the tweet objects of that particular user (original + retweet) ############

dic_user_tweets={}
set_users=set()
with open("../identify_viralTweets/viral/data/60min/users.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			set_users.add(str(id_))


print("len of users",len(set_users))


####### path contains all the json files having tweets###########
files_path= "../tweet_collection/data/"

for filename in os.listdir(files_path):
	print(filename)
	filename=files_path+"/"+filename
	fh = open(filename, 'r')
	try:
		for line in fh:
			
				tweet = json.loads(line)
				
				u_id=tweet["user"]['id_str']

				if u_id in set_users :

					if u_id not in dic_user_tweets:
						# print(tweet['created_at'])
						list1=[]
						list1.append(tweet)
						dic_user_tweets[u_id]=list1
						# print(list1)

					elif u_id in dic_user_tweets:
					
						li1=dic_user_tweets[u_id]
						li1.append(tweet)
						dic_user_tweets[u_id]=li1

				else:
					if 'retweeted_status' in tweet:
						rt = tweet['retweeted_status']
						id_str=rt["id_str"]
						rt_created_at=rt['created_at']
						u_id=rt["user"]['id_str']
						if u_id in set_users :
							if u_id not in dic_user_tweets:
								# print(tweet['created_at'])
								list1=[]
								list1.append(rt)
								dic_user_tweets[u_id]=list1
								# print(list1)

							elif u_id in dic_user_tweets:
						
								li1=dic_user_tweets[u_id]
								li1.append(rt)
								dic_user_tweets[u_id]=li1

	except:
		continue

print("len of dic_user_tweets",len(dic_user_tweets))

with open("dic_user_tweets.json", "w+") as f3:
			f3.write(json.dumps(dic_user_tweets))		