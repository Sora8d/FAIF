from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from application.models import User

class LoginForm(FlaskForm):
    useremail= StringField('Username or email', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    remember_me= BooleanField('Remember Me')
    submit= SubmitField('Sign In')

class ResetPasswordRequestForm(FlaskForm):
    email= StringField('Email', validators=[DataRequired(), Email()])
    submit= SubmitField('Request Password Reset')

class ResetPassword(FlaskForm):
    password= PasswordField('Password', validators=[DataRequired()])
    password2= PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Rquest Password Reset')
