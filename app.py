"""Calorie Counter Flask App."""

import os
import requests
from flask import Flask, session, g, request, render_template, redirect, flash, jsonify
from sqlalchemy.exc import IntegrityError
from forms import UserForm, LoginForm, GroupForm, FoodForm
from models import db, connect_db, User, Group, UserGroup, Food

CURR_USER_KEY = "curr_user"
CALORIE_NINJA_API_BASE_URL = "https://api.calorieninjas.com/v1"

app = Flask(__name__)

## uncomment lines 16-17 when in development and uncomment lines 18-19 when in production (only 1 can be uncommented at a time)
from secret import api_key, SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
# api_key = os.environ["api_key"]
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


## uncomment line 25 when in development and uncomment lines 21-24 when in production (only 1 option can be uncommented at a time)
# uri = os.environ.get("DATABASE_URL")
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# app.config['SQLALCHEMY_DATABASE_URI'] = (uri)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///calcount')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)


## CALORIE NINJA API
def get_food_cal(foodInputted):
    """Given a food, get a calorie number."""

    res = requests.get(f"{CALORIE_NINJA_API_BASE_URL}/nutrition?query={foodInputted}", headers={'X-Api-Key': api_key})
    data = res.json()
    calories = data["items"][0]['calories']
    return calories


@app.route('/api/get-food-cal', methods=["POST"])
def get_cal_for_user_food():
    """Get calories, validate input, and return information about food."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    received = request.json

    form = FoodForm(csrf_enabled=False, data=received)
    user = g.user

    if form.validate_on_submit():
        foodInputted = received["food"]
        dateInputted = received["date"]

        user_food = Food(user_id=user.id, food=foodInputted, date=dateInputted, calories=get_food_cal(foodInputted))
        db.session.add(user_food)
        db.session.commit()

        return jsonify(
            food={"food": foodInputted, "calories": get_food_cal(foodInputted)}, date={"date": dateInputted})

    else:
        return jsonify(errors=form.errors)


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
            user = User.signup(username=form.username.data, password=form.password.data, email=form.email.data, goal_cal=form.goal_cal.data, city=form.city.data, state=form.state.data)
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


@app.route('/account/<int:user_id>/groups')
def show_user_groups(user_id):
    """Show list of groups that this user is in."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    user = User.query.get_or_404(user_id)
    return render_template('groups/user-groups.html', user=user)


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


## FOLLOW ROUTES


@app.route('/account/<int:user_id>/following')
def show_following(user_id):
    """Show list of people that this user is following."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    user = User.query.get_or_404(user_id)
    return render_template('follows/following.html', user=user)


@app.route('/account/<int:user_id>/followers')
def show_followers(user_id):
    """Show list of followers of this user."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    user = User.query.get_or_404(user_id)
    return render_template('follows/followers.html', user=user)


@app.route('/account/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    g.user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/account/{g.user.id}/following")


@app.route('/account/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect("/")

    followed_user = User.query.get(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/account/{g.user.id}/following")


## JOURNAL ROUTES


@app.route('/account/<int:user_id>/food')
def log_food(user_id):
    """Display form for logging food into journal"""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect("/")

    form = FoodForm()
    user = User.query.get_or_404(user_id)

    return render_template('users/food.html', form=form, user=user)


## GROUP ROUTES


@app.route('/groups')
def all_groups():
    """Show all groups."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    groups = Group.query.all()

    return render_template('groups/groups.html', groups=groups)


@app.route('/groups/new', methods=["GET", "POST"])
def new_group():
    """Create a new group."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    form = GroupForm()

    if form.validate_on_submit():
        group = Group(name=form.name.data, description=form.description.data)

        db.session.add(group)
        db.session.commit()

        flash(f"{group.name} has been added as a support group!", 'success')
        return redirect('/groups')

    return render_template('groups/new.html', form=form)


@app.route('/groups/<int:group_id>')
def show_group(group_id):
    """Show group description and users in group."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    group = Group.query.get_or_404(group_id)

    return render_template('groups/show.html', group=group)


@app.route('/groups/<int:group_id>/join', methods=["POST"])
def join_group(group_id):
    """Logged in user joins group."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    group = Group.query.get_or_404(group_id)
    groupid = group_id
    user = g.user
    new_user_group = UserGroup(group_id=groupid, user_id=user.id)

    db.session.add(new_user_group)
    db.session.commit()

    return redirect(f'/groups/{group.id}')


@app.route('/groups/<int:group_id>/leave', methods=["POST"])
def leave_group(group_id):
    """Logged in user leaves group."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    group = Group.query.get_or_404(group_id)
    groupid = group_id
    user = g.user
    target_user_group = UserGroup(group_id=groupid, user_id=user.id)
    targetid = target_user_group.id

    db.session.delete(targetid)
    db.session.commit()

    return redirect(f'/groups/{group.id}')


@app.route('/groups/<int:group_id>/edit', methods=["GET", "POST"])
def edit_group(group_id):
    """Edit group."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    group = Group.query.get_or_404(group_id)
    form = GroupForm(obj=group)

    if form.validate_on_submit():
        group.name = form.name.data
        group.description = form.description.data

        db.session.commit()

        flash(f"Edited {group.name}", 'success')
        return redirect(f"/groups/{group.id}")

    return render_template('groups/edit.html', group_id=group.id, form=form)


@app.route('/groups/<int:group_id>/delete', methods=["POST"])
def delete_group(group_id):
    """Delete group."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    group = Group.query.get_or_404(group_id)

    db.session.delete(group)
    db.session.commit()

    return redirect('/groups')


## APPLICATION MAIN ROUTES


@app.route('/')
def homepage():
    """Application homepage. Advertisement/explanation of application with options to either signup or login."""
    return render_template('home.html')


@app.route('/about')
def about_page():
    """Application about page. Inform user's about application."""
    return render_template('about.html')


@app.errorhandler(404)
def not_found(e):
    """Custom 404 page."""
    return render_template('404.html'), 404


@app.route('/profile/<int:user_id>')
def show_profile(user_id):
    """Show profile page for user."""
    user = User.query.get_or_404(user_id)

    dates = []
    for food in user.foods:
        dates.append(food.date)
    dates.sort()

    return render_template("users/show.html", user=user, dates=set(dates))


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