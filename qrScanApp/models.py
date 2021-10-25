from datetime import datetime
from qrScanApp import storage, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, storage.Model):
    id = storage.Column(storage.Integer, primary_key=True)
    identity = storage.Column(storage.String(5), index=True, unique=True)
    first_name = storage.Column(storage.String(128), index=True)
    last_name = storage.Column(storage.String(128), index=True)
    password_hash = storage.Column(storage.String(128), unique=True)
    editor = storage.Column(storage.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.first_name)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(identity):
    return User.query.get(identity)

class Log(storage.Model):
    id = storage.Column(storage.Integer, primary_key=True)
    identity = storage.Column(storage.String(5), storage.ForeignKey('user.identity'), index=True)
    timestamp = storage.Column(storage.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Log {}>'.format(self.timestamp)

class Code(storage.Model):
    id = storage.Column(storage.Integer, primary_key=True)
    code = storage.Column(storage.String(128), index=True, unique=True)
    def __repr__(self):
        return '<Code {}>'.format(self.code)

