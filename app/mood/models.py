'''
'''
from google.appengine.ext import db

"""
id - The item's unique integer id
parent_id - The parent item's id
points - The number of points
username - The submitter's username
type - Item type (submission|comment)
url - A submission url
domain - A submission url's domain name
title - A submission title
num_comments - Number of submission comments
text - The submission/comment content
discussion{} - A comment's parent discussion
  id - The discussion's item id
  title - The discussion's item title
create_ts - When the item was created
cache_ts - When the item was last cached

"""
class NewsItem(db.Model):
  #id: will use key of db model

  text = db.TextProperty()
  create_ts = db.DateTimeProperty()
  type = db.StringProperty()
  username = db.StringProperty()
  parent_id = db.IntegerProperty() # parent_id - The parent item's id

  #sentimental analisys
  is_sentiment_processed = db.BooleanProperty(default=False)
  is_sentiment_queued = db.BooleanProperty(default=False)
  sentiment_type = db.StringProperty()
  sentiment_score = db.FloatProperty()

  #points = db.IntegerProperty()
  #parent_id: will use parent of db model instance
  #url = db.LinkProperty()
  #domain = db.StringProperty()
  #title = db.StringProperty()
  #num_comments = db.IntegerProperty()
  #created_on = db.DateTimeProperty()