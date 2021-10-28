from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, EqualTo
from qrScanApp.models import User

class LoginForm(FlaskForm):
    identity = StringField('Identity', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    identity = StringField('Identity', validators=[DataRequired()])
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    editor = BooleanField('Admin')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, identity):
        user = User.query.filter_by(identity=identity.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class DeleteForm(FlaskForm):
    identity = StringField('Identity', validators=[DataRequired()])
    submit = SubmitField('Delete')

class TimeForm(FlaskForm):
    identity = StringField('Identity', validators=[DataRequired()])
    submit = SubmitField('Access Log')
