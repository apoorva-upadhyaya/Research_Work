import json
import matplotlib.pyplot as plt
import os
import statistics

total_list_nodes=[]
total_list_edges=[]
total_list_deg=[]
total_list_gc=[]
total_list_gc_ratio=[]
total_list_cc=[]
total_list_recp=[]

file_ob=open("followers/dict_followers.json",'r')
dict_followers=json.load(file_ob)
print("dict_followers",len(dict_followers))


file_ob=open("../identify_viralTweets/viral/dict_600_info.json",'r')
dict_info=json.load(file_ob)

########### new_dict contains the tweet id as key and value as list of user that tweeted along with it's retweet users ######
new_dict={}

for tweet in dict_info:
	if tweet not in new_dict:
		li=dict_info[tweet]["rt_user"]
		li.append(dict_info[tweet]["user_id"])
		li1=set(li)
		# li1=list(li1)
		new_dict[tweet]=li1



##################### 5 mins Nw Creation & Features Computation ############
list_tweets=[]
with open("../identify_viralTweets/viral/data/5min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/5min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))


# print("No of nodes ::",len(G.nodes()))
# print("No of edges ::",len(G.edges()))


nx.write_gpickle(G,"nw_5min.pkl")

# with open('../../identify_viralTweets/viral/data/preprocessing/'+city+'/user_rest_nw.pkl','rb') as file:
# 			user_rest_nw = pickle.load(file)
# 		print("No. of nodes in user-rest extracted graph are",len(user_rest_nw))

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))

print("No of edges ::",len(G.edges()))


########## NO of nodes feature ::

########### feature_tweet contains no. of users involved with the tweet as original/retweet users within given time limit ##########
feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)

total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)

########### GC 
largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

print("feature_tweet",feature_tweet)
list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)



############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)


##################### 10 mins Nw Creation & Features Computation ############

list_tweets=[]
with open("../identify_viralTweets/viral/data/10min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/10min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))


nx.write_gpickle(G,"lock_followers_nw_10min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))

print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1


list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)


total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


########### GC

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1


list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)



##################### 15 mins Nw Creation & Features Computation ############
list_tweets=[]
with open("../identify_viralTweets/viral/data/15min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/15min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))



nx.write_gpickle(G,"nw_15min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))

print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1


list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)

total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


################ GC :::::::;

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

print("feature_tweet",feature_tweet)
list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

##################### 20 mins Nw Creation & Features Computation ############
list_tweets=[]
with open("../identify_viralTweets/viral/data/20min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/20min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))


nx.write_gpickle(G,"nw_20min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))

print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1


list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)

total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


############ GC

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

print("feature_tweet",feature_tweet)
list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)



############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

########### 25min #######################

list_tweets=[]
with open("../identify_viralTweets/viral/data/25min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/25min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))


nx.write_gpickle(G,"nw_25min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))

print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)

total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",len(largest))


################## GC
largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

print("feature_tweet",feature_tweet)
list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

############## 30min


list_tweets=[]
with open("../identify_viralTweets/viral/data/30min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/30min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))




nx.write_gpickle(G,"nw_30min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))
print("No of edges ::",len(G.edges()))

########## NO of nodes ::
feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)
total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]
	
for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


########## GC

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

print("feature_tweet",feature_tweet)
list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

############### 35min ###################


list_tweets=[]
with open("../identify_viralTweets/viral/data/35min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/35min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))


nx.write_gpickle(G,"nw_35min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))
print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)
total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


########### GC

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

print("feature_tweet",feature_tweet)
list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

###########################  40min

list_tweets=[]
with open("../identify_viralTweets/viral/data/40min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/40min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))



nx.write_gpickle(G,"nw_40min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))
print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)
total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


##############3 GC ::

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

################### 45min


list_tweets=[]
with open("../identify_viralTweets/viral/data/45min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/45min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))



nx.write_gpickle(G,"nw_45min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))
print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)
total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


############### GC :::::: 

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

################## 50min


list_tweets=[]
with open("../identify_viralTweets/viral/data/50min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/50min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))



nx.write_gpickle(G,"nw_50min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))
print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)
total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


############# GC

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

############## 55min


list_tweets=[]
with open("../identify_viralTweets/viral/data/55min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/55min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))



nx.write_gpickle(G,"nw_55min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))
print("No of edges ::",len(G.edges()))


########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)
total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)


########## GC

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1
list_feature=[]


for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)

############## 60min

list_tweets=[]
with open("../identify_viralTweets/viral/data/60min/tweets.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweets.append(str(id_))

users_all=set()

with open("../identify_viralTweets/viral/data/60min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))


users_all=list(users_all)

print("len users_all",len(users_all))

import networkx as nx
import os 
G=nx.DiGraph()
count=0
for user in dict_followers:
	if str(user) in users_all:
		followers=dict_followers[user]
		if (followers==[]):
			G.add_node(str(user))
			count=count+1
		else:	
			for i in range(0,len(followers)):
				if str(followers[i]) in users_all:
					# print((followers))
					G.add_edge(str(followers[i]),str(user))
				else:
					G.add_node(str(user))


					


nx.write_gpickle(G,"nw_60min.pkl")

nodes_=G.nodes()
print("No of nodes ::",len(G.nodes()))
print("No of edges ::",len(G.edges()))

########## NO of nodes ::

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in nodes_:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Nodes :::",feature_result)
total_list_nodes.append(feature_result)
total_list_edges.append(len(G.edges()))


############ degree

in_=dict(G.in_degree())
sum_=0
for key in in_:
	sum_=sum_+in_[key]

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				deg=in_[user]
				sum_=sum_+deg
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Degree :::",feature_result)
total_list_deg.append(feature_result)

############## GC

largest = max(nx.strongly_connected_components(G), key=len)
print("largest component nodes ::",(largest))


feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		feature_tweet[tweet]=0
		for user in li:
			if user in largest:
				feature_tweet[tweet]=feature_tweet[tweet]+1

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

list_feature1=[]
for i in list_feature:
	list_feature1.append(float(i/len(G.nodes())))


print("list_feature1",list_feature1)
feature_result=[]
feature_result.append(statistics.mean(list_feature1))
feature_result.append(statistics.stdev(list_feature1))
feature_result.append(statistics.variance(list_feature1))

print("GC component :::",feature_result)
total_list_gc_ratio.append(feature_result)


total_list_gc.append(len(largest))
len_=len(list_tweets)

gc_ratio=float(len(largest)/len_)
gc_ratio=float(gc_ratio/len(G.nodes()))

print("gc_ratio :::",gc_ratio)
# total_list_gc_ratio.append(gc_ratio)

no_comp = nx.number_strongly_connected_components(G)
print("no of components ",no_comp)

list_=[len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]
print("connected components:",list_)


############## clustering ::

# print("nx.average_clustering(G)",nx.clustering(G))

clust=dict(nx.clustering(G))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=clust[user]
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("Clustering :::",feature_result)
total_list_cc.append(feature_result)


############## reciprocity ::

# print("nx.reciprocity(G)",nx.reciprocity(G,nodes=G.nodes()))

recp=dict(nx.reciprocity(G,nodes=G.nodes()))

feature_tweet={}

for tweet in new_dict:
	if tweet in list_tweets:
		li=new_dict[tweet]
		sum_=0
		count=0
		for user in li:
			if user in nodes_:
				coeff=recp[user]
				if coeff ==None:
					coeff=0
				sum_=sum_+coeff
				count=count+1

		feature_tweet[tweet]=float(sum_/count)

list_feature=[]

for key in feature_tweet:
	list_feature.append(feature_tweet[key])	

feature_result=[]
feature_result.append(statistics.mean(list_feature))
feature_result.append(statistics.stdev(list_feature))
feature_result.append(statistics.variance(list_feature))

print("total_list_recp :::",feature_result)
total_list_recp.append(feature_result)





print("total_list_nodes ::",total_list_nodes)
print("total_list_edges ::",total_list_edges)
print("total_list_deg ::",total_list_deg)
# print("total_list_gc ::",total_list_gc)
print("total_list_gc_ratio ::",total_list_gc_ratio)
print("total_list_cc ::",total_list_cc)
print("total_list_recp ::",total_list_recp)

