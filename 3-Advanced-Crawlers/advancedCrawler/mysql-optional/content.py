class Content:
   'Common base class for all articles/pages'


   def __init__(self, id, topicId, siteId, title, body, url):
      self.id = id
      self.topicId = topicId;
      self.siteId = siteId;
      self.title = title;
      self.body = body;
      self.url = url;
      