import os
import requests

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

        print(register)

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


@app.route("/search", methods=["POST"])
@login_required
def search():

    query = request.form.get("query")

    if not query:
        flash("Submit your search query")
        return redirect("/")

    rows = db.execute("SELECT * FROM books WHERE isbn LIKE :query OR author LIKE :query OR title LIKE :query",
                       {"query": f"%{query}%"}).fetchall()

    return books(rows)


@app.route("/books")
@login_required
def books(books):

    if not books:
        flash("No matches")
        return redirect("/")

    return render_template("books.html", books=books)


@app.route("/books/<int:book_id>")
@login_required
def book_details(book_id):

    book_data = db.execute("SELECT * FROM books WHERE id = :book", {"book": book_id}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE book_id = :book", {"book": book_id}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                          params={"key": "2A54tMXDl9TuSbjhadZGqg", "isbns": book_data.isbn}).json()
    rating = {"average": res["books"][0]["average_rating"], "count": res["books"][0]["ratings_count"]}

    print(reviews)
    return render_template("book.html", book=book_data, rating=rating, reviews=reviews)


@app.route("/submit_review", methods=["POST"])
@login_required
def submit_review():

    rating = request.form.get("rating")
    review = request.form.get("review")
    book_id = request.form.get("id")

    if not rating:
        flash("Please, choose rating", category="error")
        return book_details(book_id)

    if not db.execute("SELECT * FROM books WHERE id = :book", {"book": book_id}):
        flash("No such book found in database", category="error")
        return redirect("/")

    if db.execute("SELECT * FROM reviews WHERE book_id = :book AND user_id = :user",
                          {"book": book_id, "user": session["user_id"]}).rowcount != 0:
        flash("You've submitted a review for this book before!", category="error")
        return book_details(book_id)

    submit = db.execute("INSERT INTO reviews (rating, text, book_id, user_id) VALUES (:rating, :text, :book, "
                                ":user)", {"rating": rating, "text": review, "book": book_id, "user": session["user_id"]})
    db.commit()

    flash("Thanks for your opinion!", category="success")
    return book_details(book_id)