from google.appengine.ext import db

class Headline(db.Model):
	url = db.StringProperty()
	headline = db.StringProperty()
	image = db.StringProperty()
	time = db.DateProperty()