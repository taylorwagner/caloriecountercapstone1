"""Calorie Counter Flask App."""

from flask import Flask, session, g, request, render_template, redirect, flash
from sqlalchemy.exc import IntegrityError
from forms import UserForm, LoginForm, GroupForm, CommentForm, FoodForm, ExerciseForm, DeleteForm
from models import db, connect_db, User, Group, UserGroup, Follows, Comment

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///calcount'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "shh"

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
    form = UserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data, email=form.password.data, goal_cal=form.goal_cal.data, city=form.city.data, state=form.state.data)
            db.session.commit()

        except IntegrityError as e:
            flash("Username or E-mail aldready taken.", 'danger')
            return render_template("users/signup.html", form=form)

        do_login(user)
        flash(f"Hello, {user.username}! Welcome to Calorie Counter!", 'success')
        return redirect(f"/profile/{user.id}")

    else:
        return render_template("users/signup.html", form=form)

    
@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Log in for {user.username} was successful!", 'success')
            return redirect(f"/profile/{user.id}")

        flash("Invalid credentials!", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("Successfully logged out.", 'success')

    return redirect('/')


## ACCOUNT ROUTES


@app.route('/account/<int:user_id>')
def show_account(user_id):
    """Show user's account."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')
    
    user = User.query.get_or_404(user_id)

    return render_template("users/account.html", user=user)


@app.route('/account/<int:user_id>/edit', methods=["GET", "POST"])
def edit_account(user_id):
    """Edit user's account."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    user = g.user
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.goal_cal = form.goal_cal.data
            user.city = form.city.data
            user.state = form.state.data

            db.session.commit()

            flash(f"Edited account for {user.username}", 'success')
            return redirect(f"/account/{user.id}")
        
        flash("Wrong password, please try again!!", 'danger')

    return render_template('users/edit.html', user_id=user.id, form=form)


@app.route('/account/delete', methods=["POST"])
def delete_account():
    """Delete user."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect('/')


## GROUP ROUTES


@app.route('/groups')
def show_groups():
    """Show all groups."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')
        
    groups = Group.query.all()

    return render_template('groups/groups.html', groups=groups)


## COMMENT ROUTES


## APPLICATION MAIN ROUTES


@app.route('/')
def homepage():
    """Application homepage. Advertisement/explanation of application with options to either signup or login."""
    return render_template('home.html')


@app.route('/about')
def about_page():
    """Application about page. Inform user's about application."""
    return render_template('about.html')


@app.route('/profile/<int:user_id>')
def show_profile(user_id):
    """Show profile page for user."""
    user = User.query.get_or_404(user_id)

    return render_template("users/show.html", user=user)


# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req