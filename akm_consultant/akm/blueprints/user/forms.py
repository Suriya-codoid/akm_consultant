from flask_wtf import Form
from wtforms import HiddenField, StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError,InputRequired,equal_to
from wtforms_components import EmailField, Email
from akm.blueprints.user.models import User, db
from akm.blueprints.user.validations import ensure_identity_exists, \
    ensure_existing_password_matches



class LoginForm(Form):
    next = HiddenField()
    email = StringField('Email',[InputRequired('*Email Address is required!')])
    password = PasswordField('Password',[InputRequired('*Password is required!')])
    submit = SubmitField('Sign In')

class SignupForm(Form):
    email = StringField(validators=[
        InputRequired('*Email Address is required!'), Email("* Invalid Email Address!"),Length(3, 30)
    ])
    full_name=StringField('Full Name',[InputRequired('*Full Name is required!'), Length(2, 20)])
    password = PasswordField('Password',[InputRequired('*Password is required!'), Length(8, 16)])
    confirm_password = PasswordField('Confirm Password',[InputRequired('*Confirm Password is required!'), equal_to('password',message="*Passwords didn't match!")])
    submit = SubmitField('Sign Up Now')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('*User already exists')

