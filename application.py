import cs50
import csv
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, json, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from helpers import apology, signin_required


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
db = SQL("sqlite:///taper_journey.db")


@app.route("/")
@signin_required
def index():

    # if user has not yet logged any drugs render taper page
    if not db.execute("SELECT * FROM entries WHERE user_id=?", session["user_id"]):
        return redirect ("/taper")
    else:
        #initialise summary
        summary = [];
        # get a list of all the drugs that the user is tracking
        row_drugs = db.execute("SELECT DISTINCT drug FROM entries WHERE user_id=?", session["user_id"])
        drugs = []
        for row in row_drugs:
            drugs.append(row["drug"])
        print(f"list of drugs: {drugs}")
        for d in drugs:
            row_drugEntries = db.execute("SELECT * FROM entries WHERE drug =? AND user_id =? ORDER BY entry_date DESC", (d, session["user_id"]))
            latest_entry=row_drugEntries[0]
            summary.append(latest_entry)
        return render_template("home.html", summary=summary)


@app.route("/signin", methods=["GET", "POST"])
def signin():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Validate input
        if not request.form.get("username"):
            return apology("No username entered", 400)
        if not request.form.get("password"):
            return apology("No password entered", 400)

       # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        print("You are in the get signin route")
        return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        usernameinput = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        #--> Validate input
        if not usernameinput:
            return apology("No username entered", 400)
        #if not email:
            return apology("No email entered", 400)
        if not password:
            return apology("No password entered", 400)

        #--> hash the password

        passwordHash = generate_password_hash(request.form.get("password", "sha256"))

        # Query database to check that the username is not already taken and insert into database if not
        if db.execute("SELECT username FROM users WHERE username = ?", (usernameinput)):
            return apology("The username is not available")
        else:
            db.execute("INSERT INTO users (id, username, email, hash) VALUES (NULL, ?, ?, ?)", ( usernameinput,email,passwordHash))
            return redirect("/signin")

    else:
        return render_template("signup.html")

@app.route("/taper", methods=["GET", "POST"])
@signin_required
def taper():
    if request.method == "POST":
        return apology("TODO", 400)
    else:
        return render_template("taper.html")

@app.route("/posttaperdata", methods=["POST"])
@signin_required
def posttaperdata():

    # capture data
    user_id = session["user_id"]

    #parse the date
    dateFormatted = request.form.get("date")
    date = datetime.strptime(dateFormatted, "%A, %d %b %Y").strftime("%Y-%m-%d")
    drug = request.form.get('drug')
    dose = request.form.get('dose')
    mood = request.form.get("mood")
    side_effects = request.form.get("side_effects")
    journal = request.form.get("journal")

    #--> Validate input
    if not drug:
        return apology("No dose chosen", 400)
    if not dose:
        return apology("No dose chosen", 400)
    if not mood:
        return apology("No mood specified", 400)
    if not side_effects:
        side_effects = "NULL"
    if not journal:
        journal = "NULL"

    # insert data into entries table / capture taper entry
    # If date already contains entries then the user is editing an existing entry
    if db.execute("SELECT * FROM entries WHERE entry_date = ? AND user_id= ?", (date, session["user_id"])):
        db.execute("UPDATE entries SET  drug=?, dose=?, mood=?,side_effects =?  WHERE entry_date = ? AND user_id = ?", (drug, dose, mood, side_effects, date, session["user_id"]))
        return redirect ("/")
    else:
        db.execute("INSERT INTO entries (id, drug, dose, mood,side_effects, user_id, entry_date) VALUES (NULL, ?, ?, ?,?,?,?)",( drug,dose,mood,side_effects, session["user_id"], date))
        return redirect ("/")

@app.route("/gettaperdata", methods=["POST"])
@signin_required
def gettaperdata():
    # data to be populated
    print(f"{request.form.get('date')}")
    dateHTML = request.form.get("date")
    dateSQL = datetime.strptime(dateHTML, "%A, %d %b %Y").strftime("%Y-%m-%d")

    row = db.execute("SELECT * FROM entries WHERE user_id = ? AND entry_date = ?", (session["user_id"], dateSQL))
    if not row:
        data = {"drug": "None", "dose": "", "mood": "", "side_effects": "", "date": dateHTML}
    else:
        drug = row[0]["drug"]
        dose = row[0]["dose"]
        mood = row[0]["mood"]
        if row[0]["side_effects"] == "NULL":
            side_effects = ""
        else:
            side_effects = row[0]["side_effects"]
        if row[0]["journal"] == "NULL":
            journal = ""
        else:
            journal = row[0]["journal"]
        data= {"drug": drug, "dose": dose, "mood": mood, "side_effects": side_effects, "date": dateHTML}
        print(f"{data}")
    return data

@app.route("/postjournal", methods=["POST"])
@signin_required
def postjournal():

     # data to be populated
    journal = request.form.get("journal")
    dateHTML = request.form.get("date")
    dateSQL = datetime.strptime(dateHTML, "%A, %d %b %Y").strftime("%Y-%m-%d")

    #check if th entry already exists, if it does make a update otherwise insert it into the existing database
    if not db.execute("SELECT * FROM journals WHERE user_id = ? AND entry_date = ?", (session["user_id"], dateSQL)):
        db.execute("INSERT INTO journals (journal_entry, user_id, entry_date) VALUES (?, ?, ?)", (journal, session["user_id"], dateSQL))
    else:
        db.execute("UPDATE journals SET journal_entry=?, user_id=?, entry_date = ?", (journal, session["user_id"], dateSQL))
    return redirect("/")

@app.route("/getjournal", methods=["POST"])
@signin_required
def getjournal():

    # get the date for which a journal entry is requested
    dateHTML = request.form.get("date")
    dateSQL = datetime.strptime(dateHTML, "%A, %d %b %Y").strftime("%Y-%m-%d")

    # check if there is a journal entry for this date
    if not db.execute("SELECT * FROM journals WHERE entry_date = ? AND user_id = ?", (dateSQL, session["user_id"])):
        return {"journal" : ""}
    else:
        print("YOu are in the route")
        row = db.execute("SELECT * FROM journals WHERE entry_date = ? AND user_id = ?", (dateSQL, session["user_id"]))
        return {"journal" : row[0]["journal_entry"]}








@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/signin")
