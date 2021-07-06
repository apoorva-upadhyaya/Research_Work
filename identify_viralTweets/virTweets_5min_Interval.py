import json
import matplotlib.pyplot as plt
import os
import io, pickle
import networkx as nx
from datetime import datetime 
import time
datetimeFormat='%a %b %d %H:%M:%S %z %Y'

import operator

file_ob=open("viral/600/data/dict_10_new.json",'r')
dict_10_new=json.load(file_ob)

new={}

for key in dict_10_new:
	new[key]=dict_10_new[key]["time"]

sorted_dic = sorted(new.items(), key=operator.itemgetter(1))

print("sorted_dic",len(sorted_dic)) 

date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=300):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("5min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("5min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("5min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()

########## 10min
date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff <=600):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("10min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("10min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("10min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()
############### 20 mins :

file_ob=open("viral/600/data/dict_20_new.json",'r')
dict_10_new=json.load(file_ob)

new={}

for key in dict_10_new:
	new[key]=dict_10_new[key]["time"]

sorted_dic = sorted(new.items(), key=operator.itemgetter(1))

print("sorted_dic",len(sorted_dic)) 

date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=900):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("15min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("15min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("15min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()


ate1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if diff <=1200:
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("20min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("20min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("20min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()


################## 30 min

file_ob=open("viral/600/data/dict_30_new.json",'r')
dict_10_new=json.load(file_ob)

new={}

for key in dict_10_new:
	new[key]=dict_10_new[key]["time"]

sorted_dic = sorted(new.items(), key=operator.itemgetter(1))

print("sorted_dic",len(sorted_dic)) 

date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=1500):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("25min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("25min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("25min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()


date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=1800):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("30min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("30min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("30min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()


############## 40 min

file_ob=open("viral/600/data/dict_40_new.json",'r')
dict_10_new=json.load(file_ob)

new={}

for key in dict_10_new:
	new[key]=dict_10_new[key]["time"]

sorted_dic = sorted(new.items(), key=operator.itemgetter(1))

print("sorted_dic",len(sorted_dic)) 


date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=2100):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("35min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("35min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("35min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()


date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=2400):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("40min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("40min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("40min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()


################## 50 mins

file_ob=open("viral/600/data/dict_50_new.json",'r')
dict_10_new=json.load(file_ob)

new={}

for key in dict_10_new:
	new[key]=dict_10_new[key]["time"]

sorted_dic = sorted(new.items(), key=operator.itemgetter(1))

print("sorted_dic",len(sorted_dic)) 


date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=2700):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("45min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("45min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("45min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()



date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=3000):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("50min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("50min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("50min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()


############ 60 mins

file_ob=open("viral/600/data/dict_60_new.json",'r')
dict_10_new=json.load(file_ob)

new={}

for key in dict_10_new:
	new[key]=dict_10_new[key]["time"]

sorted_dic = sorted(new.items(), key=operator.itemgetter(1))

print("sorted_dic",len(sorted_dic)) 


date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=3300):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("55min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("55min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("55min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()



date1=sorted_dic[0][1]
set_keys=set()
set_keys.add(sorted_dic[0][0])
for key,data in sorted_dic:
	date2=data
	diff=datetime.strptime(date2, datetimeFormat) - datetime.strptime(date1, datetimeFormat)
	# print("date2",date2)
	# print("date1",date1)
	# print(diff.seconds)
	diff=diff.seconds
	if (diff<=3600):
		set_keys.add(key)
	# break

print("len of set",len(set_keys))
set_keys=list(set_keys)

li_user=[]
li_text=[]
for key in set_keys :
	li_user.append(dict_10_new[key]["user"])
	li_text.append(dict_10_new[key]["text"])

with open("60min/tweets.txt","w") as f:
	for i in range(len(set_keys)):
		f.write(str(set_keys[i]))
		f.write("\n")
		f.flush()

with open("60min/text.txt","w") as f:
	for i in range(len(li_text)):
		f.write(str(li_text[i]))
		f.write("\n")
		f.flush()

with open("60min/users.txt","w") as f:
	for i in range(len(li_user)):
		f.write(str(li_user[i]))
		f.write("\n")
		f.flush()
