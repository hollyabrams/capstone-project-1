from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, DataRequired, Email
from models import User

class RegisterForm(FlaskForm):
    """Form for user registration."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Length(max=50), Email()],
    )


class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )


class EditUserForm(FlaskForm):
    """Form for user account editing."""

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('New Password (optional)', validators=[Length(min=8, max=120, message="Password must be at least 8 characters long.")])
 

class AddFavoriteCharacterForm(FlaskForm):
    """Form for adding favorite characters."""

    csrf_token = StringField('CSRF Token', validators=[DataRequired()])
