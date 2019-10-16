import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, request

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = "DATABASE_URL"
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    # validate method
    if request.method == "POST":

        # validate inputs
        name = request.form.get("name")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        if not request.form.get("name"):
            return "Please enter your name"
        if not request.form.get("password"):
            return "Please enter your password."
        if request.form.get("password") != request.form.get("confirmpassword"):
                return "Passwords do not match."

        user_exists = db.execute("SELECT * FROM users WHERE username = :username", {'username': name}).fetchall()
        if user_exists:
            return "You are already registered."
            #add user to database
        else:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": name, "password": password})
            db.commit()
            return render_template('register.html')
    else:
        return "Method Not Allowed. Please submit form."

@app.route("/login", methods=["POST"])
def login():
    session.clear()
    # validate form inputs
    username = request.form.get("username")
    if username == "":
        return "please enter your name."
    password = request.form.get("password")
    if password == "":
        return "Please enter your password."


    # validate user is registered
    user_exists = db.execute("SELECT username, password FROM users WHERE username=:username AND password=:password",
    {'username':username, 'password':password})
    user = db.execute("Select * From users WHERE username=:username", {'username':username})
    db.commit()
    session[id] = user[0]['id']

    if user_exists:
        return render_template("search.html")
    else:
        return "Password not recognized. Try again or register for an account."

    # if all else fails
    return "Something went wrong."

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    return render_template('search.html')
