import os

from flask import Flask, session, request, render_template, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Check if user is already logged in
    if session.get("user_id"):
        return redirect("/")

    if request.method == "POST":

        # Forget any session parameters
        session.clear()

        if not request.form.get("username"):
            flash("Username was not provided!", category="error")
            return render_template("/login")

        if not request.form.get("password"):
            flash("Password was not provided!", category="error")
            return render_template("/login")

        username = request.form.get("username")
        password = request.form.get("password")

        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if not user:
            flash("No such user", category="error")
            return render_template("login.html")

        if not check_password_hash(user.password, password):
            flash("Password is incorrect")
            return render_template("login.html")

        session["user_id"] = user.id
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Check if user is already logged in
    if session.get("user_id"):
        return redirect("/")

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("Username was not provided", category="error")
            render_template("register.html")

        if not password:
            flash("Password was not provided", category="error")
            render_template("register.html")

        if not request.form.get("confirmation") or password != request.form.get("confirmation"):
            flash("Passwords don't match", category="error")
            render_template("register.html")

        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
            flash("This username is already in use", category="error")
            return render_template("register.html")

        register = db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                              {"username": username, "password": generate_password_hash(password)})
        db.commit()

        # session.clear()
        # session["user_id"] = register

        flash("Successful registration")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
