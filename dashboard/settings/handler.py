import os
from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify, g
from flask.views import MethodView as RequestHandler

from dashboard.helpers import authenticated
from dashboard import keypairs
from dashboard.forms import SSHKeyAddForm

app = Blueprint('settings', __name__)

class ProfileHandler(RequestHandler):
    @authenticated
    def get(self):
        return render_template('settings/profile.html')

class SSHHandler(RequestHandler):
    @authenticated
    def get(self):
        form = SSHKeyAddForm()
        return render_template('settings/ssh.html', keys=keypairs.get_keys(g.user), form=form)

    def post(self):
        form = SSHKeyAddForm()
        if form.validate_on_submit():
            key = request.form.get('key').strip()
            fingerprint = keypairs.add_key(g.user, key)
            if fingerprint:
                g.logger.info('add ssh public key %s by %s.' % (fingerprint, g.user))
                return redirect('/settings/ssh')
        return render_template('settings/ssh.html', keys=keypairs.get_keys(g.user), form=form)

class SSHDeleteHandler(RequestHandler):
    def post(self):
        fingerprint = request.form.get('fingerprint')
        g.logger.info('delete ssh public key %s by user %s.' % (fingerprint, g.user))
        keypairs.delete_key(g.user, fingerprint)
        if request.is_xhr:
            return jsonify(status=0)
        return redirect('/settings/ssh')

app.add_url_rule('/profile', view_func=ProfileHandler.as_view('profile'))
app.add_url_rule('/ssh', view_func=SSHHandler.as_view('ssh'))
app.add_url_rule('/ssh/key/delete', view_func=SSHDeleteHandler.as_view('ssh_key_delete'))
