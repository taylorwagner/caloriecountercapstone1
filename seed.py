"""Seed file to make sample data for calcountdb."""
from models import db, User, Profile, Group, UserGroup, Follows, Comment
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Profile.query.delete()
Group.query.delete()
UserGroup.query.delete()
Follows.query.delete()
Comment.query.delete()

# Add sample users
fake_u1 = User.signup(username="sanrpor", password="password", email="sanrpor@test.com", goal_cal=1800)
fake_u1id = 553131
fake_u1.id = fake_u1id
fake_u2 = User.signup(username="leopeezy3", password="testpassword", email="lpp@gmail.com", goal_cal=1300)
fake_u2id = 771010
fake_u2.id = fake_u2id
fake_u3 = User.signup(username="meglporter", password="testpwpw", email="fake@email.com", goal_cal=1000)
fake_u3id = 660101
fake_u3.id = fake_u3id
fake_u4 = User.signup(username="pauliefbaby", password="samplepassword", email="sports@nfl.com", goal_cal=3000)
fake_u4id = 440202
fake_u4.id = fake_u4id

# Add new objects to sesion, so they'll persist
db.session.add_all([fake_u1, fake_u2, fake_u3, fake_u4])

# Commit
db.session.commit()

# Add sample profiles
fake_p1 = Profile(user_id=553131, first_name="Santana", last_name="Porter", city="Houston", state="TX", gender=False, reason="Meet people on a health journey and share my process with others")
fake_p2 = Profile(user_id=771010)
fake_p3 = Profile(user_id=660101, first_name="Megan", city="Crockett", state="TX", gender=True)
fake_p4 = Profile(user_id=440202, first_name="Paul", last_name="Stewart", city="Los Angeles", state="CA", gender=False)

# Add new objects to sesion, so they'll persist
db.session.add_all([fake_p1, fake_p2, fake_p3, fake_p4])

# Commit
db.session.commit()

# Add sample groups
fake_g1 = Group(id=9988, name="#texashealthgroup", description="For users who currently live in Texas!")
fake_g2 = Group(id=9998, name="#youngandthriving", description="For users who are in their 20's")
fake_g3 = Group(id=9999, name="#classof99")
fake_g4 = Group(id=9888, name="#healthnewbies")

# Add new objects to session, so they'll persist
db.session.add_all([fake_g1, fake_g2, fake_g3, fake_g4])

# Commit
db.session.commit()

# Add sample users_groups
fake_ug1 = UserGroup(group_id=9988, user_id=553131)
fake_ug2 = UserGroup(group_id=9988, user_id=660101)
fake_ug3 = UserGroup(group_id=9998, user_id=553131)
fake_ug4 = UserGroup(group_id=9999, user_id=771010)

# Add new objects to session, so they'll persist
db.session.add_all([fake_ug1, fake_ug2, fake_ug3, fake_ug4])

# Commit
db.session.commit()

# Add sample follows
fake_f1 = Follows(user_following_id=553131, user_followed_id=771010)
fake_f2 = Follows(user_following_id=771010, user_followed_id=553131)
fake_f3 = Follows(user_following_id=771010, user_followed_id=660101)
fake_f4 = Follows(user_following_id=440202, user_followed_id=660101)

# Add new objects to session, so they'll persist
db.session.add_all([fake_f1, fake_f2, fake_f3, fake_f4])

# Commit
db.session.commit()

# Add sample comments
fake_c1 = Comment(user_id=553131, text="Working hard this week!")
fake_c2 = Comment(user_id=553131, text="Texas here!")

# Add new objects to session, so they'll persist
db.session.add_all([fake_c1, fake_c2])

# Commit
db.session.commit()