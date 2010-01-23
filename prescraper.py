#
# prescraper.py
# Performs pre-scraping of comics to generate a strips list in the DB
# Copyright 2010 higut.com
# By Ryan Sandor Richards
# January 2nd, 2010 (Happy Birthday, Dad!)
#

from controllers.util.database import db, getComics
from controllers.util.scraper import ComicScraper
from datetime import date

today = date.today().isoformat()
comics = getComics('working')
total = len(comics)
i = 0
#for comic in comics:
for comic in comics: 
  i += 1 
  print "Processing ", i, "/", total, "[" + str( (float(i)/float(total))*100.0 )+"%]" 
  # Test to see if the comic is already in the DB
  strips = db.query('select id from strips where comic_id=' + str(comic['id']) + ' and date = %s', today)
  if len(strips) > 0:
    print "Today's " + comic.name + " is already in the database, skipping."
    continue
    
  # Scrape the comic image from the comic website
  scraper = ComicScraper(comic)

  # Check for same image on page
  strips = db.query('select MAX(date), url from strips where comic_id=' + str(comic['id']) + ';')
  if len(strips) > 0:
    print "Checking for known image..."
    url = strips[0]['url']
    
    if scraper.contentHasImage(url):
      print "Same image as last scrape, skipping."
      continue
  
  print "Scraping " + comic.name
  image = scraper.findComicImage()
  
  # If the scrape was successful pop it into the strips DB
  if image:
    sql =  'insert into strips (comic_id, date, url, alt, title, width) values '
    sql += '(' + str(comic['id']) + ', %s, %s, %s, %s, ' + str(image['width']) + ');'
    db.execute(sql, today, image['src'], image['alt'], image['title'])
    print "Strip added to the DB!"
  else:
    print "No image found! Skipping..."

