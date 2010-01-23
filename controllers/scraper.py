import re
import urllib
import xml.parsers.expat
import tornado.web

from util.scraper import ComicScraper

from basehandler import BaseHandler      
 
# 
# Formats a given string of html so it can be displayed by a browser
#
def formatHTML(s):
  s = re.sub('<', '&lt;', s)
  s = re.sub('>', '&gt;', s)
  return s


class ScraperHandler(BaseHandler):
  def get(self, id=None):
    comics = self.db.query('select * from comics where handle = %s', id)
   
    if len(comics) == 0:
      raise tornado.web.HTTPError(404)
        
    comic = comics.pop()
    scraper = ComicScraper(comic)
    scraper.scrape()
    
    self.write('<h1>Images Information</h1>')
    self.write('<p>URL: ' + scraper.url + '</p>')
    
    if scraper.image_urls and len(scraper.image_urls) > 0:
      for img in scraper.images:
        info = img['handler'].info().dict
        self.write('<h3>' + str(img['size']) + " - " + img['src'] + '</h3>')
        self.write('<p><img src="')
        self.write(img['src'])
        self.write('" ></p>')
        self.write('<ul>' + "\n".join(['<li><b>' + x + '</b> - ' + info[x] + '</li>' for x in info.keys()]) + '</ul>')
    else:
      self.write('No images found on page!')
      
    self.write('<hr>');
    self.write(formatHTML(scraper.content))
    
  