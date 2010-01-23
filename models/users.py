#!/usr/bin/python

class Users(object):
  def __init__(self, db):
    if db:
      self.db = db
    else:
      return False


  # get_user_id() - get the database id of a user based on the current cookie
  # @param current_user - cookie value stuff
  def get_user_id(self, current_user):
    user_ids = self.db.query("select id from users where username='"+current_user['email']+"'")
    return user_ids[0]['id']
  
  
  # users_add_comic() - Add a comic to the user's comic list
  def users_add_comic(self, comic_id):
    current_user_id = self.get_user_id()
    self.db.execute("insert into users_comics (user_id, comic_id, is_deleted) values ('"+str(current_user_id)+"', '"+str(comic_id)+"', 0)")
  
  
  # users_list_comics() - List all of a user's comics
  # @param current_user - cookie values
  def users_get_comics(self, current_user):
    users_comics = self.db.query("select comics.name from comics, users_comics where users_comics.user_id='"+str(self.get_user_id(current_user))+"' and comics.id=users_comics.comic_id")
    return users_comics

  def user_add_favorite(self, comic_id, current_user):
    if self.db.execute("insert into user_favorites (comic_id, user_id) values (%s, %s)"%(comic_id, current_user)):
      return True
    else:
      return False
      
  def user_remove_favorite(self, comic_id, current_user):
    if self.db.execute("delete from user_favorites where comic_id = %s and user_id= %s"%(comic_id, current_user)):
      return True
    else:
      return False
        
def main():
  print "do not run this from the command line"

if __name__ == '__main__':
  main()

