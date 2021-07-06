import csv
count=0
dict_={}
import json
import statistics

import ast 

final_list_score=[]

file_ob=openness("result_user_profile.json",'r')
dict_=json.load(file_ob)

print("len :::::",len(dict_))

users_all=set()
with open("../../identify_viralTweets/viral/data/5min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])
			

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)




############# 10min

users_all=set()
with open("../../identify_viralTweets/viral/data/10min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])
		

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)



###########15min
users_all=set()
with open("../../identify_viralTweets/viral/data/15min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

############# 20min
users_all=set()
with open("../../identify_viralTweets/viral/data/20min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))


openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])
		

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)
#positive,nega,neutral

############# 25min

users_all=set()
with open("../../identify_viralTweets/viral/data/25min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])
			

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)


################# 30min
users_all=set()
with open("../../identify_viralTweets/viral/data/30min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 35min
users_all=set()
with open("../../identify_viralTweets/viral/data/35min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 40min
users_all=set()
with open("../../identify_viralTweets/viral/data/40min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])
			

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)




################# 45min
users_all=set()
with open("../../identify_viralTweets/viral/data/45min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])
	

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 50min
users_all=set()
with open("../../identify_viralTweets/viral/data/50min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 55min
users_all=set()
with open("../../identify_viralTweets/viral/data/55min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 60min
users_all=set()
with open("../../identify_viralTweets/viral/data/60min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['percentile'])
			cons.append(val['personality'][1]['percentile'])
			extra.append(val['personality'][2]['percentile'])
			agree.append(val['personality'][3]['percentile'])
			neur.append(val['personality'][4]['percentile'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

print("final_user beahv :::::",final_list_score)


################## raw score
users_all=set()
with open("../../identify_viralTweets/viral/data/5min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)




############# 10min
users_all=set()
with open("../../identify_viralTweets/viral/data/10min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])
	

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)



###########15min
users_all=set()
with open("../../identify_viralTweets/viral/data/15min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])
		

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

############# 20min
users_all=set()
with open("../../identify_viralTweets/viral/data/20min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)
#positive,nega,neutral

############# 25min
users_all=set()
with open("../../identify_viralTweets/viral/data/25min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))

openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 30min
users_all=set()
with open("../../identify_viralTweets/viral/data/30min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 35min
users_all=set()
with open("../../identify_viralTweets/viral/data/35min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])
		
x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 40min
users_all=set()
with open("../../identify_viralTweets/viral/data/40min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)




################# 45min
users_all=set()
with open("../../identify_viralTweets/viral/data/45min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 50min
users_all=set()
with open("../../identify_viralTweets/viral/data/50min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])
		

x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 55min
users_all=set()
with open("../../identify_viralTweets/viral/data/55min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

################# 60min
users_all=set()
with open("../../identify_viralTweets/viral/data/60min/users.txt",'r',encoding='utf-8') as file:
	for line in file:
		line=line.rstrip()
		id_=line
		users_all.add(str(id_))
openness=[]
cons=[]
extra=[]
agree=[]
neur=[]
i=0
for key in dict_:
		val=(dict_[key])
		# val=ast.literal_eval(val)
		if key in users_all :
			openness.append(val['personality'][0]['raw_score'])
			cons.append(val['personality'][1]['raw_score'])
			extra.append(val['personality'][2]['raw_score'])
			agree.append(val['personality'][3]['raw_score'])
			neur.append(val['personality'][4]['raw_score'])


x1=[]
x1.append(statistics.mean(openness))
x1.append(statistics.stdev(openness))
x1.append(statistics.variance(openness))
x2=[]
x2.append(statistics.mean(cons))
x2.append(statistics.stdev(cons))
x2.append(statistics.variance(cons))
x3=[]
x3.append(statistics.mean(extra))
x3.append(statistics.stdev(extra))
x3.append(statistics.variance(extra))
x4=[]
x4.append(statistics.mean(agree))
x4.append(statistics.stdev(agree))
x4.append(statistics.variance(agree))
x5=[]
x5.append(statistics.mean(neur))
x5.append(statistics.stdev(neur))
x5.append(statistics.variance(neur))
ll=[]
ll.append(x1)
ll.append(x2)
ll.append(x3)
ll.append(x4)
ll.append(x5)
final_list_score.append(ll)

print("final_user beahv :::::",final_list_score)