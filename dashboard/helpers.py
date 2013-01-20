import os
import platform
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
