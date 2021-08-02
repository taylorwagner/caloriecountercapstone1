"""Flask-WTForms for Calorie Counter app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.fields.core import IntegerField
from wtforms.validators import InputRequired, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[InputRequired(message="Unique username is required."), Length(max=25)])
    password = PasswordField('Password', validators=[InputRequired(message="Must create a password between 8-30 characters."), Length(min=8, max=30)])
    email = StringField('E-mail', validators=[InputRequired("Unique e-mail address is required.")])

class UserProfileForm(FlaskForm):
    """Form for creating user's profile information."""

    goal_cal = IntegerField("Daily Caloric Goal", validators=[InputRequired()])
