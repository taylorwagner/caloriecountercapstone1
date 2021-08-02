"""Flask-WTForms for Calorie Counter app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired(message="Unique username is required."), Length(max=25)])
    password = PasswordField('Password', validators=[DataRequired(message="Must create a password between 8-30 characters."), Length(min=8, max=30)])
    email = StringField('E-mail', validators=DataRequired("Unique e-mail address is required."))
