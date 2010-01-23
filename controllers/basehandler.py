import tornado.web

class BaseHandler(tornado.web.RequestHandler):
  @property
  def redis(self):
    return self.application.redis

  @property
  def db(self):
    return self.application.db
          
  def get_current_user(self):
    user_json = self.get_secure_cookie("user")
    if not user_json: return None
    return tornado.escape.json_decode(user_json)
  
  def get_goddam_user(self):
    user_json = self.get_secure_cookie("goddam_user")
    if not user_json: return None
    return tornado.escape.json_decode(user_json)
    
  def get_gd_login_url(self):
    self.require_setting("gd_login_url", "@gdauthenticated")
    return self.application.settings['gd_login_url']

  def _get_demo_user(self):
    user_json = self.get_secure_cookie("higut_user")
    if not user_json: return None
    return tornado.escape.json_decode(user_json)
  
  def static_js(self, filename):
    """ Fetches the url for static JavaScript files. """
    return self.static_file('js/' + filename);

  def static_css(self, filename):
    """ Fetches the url for static CSS files. """
    return self.static_file('css/' + filename);

  def static_img(self, filename):
    """ Fetches the url for static image files. """
    return self.static_file('images/' + filename)
    
  def static_file(self, path):
    """ Fetches the url for static files. s"""
    servers =  ["higut.com", "heyigotyouthese.com", "gotyouthese.com"]
    if self.request.host.replace("www", "") in servers:
      return 'http://static.higut.com/' + path
    else:
      return '/static/' + path
    
  def request_uri(self):
    return self.request
    
