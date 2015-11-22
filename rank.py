import tweepy
import constants
import sys

auth = tweepy.OAuthHandler(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
auth.set_access_token(constants.ACCESS_KEY, constants.ACCESS_SECRET)
api = tweepy.API(auth)

trends1 = api.trends_place(1) # from the end of your code
# trends1 is a list with only one element in it, which is a 
# dict which we'll put in data.
data = trends1[0] 
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'] for trend in trends]
# put all the names together with a ' ' separating them

for t in names:
	print t
