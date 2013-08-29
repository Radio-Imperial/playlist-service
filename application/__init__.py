"""
Initialize Flask app

"""
from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

app = Flask('application')
app.config.from_object('application.settings')

# Enable jinja2 loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

def make_json_error(ex):
	response = jsonify(message=str(ex))
	response.status_code = (ex.code
							if isinstance(ex, HTTPException)
							else 500)
	return response

for code in default_exceptions.iterkeys():
	app.error_handler_spec[None][code] = make_json_error

# Pull in URL dispatch routes
import urls

