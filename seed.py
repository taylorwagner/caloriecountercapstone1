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
u1 = User(id=553131, username="sanrpor", password="password", email="sanrpor@test.com", goal_cal=1800)
u2 = User(id=771010, username="leopeezy3", password="testpassword", email="lpp@gmail.com", goal_cal=1300)
u3 = User(id=660101, username="meglporter", password="testpwpw", email="fake@email.com", goal_cal=1000)
u4 = User(id=440202, username="pauliefbaby", password="samplepassword", email="sports@nfl.com", goal_cal=3000)

# Add new objects to sesion, so they'll persist
db.session.add_all([u1, u2, u3, u4])

# Commit
db.session.commit()

# Add sample profiles
p1 = Profile(user_id=553131, first_name="Santana", last_name="Porter", city="Houston", state="TX", gender=False, reason="Meet people on a health journey and share my process with others")
p2 = Profile(user_id=771010)
p3 = Profile(user_id=660101, first_name="Megan", city="Crockett", state="TX", gender=True)
p4 = Profile(user_id=440202, first_name="Paul", last_name="Stewart", city="Los Angeles", state="CA", gender=False)

# Add new objects to sesion, so they'll persist
db.session.add_all([p1, p2, p3, p4])

# Commit
db.session.commit()

# Add sample groups
g1 = Group(id=9988, name="#texashealthgroup", description="For users who currently live in Texas!")
g2 = Group(id=9998, name="#youngandthriving", description="For users who are in their 20's")
g3 = Group(id=9999, name="#classof99")
g4 = Group(id=9888, name="#healthnewbies")

# Add new objects to session, so they'll persist
db.session.add_all([g1, g2, g3, g4])

# Commit
db.session.commit()

# Add sample users_groups
ug1 = UserGroup(group_id=9988, user_id=553131)
ug2 = UserGroup(group_id=9988, user_id=660101)
ug3 = UserGroup(group_id=9998, user_id=553131)
ug4 = UserGroup(group_id=9999, user_id=771010)

# Add new objects to session, so they'll persist
db.session.add_all([ug1, ug2, ug3, ug4])

# Commit
db.session.commit()

# Add sample follows
f1 = Follow(user_following_id=553131, user_followed_id=771010)
f2 = Follow(user_following_id=771010, user_followed_id=553131)
f3 = Follow(user_following_id=771010, user_followed_id=660101)
f4 = Follow(user_following_id=440202, user_followed_id=660101)

# Add new objects to session, so they'll persist
db.session.add_all([f1, f2, f3, f4])

# Commit
db.session.commit()

# Add sample comments
c1 = Comment(user_id=553131, text="Working hard this week!")
c2 = Comment(user_id=553131, text="Texas here!")

# Add new objects to session, so they'll persist
db.session.add_all([c1, c2])

# Commit
db.session.commit()