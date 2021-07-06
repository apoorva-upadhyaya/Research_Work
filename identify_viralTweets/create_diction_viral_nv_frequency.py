
import os
files_path="DataCollect/"
count_t=0
import json
from datetime import datetime 
import time
import bisect
dict_={}
datetimeFormat='%a %b %d %H:%M:%S %z %Y'

for filename in os.listdir(files_path):
	print(filename)
	filename=files_path+"/"+filename
	fh = open(filename, 'r')
	for line in fh:
		try:
			tweet = json.loads(line)
			count_t=count_t+1
			user=tweet["user"]["id_str"]
			if 'retweeted_status' not in tweet:
				continue
			tweet_id=tweet["id_str"]
			if "full_text" in tweet:
				tweet_text=tweet["full_text"]
			else:
				tweet_text=tweet["text"]
			tweet_time=tweet['created_at']
			rt = tweet['retweeted_status']
			id_str=rt["id_str"]
			date1=rt['created_at']
			if "full_text" in tweet:
				text=rt['full_text']
			else:
				text=rt['text']
			
			user_id=rt["user"]["id_str"]
			tweet_length=len(text)
			status_count=rt["user"]["statuses_count"]
			favorite_count=rt["user"]["favourites_count"]
			friend_count=rt["user"]["friends_count"]
			follower_count=rt["user"]["followers_count"]
			hashtags=len(rt["entities"]["hashtags"])
			urls=len(rt["entities"]["urls"])
			mentions=len(rt["entities"]["user_mentions"])
			datetime_object=datetime.strptime(str(rt['created_at']), '%a %b %d %H:%M:%S +0000 %Y')
				# print("original tweet time",date1)
			tweet_time = time.mktime(datetime_object.timetuple())
			date2=tweet['created_at']		
				# print("retweet tweet time",date2)
			diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff1= diff.days
				# print("diff",diff)
				# if(diff1<=15) :
					# print("found")
			if id_str not in dict_:
						# dict_.append({"id_str":id_str,"text":text,"rt_count":1})
						dict_[id_str]={"rt_count":1,"text":text,"created_at":date1,"user_id":user_id,"length":tweet_length,"status_count":status_count,"favorite_count":favorite_count,"friend_count":friend_count,"follower_count":follower_count,"hashtags":hashtags,"urls":urls,"mentions":mentions}
						dict_[id_str]["rate"]=[date2]
						dict_[id_str]["rt_user"]=[user]
						dict_[id_str]["rt_id"]=[tweet_id]
						dict_[id_str]["rt_text"]=[tweet_text]
						# dict_[id_str]["text"]=text
			elif id_str in dict_ :
						dict_[id_str]["rt_count"]=dict_[id_str]["rt_count"]+1
						dict_[id_str]["rate"].append(date2)
						dict_[id_str]["rt_user"].append(user)
						dict_[id_str]["rt_id"].append(tweet_id)
						dict_[id_str]["rt_text"].append(tweet_text)
		
		except:
			continue

import operator
sorted_tweets=sorted(dict_.values(),key=lambda k: k['created_at'])
print(sorted_tweets[:20])



count=0
count_0=0
print("count_t",count_t)
print("len of dict",len(dict_))

filename="viral.txt"
filename1="non_viral.txt"
tweet_1000=[]
tweet_900=[]
tweet_800=[]
tweet_700=[]
tweet_600=[]
new_dict={}
new_dict_900={}
new_dict_800={}
new_dict_700={}
new_dict_600={}
non_viral_600={}
for key in dict_:
	if dict_[key]["rt_count"] >=1000 :
		count=count+1
		new_dict[key]=dict_[key]
		tweet_1000.append(key)
	if dict_[key]["rt_count"] >=900 :
		tweet_900.append(key)
		new_dict_900[key]=dict_[key]
	if dict_[key]["rt_count"] >=800 :
		tweet_800.append(key)
		new_dict_800[key]=dict_[key]
	if dict_[key]["rt_count"] >=700 :
		tweet_700.append(key)
		new_dict_700[key]=dict_[key]
	if dict_[key]["rt_count"] >=600 :
		tweet_600.append(key)
		new_dict_600[key]=dict_[key]

	if dict_[key]["rt_count"] < 200 and dict_[key]["rt_count"] > 50  :
		non_viral_600[key]=dict_[key]


print("viral tweets:",count)
print("non_viral_600:",len(non_viral_600))

with open("viral/dict_1000_info.json", "w+") as f:
 			f.write(json.dumps(new_dict))


with open("viral/dict_900_info.json", "w+") as f:
 			f.write(json.dumps(new_dict_900))


with open("viral/dict_800_info.json", "w+") as f:
 			f.write(json.dumps(new_dict_800))


with open("viral/dict_700_info.json", "w+") as f:
 			f.write(json.dumps(new_dict_700))


with open("viral/dict_600_info.json", "w+") as f:
 			f.write(json.dumps(new_dict_600))

with open("viral/dict_nonviral_info.json", "w+") as f:
 			f.write(json.dumps(non_viral_600))




with open("viral/1000/tweet_1000.txt","w") as f:
	for i in range(len(tweet_1000)):
		f.write(str(tweet_1000[i]))
		f.write("\n")
		f.flush()

with open("viral/900/tweet_900.txt","w") as f:
	for i in range(len(tweet_900)):
		f.write(str(tweet_900[i]))
		f.write("\n")
		f.flush()

with open("viral/800/tweet_800.txt","w") as f:
	for i in range(len(tweet_800)):
		f.write(str(tweet_800[i]))
		f.write("\n")
		f.flush()

with open("viral/700/tweet_700.txt","w") as f:
	for i in range(len(tweet_700)):
		f.write(str(tweet_700[i]))
		f.write("\n")
		f.flush()

with open("viral/600/tweet_600.txt","w") as f:
	for i in range(len(tweet_600)):
		f.write(str(tweet_600[i]))
		f.write("\n")
		f.flush()

now = datetime.utcnow()
		# print("now",now)		
############################# 1000 viral 
tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 1000 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list




print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/1000/viral_dict_10.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))


########################## 20 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 1000 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/1000/viral_dict_20.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 30 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"]>= 1000 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/1000/viral_dict_30.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))




########################## 40 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 1000 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/1000/viral_dict_40.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 50 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 1000 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/1000/viral_dict_50.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 60 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000,3060,3120,3180,3240,3300,3360,3420,3480,3540,3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 1000 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/1000/viral_dict_60.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



############################## 900 

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 900 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list




print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/900/viral_dict_10.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))


########################## 20 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 900 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/900/viral_dict_20.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 30 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"]>= 900 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/900/viral_dict_30.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))




########################## 40 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 900 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/900/viral_dict_40.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 50 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 900 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/900/viral_dict_50.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 60 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000,3060,3120,3180,3240,3300,3360,3420,3480,3540,3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 900 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/900/viral_dict_60.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



##############################  800 

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 800 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list




print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/800/viral_dict_10.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))


########################## 20 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 800 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/800/viral_dict_20.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 30 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"]>= 800 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/800/viral_dict_30.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))




########################## 40 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 800 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/800/viral_dict_40.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 50 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 800 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/800/viral_dict_50.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 60 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000,3060,3120,3180,3240,3300,3360,3420,3480,3540,3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 800 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/800/viral_dict_60.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))




##############################  700 

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 700 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list




print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/700/viral_dict_10.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))


########################## 20 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 700 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/700/viral_dict_20.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 30 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"]>= 700 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/700/viral_dict_30.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))




########################## 40 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 700 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/700/viral_dict_40.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 50 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 700 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/700/viral_dict_50.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))



########################## 60 mins

tweets_viral={}
tweets_nonviral={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000,3060,3120,3180,3240,3300,3360,3420,3480,3540,3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 700 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/700/viral_dict_60.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))




##############################  600 
dict_10={}
set_10=set()
tweets_viral={}
tweets_nonviral={}
dict_10_new={}
arr=[60,120,180,240,300,360,420,480,540,600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 600 :
		date1=dict_[key]["created_at"]
		set_10.add(dict_[key]["user_id"])
		for rt in dict_[key]["rate"]:
			li=dict_[key]["rate"]
			index_user=li.index(rt)
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					list_[i]=list_[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_10.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_10:
						dict_10[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_10[key]["rate"]=[rt]
						dict_10[key]["rt_user"]=[user]
						dict_10[key]["rt_id"]=[rt_id]
						dict_10[key]["rt_text"]=[rt_text]
						dict_10_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_10_new:
						dict_10_new[rt_id]={"text":rt_text,"time":rt,"user":user}
					
				tweets_viral[key] = list_

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,9))
					curr_list[i]=curr_list[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_10.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if rt_id not in dict_10_new:
						dict_10_new[rt_id]={"text":rt_text,"time":rt,"user":user}
					if key not in dict_10:
						dict_10[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_10[key]["rate"]=[rt]
						dict_10[key]["rt_user"]=[user]
						dict_10[key]["rt_id"]=[rt_id]
						dict_10[key]["rt_text"]=[rt_text]
						dict_10_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if key in dict_10:
						dict_10[key]["rate"].append(rt)
						dict_10[key]["rt_user"].append(user)
						dict_10[key]["rt_id"].append(rt_id)
						dict_10[key]["rt_text"].append(rt_text)
				tweets_viral[key] = curr_list




print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/600/viral_dict_10.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))

with open("viral/600/data/dict_10.json", "w+") as f:
 	f.write(json.dumps(dict_10))


with open("viral/600/data/dict_10_new.json", "w+") as f:
 	f.write(json.dumps(dict_10_new))

########################## 20 mins
set_20=set()
tweets_viral={}
tweets_nonviral={}
dict_20={}
dict_20_new={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 600 :
		date1=dict_[key]["created_at"]
		set_20.add(dict_[key]["user_id"])
		for rt in dict_[key]["rate"]:
			li=dict_[key]["rate"]
			index_user=li.index(rt)
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					list_[i]=list_[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_20.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_20:
						dict_20[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_20[key]["rate"]=[rt]
						dict_20[key]["rt_user"]=[user]
						dict_20[key]["rt_id"]=[rt_id]
						dict_20[key]["rt_text"]=[rt_text]
						dict_20_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_20_new:
						dict_20_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,19))
					curr_list[i]=curr_list[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_20.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_20:
						dict_20[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_20[key]["rate"]=[rt]
						dict_20[key]["rt_user"]=[user]
						dict_20[key]["rt_id"]=[rt_id]
						dict_20[key]["rt_text"]=[rt_text]
						dict_20_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if key in dict_20:	
						dict_20[key]["rate"].append(rt)
						dict_20[key]["rt_user"].append(user)
						dict_20[key]["rt_id"].append(rt_id)
						dict_20[key]["rt_text"].append(rt_text)
					if rt_id not in dict_20_new:
						dict_20_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/600/viral_dict_20.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))

with open("viral/600/data/dict_20.json", "w+") as f:
 	f.write(json.dumps(dict_20))


with open("viral/600/data/dict_20_new.json", "w+") as f:
 	f.write(json.dumps(dict_20_new))

########################## 30 mins

set_30=set()
dict_30={}
tweets_viral={}
tweets_nonviral={}
dict_30_new={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"]>= 600 :
		date1=dict_[key]["created_at"]
		set_30.add(dict_[key]["user_id"])
		for rt in dict_[key]["rate"]:
			li=dict_[key]["rate"]
			index_user=li.index(rt)
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					list_[i]=list_[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_30.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_30:
						dict_30[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_30[key]["rate"]=[rt]
						dict_30[key]["rt_user"]=[user]
						dict_30[key]["rt_id"]=[rt_id]
						dict_30[key]["rt_text"]=[rt_text]
						dict_30_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_30_new:
						dict_30_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,29))
					curr_list[i]=curr_list[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_30.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_30:
						dict_30[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_30[key]["rate"]=[rt]
						dict_30[key]["rt_user"]=[user]
						dict_30[key]["rt_id"]=[rt_id]
						dict_30[key]["rt_text"]=[rt_text]
						dict_30_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if key in dict_30:
						dict_30[key]["rate"].append(rt)
						dict_30[key]["rt_user"].append(user)
						dict_30[key]["rt_id"].append(rt_id)
						dict_30[key]["rt_text"].append(rt_text)
					# dict_10_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_30_new:
						dict_30_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/600/viral_dict_30.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))

with open("viral/600/data/dict_30.json", "w+") as f:
 	f.write(json.dumps(dict_30))



with open("viral/600/data/dict_30_new.json", "w+") as f:
 	f.write(json.dumps(dict_30_new))

########################## 40 mins

set_40=set()
tweets_viral={}
tweets_nonviral={}
dict_40={}
dict_40_new={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 600 :
		date1=dict_[key]["created_at"]
		set_40.add(dict_[key]["user_id"])
		for rt in dict_[key]["rate"]:
			li=dict_[key]["rate"]
			index_user=li.index(rt)
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					list_[i]=list_[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_40.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_40:
						dict_40[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_40[key]["rate"]=[rt]
						dict_40[key]["rt_user"]=[user]
						dict_40[key]["rt_id"]=[rt_id]
						dict_40[key]["rt_text"]=[rt_text]
						dict_40_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_40_new:
						dict_40_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,39))
					curr_list[i]=curr_list[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_40.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_40:
						dict_40[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_40[key]["rate"]=[rt]
						dict_40[key]["rt_user"]=[user]
						dict_40[key]["rt_id"]=[rt_id]
						dict_40[key]["rt_text"]=[rt_text]
						dict_40_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if key in dict_40:
						dict_40[key]["rate"].append(rt)
						dict_40[key]["rt_user"].append(user)
						dict_40[key]["rt_id"].append(rt_id)
						dict_40[key]["rt_text"].append(rt_text)
					# dict_10_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_40_new:
						dict_40_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/600/viral_dict_40.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))

with open("viral/600/data/dict_40.json", "w+") as f:
 	f.write(json.dumps(dict_40))


with open("viral/600/data/dict_40_new.json", "w+") as f:
 	f.write(json.dumps(dict_40_new))

########################## 50 mins

set_50=set()
tweets_viral={}
tweets_nonviral={}
dict_50={}
dict_50_new={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 600 :
		date1=dict_[key]["created_at"]
		set_50.add(dict_[key]["user_id"])
		for rt in dict_[key]["rate"]:
			li=dict_[key]["rate"]
			index_user=li.index(rt)
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					list_[i]=list_[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_50.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_50:
						dict_50[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_50[key]["rate"]=[rt]
						dict_50[key]["rt_user"]=[user]
						dict_50[key]["rt_id"]=[rt_id]
						dict_50[key]["rt_text"]=[rt_text]
						dict_50_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_50_new:
						dict_50_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,49))
					curr_list[i]=curr_list[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_50.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_50:
						dict_50[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_50[key]["rate"]=[rt]
						dict_50[key]["rt_user"]=[user]
						dict_50[key]["rt_id"]=[rt_id]
						dict_50[key]["rt_text"]=[rt_text]
						dict_50_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if key in dict_50:	
						dict_50[key]["rate"].append(rt)
						dict_50[key]["rt_user"].append(user)
						dict_50[key]["rt_id"].append(rt_id)
						dict_50[key]["rt_text"].append(rt_text)
					# dict_10_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_50_new:
						dict_50_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/600/viral_dict_50.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))

with open("viral/600/data/dict_50.json", "w+") as f:
 	f.write(json.dumps(dict_50))


with open("viral/600/data/dict_50_new.json", "w+") as f:
 	f.write(json.dumps(dict_50_new))

########################## 60 mins

set_60=set()
tweets_viral={}
tweets_nonviral={}
dict_60={}
dict_60_new={}
arr=[60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320,1380,1440,1500,1560,1620,1680,1740,1800,1860,1920,1980,2040,2100,2160,2220,2280,2340,2400,2460,2520,2580,2640,2700,2760,2820,2880,2940,3000,3060,3120,3180,3240,3300,3360,3420,3480,3540,3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 600 :
		date1=dict_[key]["created_at"]
		set_60.add(dict_[key]["user_id"])
		for rt in dict_[key]["rate"]:
			li=dict_[key]["rate"]
			index_user=li.index(rt)
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					list_[i]=list_[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_60.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_60:
						dict_60[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_60[key]["rate"]=[rt]
						dict_60[key]["rt_user"]=[user]
						dict_60[key]["rt_id"]=[rt_id]
						dict_60[key]["rt_text"]=[rt_text]
						dict_60_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_60_new:
						dict_60_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,59))
					curr_list[i]=curr_list[i]+1
					l=dict_[key]["rt_user"]
					user=l[index_user]
					set_60.add(user)
					l1=dict_[key]["rt_id"]
					rt_id=l1[index_user]
					l2=dict_[key]["rt_text"]
					rt_text=l2[index_user]
					if key not in dict_60:
						dict_60[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
						dict_60[key]["rate"]=[rt]
						dict_60[key]["rt_user"]=[user]
						dict_60[key]["rt_id"]=[rt_id]
						dict_60[key]["rt_text"]=[rt_text]
						dict_60_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if key in dict_60:
						dict_60[key]["rate"].append(rt)
						dict_60[key]["rt_user"].append(user)
						dict_60[key]["rt_id"].append(rt_id)
						dict_60[key]["rt_text"].append(rt_text)
					# dict_10_new[key]={"text":dict_[key]["text"],"time":dict_[key]["created_at"],"user":dict_[key]["user_id"]}
					if rt_id not in dict_60_new:
						dict_60_new[rt_id]={"text":rt_text,"time":rt,"user":user}
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/600/viral_dict_60.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))

with open("viral/600/data/dict_60.json", "w+") as f:
 	f.write(json.dumps(dict_60))

with open("viral/600/data/dict_60_new.json", "w+") as f:
 	f.write(json.dumps(dict_60_new))

set_10=list(set_10)
set_20=list(set_20)
set_30=list(set_30)
set_40=list(set_40)
set_50=list(set_50)
set_60=list(set_60)


with open("viral/600/data/set_users_10.txt","w") as f:
	for i in range(len(set_10)):
		f.write(str(set_10[i]))
		f.write("\n")
		f.flush()

with open("viral/600/data/set_users_20.txt","w") as f:
	for i in range(len(set_20)):
		f.write(str(set_20[i]))
		f.write("\n")
		f.flush()

with open("viral/600/data/set_users_30.txt","w") as f:
	for i in range(len(set_30)):
		f.write(str(set_30[i]))
		f.write("\n")
		f.flush()

with open("viral/600/data/set_users_40.txt","w") as f:
	for i in range(len(set_40)):
		f.write(str(set_40[i]))
		f.write("\n")
		f.flush()

with open("viral/600/data/set_users_50.txt","w") as f:
	for i in range(len(set_50)):
		f.write(str(set_50[i]))
		f.write("\n")
		f.flush()

with open("viral/600/data/set_users_60.txt","w") as f:
	for i in range(len(set_60)):
		f.write(str(set_60[i]))
		f.write("\n")
		f.flush()



########################## 10 sec window 600

tweets_viral={}
tweets_nonviral={}
arr=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300, 1310, 1320, 1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400, 1410, 1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490, 1500, 1510, 1520, 1530, 1540, 1550, 1560, 1570, 1580, 1590, 1600, 1610, 1620, 1630, 1640, 1650, 1660, 1670, 1680, 1690, 1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1780, 1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170, 2180, 2190, 2200, 2210, 2220, 2230, 2240, 2250, 2260, 2270, 2280, 2290, 2300, 2310, 2320, 2330, 2340, 2350, 2360, 2370, 2380, 2390, 2400, 2410, 2420, 2430, 2440, 2450, 2460, 2470, 2480, 2490, 2500, 2510, 2520, 2530, 2540, 2550, 2560, 2570, 2580, 2590, 2600, 2610, 2620, 2630, 2640, 2650, 2660, 2670, 2680, 2690, 2700, 2710, 2720, 2730, 2740, 2750, 2760, 2770, 2780, 2790, 2800, 2810, 2820, 2830, 2840, 2850, 2860, 2870, 2880, 2890, 2900, 2910, 2920, 2930, 2940, 2950, 2960, 2970, 2980, 2990, 3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3200, 3210, 3220, 3230, 3240, 3250, 3260, 3270, 3280, 3290, 3300, 3310, 3320, 3330, 3340, 3350, 3360, 3370, 3380, 3390, 3400, 3410, 3420, 3430, 3440, 3450, 3460, 3470, 3480, 3490, 3500, 3510, 3520, 3530, 3540, 3550, 3560, 3570, 3580, 3590, 3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 600 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/600/viral_freq_series_360.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))


########################## 10 sec window 700

tweets_viral={}
tweets_nonviral={}
arr=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300, 1310, 1320, 1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400, 1410, 1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490, 1500, 1510, 1520, 1530, 1540, 1550, 1560, 1570, 1580, 1590, 1600, 1610, 1620, 1630, 1640, 1650, 1660, 1670, 1680, 1690, 1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1780, 1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170, 2180, 2190, 2200, 2210, 2220, 2230, 2240, 2250, 2260, 2270, 2280, 2290, 2300, 2310, 2320, 2330, 2340, 2350, 2360, 2370, 2380, 2390, 2400, 2410, 2420, 2430, 2440, 2450, 2460, 2470, 2480, 2490, 2500, 2510, 2520, 2530, 2540, 2550, 2560, 2570, 2580, 2590, 2600, 2610, 2620, 2630, 2640, 2650, 2660, 2670, 2680, 2690, 2700, 2710, 2720, 2730, 2740, 2750, 2760, 2770, 2780, 2790, 2800, 2810, 2820, 2830, 2840, 2850, 2860, 2870, 2880, 2890, 2900, 2910, 2920, 2930, 2940, 2950, 2960, 2970, 2980, 2990, 3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3200, 3210, 3220, 3230, 3240, 3250, 3260, 3270, 3280, 3290, 3300, 3310, 3320, 3330, 3340, 3350, 3360, 3370, 3380, 3390, 3400, 3410, 3420, 3430, 3440, 3450, 3460, 3470, 3480, 3490, 3500, 3510, 3520, 3530, 3540, 3550, 3560, 3570, 3580, 3590, 3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 700 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/700/viral_freq_series_360.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))


########################## 10 sec window 800

tweets_viral={}
tweets_nonviral={}
arr=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300, 1310, 1320, 1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400, 1410, 1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490, 1500, 1510, 1520, 1530, 1540, 1550, 1560, 1570, 1580, 1590, 1600, 1610, 1620, 1630, 1640, 1650, 1660, 1670, 1680, 1690, 1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1780, 1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170, 2180, 2190, 2200, 2210, 2220, 2230, 2240, 2250, 2260, 2270, 2280, 2290, 2300, 2310, 2320, 2330, 2340, 2350, 2360, 2370, 2380, 2390, 2400, 2410, 2420, 2430, 2440, 2450, 2460, 2470, 2480, 2490, 2500, 2510, 2520, 2530, 2540, 2550, 2560, 2570, 2580, 2590, 2600, 2610, 2620, 2630, 2640, 2650, 2660, 2670, 2680, 2690, 2700, 2710, 2720, 2730, 2740, 2750, 2760, 2770, 2780, 2790, 2800, 2810, 2820, 2830, 2840, 2850, 2860, 2870, 2880, 2890, 2900, 2910, 2920, 2930, 2940, 2950, 2960, 2970, 2980, 2990, 3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3200, 3210, 3220, 3230, 3240, 3250, 3260, 3270, 3280, 3290, 3300, 3310, 3320, 3330, 3340, 3350, 3360, 3370, 3380, 3390, 3400, 3410, 3420, 3430, 3440, 3450, 3460, 3470, 3480, 3490, 3500, 3510, 3520, 3530, 3540, 3550, 3560, 3570, 3580, 3590, 3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 800 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/800/viral_freq_series_360.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))


########################## 10 sec window 900

tweets_viral={}
tweets_nonviral={}
arr=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300, 1310, 1320, 1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400, 1410, 1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490, 1500, 1510, 1520, 1530, 1540, 1550, 1560, 1570, 1580, 1590, 1600, 1610, 1620, 1630, 1640, 1650, 1660, 1670, 1680, 1690, 1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1780, 1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170, 2180, 2190, 2200, 2210, 2220, 2230, 2240, 2250, 2260, 2270, 2280, 2290, 2300, 2310, 2320, 2330, 2340, 2350, 2360, 2370, 2380, 2390, 2400, 2410, 2420, 2430, 2440, 2450, 2460, 2470, 2480, 2490, 2500, 2510, 2520, 2530, 2540, 2550, 2560, 2570, 2580, 2590, 2600, 2610, 2620, 2630, 2640, 2650, 2660, 2670, 2680, 2690, 2700, 2710, 2720, 2730, 2740, 2750, 2760, 2770, 2780, 2790, 2800, 2810, 2820, 2830, 2840, 2850, 2860, 2870, 2880, 2890, 2900, 2910, 2920, 2930, 2940, 2950, 2960, 2970, 2980, 2990, 3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3200, 3210, 3220, 3230, 3240, 3250, 3260, 3270, 3280, 3290, 3300, 3310, 3320, 3330, 3340, 3350, 3360, 3370, 3380, 3390, 3400, 3410, 3420, 3430, 3440, 3450, 3460, 3470, 3480, 3490, 3500, 3510, 3520, 3530, 3540, 3550, 3560, 3570, 3580, 3590, 3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 900 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/900/viral_freq_series_360.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))


########################## 10 sec window 1000

tweets_viral={}
tweets_nonviral={}
arr=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300, 1310, 1320, 1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400, 1410, 1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490, 1500, 1510, 1520, 1530, 1540, 1550, 1560, 1570, 1580, 1590, 1600, 1610, 1620, 1630, 1640, 1650, 1660, 1670, 1680, 1690, 1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1780, 1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170, 2180, 2190, 2200, 2210, 2220, 2230, 2240, 2250, 2260, 2270, 2280, 2290, 2300, 2310, 2320, 2330, 2340, 2350, 2360, 2370, 2380, 2390, 2400, 2410, 2420, 2430, 2440, 2450, 2460, 2470, 2480, 2490, 2500, 2510, 2520, 2530, 2540, 2550, 2560, 2570, 2580, 2590, 2600, 2610, 2620, 2630, 2640, 2650, 2660, 2670, 2680, 2690, 2700, 2710, 2720, 2730, 2740, 2750, 2760, 2770, 2780, 2790, 2800, 2810, 2820, 2830, 2840, 2850, 2860, 2870, 2880, 2890, 2900, 2910, 2920, 2930, 2940, 2950, 2960, 2970, 2980, 2990, 3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3200, 3210, 3220, 3230, 3240, 3250, 3260, 3270, 3280, 3290, 3300, 3310, 3320, 3330, 3340, 3350, 3360, 3370, 3380, 3390, 3400, 3410, 3420, 3430, 3440, 3450, 3460, 3470, 3480, 3490, 3500, 3510, 3520, 3530, 3540, 3550, 3560, 3570, 3580, 3590, 3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] >= 1000 :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/1000/viral_freq_series_360.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))

######################################### non viral <600

tweets_viral={}
tweets_nonviral={}
arr=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070, 1080, 1090, 1100, 1110, 1120, 1130, 1140, 1150, 1160, 1170, 1180, 1190, 1200, 1210, 1220, 1230, 1240, 1250, 1260, 1270, 1280, 1290, 1300, 1310, 1320, 1330, 1340, 1350, 1360, 1370, 1380, 1390, 1400, 1410, 1420, 1430, 1440, 1450, 1460, 1470, 1480, 1490, 1500, 1510, 1520, 1530, 1540, 1550, 1560, 1570, 1580, 1590, 1600, 1610, 1620, 1630, 1640, 1650, 1660, 1670, 1680, 1690, 1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1780, 1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150, 2160, 2170, 2180, 2190, 2200, 2210, 2220, 2230, 2240, 2250, 2260, 2270, 2280, 2290, 2300, 2310, 2320, 2330, 2340, 2350, 2360, 2370, 2380, 2390, 2400, 2410, 2420, 2430, 2440, 2450, 2460, 2470, 2480, 2490, 2500, 2510, 2520, 2530, 2540, 2550, 2560, 2570, 2580, 2590, 2600, 2610, 2620, 2630, 2640, 2650, 2660, 2670, 2680, 2690, 2700, 2710, 2720, 2730, 2740, 2750, 2760, 2770, 2780, 2790, 2800, 2810, 2820, 2830, 2840, 2850, 2860, 2870, 2880, 2890, 2900, 2910, 2920, 2930, 2940, 2950, 2960, 2970, 2980, 2990, 3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3200, 3210, 3220, 3230, 3240, 3250, 3260, 3270, 3280, 3290, 3300, 3310, 3320, 3330, 3340, 3350, 3360, 3370, 3380, 3390, 3400, 3410, 3420, 3430, 3440, 3450, 3460, 3470, 3480, 3490, 3500, 3510, 3520, 3530, 3540, 3550, 3560, 3570, 3580, 3590, 3600]
current_time = time.mktime(now.timetuple())
for key in dict_:
	if dict_[key]["rt_count"] < 200 and dict_[key]["rt_count"] > 50  :
		date1=dict_[key]["created_at"]
		for rt in dict_[key]["rate"]:
			diff=datetime.strptime(rt, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
			diff= diff.seconds
		
			xxx=current_time-tweet_time
			# print("current_time",current_time)
			# print("diff",(xxx/3600))
			last_index=len(arr)-1
		
			if key not in tweets_viral:
				list_=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					list_[i]=list_[i]+1
				tweets_viral[key] = list_
			

			else :
				curr_list=tweets_viral[key]
				if(diff <= arr[last_index]) :
					i = (bisect.bisect_left(arr,diff,0,359))
					curr_list[i]=curr_list[i]+1
				tweets_viral[key] = curr_list

	

print("len of viral:",len(tweets_viral))
print("len of non viral:",len(tweets_nonviral))

with open("viral/non_viral_freq_series_360.json", "w+") as f:
 	f.write(json.dumps(tweets_viral))
