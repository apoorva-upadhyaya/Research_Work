######### procedure to calculate nw features #########


First, all the tweets found are sorted as per their creation timestamp.

followers/create_followers.py , friends/create_friends.py: Followers and friends of the users who tweeted/retweeted within particular time intervals are calculated.

nw_features.py script : Networks are created for each 5 min time interval , edges constitute follower-followee relation.
All network features such as mean number of nodes per tweet, connectivity(degree and giant component), clustering, reciprocity are calculated per network per time interval.

user_tweet_dict.py script: A dctionary is created containing user_id as key and correspondng tweets/retweets objects of users. This is required for cascade and user features.


