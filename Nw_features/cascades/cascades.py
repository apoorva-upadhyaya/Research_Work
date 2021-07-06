import json, io, os, pickle
import networkx as nx
from datetime import datetime
import time
from dateutil import tz
from collections import Counter
import statistics
def to_epoch(date_str):
	utc_time = datetime.strptime(date_str, '%a %b %d %H:%M:%S +0000 %Y')
	start = datetime.strptime('Jan 01 00:00:00 1970', '%b %d %H:%M:%S %Y')
	epoch_time = (utc_time - start).total_seconds()	
	return int(epoch_time)

def to_days(epoch_this, epoch_that):
	difference = epoch_that - epoch_this
	days = float(difference) / 86400

	return days

def check_valid(epoch_this, epoch_that, latency)	:
	days = to_days(epoch_this, epoch_that)
	return days > 0 and days <= latency

def search(users, content, pdan, latency, cascade, seen):
	new_users = {}
	for user in users:
		this_tweet = users[user]
		this_time = to_epoch(this_tweet['created_at'])
		for follower in [x[0] for x in pdan.in_edges(user) if x[0] not in cascade]:
			consider_tweets = [x for x in content[follower] if check_valid(this_time, to_epoch(x['created_at']), latency) and x['id'] not in seen]
			for tweet in consider_tweets:
				content[follower].remove(tweet)

			if len(consider_tweets) > 0:
				#that_time = max([to_epoch(x['created_at']) for x in consider_tweets])
				that_tweet = max(consider_tweets, key = lambda x : x['created_at'])
				that_time = to_epoch(that_tweet['created_at'])
				new_users[follower] = that_tweet
				cascade.add_edge(user, follower)
				for tweet in consider_tweets:
					seen[tweet['id']] = 1 

				if 'created_at' not in cascade.node[user]:
					cascade.node[user]['created_at'] = this_time
					cascade.node[user]['tweet_id'] = this_tweet['id']
				cascade.node[follower]['created_at'] = that_time	
				cascade.node[follower]['tweet_id'] = that_tweet['id']	
				

	return new_users, seen, cascade

def get_cascade(seen, sorted_tweets, pdan, content, latency = 9):
	# get seed to start
	seed = None
	for x in sorted_tweets:
		if x['id'] not in seen:
			seed = x
			seen[x['id']] = 1
			break;

	if seed == None:
		return None, None, None

	print("Found seed {}".format(seed['id']))
	user = seed['user']['id_str']
	content[user].remove(seed)

	search_users = {user: seed}
	cascade = nx.DiGraph()
	i = 1
	while len(search_users) > 0:
		print("Iteration {} {} users".format(i, len(search_users)))
		i += 1
		new_users, seen, cascade = search(search_users, content, pdan, latency, cascade, seen)
		search_users = new_users

	return cascade, seen, seed['id']

import jsonpickle


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


if __name__ == '__main__':
	
	users_all=set()
	final_list_all=[]
	final_nodes=[]
	with open("../../identify_viralTweets/viral/data/5min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_5min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("5 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_5min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_5min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	final_nodes.append(len(list_win))
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("5minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)


	#################### 10min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/10min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_10min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("10 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_10min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_10min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	final_nodes.append(len(list_win))
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("10minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

	


		#################### 15min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/15min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_15min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("15 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_15min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_15min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("15minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

		#################### 20min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/20min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_20min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("20 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_20min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_20min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("20minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

		#################### 25min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/25min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_25min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("25 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_25min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_25min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("25minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

		#################### 30min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/30min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_30min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("30 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_30min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_30min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("30minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

		#################### 35min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/35min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_35min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("35 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_35min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_35min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("35minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)
		#################### 40min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/40min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_40min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("40 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_40min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_40min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("40minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

		#################### 45min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/45min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_45min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("45 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_45min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_45min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("45minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

		#################### 50min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/50min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_50min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("50 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_50min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_50min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("50minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

		#################### 55min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/55min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_55min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("55 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_55min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_55min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("55minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

		#################### 10min
	users_all=set()

	with open("../../identify_viralTweets/viral/data/60min/users.txt",'r',encoding='utf-8') as file:
		for line in file:
			line=line.rstrip()
			id_=line
			users_all.add(str(id_))
	print("Loading network...")
	# pdan_retweet = pickle.load(open('baduria_followers_nw.pkl'))
	with open('../nw_60min.pkl','rb') as file:
			pdan_retweet = pickle.load(file)
	
	print("10 minutes ###########")
	total_nodes=pdan_retweet.nodes()
	file_ob=open("../dic_user_tweets.json",'r')
	tweets=json.load(file_ob)
	users_all=pdan_retweet.nodes()
	content = {}
	for user in tweets:
		if user in users_all:
			content[user] = tweets[user]
			content[user] = sorted(content[user], key = lambda x : x['created_at'])
	
	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))	
	list_nodes= list(pdan_retweet.nodes())
	set_nodes=set(content.keys())

	for i in list_nodes:
		if i not in set_nodes:
			pdan_retweet.remove_node(i)

	# print("Total users = {}".format(len(content)))	
	# print("graph users",len(pdan_retweet.nodes()))

	# sorted tweets by date
	dict_={}
	seen = {}
	tweet_sorted = []
	for user in content:
		for tweet in content[user]:
			tweet_sorted.append(tweet)

	tweet_sorted = sorted(tweet_sorted, key = lambda x : to_epoch(x['created_at']))
	# print("tweet_sorted ########  ",tweet_sorted[0])
	# print("tweet_sorted#########",tweet_sorted[1])
	# print("###############",tweet_sorted[2])
	# print("Total tweets = {}".format(len(tweet_sorted)))

	size = len(tweet_sorted)
	flag=0
	

	while (len(seen) != size):
		cascade, seen, seed_id = get_cascade(seen, tweet_sorted, pdan_retweet, content)
		if(cascade != None):
			# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
		 	# if len(cascade.nodes) > 0:
			if len(cascade.nodes) ==0:
				print("no cascades")

			else:
				# print("Cascade {}, seen {}".format(len(cascade.nodes), len(seen)))
				with open('cascades/' + str(seed_id)  + '.pkl', 'wb') as outfile:		
					pickle.dump(cascade, outfile)
		if(seen == None) :
			break

	list_depth=[]		
	import os
	files_path="cascades"
	dict_={}
	list_short_path=[]
	for filename in os.listdir(files_path):
		# print(filename)
		name=filename.split(".")
		# print("name::",name[0])
		# seed=name[0]
		filename=files_path+"/"+filename
		with open(filename,'rb') as file:
			cascade = pickle.load(file)
			no_nodes=len(cascade.nodes())
			if(no_nodes>0):
				avg_short_path=nx.average_shortest_path_length(cascade)
				# print("avg_short_path",avg_short_path)

				H = cascade.to_undirected()
				n=no_nodes
				weiner_index= nx.wiener_index(H)
				weiner_index=float(weiner_index/(n*(n-1)))
				# print("weiner_index",weiner_index)
				avg_short_path=nx.average_shortest_path_length(H)
				# print("avg_short_path undire",avg_short_path)
				
				nodes_=list(cascade.nodes())
				no_edges=len(cascade.edges())
				first_neigh=[1]
				sec_neigh=[1]
				# print("first_neigh :",len(first_neigh))
				# list_=list(nx.dfs_edges(H))
				li=[]
				for i in nodes_:
					x=list(nx.edge_dfs(cascade,i,orientation='original'))
					# print("x:",x)
					li.append(len(x))

				# list_depth.append(len(list_))
				max_depth=max(li)
				# if(max_depth==29):
				list_succ=[]
				for i in nodes_:
					dic=nx.dfs_successors(cascade,i)
					# print("successors:",i,dic)
					if i in dic:
						list_=dic[i]
						list_succ.append(len(list_))

					# x=nx.to_numpy_matrix(cascade)
					# print(x)
				max_succ=max(list_succ)
				list_depth=[]
				for i in nodes_:
					dic=nx.shortest_path_length(cascade,i)
					li=[]
					for key in dic:
						li.append(dic[key])
					max_=max(li)
					list_depth.append(max_)

					# print(nx.shortest_path_length(cascade,str(name[0])))
				# print("G.edges()::",cascade.edges())
				max_depth=statistics.mean(list_depth)
				avg_depth=nx.diameter(H)
			
				dict_[name[0]]={"nodes":no_nodes,"no_edges":no_edges,"avg_short_path":avg_short_path,"win":weiner_index,"first_neigh":len(first_neigh),"sec_neigh":len(sec_neigh),
				"max_depth":max_depth,"diameter":avg_depth,"max_succ":max_succ,}

		with open("dict_cascades_60min.json", "w+") as f4:
			 		# f4.write(json.dumps(dict_))
			 		f4.write(json.dumps(dict_))
	import operator
	sorted_d=sorted(dict_.values(),key=lambda k: k['win'],reverse=True)
	# print("############## win ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['nodes'],reverse=True)
	# print("############## nodes ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['avg_short_path'],reverse=True)
	# print("############## avg_short_path ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['first_neigh'],reverse=True)
	# print("############## first_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['sec_neigh'],reverse=True)
	# print("############## sec_neigh ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_depth'],reverse=True)
	# print("############## max_depth ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['diameter'],reverse=True)
	# print("############## diameter ::::",(sorted_d[:5]))
	sorted_d=sorted(dict_.values(),key=lambda k: k['max_succ'],reverse=True)
	# print("############## max_succ ::::",(sorted_d[:5]))



	file_ob=open("dict_cascades_60min.json",'r')
	dict_cascades=json.load(file_ob)

	list_win=[]
	list_path=[]
	list_nodes=[]
	list_max_depth=[]
	list_diameter=[]
	list_first=[]
	list_second=[]
	list_max_succ=[]
	for key in dict_cascades :
		val=dict_cascades[key]["win"]
		list_win.append(val)
		list_path.append(dict_cascades[key]["avg_short_path"])
		list_nodes.append(dict_cascades[key]["nodes"])
		list_max_depth.append(dict_cascades[key]["max_depth"])
		list_diameter.append(dict_cascades[key]["diameter"])
		list_first.append(dict_cascades[key]["first_neigh"])
		list_second.append(dict_cascades[key]["sec_neigh"])
		list_max_succ.append(dict_cascades[key]["max_succ"])
	
	print("mean list_win ::",statistics.mean(list_win))
	print("std dev list_win ::",statistics.stdev(list_win))
	print("variance list_win ::",statistics.variance(list_win))

	print("mean avg_depth ::",statistics.mean(list_max_depth))
	print("std dev list_avg_depth ::",statistics.stdev(list_max_depth))
	print("variance list_avg_depth ::",statistics.variance(list_max_depth))
	list_5minutes=[]
	list_5minutes.append(statistics.mean(list_win))
	list_5minutes.append(statistics.stdev(list_win))
	list_5minutes.append(statistics.variance(list_win))
	list_5minutes.append(statistics.mean(list_max_depth))
	list_5minutes.append(statistics.stdev(list_max_depth))
	list_5minutes.append(statistics.variance(list_max_depth))
	print("60minutes#################",list_5minutes)
	final_list_all.append(list_5minutes)

	print('final list::::::',final_list_all)
	print("	final_nodes.append(len(list_win",	final_nodes)