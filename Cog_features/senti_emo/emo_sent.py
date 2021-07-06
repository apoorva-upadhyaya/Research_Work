import csv
count=0
dict_={}
import json
import statistics

import ast 


with open("all_emotions_nochange_up.csv", 'r') as f:
	mycsv = csv.reader(f,delimiter=";")
	for row in mycsv:
		# if()
		# if('\;' in row[1]):
		# 	print("apoo")
		# # row=row[1].replace("")
		id_=row[0]
		x=row[1]
		i=3
		if id_ not in dict_:
			dict_[id_]=(x)
		# print(x)

print("len :::::",len(dict_))


with open("dic_emotion_viral.json", "w+") as f4:
	f4.write(json.dumps(dict_))


anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
list_tweet=[]
with open("../../identify_viralTweets/viral/data/5min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		if key in list_tweet :
			anger.append(val["anger"])
			sadness.append(val["sadness"])
			joy.append(val["joy"])
			fear.append(val["fear"])
			disgust.append(val["disgust"])
	
x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)




############# 10min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/10min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		if key in list_tweet :
			anger.append(val["anger"])
			sadness.append(val["sadness"])
			joy.append(val["joy"])
			fear.append(val["fear"])
			disgust.append(val["disgust"])


x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)



###########15min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/15min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])


x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

############# 20min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/20min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])
		

x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)
#positive,nega,neutral

############# 25min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/25min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])


x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)



################# 30min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/30min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])

x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 35min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/35min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])


x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 40min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/40min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])


x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)




################# 45min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/45min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])


x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 50min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/50min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])

x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 55min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/55min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])


x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 60min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/60min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
anger=[]
sadness=[]
joy=[]
fear=[]
disgust=[]
i=0
for key in dict_:
		val=(dict_[key])
		val=ast.literal_eval(val)
		anger.append(val["anger"])
		sadness.append(val["sadness"])
		joy.append(val["joy"])
		fear.append(val["fear"])
		disgust.append(val["disgust"])

x1=[]
x1.append(statistics.mean(anger))
x1.append(statistics.stdev(anger))
x1.append(statistics.variance(anger))
x2=[]
x2.append(statistics.mean(sadness))
x2.append(statistics.stdev(sadness))
x2.append(statistics.variance(sadness))
x3=[]
x3.append(statistics.mean(joy))
x3.append(statistics.stdev(joy))
x3.append(statistics.variance(joy))
x4=[]
x4.append(statistics.mean(fear))
x4.append(statistics.stdev(fear))
x4.append(statistics.variance(fear))
x5=[]
x5.append(statistics.mean(disgust))
x5.append(statistics.stdev(disgust))
x5.append(statistics.variance(disgust))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

print("final_emo :::::",final_list_score)


dict_={}
final_list_score=[]
with open("senti_nochange_up.csv", 'r') as f:
	mycsv = csv.reader(f,delimiter=";")
	for row in mycsv:
		# if()
		# if('\;' in row[1]):
		# 	print("apoo")
		# # row=row[1].replace("")
		id_=row[0]
		label=row[2]
		score=row[1]
		if id_ not in dict_:
			dict_[id_]={"score":score,"label":label}
		# print(x)
# print(dict_)
with open("dic_senti_viral.json", "w+") as f4:
	f4.write(json.dumps(dict_))


list_tweet=[]
with open("../../identify_viralTweets/viral/data/5min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)

		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))


x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))


ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)


########## 10 min 
list_tweet=[]
with open("../../identify_viralTweets/viral/data/10min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))
		

x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))


ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)


############### 15min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/15min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))

x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

###################20min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/20min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))
		

x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

############### 25min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/25min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))

x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

############### 30min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/30min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))


x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

############### 35min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/35min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))
		

x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

############### 40min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/40min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))
		
x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

############### 45min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/45min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))

x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

############### 50min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/50min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# print("val",val)
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))
x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

############### 55min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/55min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))


x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)

############### 60min
list_tweet=[]
with open("../../identify_viralTweets/viral/data/60min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))
positive=[]
negative=[]
neutral=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in list_tweet :
			if val["label"] == "positive" :
				positive.append(float(val["score"]))
			if val["label"] == "negative" :
				negative.append(float(val["score"]))
			if val["label"] == "neutral" :
				neutral.append(float(val["score"]))

x1=[]
x1.append(statistics.mean(positive))
x1.append(statistics.stdev(positive))
x1.append(statistics.variance(positive))

x2=[]
x2.append(statistics.mean(negative))
x2.append(statistics.stdev(negative))
x2.append(statistics.variance(negative))

x3=[]
x3.append(statistics.mean(neutral))
x3.append(statistics.stdev(neutral))
x3.append(statistics.variance(neutral))

ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)

final_list_score.append(ll)
print("final senti ::::::::",final_list_score)