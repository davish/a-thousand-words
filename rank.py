#import tweepy
from difflib import SequenceMatcher
import constants
from scraper import *
#import models

class Rank:
	"""
	Ranking Algorithm class
	"""
	def __init__(self):
  		self.location = 1

    def ratio(self, s1, s2):
        m = SequenceMatcher(None, s1, s2);
        return m.ratio();
	#def trending(self):
  	#	auth = tweepy.OAuthHandler(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
	#	auth.set_access_token(constants.ACCESS_KEY, constants.ACCESS_SECRET)
	#	api = tweepy.API(auth)
#
	#	#set trends place
	#	trends1 = api.trends_place(self.location)
	#	data = trends1[0] 
#
	#	# grab the trends
	#	trends = data['trends']
	#	# grab the name from each trend
	#	twitter_trending = [trend['name'] for trend in trends]
	#	# put all the names together with a ' ' separating them
	#	return twitter_trending

	def news_headlines_images(self):
		nytimes = NYTimes()
		aljazeera = Aljazeera()
		cnn = CNN()
		bbc = BBC()
		independent = Independent()
		timemagazine = TimeMagazine()

		headlines = []
		headlines.extend(nytimes.get_headline_texts())
		headlines.extend(aljazeera.get_headline_texts())
		headlines.extend(cnn.get_headline_texts())
		headlines.extend(bbc.get_headline_texts())
		headlines.extend(timemagazine.get_headline_texts())

		images = []
		images.extend(nytimes.get_image_urls())
		images.extend(aljazeera.get_image_urls())
		images.extend(cnn.get_image_urls())
		images.extend(bbc.get_image_urls())
		images.extend(timemagazine.get_image_urls())

		urls = []
		urls.extend(nytimes.get_headline_urls())

        headlines = filter(None, headlines)
        ranked = []

        for h1 in headlines:
            add = 1
            for h2 in ranked:
                try:
                    if self.ratio(h1, h2) > 0.2:
                        print h1
                        print "\n"
                        add = 0
                        break
                    break
                except:
                    print 'some error'
            if add:
                ranked.append(h1);

        return ranked

		res = []
		for headline, image, url in zip(headlines, images, urls):
			if headline is not None and image is not None and url is not None:
				res.append([headline, image, url])

		return res


if __name__ == '__main__':
	rank = Rank()
	print rank.news_headlines_images()

