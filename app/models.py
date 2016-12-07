"""
models.py

App Engine datastore models

"""
from google.appengine.ext import ndb

class PlaylistItemModel(ndb.Model):
    """Song Model"""
    artist = ndb.StringProperty()
    title = ndb.StringProperty(required=True)
    started_time = ndb.DateTimeProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
