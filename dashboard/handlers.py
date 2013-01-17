import os
from pprint import pprint
from flask import request, g, render_template, redirect, session
from flask.views import MethodView as RequestHandler

from forms import SigninForm
from helpers import authenticated

class MainHandler(RequestHandler):
    @authenticated
    def get(self):
        return redirect('/settings/ssh')
        return render_template('index.html')

class AccountSigninHandler(RequestHandler):
    def get(self):
        next_url = request.args.get('next', '/')
        if g.user:
            return redirect(next_url)
        form = SigninForm()
        return render_template('signin.html', form=form)

    def post(self):
        next_url = request.args.get('next', '/')
        form = SigninForm()
        if form.validate_on_submit():
            session.permanent = True
            session['username'] = form.username.data
            return redirect(next_url)
        return render_template('signin.html', form=form)

class AccountSignoutHandler(RequestHandler):
    def get(self):
        next_url = request.args.get('next', '/account/signin')
        if 'username' not in session:
            return
        session.pop('username')
        return redirect(next_url)
