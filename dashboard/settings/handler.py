import os
from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify, g
from flask.views import MethodView as RequestHandler

from helpers import authenticated, get_ssh_public_key_fingerprint, home_dir

app = Blueprint('settings', __name__)

class ProfileHandler(RequestHandler):
    @authenticated
    def get(self):
        return render_template('settings/profile.html')

class SSHHandler(RequestHandler):
    @authenticated
    def get(self):
        authorized_keys = os.path.join(home_dir(g.user), '.ssh', 'authorized_keys')
        keys = []
        with open(authorized_keys, 'r') as fp:
            for line in fp.readlines():
                if len(line) < 50:
                    continue
                name = line.split()[-1].rstrip()
                keys.append({
                    'name': name,
                    'fingerprint': get_ssh_public_key_fingerprint(line.rstrip())
                })
        return render_template('settings/ssh.html', keys=keys)

class SSHAddHandler(RequestHandler):
    def post(self):
        authorized_keys = os.path.join(home_dir(g.user), '.ssh', 'authorized_keys')
        key = request.form.get('key').strip()
        fingerprint = get_ssh_public_key_fingerprint(key)
        with open(authorized_keys, 'a+') as fp:
            fp.write('%s\n' % key)
            g.logger.info('add ssh public key %s by %s.' % (fingerprint, g.user))
        return redirect('/settings/ssh')

class SSHDeleteHandler(RequestHandler):
    def post(self):
        fingerprint = request.form.get('fingerprint')
        authorized_keys = os.path.join(home_dir(g.user), '.ssh', 'authorized_keys')
        g.logger.info('delete ssh public key %s by user %s.' % (fingerprint, g.user))
        with open(authorized_keys, 'r') as fp:
            lines = fp.readlines()
            with open(authorized_keys, 'w') as output:
                for line in lines:
                    if get_ssh_public_key_fingerprint(line.rstrip()) != fingerprint:
                        output.write(line)
        if request.is_xhr:
            return jsonify(status=0)
        return redirect('/settings/ssh')

app.add_url_rule('/profile', view_func=ProfileHandler.as_view('/profile'))
app.add_url_rule('/ssh', view_func=SSHHandler.as_view('/ssh'))
app.add_url_rule('/ssh/key/add', view_func=SSHAddHandler.as_view('/ssh/key/add'))
app.add_url_rule('/ssh/key/delete', view_func=SSHDeleteHandler.as_view('/ssh/key/delete'))
