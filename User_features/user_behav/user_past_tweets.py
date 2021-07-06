

import tweepy #https://github.com/tweepy/tweepy
import csv
import json
import os
import time

#Twitter API credentials

consumer_key="" 
consumer_secret=""
access_key=""
access_secret=""

users_all=[]

with open("users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.append(str(id_))

print("len of users_all:",len(users_all ))

def get_all_tweets(user_id):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	try:
		new_tweets = api.user_timeline(user_id = user_id,count=1500)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		print("user id:",user_id)
		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			# print "getting tweets before %s" % (oldest)
			
			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(user_id = user_id,count=1500,max_id=oldest)
			
			#save most recent tweets
			alltweets.extend(new_tweets)
			
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			
			print("...%s tweets downloaded so far",(len(alltweets)))
		
		#transform the tweepy tweets into a 2D array that will populate the csv	

		outtweets = [[tweet.id_str, str(tweet.created_at), tweet.text,tweet.retweet_count] for tweet in alltweets]
	
	except Exception as e:
		outtweets=[] 
		print(e)

	#write the csv	
	# with open('%s_tweets.csv' % screen_name, 'wb') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(["id","created_at","text"])
	# 	writer.writerows(outtweets)
	
	return outtweets


######## dict_user_past_tweets contains user_id as ky and past max 3200 tweet objects of the key user #########

if __name__ == '__main__':
	#pass in the username of the account you want to download
	
	dic={}
	count=1
	count1=0
	for i in users_all:
		print("count",count)
		all_tweets=get_all_tweets(i)
		dic[i]=all_tweets
		if(count1>10):
			time.sleep(180)
			count1=0
		# print(all_tweets)
		# break

		with open("dict_user_past_tweets.json", "w+") as f3:
			f3.write(json.dumps(dic))
			f3.flush()



