import tweepy
import constants
from scraper import *
from difflib import SequenceMatcher

class Rank:
    """
    Ranking Algorithm class
    """
    def __init__(self):
        self.location = 1 #1 is GLOBAL

    def trending(self):
        auth = tweepy.OAuthHandler(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
        auth.set_access_token(constants.ACCESS_KEY, constants.ACCESS_SECRET)
        api = tweepy.API(auth)

        #set trends place
        trends1 = api.trends_place(self.location)
        data = trends1[0] 

        # grab the trends
        trends = data['trends']
        # grab the name from each trend
        twitter_trending = [trend['name'] for trend in trends]
        # put all the names together with a ' ' separating them
        return twitter_trending
    
    def ratio(self, s1, s2):
        m = SequenceMatcher(None, s1, s2);
        return m.ratio();

    def news_headlines(self):
        nytimes = NYTimes()
        aljazeera = Aljazeera()
        cnn = CNN()
        washingtonpost = WashingtonPost()
        spiegel = Spiegel()
        bbc = BBC()
        independent = Independent()
        timemagazine = TimeMagazine()

        headlines = []
        headlines.extend(nytimes.get_headline_texts())
        headlines.extend(aljazeera.get_headline_texts())
        headlines.extend(cnn.get_headline_texts())
        headlines.extend(washingtonpost.get_headline_texts())
        # headlines.extend(spiegel.get_headline_texts())
        headlines.extend(bbc.get_headline_texts())
        # headlines.extend(independent.get_headline_texts())
        headlines.extend(timemagazine.get_headline_texts())
        
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

    def rank(self):
        headlines = self.news_headlines()
        trending = self.trending()


if __name__ == '__main__':
    rank = Rank()
    print rank.news_headlines()
