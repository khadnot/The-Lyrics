from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect database to Flask app."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, password, first_name, last_name, email):
        """Sign up user

        Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Finds user by username and password."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
    
        return False

class Genre(db.Model):
    """The Music Genres"""

    __tablename__ = 'genres'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    genre = db.Column(
        db.Text,
    )


class Song(db.Model):
    """Song information"""

    __tablename__ = 'songs'

    id = db.Column(
        db.Integer,
        nullable=False,
        primary_key=True,
    )

    song_artist = db.Column(
        db.Text,
        nullable=False,
    )

    song_name = db.Column(
        db.Text,
        nullable=False,
    )

    song_id = db.Column(
        db.Integer,
        nullable=False,
    )

    genre_id = db.Column(
        db.Integer,
        db.ForeignKey('genres.id'),
        nullable=False,
    )

    genre = db.relationship('Genre', backref='songs')

