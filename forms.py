"""Flask-WTForms for Calorie Counter app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.core import DateField, IntegerField
from wtforms.validators import InputRequired, Length, Optional

STATE_ABBREV = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


class UserForm(FlaskForm):
    """Form for adding/editing users."""

    username = StringField('Username', validators=[InputRequired(message="Unique username is required."), Length(max=25)])
    password = PasswordField('Password', validators=[InputRequired(message="Must create a password with a minimum of 8 characters."), Length(min=8)])
    email = StringField('E-mail', validators=[InputRequired(message="Unique e-mail address is required.")])
    goal_cal = IntegerField("Daily Caloric Goal", validators=[InputRequired(message="Must include a daily caloric goal to sign-up. May change goal later.")])
    city = StringField('City', validators=[InputRequired(message="City is required.")])
    state = SelectField('State', choices=[(state, state) for state in STATE_ABBREV], validators=[InputRequired(message="State is required.")])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired(message="Unique username is required."), Length(max=25)])
    password = PasswordField('Password', validators=[InputRequired(message="Must create a password with a minimum of 8 characters."), Length(min=8)])


class GroupForm(FlaskForm):
    """Form for adding/editing groups."""

    name = StringField('Name of Group', validators=[InputRequired(message="Must include a comment.")])
    description = StringField('Description of Group', validators=[Optional()])


class FoodForm(FlaskForm):
    """Form for logging food items."""

    food = StringField('Food Item', validators=[InputRequired(message="Must include food item.")])
    date = DateField('Date', validators=[InputRequired(message="Must include the date.")])


class ExerciseForm(FlaskForm):
    """Form for logging exercises."""

    exercise = StringField('Exercise Type', validators=[InputRequired(message="Must include an exercise type.")])
    date = DateField('Date', validators=[InputRequired(message="Must include the date.")])


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""