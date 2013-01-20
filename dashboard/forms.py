import platform
import base64
import ssh
from flask import g, request
from flask.ext.wtf import Form
from flask.ext.wtf import TextField, TextAreaField, PasswordField
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
        if platform.system().lower() == 'linux':
            g.logger.debug('use pam for authenticate.')
            from pam import authenticate
            if authenticate(username, field.data):
                g.logger.info('session opened for user %s.' % username)
                return username
            else:
                raise ValueError('Authentication failure.')
        return username

class SSHKeyAddForm(Form):
    key = TextAreaField(
        'Key', validators=[Required(), Length(min=100)],
        description='Key'
    )

    def validate_key(self, field):
        key = field.data.strip()
        _key = None
        # pattern = r'^ssh-(rsa|dss)\s[a-zA-Z0-9/+=]+\s.*$'
        # if not re.match(pattern, key):
        #     raise ValueError('Invalid key.')
        if key.startswith('ssh-rsa'):
            try:
                _key = ssh.RSAKey(data=base64.b64decode(key.split()[1]))
            except ssh.SSHException:
                raise ValueError('Invalid key.')
        elif key.startswith('ssh-dss'):
            try:
                _key = ssh.DSSKey(data=base64.b64decode(key.split()[1]))
            except ssh.SSHException:
                raise ValueError('Invalid key.')
        else:
            raise ValueError('Invalid key.')
        return _key
