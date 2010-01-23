#!/usr/bin/python

class Favorites(object):
  def __init__(self, db):
    if db:
      self.db = db
    else:
      return False
      
  def get_favorites_from_user_id(self, user_id):
    rows = self.db.query("select * from user_favorites where user_id = %s"%(user_id))
        
    fav = []
        
    for row in rows:
     comic_id = row['comic_id']
     comic = self.db.query("select * from comics where id = %s limit 1"%(comic_id))
     name = comic[0]['name']
     url = comic[0]['site_url']
       
     json = '[ "name" : %s, "url" : %s, "comic_id" : %s ]'%(name, url, str(comic_id))

     return json
      
  
    

def main():
  print "do not run this from the command line"

if __name__ == '__main__':
  main()

