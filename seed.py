"""Seed file to make sample data for calcountdb."""
from models import db, User, Profile, Group, UserGroup, Follow, Comment
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Profile.query.delete()
Group.query.delete()
UserGroup.query.delete()
Follow.query.delete()
Comment.query.delete()

# Add sample users
u1 = User(id=553131, username="sanrpor", password="password", email="sanrpor@test.com")
u2 = User(id=771010, username="leopeezy3", password="testpassword", email="lpp@gmail.com")
u3 = User(id=660101, username="meglporter", password="testpwpw", email="fake@email.com")
u4 = User(id=440202, username="pauliefbaby", password="samplepassword", email="sports@nfl.com")

# Add new objects to sesion, so they'll persist
db.session.add.all([u1, u2, u3, u4])

# Commit
db.session.commit()

# Add sample profiles
p1 = Profile(user_id=553131, first_name="Santana", last_name="Porter", city="Houston", state="TX", gender=False, dob="05/31/2000", reason="Meet people on a health journey and share my process with others", goal_cal=1800)
p2 = Profile(user_id=771010, goal_cal=1300)
p3 = Profile(user_id=660101, first_name="Megan", city="Crockett", state="TX", gender=True, dob="06/01/1981", goal_cal=1000)
p4 = Profile(user_id=440202, first_name="Paul", last_name="Stewart", city="Los Angeles", state="CA", gender=False, goal_cal=3000)

# Add new objects to sesion, so they'll persist
db.session.add.all([p1, p2, p3, p4])

# Commit
db.session.commit()