"""
views.py

URL route handlers

"""
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.api.datastore_errors import BadValueError

import logging

from datetime import datetime

from flask import request, jsonify, abort

# from flask_cache import Cache

from application import app
from models import SongModel

# Flask-Cache (configured to use App Engine Memcache API)
# cache = Cache(app)

def songs():
    """List and create songs"""
    if request.method == 'GET':
        songs = SongModel.query().fetch(10)
        songs_dict = []
        for song in songs:
            songs_dict.append(song.to_dict())
        return jsonify(songs = songs_dict)
    elif request.method == 'POST':
        song_artist = request.values.get('artist', None)
        song_name = request.values.get('name', None)
        song_started_time = request.values.get('started_time', None)
        if song_started_time is not None:
            song_started_time_datetime = datetime.fromtimestamp(float(song_started_time))
        try:
            song = SongModel(
                    song_artist = song_artist,
                    song_name = song_name,
                    song_started_time = song_started_time_datetime
            )
            song.put()
            return jsonify(id = song.key.id())
        except CapabilityDisabledError as e:
            return jsonify(message = u'App Engine Datastore is currently in read-only mode.'), 500
        except BadValueError as e:
            abort(400)
        except TypeError as e:
            abort(400)
        except Exception as e:
            logging.error(e.args[0])
            abort(500)
    return abort(405)

def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
