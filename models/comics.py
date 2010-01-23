#!/usr/bin/python
from urllib2 import Request, urlopen, HTTPError, URLError

class Comics(object):
  def __init__(self, db):
    if db:
      self.db = db
    else:
      return False
      
  def get_comic_from_id(self, comic_id):
    rows = self.db.query("SELECT * FROM comics WHERE id = '%s'"%(comic_id))
    if len(rows) != 1:
      return False
    return rows[0]
      
  def get_comic_url_from_id(self, id):
    rows = self.db.query("SELECT * FROM comics WHERE id = '%s'" %(id))
    if len(rows) != 1:
      return False
    else:
      print "comic_url", rows[0]['comic_url']
      if rows[0]['comic_url'] in [0, "0", None]:
        url = rows[0]['site_url']
      else:
        url = rows[0]['comic_url']
    return url
    
  def get_rank_scraper_rules(self, id):
    rows = self.db.query("SELECT * FROM comic_scraping WHERE id = '%s'" %(id))
    if len(rows) != 1:
      return False
    else:
      print 'rule', rows[0]['rule']
      return rows[0]['rule']
  
  def get_all_comics(self):
  # get all of the comics on the database
    return self.db.query("select * from comics order by name")
    
  def shorten(self, longurl):
    req = Request("http://api.bit.ly/shorten?version=2.0.1&longUrl="+longurl+"&login=heyigotyouthis&apiKey=R_a687ade66b0b49fdb9cb3c6e610bd38c")
    
    try:
        short = urlopen(req)
        html = short.read()
        json = tornado.escape.json_decode(html)
        json = json['results']
        json = json[longurl]
        shorturl = json['shortUrl']
    except Exception, e:
        shorturl = "http://rrichards.higut.com/demo"
        
    return shorturl
    

def main():
  print "do not run this from the command line"

if __name__ == '__main__':
  main()

