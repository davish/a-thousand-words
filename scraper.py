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
    self.html = requests.get(url).content
    self.soup = BeautifulSoup(self.html, 'html.parser')

  def absolute_url(self, url):
    if self.url.startswith(url):
      return url

    if url[0] == '/':
      return self.url + url[1:]
    else:
      return self.url + url

  def refresh(self):
    self.html = requests.get(self.url).content
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

  def get_headline_texts(self):
    return [x.a.string for x in self.get_headlines()]

  def get_headline_url(self):
    return self.absolute_url(self.get_headline().a.get('href'))

  def get_headline_urls(self):
    res = [self.absolute_url(headline.a.get('href')) for headline in self.get_headlines()]
    return res

  def get_headline_soup(self):
    page_url = self.get_headline_url()
    html = requests.get(page_url).content
    return BeautifulSoup(html, 'html.parser')

  def get_headline_soups(self):
    res = []
    for page_url in self.get_headline_urls():
      html = requests.get(page_url).content
      res.append(BeautifulSoup(html, 'html.parser'))
    return res

  def get_image_url(self):
    s = self.get_headline_soup()
    return s.img.get('src')

  def get_image_urls(self):
    res = []
    for s in self.get_headline_soups():
      res.append(s.img.get('src'))
    return res

class NYTimes(Newspaper):
  """
  NY Times headline image scraper.

  Grabs the first article on the homepage (upper left hand corner)
  and finds the url of the image.
  """
  def __init__(self):
    Newspaper.__init__(self, 'http://nytimes.com')

  def absolute_url(self, url):
    return url

  def get_articles(self):
    return self.soup.find_all('article')

  def get_headline(self):
    return self.get_articles()[0]

  def get_headlines(self):
    return self.get_articles()[0:9]


class Aljazeera(Newspaper):
  def __init__(self):
    Newspaper.__init__(self, 'http://america.aljazeera.com/')
 
  def get_articles(self):
    return self.soup.find_all('article')

  def get_headline(self):
    return self.soup.find('h1', 'topStories-headline')

  def get_image_url(self):
    a = self.get_articles()[0].img.get('src')
    return self.absolute_url(a)

class CNN(Newspaper):
    def __init__(self):
        Newspaper.__init__(self, 'http://cnn.com/')
    def get_articles(self):
        return self.soup.find_all('article')
    def get_headline(self):
        return self.soup.find('h3', 'cd__headline')
    
    def get_image_url(self):
        s = self.soup.find_all('article')[0].find_all('img')[0].get('data-src-medium')
        return s

class WashingtonPost(Newspaper):
  def __init__(self):
    Newspaper.__init__(self, 'https://www.washingtonpost.com/')
  def get_articles(self):
    return self.soup.find_all('div', 'headline')

  def get_headline(self):
    return self.get_articles()[0]

  def get_image_url(self):
    return self.get_headline_soup().find('div', id='article-body').img.get('src')

class Spiegel(Newspaper):
  def __init__(self):
    Newspaper.__init__(self, 'http://www.spiegel.de/international/')

  def get_image_url(self):
    return self.soup.find('div', id='content-main').img.get('src')

class BBC(Newspaper):
  def __init__(self):
    Newspaper.__init__(self, 'http://www.bbc.com/')

  def get_articles(self):
    return self.soup.find_all('li', 'media-list__item')
  def get_article(self):
    return self.get_articles()[0]
  def get_headline(self):
    return self.get_article().find('div', 'media__content').find('h3', 'media__title')

  def get_image_url(self):
    return self.get_headline_soup().find('div', 'story-body__inner').img.get('src')

class Independent(Newspaper):
    def __init__(self):
        Newspaper.__init__(self, 'http://www.independent.co.uk/')
    def get_articles(self):
        return self.soup.find_all('article');
    def get_headline(self):
        return self.get_articles()[0]

if __name__ == '__main__':
    i = Independent()
    print i.get_image_url();
