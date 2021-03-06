"""SQLAlchemy models for Calorie Counter."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = "follows"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_following_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    user_followed_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))

    def __repr__(self):
        """Human readable representation of follow table data."""
        return f"<Follows #{self.id}: user_following_id={self.user_following_id}, user_followed_id={self.user_followed_id}>"


class User(db.Model):
    """User in the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    goal_cal = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(2), nullable=False)

    following = db.relationship("User", secondary="follows", primaryjoin=(Follows.user_following_id == id), secondaryjoin=(Follows.user_followed_id == id))

    followers = db.relationship("User", secondary="follows", primaryjoin=(Follows.user_followed_id == id), secondaryjoin=(Follows.user_following_id == id), overlaps="following")

    groups = db.relationship("Group", secondary="users_groups", backref="users")

    foods = db.relationship("Food")

    def __repr__(self):
        """Human readable representation of user table data."""
        return f"<User #{self.id}: {self.username}, {self.email}, goal_calories={self.goal_cal} city={self.city} state={self.state}>"

    def is_following(self, other_user):
        """Is this user following `other_user`?"""

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1

    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    @classmethod
    def signup(cls, username, password, email, goal_cal, city, state):
        """Sign up a user. Hashes password and adds user to the system."""
        hashed_pw = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, password=hashed_pw, email=email, goal_cal=goal_cal, city=city, state=state)

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with matching 'username' and 'password' combination."""
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Group(db.Model):
    """Support groups for users to join"""

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        """Human readable representation of group table data."""
        return f"<Group: id={self.id} name={self.name} desc='{self.description}'>"


class UserGroup(db.Model):
    """Connection of a user <-> support group."""

    __tablename__ = "users_groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete="cascade"))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))

    def __repr__(self):
        """Human readable representation of user_group table data."""
        return f"<UserGroup: id={self.id} group_id={self.group_id} user_id={self.user_id}>"


class Food(db.Model):
    """Connection of a user <-> food input."""

    __tablename__ = "foods"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
    date = db.Column(db.String, nullable=False)
    food = db.Column(db.String, nullable=False)
    calories = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        """Human readable representation of food table data."""
        return f"<Food: id={self.id} user_id={self.user_id} date={self.date} food={self.food} calories={self.calories}>"


def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)