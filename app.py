"""Calorie Counter Flask App."""

from secret import api_id, api_key
import requests
from flask import Flask, session, g, request, render_template, redirect, flash, jsonify
from sqlalchemy.exc import IntegrityError
from forms import UserForm, LoginForm, GroupForm, FoodForm, ExerciseForm, DeleteForm
from models import db, connect_db, User, Group, UserGroup, Follows

CURR_USER_KEY = "curr_user"
NUTRITIONIX_API_BASE_URL = "https://trackapi.nutritionix.com/v2/natural"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///calcount'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "shh"

connect_db(app)


## NUTRITIONIX API
def get_cal_for_food(user_food):
    """Given a food, get a calorie number."""

    res = requests.post(f"{NUTRITIONIX_API_BASE_URL}/nutrients", headers={"x-app-Id": api_id, "x-app-Key": api_key, "x-remote-user-id": 0}, body={"query": user_food})
    data = res.json()
    food = data["foods"][0]['food_name']
    calories = data["foods"][0]['nf_calories']
    food_cal = {'food': food, 'calories': calories}
    return food_cal


def get_cal_for_exercise(user_exercise):
    """Given an exerise, get a calorie number."""

    res = requests.post(f"{NUTRITIONIX_API_BASE_URL}/exercise", headers={"x-app-Id": api_id, "x-app-Key": api_key, "x-remote-user-id": 0}, body={"query": user_exercise})
    data = res.json()
    exercise = data["exercises"][0]['user_input']
    calories = data["exercises"][0]['nf_calories']
    exercise_cal = {'exercise': exercise, 'calories': calories}
    return exercise_cal


# @app.route('/api/get-food-cal', methods=["POST"])
# def get_cal_for_user_food():
#     """Get calories, validate input, and return information about food."""

#     received = request.json

#     form = FoodForm(data=received)

#     if form.validate_on_submit():
#         food = received['food']
#         food_cal_user = get_cal_for_food(food)

#         return food_cal_user

#     else:
#         return jsonify(errors=form.errors)


# @app.route('/api/get-exercise-cal', methods=["POST"])
# def get_cal_for_user_exercise():
#     """Get calories, validate input, and return information about exercise."""

#     received = request.json

#     form = ExerciseForm(data=received)

#     if form.validate_on_submit():
#         exercise = received['exercise']
#         exercise_cal_user = get_cal_for_exercise(exercise)

#         return exercise_cal_user

#     else:
#         return jsonify(errors=form.errors)


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


@app.route('/account/<int:user_id>/groups')
def show_user_groups(user_id):
    """Show list of people that this user is following."""
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


@app.route('/account/<int:user_id>/exercise')
def log_exercise(user_id):
    """Display form for logging exercise into journal"""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect("/")

    form = ExerciseForm()
    user = User.query.get_or_404(user_id)

    return render_template('users/exercise.html', form=form, user=user)


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


@app.route('/groups/<int:group_id>/join')
def join_group(group_id):
    """Logged in user joins group."""
    if not g.user:
        flash("Access unauthorized.", 'danger')
        return redirect('/')

    group = Group.query.get_or_404(group_id)
    user = g.user
    new_user_group = UserGroup(group_id=group, user_id=user.id)

    db.session.add(new_user_group)
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