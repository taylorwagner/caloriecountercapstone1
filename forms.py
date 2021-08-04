"""Flask-WTForms for Calorie Counter app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.fields.core import BooleanField, DateField, IntegerField
from wtforms.validators import InputRequired, Length, Optional

STATE_ABBREV = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[InputRequired(message="Unique username is required."), Length(max=25)])
    password = PasswordField('Password', validators=[InputRequired(message="Must create a password between 8-30 characters."), Length(min=8, max=30)])
    email = StringField('E-mail', validators=[InputRequired(message="Unique e-mail address is required.")])
    goal_cal = IntegerField("Daily Caloric Goal", validators=[InputRequired(message="Must include a daily caloric goal to sign-up. May change goal later.")])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired(message="Unique username is required."), Length(max=25)])
    password = PasswordField('Password', validators=[InputRequired(message="Must create a password between 8-30 characters."), Length(min=8, max=30)])


class UserProfileForm(FlaskForm):
    """Form for creating user's profile information."""

    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    state = SelectField('State', choices=[(state, state) for state in STATE_ABBREV], validators=[Optional()])
    gender = BooleanField('Male/Female', validators=[Optional()])
    dob = DateField('Date of Birth', validators=[Optional()])
    reason = TextAreaField('Reason(s) for Joining Calorie Counter', validators=[Optional()])