from basehandler import BaseHandler

class ReportHandler(BaseHandler):
  def get(self):
    try:
      comics = self.db.query("select c.id as comic_id, c.handle as handle, c.name as name, c.site_url as site_url, " +
        " s.url as current_url, MAX(s.date) as date from strips as s, comics as c " +
        " where s.comic_id = c.id and s.status='working' and s.verified = 0 and c.status='working' group by s.comic_id order by c.name")
        
      self.render("report.html", 
        static_file=self.static_file,
        static_css=self.static_css,
        static_js=self.static_js,
        static_img=self.static_img, 
        comics=comics)    
        
    except IOError:
      self.write("<h1>Error</h1>");
      self.write("<p>No result file with name '" + result_file + "'.</p>")
      
  def post(self):
    mode = self.get_argument('m')
    if mode == 'broken':
      comic_id = self.get_argument('comic_id')
      sql = "update comics set status='broken' where id = " + str(comic_id)
      sql2 = "delete from strips where comic_id = " + str(comic_id)
      try:
        self.db.execute(sql)
        self.db.execute(sql2)
      except:
        msg = "A SQL error occurred:\n" + sql + "\n\n" + sql2
        self.write(msg)
        
    elif mode == 'verify':
      comic_id = self.get_argument('comic_id')
      sql = "update strips set verified = 1 where comic_id = " + str(comic_id)
      try:
        self.db.execute(sql)
      except:
        msg = "ERROR SQL: " + sql
        self.write(msg)

      
