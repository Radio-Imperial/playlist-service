"""
Initialize Flask app

"""
import os
from flask import Flask

app = Flask(__name__, static_folder=os.getcwd() + '/static', static_url_path='', template_folder=os.getcwd() + '/templates')
app.config.from_object('app.settings')

# Pull in URL dispatch routes
import urls
