from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorite_characters = db.relationship('FavoriteCharacter', backref='user', lazy=True)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):  
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
        
    @classmethod
    def register(cls, username, password, email):
        """Register a user, hashing their password."""

        hashed = Bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    added_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True) 

    def __repr__(self):
        return f"FavoriteCharacter('{self.name}','{self.character_id}', '{self.user_id}')"




def connect_db(app):
    """Connect this database to Flask app."""
    db.app = app
    db.init_app(app)

