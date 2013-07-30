"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import jsonify

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# List and create songs
app.add_url_rule('/v1/songs', 'songs', view_func=views.songs, methods=['GET', 'POST'])
