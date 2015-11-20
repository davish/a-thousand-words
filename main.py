import webapp2
import bs4
import urllib2

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hello, World!');

app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)