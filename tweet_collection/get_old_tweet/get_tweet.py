import GetOldTweets3 as got
import json
import datetime
import time
set_id=set()
def main():
	try:
		data={}
		
		with open('keywords.txt','r') as f1:
			keywords = f1.read().splitlines()
		
		for k in keywords:
			tweetCriteria = got.manager.TweetCriteria().setSince('2017-08-25').setUntil('2017-09-25').setQuerySearch(k).setMaxTweets(100000)
			tweets = got.manager.TweetManager.getTweets(tweetCriteria)
			
			
			
			for tweet in tweets:
				# data['%s'%tweet.id]={}
				# data['%s'%tweet.id]["id"]=tweet.id
				local_date = tweet.date.strftime("%m/%d/%Y, %H:%M:%S")
				# data['%s'%tweet.id]["date"]=local_date
				# data['%s'%tweet.id]["text"]=tweet.text
				# data['%s'%tweet.id]["retweet_count"]=tweet.retweets
				
				# id_int=int(tweet.id)
				# print(local_date,"\t",type(local_date))
				# print(id_int,"\t",type(id_int))
				# print("text:","\t",tweet.text)
				if tweet.id not in set_id:
					set_id.add(tweet.id)
					w=open("tweet_ids.txt",'a+',encoding='utf-8')
					w.write(tweet.id)
					w.write("\n")
					w.flush()

	except Exception as exc:
		print('%s' % (exc))
	finally:
				
		print("Done")


	
			
	

if __name__ == '__main__':
	print("Wait PLEASE...................................")
	main()
