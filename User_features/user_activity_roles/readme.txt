We identify user structural role and activity as features.

Structural Importance of rule is based on their hubs and authority scores calculated using HITS Algorithm. Users are divided as :
a.seekers, who have high hub and low authority scores;
b.sharers, who have high authority and low hub scores; 
c.leaders, who have high hub as well as high authority scores; 
d.fringe, who have low hub and low authority scores.

User Activity considers both the number of tweets made by the user as well as the average frequency of her engagement on Twitter. We consider a user as active if the activity score is greater than a threshold and the threshold values are determined by the head/tail breaks algorithm.

User Behavior : We scrutinize the Big Five Model(Big5) [Ack19] to acquire personality traits (Openness to Experience, Conscientiousness, Extraversion, Agreeableness, Neuroticism). We make use of the Personality Insights service of IBM Cloud. In order to predict the scores of each of the five traits, we fed
a maximum of 3200 previous tweets of the users extracted using the script and find the personality trait scores using -- script.  
