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

# Return last item from playlist
app.add_url_rule('/v1/playlist/last', 'last', view_func=views.last, methods=['GET'])

# Add new item to playlist
app.add_url_rule('/v1/playlist/add', 'add', view_func=views.add, methods=['POST'])

# Return last ? items from playlist
app.add_url_rule('/v1/playlist/list', 'list', view_func=views.list, methods=['GET'])