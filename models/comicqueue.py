from redis import Redis

class ComicQueue(object):
  def __init__(self, r=None):
    if not r:
      self.redis = Redis()
    else:
      self.redis = r
    self.queue_key = "requested_comics_queue"
    
  def enqueue(self, string):
    try:
      self.redis.push(self.queue_key, string)
    except Exception, e:
      print e
      return False
    return True
    
  def get_queue(self, pages=[0,-1]):
    try:
      queue = self.redis.lrange(self.queue_key, pages[0], pages[1])
    except Exception, e:
      print e
      return False
    return queue
    
  def dequeue(self):
    try:
      # head = self.redis.pop(self.queue_key)
      head = "DO NOT USE YET"
    except Exception, e:
      return False
    return head