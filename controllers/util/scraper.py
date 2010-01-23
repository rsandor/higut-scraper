#
# scraper.py
# Higut.com webcomic scraping utility library
# Friday December 25th, 2009
# By Ryan Sandor Richards
# Copyright 2009, Higut.com
#

from tempfile import NamedTemporaryFile
from PIL import Image
import re, urllib

class Scraper:
  """ Generic URL scraping class. Serves as the base class for all scrapers. """
  def __init__(self, url=None):
    self.url = url
    self.content = None

  def scrape(self):
    return self._getContent(self)

  def _getContent(self, refresh=False):
    """ 
    Connects to the URL and grabs its textual content. 
    Sets the self.content variable and returns the results.
    Note that if the self.content variable is already set
    then this function will return its current value unless
    the refresh argument is set to True.
    """
    if refresh or not self.content:
      try:
        self.content = "".join(urllib.urlopen(self.url).readlines())
      except IOError:
        self.content = "Error occurred upon connection."
    return self.content


class ComicScraper(Scraper):
  """ Comic Scraping Utility Class """
  
  #imgExpr = re.compile('<\s*img.+src=["\']([^"\']+)["\']', re.IGNORECASE)
  imgExpr = re.compile('<\s*img\s*([^>]+)\s*>', re.IGNORECASE)
  srcExpr = re.compile('src\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
  altExpr = re.compile('alt\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
  imgTitleExpr = re.compile('title\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE);
  titleExpr = re.compile('<\s*title[^>]*>([^<>]+)', re.IGNORECASE)  
  
  supportedExtensions = [
    'png',
    'jpg',
    'gif'
  ]
  
  blacklist = [
    'statcounter.com',
    'projectwonderful.com',
    '2mdn.net',
    'thewebcomiclist.com',
    'comicrank.com',
    'topwebcomics.com',
    'buzzcomix.net',
    'tinycounter.com',
    'onlinecomics.net',
    'google.com',
    'ad.doubleclick.net',
    'webcomicz.com',
    'thecomicportal.com',
    'quantserve.com',
    'adstounding.com',
    'thefunnycartoon.com',
    'petfinder.com',
    'burstnet.com',
    'facebook.com',
    'twitter.com',
    'creativecommons.org',
    'akiko.megatokyo.com/adsystem',
    'analytics.hosting24.com',
    'extreme-dm.com',
    'akamai.net',
    'easycounter.com',
    'ads.reallifecomics.com',
    'inertsoap.com',
    'toothpastefordinner.com/banners',
    'openx.blindferret.com',
    
  ]
  
  rules = [
    lambda x, y: -1,                                        # Rule 0: Identity, syntactic order
    lambda x, y: cmp(int(x['size']), int(y['size'])),       # Rule 1: Largest Content-Length
    lambda x, y: cmp(int(x['width']), int(y['width'])),     # Rule 2: Largest Width
    lambda x, y: cmp(int(x['height']), int(y['height'])),   # Rule 3: Largest Height
    lambda x, y: cmp(int(x['pixels']), int(y['pixels'])),   # Rule 4: Largest Number of Pixels
  ]


  def __init__(self, comic):
    self.comic = comic;

    if comic['comic_url'] and comic['comic_url'] != '0':
      url = comic['comic_url']
    else:
      url = comic['site_url']
    
    if not url or url == '':
      raise Exception('Comic with handle ' + handle + ' does not have associated website information in the database.')
    
    Scraper.__init__(self, url)
  
    self.image_urls = None
    self.images = None
    self.title = None
    self.alts = {}
    self.titles = {}

      
  def scrape(self):
    """ Scrapes the comic URL page for all information about the comic """
    self._getContent()
    self._getImageURLs()
    self._getImages()
    
    # Finds the comic's title
    #titles = ComicScraper.titleExpr.findall(html)
    #if titles and len(titles) > 0:
    #  self.title = titles[0]
    
  
  def contentHasImage(self, url):
    """ Checks to see if the page has an image tag with the given url """
    if url == None:
      return False
    
    self._getImageURLs()
    
    for u in self.image_urls:
      if not u:
        continue
      if u.strip() == url.strip():
        return True
        
    return False
  
  def findComicImage(self, rule=4):
    """ Finds a comic based off the given rule in the set of images """
    images = self._getImages()
    rule = int(rule)
    if rule < 0 or rule >= len(self.rules):
      raise Exception('Rule number ' + rule + ' is invalid.')
    if images and len(images):
      images.sort(self.rules[rule])
      return images[-1]
    return None
  
  
  def _getImageURLs(self, refresh=False):
    """
    Scrapes all image tags from the site's HTML, sets the self.image_urls
    variable and returns the results. If the self.image_urls is already set
    and the refresh argument is False then this just returns the contents of
    the self.image_urls variable.
    
    Note: this does not find CSS images.
    """
    if refresh or not self.image_urls:    
      html = self._getContent()
      baseurl = self.url.rstrip('/')
      
      # Remove pesky filenames from the end of the URL (for relative pathing)
      if baseurl.split('/')[-1].find('.'):
        baseurl = "/".join(baseurl.split('/')[0:-1])
      
      urls = []
      for img in ComicScraper.imgExpr.findall(html):
        src = ComicScraper.srcExpr.findall(img)
        if len(src) == 0:
          continue
        
        url = src[0];
        
        # Fix relative paths
        if url.find('http://') == -1:
          url = baseurl + '/' + url.lstrip('/')
          
        # Check image url against blacklist
        blacklisted = False
        for b in ComicScraper.blacklist:
          if url.find(b) != -1:
            blacklisted = True
            break
        
        if blacklisted:
          continue
        
        # Fix double slashes in urls (shouldn't happen, but just in case...)
        parts = url.split('://');
        if len(parts) == 2:
          parts[1].replace('//', '/')
          url = "://".join(parts)
        else:
          continue
        
        # Finally make sure it has the supported extension
        #if url.split('.')[-1] not in ComicScraper.supportedExtensions:
        #  continue
        
        # Find the alt text if it exists
        alt = ComicScraper.altExpr.findall(img)
        if len(alt) > 0:
          self.alts[url] = alt[0]  
          
        # Find the image title attribute if it exists
        title = ComicScraper.imgTitleExpr.findall(img)
        if len(title) > 0:
          self.titles[url] = title[0]
             
        urls.append(url)
        
      self.image_urls = urls
      
    return self.image_urls
  
    
  def _getImages(self, refresh=False):
    """
    Compiles a list of information about images on the comic site.
    Sets the self.images variable and returns the result. This will
    simply return the contents of the self.images variable if it is
    set and the refresh argument is false.
    """
    if refresh or not self.images:
      urls = self._getImageURLs()
      images = []
      
      if not urls:
        return None
      
      for url in urls:
        try:
          h = urllib.urlopen(url)
          if h:
            # Generate the basic image information
            info = h.info()
            image = {'handler':h, 'src': h.geturl(), 'alt': '', 'title': ''}
            
            if url in self.alts:
              image['alt'] = self.alts[url]

            if url in self.titles:
              image['title'] = self.titles[url]
            
            # Determine image content-length
            if 'content-length' in info:
              image['size'] = info['content-length']
            else:
              image['size'] = '0'
              
            # Determine image dimensions
            try:
              tmp = NamedTemporaryFile()
              tmp.write(h.read())
              imageObj = Image.open(tmp.name)
              image['width'], image['height'] = imageObj.size
              tmp.close()
            except IOError:
              image['width'] = 0
              image['height'] = 0
            
            image['pixels'] = int(image['width']) * int(image['height'])
            
            # Add the image to the list
            images.append(image)  
        except IOError:
          pass    
          
      self.images = images
    
    return self.images


class LinkScraper(Scraper):
  """ Scrapes pages for links. """
  def __init__(self, url, exprStr):
    Scraper.__init__(self, url)
    self.expr = re.compile(expr)
  
  def scrape(self):
    return self.expr.findall(self._getContent())
    
  
