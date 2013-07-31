"""
views.py

URL route handlers

"""
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.api.datastore_errors import BadValueError

import logging

from datetime import datetime

from flask import request, jsonify, abort

from flask_cache import Cache

from application import app
from models import SongModel
from decorators import crossdomain

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

def add():
    try:
        song_artist = request.values.get('artist', None)
        song_name = request.values.get('name', None)
        song_started_time = request.values.get('started_time', None)
        song_started_time_datetime = None
        if song_started_time is not None:
            song_started_time_datetime = datetime.fromtimestamp(float(song_started_time))
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

@cache.cached(timeout=60)
@crossdomain(origin='*')
def last():
    last = SongModel.query().order(-SongModel.timestamp).fetch(1)
    try:
        return jsonify(iter(last).next().to_dict())
    except StopIteration:
        return jsonify({})
    except Exception as e:
        logging.error(e.args[0])
        abort(500)

@crossdomain(origin='*')
def list():
    songs_dict = []
    try:
        max = int(request.values.get('max', '5'))
        songs = SongModel.query().fetch(max)
        for song in songs:
            songs_dict.append(song.to_dict())
    except TypeError as e:
        abort(400)
    except Exception as e:
        logging.error(e.args[0])
        abort(500)
    return jsonify(songs = songs_dict)

def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
