"""
models.py

App Engine datastore models

"""
from google.appengine.ext import ndb

class SongModel(ndb.Model):
    """Song Model"""
    song_artist = ndb.StringProperty()
    song_name = ndb.StringProperty(required=True)
    song_started_time = ndb.DateTimeProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
