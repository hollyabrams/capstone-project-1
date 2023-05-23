import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, jsonify, g, get_flashed_messages
from flask_wtf import FlaskForm
from flask_login import LoginManager
from flask_login import login_required, current_user, logout_user, login_user
from forms import RegisterForm, LoginForm, EditUserForm, AddFavoriteCharacterForm
from models import db, connect_db, User, FavoriteCharacter
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///disney'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "topsecret"

bcrypt = Bcrypt(app)

# Configure the LoginManager part of the app instance
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

connect_db(app)

# Function to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

BASE_URL = "https://api.disneyapi.dev"

# Routes

# Main route #############################################################################
@app.route("/")
def index():
    form = FlaskForm()
    if current_user.is_authenticated:
        return render_template("index.html", form=form)
    else:
        return render_template("landing_page.html", form=form)

@app.route("/guest")
def guest():
    form = FlaskForm()
    return render_template("index.html", form=form)

# User Routes #############################################################################

@app.route('/users/<string:username>', methods=['GET', 'POST'])
def user_profile(username):
    form = FlaskForm()
    # Check if the current user is authenticated and the username matches
    if not current_user.is_authenticated or current_user.username != username:
        abort(403)

    user = User.query.filter_by(username=username).first_or_404()

    # Get user's favorite characters
    favorite_characters = FavoriteCharacter.query.filter_by(user_id=user.id).all()

    edit_form = EditUserForm(obj=user)

    if edit_form.validate_on_submit():
        user.username = edit_form.username.data
        user.email = edit_form.email.data

        db.session.commit()
        session['username'] = user.username

        return redirect(url_for("user_profile", username=user.username))

    return render_template("user_profile.html", edit_form=edit_form, user=user, favorite_characters=favorite_characters, form=form)

# Delete user route 
@app.route("/users/delete/<string:username>", methods=["POST"])
def delete_user(username):
    # Ensure the current user is authenticated and the username matches
    if not current_user.is_authenticated or current_user.username != username:
        abort(403)
    
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash("Your account has been deleted.", "success")
    return redirect(url_for("index"))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if current_user.is_authenticated:
        return redirect(f"/users/{current_user.username}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create a new user
        user = User(username=username, password=hashed_password, email=email)

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        return redirect(url_for("index"))

    else:
        return render_template("register.html", form=form)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            login_user(user)  # This sets up the user session
            return redirect(url_for("index"))
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)

# Logout route
@app.route("/logout")
def logout():
    """Logout route."""

    logout_user()
    return redirect("/login")


# Character Routes ############################################################################

# Error handling function for API calls
def handle_api_errors(api_func):
    @wraps(api_func)
    def wrapper(*args, **kwargs):
        try:
            return api_func(*args, **kwargs)
        except requests.exceptions.JSONDecodeError:
            flash("There was an issue retrieving data from the API. Please try again later.", "error")
            return redirect(url_for("index"))
    return wrapper

@app.route("/characters")
@handle_api_errors
def all_characters():
    page = request.args.get("page", 1)
    response = requests.get(f"{BASE_URL}/character?page={page}")
    data = response.json()
    return render_template("characters.html", data=data)

# Route for individual character
@app.route("/character/<int:character_id>")
@handle_api_errors
def single_character(character_id):
    response = requests.get(f"{BASE_URL}/character/{character_id}")
    data = response.json()
    form = AddFavoriteCharacterForm() 
    favorite_characters = [str(char.character_id) for char in current_user.favorite_characters]

    if current_user.is_authenticated:
        is_favorite = any(fav.character_id == character_id for fav in current_user.favorite_characters)
    else:
        is_favorite = False
    
    return render_template("character.html", data=data["data"], form=form, is_favorite=is_favorite, favorite_characters=",".join(favorite_characters))


# Route for filtering character by name
@app.route("/filter-character")
@handle_api_errors
def filter_character():
    name = request.args.get("name")
    response = requests.get(f"{BASE_URL}/character?name={name}")
    data = response.json()
    return render_template("characters.html", data=data)


# Route for adding character to favorites
@app.route('/favorite_character/<character_id>', methods=['POST'])
@login_required
def favorite_character(character_id):
    # Fetch character details from the API
    response = requests.get(f"{BASE_URL}/character/{character_id}")
    if response.status_code == 200:
        data = response.json()
        character_name = data["data"]["name"]
        character_image_url = data["data"]["imageUrl"]
    else:
        character_name = "Unknown Character"
        character_image_url = "image.jpg"

    favorite = FavoriteCharacter.query.filter_by(user_id=current_user.id, character_id=character_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"status": "unfavorited"})
    else:
        new_favorite = FavoriteCharacter(
            user_id=current_user.id,
            character_id=character_id,
            name=character_name,
            image_url=character_image_url
        )
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"status": "favorited"})




# Search route ############################################################################
@app.route('/search', methods=['GET'])
def search_characters():
    form = FlaskForm()
    query = request.args.get('query')
    if not query:
        return redirect(url_for('index'))
    
    query_tokens = query.split(' ')
    characters = []

    for token in query_tokens:
        encoded_token = requests.utils.quote(token)

        # Search by character name
        url = f"https://api.disneyapi.dev/character?name={encoded_token}"
        response = requests.get(url)
        data = response.json()
        characters += data.get('data', [])

    # Filter out non-dictionary items
    characters = [character for character in characters if isinstance(character, dict)]

    # Remove duplicate characters from the list
    characters = list({character['_id']: character for character in characters}.values())

    return render_template('search_results.html', characters=characters, form=form)



# 404 error handling ########################################################################
@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404


# Adding non-caching headers on every request for development purposes
@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


