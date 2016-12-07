from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.api.datastore_errors import BadValueError
from flask import Response, abort, jsonify
import json
import urllib2
import logging
import pytz
import re
from time import strptime, mktime
from calendar import timegm
from datetime import datetime
import xml.etree.ElementTree as ET
from models import PlaylistItemModel

class Item:
    def __init__(self, artist, title, started_time, type):
        self.artist = artist
        self.title = title
        self.started_time = started_time
        self.type = type
        if self.type == '1':
            if self.title[0:3] == '_n_':
                self.artist = None
                self.title = u'Bloco Comercial'
        elif self.type == '0':
            self.artist = None
            self.title = u'Bloco Comercial'
        elif self.type == '2':
            self.artist = None
            self.title = u'Ao Vivo!'
        elif self.type == '3':
            self.artist = None
            self.title = u'Ao Vivo!'
        elif self.type == '4':
            self.artist = None
            self.title = u'Hora Certa!'
        else:
            self.artist = None
            self.title = u'Sem Informa\xe7\xe3o'

    def __cmp__(self, other):
        if other is None:
            return -1
        if self.type != other.type:
            return -1
        if (self.artist != other.artist) or (self.title != other.title):
            return -1
        return 0


def convert_playlist_time(str_time):
    playlist_datetime = None
    try:
        time = strptime(str_time, '%d/%m/%Y %H:%M:%S')
        brt = pytz.timezone('America/Sao_Paulo')
        dt = datetime.fromtimestamp(mktime(time))
        brt_dt = brt.localize(dt)
        utc_dt = brt_dt - brt_dt.utcoffset()
        utc_dt = utc_dt.replace(tzinfo=pytz.utc)
        timestamp = timegm(utc_dt.utctimetuple())
        playlist_datetime = datetime.fromtimestamp(timestamp)
    except Exception as e:
        logging.exception(e)
        pass
    return playlist_datetime


def should_update(item):

    try:
        query = PlaylistItemModel.query().order(-PlaylistItemModel.timestamp).fetch(1)
        last = iter(query).next()
        if (item.artist != last.artist) or (item.title != last.title) or (item.started_time != last.started_time):
            return True
        else:
            return False
    except StopIteration:
        return True

def update_playlist(item):
    if should_update(item):
        try:
            item = PlaylistItemModel(
                artist=item.artist,
                title=item.title,
                started_time=item.started_time
            )
            item.put()
            return jsonify(id=item.key.id())
        except CapabilityDisabledError:
            return jsonify(message=u'App Engine Datastore is currently in read-only mode.'), 500
        except BadValueError:
            abort(400)
        except TypeError:
            abort(400)
        except Exception as e:
            logging.error(e.args[0])
            abort(500)
    else:
        return jsonify(message=u'Playlist is current. No update needed.'), 200


def parse_playlist(obj):
    filename = None
    try:
        tree = ET.parse(obj)
        root = tree.getroot()
        onair = root.find('OnAir')
        curins = onair.find('CurIns')
        started_time = curins.find('StartedTime').text
        type = curins.find('Type').text
        filename = curins.find('Filename').text
    except IOError:
        logging.error('Cannot read playlist file.')
        abort(500)
    except Exception as e:
        logging.exception(e)
        abort(500)
    if filename is not None:
        try:
            match = re.match(r'(.*) - (.*).(mp3|wav|aac)', filename, re.I)
            if match:
                artist = match.group(1)
                title = match.group(2)
            else:
                match = re.match(r'(.*).(mp3|wav|aac)', filename, re.I)
                if match:
                    artist = None
                    title = match.group(1)
                else:
                    artist = None
                    title = None
            item = Item(artist, title, convert_playlist_time(started_time), type)
            return update_playlist(item)
        except Exception as e:
            logging.exception(e)
            abort(500)
    else:
        logging.error("Filename is None.")
        abort(500)

def load_data():
    url = "http://imperial.fm.br/playlist.xml"
    try:
        obj = urllib2.urlopen(url)
        return parse_playlist(obj)
    except urllib2.HTTPError as e:
        return jsonify(message=u'Could not load playlist.'), 500
