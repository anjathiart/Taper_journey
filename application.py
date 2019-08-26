import cs50
import csv
from datetime import datetime, date

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

        #initialise drugInfo for day | date | object: drug, dose | mood |journal
        drugInfo = [];
        # get the info for the latest entry date
        row = db.execute("SELECT * FROM entries WHERE user_id=? ORDER BY entry_date DESC", session["user_id"])
        dateHTML = datetime.strptime(row[0]["entry_date"], "%Y-%m-%d").strftime("%A, %d %b %Y")
        print(f"{row}")
        if row[0]["drugs"] != "NULL":
            drugs = row[0]["drugs"].split(",")
            doses = row[0]["doses"].split(",")
        side_effects = row[0]["side_effects"]
        mood = row[0]["mood"]
        journal = row[0]["journal"]

        print(f"list of drugs: {drugs}")
        for i in range(len(drugs)):
            drugEntry = {"drug":  drugs[i], "dose": doses[i]}
            print(f"{drugEntry}")
            drugInfo.append(drugEntry)
        print(f"{drugInfo}")
        data = {"date": dateHTML, "drugInfo": drugInfo, "mood": mood, "side_effedts": side_effects, "journal": journal }
        return render_template("home.html", data=data)


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
        drug_options = ["Cymbalta", "Epitec", "Abilify", "Ivedel"]
        side_effect_options = ["Fatigue", "Nausea", "Headache", "Weigt-gain", "Weight-los", "Mania", "Insomnia"]
        pageData = {"drug_options": drug_options, "side_effect_options": side_effect_options}
        return render_template("taper.html", pageData = pageData)
    else:
        drug_options = ["Cymbalta","Epitec","Abilify","Ivedel"]
        side_effect_options = ["Fatigue","Nausea","Headache","Weigt-gain","Weight-los","Mania","Insomnia"]
        pageData = {"drug_options": drug_options, "side_effect_options": side_effect_options}
        print(f"{pageData}")
        return render_template("taper.html", pageData = pageData)

@app.route("/posttaperdata", methods=["POST"])
@signin_required
def posttaperdata():

    # capture data
    user_id = session["user_id"]

    #parse the date
    dateFormatted = request.form.get("date")
    date = datetime.strptime(dateFormatted, "%A, %d %b %Y").strftime("%Y-%m-%d")

    drugs = request.form.get('drugs')
    doses = request.form.get('doses')
    mood = request.form.get("mood")
    journal = request.form.get("journal")
    side_effects = request.form.get("side_effects")

    #--> Validate input
    if not drugs:
        return apology("No dose chosen", 400)
    if not doses:
        return apology("No dose chosen", 400)
    if not mood:
        return apology("No mood specified", 400)
    if not side_effects:
        side_effects = "NULL"

    # insert data into entries table / capture taper entry
    # If date already contains entries then the user is editing an existing entry
    if db.execute("SELECT * FROM entries WHERE entry_date = ? AND user_id= ?", (date, session["user_id"])):
        db.execute("UPDATE entries SET  drugs=?, doses=?, mood=?,side_effects =?, journal=?  WHERE entry_date = ? AND user_id = ?", (drugs, doses, mood, side_effects, journal,  date, session["user_id"]))
        return redirect ("/")
    else:
        db.execute("INSERT INTO entries (id, drugs, doses, mood,side_effects, user_id, entry_date , journal) VALUES (NULL, ?, ?, ?,?,?,?, ?)",( drugs,doses,mood,side_effects, session["user_id"], date, journal))
        return redirect ("/")

# Sends the taper data for a specific date to the front end
@app.route("/gettaperdata", methods=["POST"])
@signin_required
def gettaperdata():

    # data to be populated
    dateHTML = request.form.get("date")
    dateSQL = datetime.strptime(dateHTML, "%A, %d %b %Y").strftime("%Y-%m-%d")

    row = db.execute("SELECT * FROM entries WHERE user_id = ? AND entry_date = ?", (session["user_id"], dateSQL))
    latest_drugs = ""
    latest_doses = ""
    if not row:
        row = db.execute("SELECT * FROM entries WHERE user_id= ? AND drugs IS NOT NULL AND entry_date <= ? ORDER BY entry_date DESC", (session["user_id"], dateSQL))
        if not row:
            latest_drugs = "None"
            latest_doses = "None"
        else:
            latest_drugs = row[0]["drugs"]
            latest_doses = row[0]["doses"]
        data = {"drugs": "None", "doses": "", "mood": "", "side_effects": "", "date": dateHTML, "journal": "", "latest_drugs": latest_drugs,"latest_doses": latest_doses }
    else:
        drugs = row[0]["drugs"]
        doses = row[0]["doses"]
        mood = row[0]["mood"]
        if row[0]["side_effects"] == "NULL":
            side_effects = ""
        else:
            side_effects = row[0]["side_effects"]
        if row[0]["journal"] == "NULL":
            journal = ""
        else:
            journal = row[0]["journal"]
        data= {"drugs": drugs, "doses": doses, "mood": mood, "side_effects": side_effects, "date": dateHTML, "journal": journal,"latest_drugs": drugs,"latest_doses": doses}
    return data



# get the latest list of drugs being tracked by the user and send to front end
@app.route("/getlatestdrugs", methods=["POST"])
@signin_required
def getlatestdrugs():

     # data to be populated
    dateHTML = request.form.get("date")
    dateSQL = datetime.strptime(dateHTML, "%A, %d %b %Y").strftime("%Y-%m-%d")


    row = db.execute("SELECT * FROM entries WHERE user_id= ? AND drugs IS NOT NULL AND entry_date <= ? ORDER BY entry_date DESC", (session["user_id"], dateSQL))
    if not row:
        data = "None"
    else:
        data = row[0]["drugs"]
    return data


@app.route("/postjournal", methods=["POST"])
@signin_required
def postjournal():

     # data to be populated
    journal = request.form.get("journal")
    dateHTML = request.form.get("date")
    dateSQL = datetime.strptime(dateHTML, "%A, %d %b %Y").strftime("%Y-%m-%d")

    #check if th entry already exists, if it does make a update otherwise insert it into the existing database
    if not db.execute("SELECT drugs, entry_date FROM journals WHERE user_id = ? AND entry_date = ?", (session["user_id"], dateSQL)):
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

    # check if there are journal entries
    if not db.execute("SELECT (journal, entry_date) FROM entries WHERE user_id = ? ORDER BY entry_date DESC", (session["user_id"])):
        return {"journal" : ""}
    else:
        row = db.execute("SELECT journal, entry_date FROM entries WHERE user_id = ? ORDER BY entry_date DESC", (session["user_id"]))
        return {"journal" : row[0]["journal"]}

@app.route("/getdrugoptionslist", methods=["POST"])
@signin_required
def getdrugoptionslist():
    return {"options": ["Cymbalta", "Epitec", "Abilify", "Ivedel"]}

@app.route("/getsideeffectslist", methods=["POST"])
@signin_required
def getsideefectslist():
    return ["Fatigue", "Nausea", "Headache", "Weigt-gain", "Weight-los", "Mania", "Insomnia"]


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/signin")
