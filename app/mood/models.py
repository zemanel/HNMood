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

class News(db.Model):
    title = db.StringProperty(required=True)
    description = db.TextProperty()
    time = db.DateTimeProperty()
    location = db.TextProperty()
    creator = db.UserProperty()
    edit_link = db.TextProperty()
    gcal_event_link = db.TextProperty()
    gcal_event_xml = db.TextProperty()