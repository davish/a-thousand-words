#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.ext import vendor
from rank import *
import scraper
import models
import datetime

vendor.add('lib')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class ScrapeNews(webapp2.RequestHandler):
	def get(self):
		rank = Rank()
		#news = rank.news_headlines_images()
		news = scraper.getFirstPictures()

		#headlines = models.Headline.all()
		#for headline in headlines:
		#	headline.delete()

		for n in news:
			headline = n[0].encode('ascii', 'ignore')
			image = n[1].encode('ascii', 'ignore')
			url = n[2].encode('ascii', 'ignore')
			source = n[3].encode('ascii', 'ignore')
			#if models.Headline.gql("WHERE url = :1", url).count() < 1:
			headline = models.Headline(headline=headline, image=image, url=url, source=source, time=datetime.datetime.now())
			headline.put()
		self.response.out.write("Sometimes, you eat the bear... and sometimes, well, the bear eats you")

class GetNews(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
			<html>
	<head>
		<title>News in Pictures</title>
		<link rel="stylesheet" href="./style.css">
		<meta http-equiv="refresh" content="600; URL=/">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"/>
        <meta http-equiv="Pragma" content="no-cache"/>
        <meta http-equiv="Expires" content="0"/>
	</head>
	<body>
			""")
		headlines = models.Headline.gql("WHERE time != DATE('2015-01-01') ORDER BY time DESC").fetch(limit=6)

		for headline in headlines:
			self.response.out.write('<div class="img" style="background-image: url(\'' + str(headline.image) + '\');">')
			self.response.out.write('<a href="' + str(headline.url) + '">')
			self.response.out.write('<span class="text-content">')
			self.response.out.write('<span class="headline">')
   		 	self.response.out.write(str(headline.headline))
			self.response.out.write('</span>')
			self.response.out.write('<span class="blurb">')
			self.response.out.write('Blurb goes here')
   		 	self.response.out.write('</span>')
   		 	self.response.out.write('<span class=logo>')
   		 	self.response.out.write('<img src="/' + str(headline.source) +'.png" alt="">')
   		 	self.response.out.write('</span>')
			self.response.out.write('</span>')
			self.response.out.write('</a>')
			self.response.out.write('</div>')
			self.response.out.write('\n')

		self.response.out.write("""

		</body>
		</html>


			""")
		


app = webapp2.WSGIApplication([
	('/', GetNews),
	('/scrape', ScrapeNews),
], debug=True)
