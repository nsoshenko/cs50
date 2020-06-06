import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    results = []

    # Get the data from DB
    symbols = db.execute("SELECT symbol, SUM(amount) FROM purchases WHERE user_id = :user AND symbol != '-' GROUP BY symbol HAVING SUM(amount) > 0", user=session["user_id"])
    user_info = db.execute("SELECT username, cash FROM users WHERE id = :user", user=session["user_id"])[0]
    username = user_info["username"]
    balance = user_info["cash"]

    # Prepare data for the table
    for i in range(len(symbols)):
        response = lookup(symbols[i]["symbol"])
        amount = symbols[i]["SUM(amount)"]
        total = round(amount * response["price"], 2)
        balance += total # add stocks value to cash balance
        temp = {"id": i+1, "name": response["name"], "symbol": response["symbol"], "amount": amount, "price": response["price"], "total": total}
        results.append(temp)

    return render_template("channels.html", results=results, username=username, balance=balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        elif not request.form.get("shares"):
            return apology("must provide number of shares", 403)

        else:
            symbol = request.form.get("symbol").upper()
            shares = int(request.form.get("shares").split(".")[0])
            if shares <= 0:
                return apology("number of shares should be positive", 403)

        response = lookup(symbol)

        if not response:
            return apology("no such symbol in database", 403)

        user_balance = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]["cash"]

        if (shares * response["price"]) > user_balance:
            return apology("insufficient balance", 403)
        else:
            # Perform purchase transaction
            backup_balance = user_balance
            user_balance -= shares * response["price"]
            db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=user_balance, user=session["user_id"])
            purchase_success = db.execute("INSERT INTO purchases (user_id, symbol, price, amount) VALUES (?,?,?,?)",
            session["user_id"], symbol, response["price"], shares)

            if not purchase_success:
                db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=backup_balance, user=session["user_id"])
                return apology("oops, something went wrong", 403)

        flash("Successful purchase!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    results = []

    # Get the data from DB
    response = db.execute("SELECT * FROM purchases WHERE user_id = :user", user=session["user_id"])

    # Prerape data for the table
    for transaction in response:
        type = None
        if transaction["amount"] < 0:
            type = "Sell"
        elif transaction["symbol"] == "-":
            type = "Deposit"
        else:
            type = "Buy"
        temp = {"id": transaction["id"], "type": type, "symbol": transaction["symbol"], "amount": transaction["amount"],
        "price": transaction["price"], "time" : transaction["created_at"]}
        results.append(temp)

    return render_template("history.html", results=results)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        response = lookup(request.form.get("symbol"))
        if response:
            return render_template("quoted.html", name=response["name"], price=response["price"])
        else:
            return apology("no such symbol in database", 403)

    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")

        if not username:
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords don't match", 403)

        # Check for existing username in DB
        elif db.execute("SELECT * FROM users WHERE username = :username", username=username):
            return apology("this username already exists", 403)

        else:
            register = db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
            username, generate_password_hash(request.form.get("password")))
            if not register:
                return apology("oops, something went wrong", 403)
            else:
                session.clear()
                session["user_id"] = register
            flash("Registered successfully!")
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must choose symbol", 403)

        elif not request.form.get("shares"):
            return apology("must provide number of shares", 403)

        else:
            symbol = request.form.get("symbol")
            shares = int(request.form.get("shares").split(".")[0])
            if shares <= 0:
                return apology("number of shares should be positive", 403)

            # Check how many stocks of provided symbol does user own
            available = db.execute("SELECT SUM(amount) FROM purchases WHERE user_id = :user AND symbol = :symbol",
            user=session["user_id"], symbol=symbol)[0]["SUM(amount)"]
            if not available or shares > available:
                return apology("you haven't as many available stocks", 403)

            # Lookup for the current stock data
            response = lookup(symbol)
            if not response:
                return apology("no such symbol in database", 403)

            # Perform selling transaction
            user_balance = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]["cash"]
            backup_balance = user_balance
            user_balance += shares * response["price"]
            db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=user_balance, user=session["user_id"])
            sell_success = db.execute("INSERT INTO purchases (user_id, symbol, price, amount) VALUES (?,?,?,?)",
            session["user_id"], symbol, response["price"], -shares)

            if not sell_success:
                db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=backup_balance, user=session["user_id"])
                return apology("oops, something went wrong", 403)

            flash("Succesfull selling!")
            return redirect("/")

    else:
        # Check which stocks does user own
        response = db.execute("SELECT symbol, SUM(amount) FROM purchases WHERE user_id = :user AND symbol != '-' GROUP BY symbol HAVING SUM(amount) > 0", user=session["user_id"])
        if not response:
            return apology("you have nothing to sell", 403)

        else:
            results = []
            for symbol in response:
                results.append(symbol["symbol"])

        return render_template("sell.html", results=results)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Add cash to user's balance"""
    if request.method == "POST":

        if not request.form.get("amount"):
            return apology("must enter amount to deposit", 403)
        else:
            deposit = int(request.form.get("amount").split(".")[0])
            if deposit <= 0:
                return apology("deposit must be a positive number", 403)

        user_balance = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]["cash"]
        backup_balance = user_balance
        user_balance += deposit
        db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=user_balance, user=session["user_id"])
        deposit_success = db.execute("INSERT INTO purchases (user_id, symbol, price, amount) VALUES (?,?,?,?)",
            session["user_id"], "-", deposit, 1)

        if not deposit_success:
            db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash=backup_balance, user=session["user_id"])
            return apology("oops, something went wrong", 403)

        flash("Succesfull deposit!")
        return redirect("/")

    else:
        return render_template("deposit.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change password"""
    if request.method == "POST":

        old_password = request.form.get("oldPassword")

        if not old_password:
            return apology("must provide old password", 403)

        elif not request.form.get("newPassword"):
            return apology("must provide new password", 403)

        elif not request.form.get("newPassword") == request.form.get("confirmation"):
            return apology("new passwords don't match", 403)

        check = db.execute("SELECT hash FROM users WHERE id = :user", user=session["user_id"])[0]["hash"]
        if not check_password_hash(check, old_password):
            return apology("invalid current password", 403)

        update_password = db.execute("UPDATE users SET hash = :new_password WHERE id = :user",
        new_password=generate_password_hash(request.form.get("newPassword")), user=session["user_id"])
        if not update_password:
            return apology("oops, something went wrong", 403)

        flash("Password is changed!")
        return redirect("/")

    else:
        return render_template("change_password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
