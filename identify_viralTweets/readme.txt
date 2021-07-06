######### steps to be followed ########

identifyNumberViralTweets.py : script extracts the viral tweets from all the tweet objects collected. We select top 2% of tweets whose retweet count is greater than a threshold (say 1000) and consider them as viral tweets. The rest of them are considered as non-viral.

virTweets_5min_Interval.py: sort all the tweets as per their creatime timestamp. All the tweets,corresponding author and text are divided into 5min interval upto 1 hour starting from the first tweet of the event.

create_diction_viral_nv_frequency.py: creates viral and non-viral dictionary with tweet id as key and frequency of retweets per time interval 

