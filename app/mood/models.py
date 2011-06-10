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
    text = db.TextProperty()
    created_on = db.DateTimeProperty(auto_now_add=True)
    
    #sentimental analisys
    is_sentiment_processed = db.BooleanProperty(default=False)
    sentiment_type = db.StringProperty()
    sentiment_score = db.FloatProperty()

    #id: will use key of db model
    #points = db.IntegerProperty()
    #parent_id: will use parent of db model instance
    #username = db.StringProperty()
    #type = db.StringProperty()
    #url = db.LinkProperty()
    #domain = db.StringProperty()
    #title = db.StringProperty()
    #num_comments = db.IntegerProperty()
    #created_on = db.DateTimeProperty()