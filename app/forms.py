from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    # syntax validate_FIELD_NAME tells WTF forms to append existing stock validators so you can use them
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username already exists - someone has already anticipated you... or it was you from the past :)')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Looks like your email is already here! Username:' + user.username.data)
            
class EditProfile(FlaskForm):
    username_field = StringField('Username', validators=[DataRequired(),Length(min=3, max=30)])
    about_me_field = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username_field(self, username_field):
        if username_field.data != self.original_username:
            user = User.query.filter_by(username=username_field.data).first()
            if user is not None:
                raise ValidationError('You cannot use this username because it is occupied, sorry')
                
                
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
    # empty form that underneath has data, that will be transferred via POST

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)
    ])
    submit = SubmitField('Submit')
