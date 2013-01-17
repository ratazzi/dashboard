import platform
import redis
import hashlib
from flask import g, request
from flask.ext.wtf import Form
from flask.ext.wtf import TextField, PasswordField
from flask.ext.wtf import Required, Length

class SigninForm(Form):
    username = TextField(
        'Username', validators=[Required(), Length(min=3, max=20)],
        description='Username'
    )
    password = PasswordField(
        'Password', validators=[Required(), Length(min=6)],
    )

    def validate_password(self, field):
        """use Linux PAM for authenticate"""
        username = self.username.data
        # r = redis.StrictRedis(host='localhost', port=6379, db=1)
        # key = request.remote_addr
        # retry = r.get(key)
        # print request.remote_addr
        # print request.headers
        # if retry >= 5:
        #     raise ValueError('Exceed the maximum number of retries.')

        if platform.system().lower() == 'linux':
            g.logger.debug('use pam for authenticate.')
            from pam import authenticate
            if authenticate(username, field.data):
                g.logger.info('session opened for user %s.' % username)
                return username
            else:
                pass
                # if not r.exists(key):
                #     r.set(key, 1)
                #     r.expire(key, 3600)
                # else:
                #     r.incr(key)
                raise ValueError('Authentication failure.')
        return username

class SSHKeyAddForm(Form):
    username = TextField(
        'Keys', validators=[Required(), Length(min=50)],
        description='Keys'
    )

    def validate_keys(self, field):
        pass
