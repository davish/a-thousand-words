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

  def get_headline_text(self):
    """ Get the actual text of the headline. """
    raise NotImplementedError('Abstract Method')

  def get_headline_url(self):
    """ Get the URL of the full headline story. """
    raise NotImplementedError('Abstract Method')

  def get_headline_soup(self):
    """ Get the BS object for the headline page. """
    raise NotImplementedError('Abstract Method')

  def get_image_url(self, page_url):
    """ Retrieve the URL for the headline image. """
    raise NotImplementedError('Abstract Method')

class NYTimes(Newspaper):
  """
  NY Times headline image scraper.

  Grabs the first article on the homepage (upper left hand corner)
  and finds the url of the image.
  """
  def __init__(self):
    super(NYTimes, self).__init__('http://nytimes.com')

  def get_articles(self):
    return self.soup.find_all('article')

  def get_headline(self):
    return self.get_articles()[0];

  def get_headline_text(self):
    return self.get_headline().a.string

  def get_headline_url(self):
    return self.get_headline().a.get('href')
  
  def get_headline_soup(self):
    page_url = get_headline_url()
    html = requests.get(page_url).text
    return BeautifulSoup(html, 'html.parser')

  def get_image_url(self):
    s = get_headline_soup()
    return s.img.get('src')






