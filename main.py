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
import models
import datetime

vendor.add('lib')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class ScrapeNews(webapp2.RequestHandler):
	def get(self):
		rank = Rank()
		news = rank.news_headlines_images()

		for n in news:
			headline = n[0].encode('ascii', 'ignore')
			image = n[1].encode('ascii', 'ignore')
			url = n[2].encode('ascii', 'ignore')
			headline = models.Headline(headline=headline, image=image, url=url, time=datetime.datetime.now().date())
			headline.put()

class GetNews(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("""
			<html>
	<head>
		<title>a-thousand-words</title>
		<link rel="stylesheet" href="./style.css">
	</head>
	<body>
			""")
		headlines = models.Headline.gql('WHERE time = :1', datetime.datetime.now().date()).fetch(limit=9)

		for headline in headlines:
			self.response.out.write('<div class="img" title="' + str(headline.headline) + '"">')
			self.response.out.write('<a href="' + str(headline.url) + '">')
			self.response.out.write('<img src="' + str(headline.image) + '" alt="' + str(headline.headline) + '">')
			self.response.out.write('</a>')
			self.response.out.write('</div>')

		self.response.out.write("""

		</body>
		</html>


			""")
		


app = webapp2.WSGIApplication([
	('/', GetNews),
	('/scrape', ScrapeNews),
], debug=True)
