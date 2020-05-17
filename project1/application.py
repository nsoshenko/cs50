import os  # to get env configs from os to flask
import requests

from flask import Flask, session, request, render_template, redirect, flash, jsonify
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

# Turn off alphabetical sorting for JSON responses
# https://flask.palletsprojects.com/en/1.1.x/config/#config
app.config["JSON_SORT_KEYS"] = False

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    """Renders main page with search bar"""

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs user in and creates a session"""

    # Check if user is already logged in
    if session.get("user_id"):
        return redirect("/")

    if request.method == "POST":

        # Forget any session parameters
        session.clear()

        # Check for inputs
        if not request.form.get("username"):
            flash("Username was not provided!", category="error")
            return render_template("/login")

        if not request.form.get("password"):
            flash("Password was not provided!", category="error")
            return render_template("/login")

        # Memorize inputs for comfort
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if there a user with such username in DB
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if not user:
            flash("No such user", category="error")
            return render_template("login.html")

        # Check if password hashes of the input and DB match
        if not check_password_hash(user.password, password):
            flash("Password is incorrect")
            return render_template("login.html")

        # Create session if all checks were passed
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page and creation of a user in DB"""

    # Check if user is already logged in
    if session.get("user_id"):
        return redirect("/")

    if request.method == "POST":

        # Memorize inputs for comfort
        username = request.form.get("username")
        password = request.form.get("password")

        # Check for inputs
        if not username:
            flash("Username was not provided", category="error")
            render_template("register.html")

        if not password:
            flash("Password was not provided", category="error")
            render_template("register.html")

        if not request.form.get("confirmation") or password != request.form.get("confirmation"):
            flash("Passwords don't match", category="error")
            render_template("register.html")

        # Check if the username is free
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount > 0:
            flash("This username is already in use", category="error")
            return render_template("register.html")

        # Create user in DB if all checks were passed
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                  {"username": username, "password": generate_password_hash(password)})
        db.commit()

        # Additional select for autologin after registration (haven't managed to do it with INSERT result)
        autologin = db.execute("SELECT id FROM users WHERE username = :username", {"username": username}).fetchone()

        # Create session to login the user
        session.clear()
        session["user_id"] = autologin.id
        session["username"] = username

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
    """Search for books in DB"""

    # Memorize input for comfort
    query = request.form.get("query")

    # Check for input
    if not query:
        flash("Submit your search query", category="error")
        return redirect("/")

    # Execute search in DB
    rows = db.execute("SELECT * FROM books WHERE isbn LIKE :query OR author LIKE :query OR title LIKE :query",
                      {"query": f"%{query}%"}).fetchall()

    # Pass the search results to the Books page
    return books(rows)


@app.route("/books")
@login_required
def books(books):
    """Renders search results table"""

    # Check for search results
    if not books:
        flash("No matches")
        return redirect("/")

    return render_template("books.html", books=books)


@app.route("/books/<int:book_id>")
@login_required
def book_details(book_id):
    """Renders book details page"""

    # Select title, author, year, isbn by id from DB
    book_data = db.execute("SELECT * FROM books WHERE id = :book", {"book": book_id}).fetchone()

    # Select all reviews for current book by id from DB
    reviews = db.execute("SELECT rating, text, username, created_at FROM reviews"
                         " JOIN users ON user_id = users.id"
                         " WHERE book_id = :book"
                         " ORDER BY created_at DESC", {"book": book_id}).fetchall()

    # Select rating statistics from Goodreads by API request
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "2A54tMXDl9TuSbjhadZGqg", "isbns": book_data.isbn}).json()
    rating = {"average": res["books"][0]["average_rating"], "count": res["books"][0]["ratings_count"]}

    return render_template("book.html", book=book_data, rating=rating, reviews=reviews)


@app.route("/submit_review", methods=["POST"])
@login_required
def submit_review():
    """Writes review to the DB"""

    # Memorize inputs for comfort
    rating = request.form.get("rating")
    review = request.form.get("review")
    book_id = request.form.get("id")

    # Check for inputs
    if not rating:
        flash("Please, choose rating", category="error")
        return book_details(book_id)

    if not db.execute("SELECT * FROM books WHERE id = :book", {"book": book_id}):
        flash("No such book found in database", category="error")
        return redirect("/")

    # Check if there already exists review for this book from current user
    if db.execute("SELECT * FROM reviews WHERE book_id = :book AND user_id = :user",
                  {"book": book_id, "user": session["user_id"]}).rowcount != 0:
        flash("You've submitted a review for this book before!", category="error")
        return book_details(book_id)

    # Insert review to DB if all checks were passed
    db.execute("INSERT INTO reviews (rating, text, book_id, user_id) VALUES (:rating, :text, :book, :user)",
              {"rating": rating, "text": review, "book": book_id, "user": session["user_id"]})
    db.commit()

    flash("Thanks for your opinion!", category="success")
    return book_details(book_id)


@app.route("/api/<isbn>")
def api_book_info(isbn):
    """API method to get book data by ISBN"""

    # Search for a book by ISBN in DB
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    # Return 404 error with JSON if no match
    if not book:
        return jsonify({"error": "No such book in database"}), 404

    # Get ratings statistics from Goodreads by API request
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "2A54tMXDl9TuSbjhadZGqg", "isbns": book.isbn}).json()
    rating = {"average": res["books"][0]["average_rating"], "count": res["books"][0]["ratings_count"]}

    # Return JSON
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": rating["count"],
        "average_score": rating["average"]
    })
