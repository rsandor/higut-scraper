#
# StatsBase.py
# Base class for all higut statistics and reporting related classes
# By Ryan Sandor Richards
# December 27th, 2009
# Copyright 2009, Higut.com
#

from tornado.options import define, options
import tornado.database, re

define("port", default=8079, help="run on this port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="higut_dev", help="blog database name")
define("mysql_user", default="higut", help="blog database user")
define("mysql_password", default="bevyofbeavers", help="blog database password")

db = tornado.database.Connection(
      host=options.mysql_host, database=options.mysql_database,
      user=options.mysql_user, password=options.mysql_password)  
  
def getComicsListFromFile(filename):
  """
  Loads a list of comics from a whitespace or comma delimited file.
  The file should contain the handles for all of the comics to fetch
  Since each handle must be of the form [a-zA-Z]+ you can delimit the
  handles using anything but those characters.
  
  This function is particularly useful for parsing "broken" comic lists
  from the reports pages.
  
  For the file:
  
    xkcd, dominicdeegan #))#) happy )_S)))#) wow_WOOOW
  
  The list generated would contain
  
    ['xkcd', 'dominicdeegan', 'happy', 'wow']

  
  Throws an IOException if the file cannot be opened or if a file read
  error occurs.
  """
  h = open(filename)
  contents = "\n".join(h.readlines())
  expr = re.compile("([a-z0-9]+)")
  return expr.findall(contents)

def loadComics(handles):
  """ Loads a list of comics from a list of handles. """
  sql = "select * from comics where handle in ('" + "', '".join(handles) + "')"
  results = db.query(sql)
  return results

def setComicStatus(self, handles, status):
  """ Sets the status of all comics with the given handles. """
  db.execute("update comics set status=%s where handle in ('" + "', '".join(handles) + "')", status)
  
def getComic(handle):
  """
  Fetches a comic with the given handle from the DB.
  """
  result = self.db.query('select from comics where handle = %s limit 1', handle)
  if len(result) < 1:
    return None
  else:
    return result[0]

def getComics(status=None, start=None, length=None):
  """
  Fetches a list of comics with the given status limited to a starting point and range.
  Missing arguments are ignored.
  """
  sql = 'select * from comics '
  if status or start or length:
    sql += 'where '
  
  if status:
    sql += "status = '" + status.replace("'", "\\'") + "' "
  
  if start and not length:
    sql += 'limit ' + str(int(start))
  elif length and not start:
    sql += 'limit ' + str(int(length))
  elif start and length:
    sql += 'limit ' + str(int(start)) + ', ' + str(int(length))
 
  sql += ';'
    
  results = db.query(sql)
  
  return results