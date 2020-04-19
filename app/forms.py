from flask_wtf import FlaskForm
from flask import request
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

####################################################################################
#--------------------------------authentication forms-------------------------------
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(message="What's the username?")])
	password = PasswordField('Password', validators=[DataRequired(message="Password?")])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('ID Number', validators=[DataRequired(message="Your student ID")])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
		'Confirm password', validators=[DataRequired(), EqualTo('password',message="Not exactly the same. Type again")])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already exists.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email address already exists.')
