import cs50
import csv
from datetime import date

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///taper_journal.db")

@app.route("/", methods=["GET"])
def get_index():
    if session.get('user_id'):
        return render_template("/home.html")
    else:
        return redirect("/welcome")

@app.route("/", methods=["GET"])
def index():
    if not session["user_id"]:
        return redirect("/signin")
    else:
        return render_template("home.html")


@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/signup", methods=["GET"])
def get_signup():
    return render_template("signup.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():

    # Forget any user_id
    session.clear()

    if request.method == "POST":


        # Validate input
        if not request.form.get("username"):
            return apology("No username entered", 403)
        if not request.form.get("password"):
            return apology("No password entered", 403)

       # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        #--> Validate input
        if not username:
            return apology("No username entered", 403)
        if not email:
            return apology("No email entered", 403)
        if not password:
            return apology("No password entered", 403)

        #--> hash the password
        passwordHash = generate_password_hash(request.form.get("password", "sha256"))

        # Query database to check that the username is not already taken and insert into database if not
        if db.execute("SELECT username FROM users WHERE username = ?", (username)):
            return apology("username already used", 403);
        else:
            db.execute("INSERT INTO users (id, username, email, hash) VALUES (NULL, ?, ?, ?)", ( username,email,passwordHash))
            return redirect("/signin")

    else:
        return render_template("signup.html")

@app.route("/taper", methods=["GET", "POST"])
def taper():

    if request.method == "POST":

        drug = request.form.get('drug')
        dose = request.form.get('dose')

        #--> Validate input
        if not drug:
            return apology("No drug chosen", 403)
        if not dose:
            return apology("No dose entered", 403)

        # Query medication to check that the username is not already taken and insert into database if not
        if db.execute("SELECT drug FROM taper_actions WHERE id = ?", (session['user_id'])):
            return apology("medication already registered", 403);
        else:
            db.execute("INSERT INTO taper_actions (id, drug, dose, mood) VALUES (NULL, ?, ?, ?)", ( drug,dose,mood))
            return apology("TODO")

    else:
        return render_template("taper.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
