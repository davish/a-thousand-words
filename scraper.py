from bs4 import BeautifulSoup
import requests

class Newspaper:
  def __init__(self, url):
    self.url = url
    self.html = requests.get(url).text
    self.soup = BeautifulSoup(self.html, 'html.parser')

  def refresh(self):
    self.html = requests.get(self.url).text
    self.soup = BeautifulSoup(self.html, 'html.parser')

  def get_articles(self):
    raise NotImplementedError('Abstract Method')

  def get_headline(self):
    raise NotImplementedError('Abstract Method')

  def get_headline_url(self):
    raise NotImplementedError('Abstract Method')

  def get_image_url(self, page_url):
    raise NotImplementedError('Abstract Method')

class NYTimes(Newspaper):
  def get_articles(self):
    return soup.find_all('article')

  def get_headline(self):
    return self.get_articles()[0].a.string

  def get_headline_url(self):
    return self.get_articles()[0].a.get('href')
  
  def get_headline_soup(self):
    page_url = get_headline_url()
    html = requests.get(page_url).text
    return BeautifulSoup(html, 'html.parser')
    
  def get_image_url(self):
    s = get_headline_soup(self)
    return s.img.get('src')






