#!/usr/bin/env python
# coding=utf-8

from gevent import monkey; monkey.patch_all()
import os
import sys
from flask import Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
from flask import render_template, g, request

try:
    import dashboard
except ImportError:
    import site
    ROOT_DIR = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    site.addsitedir(ROOT_DIR)

from dashboard import handlers
from dashboard.helpers import get_current_user

@app.before_request
def before_request():
    g.user = get_current_user()
    g.logger = app.logger

app.config['SECRET_KEY'] = 'NjE1YmU3ODk0NmQ3NDY5NWJkNDBjMGIwODNlZDQ0MTdiNjE3ZjMzOSAgLQo='
app.add_url_rule('/', view_func=handlers.MainHandler.as_view('/'))
app.add_url_rule('/account/signin', view_func=handlers.AccountSigninHandler.as_view('account_signin'))
app.add_url_rule('/account/signout', view_func=handlers.AccountSignoutHandler.as_view('account_signout'))

from dashboard.settings.handler import app as settings_handler
app.register_blueprint(settings_handler, url_prefix='/settings')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
