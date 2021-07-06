import json
import matplotlib.pyplot as plt
import os
import io, pickle
import networkx as nx
from datetime import datetime 
import time
datetimeFormat='%a %b %d %H:%M:%S %z %Y'



file_ob=open("../Nw_features/dic_user_tweets.json",'r')
dic_user_tweets=json.load(file_ob)

total_result=[]
def htb(data):
 
    assert data, "Input must not be empty."
    assert all(isinstance(datum, int) or isinstance(datum, float) for datum in data), "All input values must be numeric."

    results = []  # array of break points

    def htb_inner(data):
    
        data_length = float(len(data))
        data_mean = sum(data) / data_length
        results.append(data_mean)
        head = [datum for datum in data if datum > data_mean]
        while len(head) > 1 and len(head) / data_length < 0.40:
            return htb_inner(head)
    htb_inner(data)
    return results

def n_hop(graph, nodes, n):
	result = set(nodes)
	new = set(nodes)
	for i in range(n):
		traversed = []
		for node in new:
			traversed.extend([n for n in graph.neighbors(node)])
		traversed = set(traversed)
		new = traversed.difference(result)
		result = traversed.union(result)
	return result.difference(set(nodes))




with open('../Nw_features/nw_5min.pkl','rb') as file:
	foll_nw = pickle.load(file)

nodes_=foll_nw.nodes()
no_of_nodes=len(nodes_)
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 100, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/5min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)

print("list_score1",list_score1)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)


len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per Inactive users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/no_of_nodes))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/no_of_nodes))


total_result.append(list_results)

print("5 minutes ############")
print("total_result :: ",list_results)

#################10min 

with open('../Nw_features/nw_10min.pkl','rb') as file:
	foll_nw = pickle.load(file)


nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 50, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/10min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)


len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)


print("10 minutes ############")
print("total_result :: ",list_results)


################# 15min

with open('../Nw_features/nw_15min.pkl','rb') as file:
	foll_nw = pickle.load(file)


nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/15min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)


len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)


print("15 minutes ############")
print("total_result :: ",list_results)


######################20min

with open('../Nw_features/nw_20min.pkl','rb') as file:
	foll_nw = pickle.load(file)

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/20min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)

# results activity list_score:::  [2.590971501615742e-06, 6.842442088209738e-05, 0.00025232947921753103, 0.00045410834490864407, 0.0006544502617801048]

len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)


print("20 minutes ############")
print("total_result :: ",list_results)


################## 25min

with open('../Nw_features/nw_25min.pkl','rb') as file:
	foll_nw = pickle.load(file)

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/25min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)


len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)

print("25 minutes ############")
print("total_result :: ",list_results)


#################### 30min

with open('../Nw_features/nw_30min.pkl','rb') as file:
	foll_nw = pickle.load(file)

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/30min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)


len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)

print("30 minutes ############")
print("total_result :: ",list_results)

###################### 35min

with open('../Nw_features/nw_35min.pkl','rb') as file:
	foll_nw = pickle.load(file)

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/35min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)

len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)


print("40 minutes ############")
print("total_result :: ",list_results)

###############40min
with open('../Nw_features/nw_40min.pkl','rb') as file:
	foll_nw = pickle.load(file)

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/40min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)

len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)

print("40 minutes ############")
print("total_result :: ",list_results)

##############45min
with open('../Nw_features/nw_45min.pkl','rb') as file:
	foll_nw = pickle.load(file)

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/45min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)

len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)

print("45 minutes ############")
print("total_result :: ",list_results)

################# 50min

with open('../Nw_features/nw_50min.pkl','rb') as file:
	foll_nw = pickle.load(file)

# with open('../../../identify_viralTweets/viral/data/preprocessing/'+city+'/user_rest_nw.pkl','rb') as file:
# 			user_rest_nw = pickle.load(file)
# 		print("No. of nodes in user-rest extracted graph are",len(user_rest_nw))

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/50min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)

len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)

print("50 minutes ############")
print("total_result :: ",list_results)

################### 55min

with open('../Nw_features/nw_55min.pkl','rb') as file:
	foll_nw = pickle.load(file)

# with open('../../../identify_viralTweets/viral/data/preprocessing/'+city+'/user_rest_nw.pkl','rb') as file:
# 			user_rest_nw = pickle.load(file)
# 		print("No. of nodes in user-rest extracted graph are",len(user_rest_nw))

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/55min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)

len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)

print("55 minutes ############")
print("total_result :: ",list_results)

########################## 60min

with open('../Nw_features/nw_60min.pkl','rb') as file:
	foll_nw = pickle.load(file)

nodes_=foll_nw.nodes()
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))

out=dict(foll_nw.out_degree())

in_=dict(foll_nw.in_degree())

di={}
list_deg=[]
di_={}
count=0
isolated=set()
for key in in_:

	kin=in_[key]
	kout=out[key]
	if(kin ==0 and kout==0):
		count=count+1
		isolated.add(key)
		foll_nw.remove_node(key)
	elif(kout !=0):
		ratio=float(kin/kout)
		di[key]=float(ratio/len(in_))
		di_[key]=ratio
		list_deg.append(ratio)
	# di[key]=0
	# list_deg.append(0)

nodes_=foll_nw.nodes()
# print("No of isolated nodes :",count)
# print("ratio of isolated nodes :",count/len(nodes_))
# print("No of nodes ::",len(foll_nw.nodes()))

# print("No of edges ::",len(foll_nw.edges()))
list_deg1=sorted(list_deg,reverse=True)
list_deg=[float(x/len(in_)) for x in list_deg]




############ hubs, authorities 
hubs, authorities = nx.hits(foll_nw, max_iter = 500, normalized = True) 


list_hub=[]
for key in hubs:
	val=hubs[key]
	list_hub.append(val) 

list_auth=[]
for key in authorities:
	val=authorities[key]
	list_auth.append(val)


results_hub=htb(list_hub)
print("results of hub scores ::: ",results_hub)

results_auth=htb(list_auth)
print("results of auth scores ::: ",results_auth)


high_hub=[]
low_hub=[]
for key in hubs:
	val=hubs[key]
	if(val>results_hub[0]):
		high_hub.append(key)
	else:
		low_hub.append(key)

high_auth=[]
low_auth=[]
for key in authorities :
	val=authorities[key]
	if(val > results_auth[0]) :
		high_auth.append(key)
	else:
		low_auth.append(key)

print("high_hub ::", len(high_hub))
print("low_hub ::", len(low_hub))
print("high_auth ::", len(high_auth))
print("low_auth ::", len(low_auth))

print("len of hubs",len(hubs))

### high hub and low auth
seekers=[]
### low hub and high auth
sharers=[]
### high hub and high auth
leaders=[]
### low hub and low auth
inactive=[]


total_nodes=len(hubs)
for i in hubs:
	if(i in high_hub and i in low_auth ):
		seekers.append(i)
	elif(i in low_hub and i in high_auth) :
		sharers.append(i)
	elif(i in high_hub and i in high_auth) :
		leaders.append(i)
	elif(i in low_hub and i in low_auth) :
		inactive.append(i)

print("No of info seekers :",len(seekers))
print("Percentage of info seekers :",len(seekers)/total_nodes)
print("No of info sharers :",len(sharers))
print("Percentage of info sharers :",len(sharers)/total_nodes)
print("No of info leaders :",len(leaders))
print("Percentage of info leaders :",len(leaders)/total_nodes)
print("No of info inactive nodes :",len(inactive))
print("Percentage of info inactive nodes :",len(inactive)/total_nodes)


roles=[]
roles.append(len(seekers)/total_nodes)
roles.append(len(sharers)/total_nodes)
roles.append(len(leaders)/total_nodes)
roles.append(len(inactive)/total_nodes)


######## activeness ############


list_tweet=[]
with open("../../identify_viralTweets/viral/data/60min/tweets.txt",'r') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			list_tweet.append(str(id_))

dic_={}
for user in dic_user_tweets:
	if user in nodes_ :
		tweets=dic_user_tweets[user]
		for tweet in tweets:
			tid=tweet["id_str"]
			if tid in list_tweet:
				date_=tweet['created_at']
				# print(date_)
				tweet_time=tweet['created_at']
				datetime_object=datetime.strptime(str(tweet_time), '%a %b %d %H:%M:%S +0000 %Y')
				tweet_time = time.mktime(datetime_object.timetuple())
				u_id=tweet['user']['id_str']
				if u_id in nodes_ :
					if u_id not in dic_:
						list_=set()
						list_.add(tweet_time)
						dic_[u_id]=list_						
					elif u_id in dic_:
						li=dic_[u_id]
						li.add(tweet_time)
						dic_[u_id]=li

list_score=[]
dic_score={}
for key in dic_:
	list_=dic_[key]
	list_=sorted(list_)
	# print(list_)
	mod_Ti=len(list_)
	if(mod_Ti >1):
		last=list_[mod_Ti-1]
		first=list_[0]
		x=last-first
		li=(float)(x/(mod_Ti-1))
		score=(float)(mod_Ti/li)
		# score=(float)(score/len(dic_))
		dic_score[key]=score
		list_score.append(score)
	elif(mod_Ti==1):
		score=0
		dic_score[key]=0
		list_score.append(score)

# list_score=[float(x/len(dic_)) for x in list_score]

list_score1=sorted(list_score,reverse=True)
# plt.plot(list_score1)
# plt.title("activity_Score")
# plt.savefig("../user_feature/activity_Score.png")
# plt.clf()



# data = list(list_score) # data can be list or numpy array
# results = powerlaw.Fit(data)
# ax=powerlaw.plot_ccdf(data,color='b',linewidth=2)
# ax.grid(True)
# ax.set_xlabel('activity score of users')
# ax.set_ylabel('CCDF')

# plt.savefig("../user_feature//CCDF_activityScore.png")
# ax.remove()

results=htb(list_score)
print("results activity list_score::: ",results)

len_=len(results)
xxyy=results[0]
print("xxyy",xxyy)
nonzero=0
zero=0
high=0
list_high_active=[]
list_medium_active=[]
list_inactive=[]
medium=0
for key in dic_score:
	val=dic_score[key]
	if(val>xxyy):
			high=high+1
			list_high_active.append(key)
	else:
		zero=zero+1
		list_inactive.append(key)


print("zero activity score/ inactive users ::",len(list_inactive))
print("##### per in active users::",len(list_inactive)/len(nodes_))

print("high active users::",len(list_high_active))
print("##### per high active users::",len(list_high_active)/len(nodes_))

# list_high_active=set(list_high_active)
# s=info_booster.intersection(list_high_active)
# print("s::;",len(s))

first_nbrs=n_hop(foll_nw,list_high_active,1)
print("For HIGHLY Active  users ::::",len(list_high_active))
print("len of first hop neighbours:",(len(first_nbrs)))
print("Per covered first hop neighbours:",float((len(first_nbrs))/len(nodes_)))


list_results=[]
list_results.append(roles)
list_results.append(len(list_high_active)/len(nodes_))
list_results.append(len(list_inactive)/len(nodes_))
list_results.append(float((len(first_nbrs))/len(nodes_)))

total_result.append(list_results)

print("60 minutes ############")
print("total_result :: ",list_results)

print("results::::::",total_result)