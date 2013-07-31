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
from models import PlaylistItemModel
from decorators import crossdomain

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

def add():
    try:
        artist = request.values.get('artist', None)
        title = request.values.get('title', None)
        started_time = request.values.get('started_time', None)
        started_time_datetime = None
        if started_time is not None:
            started_time_datetime = datetime.fromtimestamp(float(started_time))
        item = PlaylistItemModel(
            artist = artist,
            title = title,
            started_time = started_time_datetime
        )
        item.put()
        return jsonify(id = item.key.id())
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
    last = PlaylistItemModel.query().order(-PlaylistItemModel.timestamp).fetch(1)
    try:
        return jsonify(iter(last).next().to_dict())
    except StopIteration:
        return jsonify({})
    except Exception as e:
        logging.error(e.args[0])
        abort(500)

@crossdomain(origin='*')
def list():
    items_dict = []
    try:
        max = int(request.values.get('max', '5'))
        items = PlaylistItemModel.query().fetch(max)
        for item in items:
            items_dict.append(item.to_dict())
    except TypeError as e:
        abort(400)
    except Exception as e:
        logging.error(e.args[0])
        abort(500)
    return jsonify(itemss = items_dict)

def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''
