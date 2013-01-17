import os
import platform
import base64
import hashlib
import functools
from flask import g, request, redirect, url_for
from flask import session

def get_current_user():
    if 'username' not in session:
        return None
    return session['username']

def authenticated(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if not g.user:
            url = '/account/signin'
            if '?' not in url:
                url += '?next=' + request.url
            return redirect(url)
        return method(*args, **kwargs)
    return wrapper

def get_ssh_public_key_fingerprint(line):
    key = base64.b64decode(line.strip().split()[1])
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))

def home_dir(username):
    base_dir = '/home'
    if platform.system().lower() == 'darwin':
        base_dir = '/Users'
    return os.path.abspath(os.path.join(base_dir, username))
