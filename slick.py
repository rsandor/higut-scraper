from controllers.util.database import db, getComics
from controllers.util.scraper import ComicScraper, Scraper
from datetime import date
import re

today = date.today().isoformat()
i = 0
comic_name = 'lookingforgroup' 
comic_id = '8'

top = 1

for j in range(top):

  #url = 'http://www.agreeablecomics.com/therack/?p='+ str(j)
  #url = 'http://www.xkcd.com'
  url = 'http://lfgcomic.com/page/latest'
  scraper = ComicScraper({'site_url':url, 'comic_url': u'0'})
  
  i += 1 
  print "Processing ", i, "/", top, "[" + str( (float(i)/float(top))*100.0 )+"%]" 
  image = scraper.findComicImage()
  print image
  
  
  # # # #
  if ('rack-header.jpg') in image['src']:
    print 'header: BUST!\n'
    continue
    
  # Check for same image on page
  strips = db.query('select url from strips where comic_id=' + comic_id + ';')
  if len(strips) > 0:
    found = False
    
    print "Checking for known image..."
    for urlIn in strips:
      print urlIn
      if not found and scraper.contentHasImage(urlIn['url']):
        print "Same image as last scrape, skipping.\n"
        found = True
        continue
    if found:
      continue
      
    print "Scraping " + comic_name
  # If the scrape was successful pop it into the strips DB
  if image:
    wid = str(image['width'])
    src = str(image['src'])
    alt = str(image['alt'])
    tit = str(image['title'])
    
    sql =  'insert into strips (comic_id, date, url, alt, title, width) values '
    sql += '(' + comic_id +','+today+','+src+','+alt+','+tit+','+ wid + ');'
    print (sql)    
    #sql += '(' + comic_id + ', %s, %s, %s, %s, ' + str(image['width']) + ');'
    #db.execute(sql, today, image['src'], image['alt'], image['title'])
    print "Strip added to the DB!\n"
  else:
    print "No image found! Skipping...\n"

