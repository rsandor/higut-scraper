#!/usr/bin/python

import os, sys, atexit
import tornado.auth
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import urllib
import xml.parsers.expat
from redis import Redis
import time

#this needs to be changed to run on your dev port
define("port", default=8079, help="run on this port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="higut_dev", help="blog database name")
define("mysql_user", default="higut", help="blog database user")
define("mysql_password", default="bevyofbeavers", help="blog database password")
pidfile = 'pids/server.pid'

#avoid those nasty .pyc files
sys.dont_write_bytecode=True

from controllers.basehandler import BaseHandler
from controllers.scraper import ScraperHandler
from controllers.report import ReportHandler

#from models.comic_queue import comic_enqueueasdfsdfs

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"/report", ReportHandler),
      (r"/scraper/([a-z\d]+)?", ScraperHandler)
    ]
    settings = dict(
      debug=True,
      template_path=os.path.join(os.path.dirname(__file__), "templates"),
      static_path=os.path.join(os.path.dirname(__file__), "static"),
      # xsrf_cookies=True,
      cookie_secret='Dew1jtM4RdOdJQqFSdQT62FcXS1TQEfBvWNTfx35csA=',
      gd_login_url="/goddam/login"
    )
    tornado.web.Application.__init__(self, handlers, **settings)
    # Have one global connection to the blog DB across all handlers
    self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)
    self.redis = Redis()
        
def main():
  # Handle PIDs for stop/start/restart
  global pidfile
  filename, extension = pidfile.split('.')
  pidfile =  filename + "_" + str(options.port) + "." + extension
  pid = str(os.getpid())
  if os.path.isfile(pidfile):
    import urllib2
    req = urllib2.Request("http://127.0.0.1:" + str(options.port))
    try:
      urllib2.urlopen(req)
    except (urllib2.HTTPError, urllib2.URLError), e:
      file(pidfile, 'w').write(pid)
      atexit.register(clear_pid)
    else:
      print "Tornado port=%s instance already running @ pid %s, exiting" %(options.port, int(pid))
      sys.exit()
      
  file(pidfile, 'w').write(pid)
  atexit.register(clear_pid)
  
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
  
def clear_pid():
  global pidfile
  os.unlink(pidfile)
  # add alerting later? @@@

if __name__ == '__main__':
  main()

