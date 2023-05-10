import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_login import LoginManager
from flask_login import login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, EditUserForm
from models import db, connect_db, User
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///disney'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "topsecret"

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

connect_db(app) 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

BASE_URL = "https://api.disneyapi.dev"


@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html")
    else:
        return render_template("landing_page.html")

@app.route("/guest")
def guest():
    return render_template("index.html")

@app.route('/users/<string:username>', methods=['GET', 'POST'])
def user_profile(username):
    if "username" not in session or session['username'] != username:
        abort(403)

    user = User.query.filter_by(username=username).first_or_404()

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data

        db.session.commit()
        session['username'] = user.username

        return redirect(url_for("user_profile", username=user.username))

    return render_template("user_profile.html", form=form, user=user)

@app.route("/users/delete/<string:username>", methods=["POST"])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    if user.username != session['username']:
        abort(403)

    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    flash("Your account has been deleted.", "success")
    return redirect(url_for("index"))


@app.route("/characters")
def all_characters():
    page = request.args.get("page", 1)
    response = requests.get(f"{BASE_URL}/character?page={page}")
    data = response.json()
    return render_template("characters.html", data=data)

@app.route("/character/<int:character_id>")
def single_character(character_id):
    response = requests.get(f"{BASE_URL}/character/{character_id}")
    data = response.json()
    return render_template("character.html", data=data["data"])

@app.route("/filter-character")
def filter_character():
    name = request.args.get("name")
    response = requests.get(f"{BASE_URL}/character?name={name}")
    data = response.json()
    return render_template("characters.html", data=data)


# Search
@app.route('/search', methods=['GET'])
def search_characters():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('index'))
    
    # Properly encode the query to handle multiple words
    encoded_query = requests.utils.quote(query)

    # Search by character name
    url = f"https://api.disneyapi.dev/character?name={encoded_query}"
    response = requests.get(url)
    data = response.json()
    characters = data.get('data', [])

    # Search by movie
    if not characters:
        url = f"https://api.disneyapi.dev/character?films={encoded_query}"
        response = requests.get(url)
        data = response.json()
        characters = data.get('data', [])
    
    return render_template('search_results.html', characters=characters)


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

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


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            return redirect(url_for("index"))
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


#Logout
@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")


# Error Handler

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404






