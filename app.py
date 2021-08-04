"""Calorie Counter Flask App."""

import os
from flask import Flask, session, g, request, render_template, redirect, flash
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm
from models import db, connect_db, User, Profile, Group, UserGroup, Follow, Comment

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///calcount'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "shh")

connect_db(app)


## USER SIGNUP/LOGIN/LOGOUT


@app.before_request
def add_user_to_g():
    """If user logged in, add current user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    
    else:
        g.user = None

def do_login(user):
    """Login user."""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup. Create new user and add to DB. Redirect to homepage. If the form is not valid, present form. If the username or email is not unique, flash message and reload the form."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data, email=form.password.data, goal_cal=form.goal_cal.data)
            db.session.commit()

        except IntegrityError as e:
            flash("Username or E-mail aldready taken.", 'danger')
            return render_template("users/signup.html", form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template("users/signup.html", form=form)