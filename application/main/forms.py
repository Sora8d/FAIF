from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from application.models import User

#This is the form that will be passed later to a template
#WTFForms are customized versions, as flask_wtf doesnt provide customized versions of fields.
#Validators argument is used to attach validation behaviors to fields. DataRequired validators
#simply checks that the field is not submitted empty. There are other validators available.

class RegisForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    password2= PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Register')
    def validate_username(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use another username.')
    def validate_email(self, email):
        user= User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditInf(FlaskForm):
    username= StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditInf, self).__init__(*args, **kwargs)
        self.original_username= original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user= User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

#This one is used for following and unfollowing, basically its a POST method, but as it doesnt need anyting more than a button, it is reusable
class EmptyForm(FlaskForm):
    submit= SubmitField('Submit')

class PostForm(FlaskForm):
    post= TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit= SubmitField('Submit')
