from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, EqualTo
from qrScanApp.models import User, Admin

class LoginForm(FlaskForm):
    student_number = IntegerField('Student_id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    student_id = IntegerField('Student_id', validators=[DataRequired()])
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, student_id):
        user = User.query.filter_by(student_id=student_id.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class AdminLoginForm(FlaskForm):
    teacher_code = StringField('Teacher_code', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AdminRegistrationForm(FlaskForm):
    teacher_code = StringField('Teacher_Code', validators=[DataRequired()])
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, teacher_code):
        admin = Admin.query.filter_by(teacher_code=teacher_code.data).first()
        if admin is not None:
            raise ValidationError('Please use a different username.')

class DeleteForm(FlaskForm):
    student_id = IntegerField('Student_id', validators=[DataRequired()])
    submit = SubmitField('Delete')


class AdminDeleteForm(FlaskForm):
    teacher_code = StringField('Teacher_Code', validators=[DataRequired()])
    submit = SubmitField('Delete')
