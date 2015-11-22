from twitter import *
import constants

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = twitter.Twitter(
            auth = OAuth(constants.ACCESS_KEY, constants.ACCESS_SECRET, constants.CONSUMER_KEY, constants.CONSUMER_SECRET))

#-----------------------------------------------------------------------
# retrieve global trends.
# other localised trends can be specified by looking up WOE IDs:
#   http://developer.yahoo.com/geo/geoplanet/
# twitter API docs: https://dev.twitter.com/docs/api/1/get/trends/%3Awoeid
#-----------------------------------------------------------------------
results = twitter.trends.place(_id = 1)

print "Global Trends"

for location in results:
    for trend in location["trends"]:
        print " - %s" % trend["name"]
