from datetime import datetime
from qrScanApp import storage, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, storage.Model):
    id = storage.Column(storage.Integer, primary_key=True)
    student_id = storage.Column(storage.Integer, index=True, unique=True)
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
def load_user(student_id):
    return User.query.get(int(student_id))

class Log(storage.Model):
    id = storage.Column(storage.Integer, primary_key=True)
    student = storage.Column(storage.Integer, storage.ForeignKey('user.student_id'), index=True)
    timestamp = storage.Column(storage.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Log {}>'.format(self.timestamp)

class Admin(UserMixin, storage.Model):
    id = storage.Column(storage.Integer, primary_key=True)
    teacher_code = storage.Column(storage.String(3), index=True)
    first_name = storage.Column(storage.String(128), index=True)
    last_name = storage.Column(storage.String(128), index=True)
    password_hash = storage.Column(storage.String(128), unique=True)
    editor = storage.Column(storage.Boolean, default=True)

    def __repr__(self):
        return '<Admin {}>'.format(individual.teacher_code)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Code(storage.Model):
    id = storage.Column(storage.Integer, primary_key=True)
    code = storage.Column(storage.String(128), index=True, unique=True)
    def __repr__(self):
        return '<Code {}>'.format(self.code)

