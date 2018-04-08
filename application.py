# -*- coding: utf-8 -*-
from flask import Flask, redirect

from main.telegram import telegram
from main.scheduler import scheduler


__author__ = 'oon arfiandwi'


application = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

# blueprints
application.register_blueprint(telegram)
application.register_blueprint(scheduler)


@application.route('/')
def index():
    return redirect('http://makassar.dilo.id', code=302)


@application.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@application.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
