#!/usr/bin/python
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

class GMail(object):
  """Compose and Send via GMail"""
  def __init__(self, email_address, password):
    super(GMail, self).__init__()
    self.email_address = email_address
    self.password = password
    
  def email(self, to, subject, text):
    msg = self.compose(to, subject, text)
    try:
      mailServer = smtplib.SMTP("smtp.gmail.com", 587)
      mailServer.ehlo()
      mailServer.starttls()
      mailServer.ehlo()
      mailServer.login(self.email_address, self.password)
      mailServer.sendmail(self.email_address, msg['To'], msg.as_string())
      mailServer.close()
    except Exception, e:
      return False
    return True
  
  def compose(self, to, subject, text):
    msg = MIMEMultipart()
    msg['From'] = self.email_address
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    return msg
    

def main():
  """Don't run as main"""
  print "Please don't run this script by itself."
  # # Usage Example:
  # gmail = GMail('bernard.higut@gmail.com', "PASSWORD GOES HERE")
  # gmail.email('YOUR_EMAIL_ADDRESS_HERE', 'testing factored out code', 'does it work?')

if __name__ == '__main__':
  main()