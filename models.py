from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

bcrypt = Bcrypt()

class User(db.Model):
    
    """User Table"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)

    email = db.Column(db.String(50),nullable = False, unique= True)

    password = db.Column(db.String(),nullable = False, unique= False)

    first_name = db.Column(db.String(30),nullable = False, unique= False)

    last_name = db.Column(db.String(30),nullable = False, unique= False)

    feedback = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, email, pwd, first_name, last_name):

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username = username, email = email, password = hashed_utf8, first_name = first_name, last_name = last_name)


    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            # return user instance
            return user
        else:
            return False

    

class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100),nullable = False, unique= False)

    content = db.Column(db.String(140),nullable = False, unique= False)

    user_username = db.Column(db.String(), db.ForeignKey('users.username'))