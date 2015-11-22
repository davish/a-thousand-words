import sys
from bs4 import BeautifulSoup
import requests

class Newspaper:
  """
  Abstract class for scraping a newspaper for its headline images.

  Includes methods that we expect to be implemented for every newspaper.

  Methods are short on purpose, in order to compartmentalize scraping.
  If, for some site, it's hard to collect all the articles, the 
  get_articles() method can be long without making the code hard to read.

  If finding the headline is harder, that method can be longer and the rest 
  of the code can look very similar between newspapers.
  """

  def __init__(self, url):
    self.url = url
    self.html = requests.get(url).text
    self.soup = BeautifulSoup(self.html, 'html.parser')

  def refresh(self):
    self.html = requests.get(self.url).text
    self.soup = BeautifulSoup(self.html, 'html.parser')

  def get_articles(self):
    """ Get an array of articles on the homepage. """
    raise NotImplementedError('Abstract Method')

  def get_headline(self):
    """ Get the BS object for the headline. """
    raise NotImplementedError('Abstract Method')

  def get_headlines(self):
    raise NotImplementedError('Abstract Method')

  def get_headline_text(self):
    return self.get_headline().a.string

  def get_headline_url(self):
    return self.get_headline().a.get('href')

  def get_headline_texts(self):
    return [x.a.string for x in self.get_headlines()]

  def get_headline_urls(self):
    return self.get_headline.a.get('href')
  
  def get_headline_soup(self):
    page_url = self.get_headline_url()
    html = requests.get(page_url).text
    return BeautifulSoup(html, 'html.parser')

  def get_image_url(self):
    s = self.get_headline_soup()
    return s.img.get('src')

class NYTimes(Newspaper):
  """
  NY Times headline image scraper.

  Grabs the first article on the homepage (upper left hand corner)
  and finds the url of the image.
  """
  def __init__(self):
    Newspaper.__init__(self, 'http://nytimes.com')

  def get_articles(self):
    return self.soup.find_all('article')

  def get_headline(self):
    return self.get_articles()[0];

class WSJ(Newspaper):
  def __init__(self):
    Newspaper.__init__(self, 'http://www.wsj.com/')

  def get_articles(self):
    return self.soup.find_all('h3', 'wsj-headline')

  def get_headline(self):
    return self.get_articles()[0]

if __name__ == '__main__':
  i = NYTimes()
  print i.get_image_url()

