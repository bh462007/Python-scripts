from flask import Flask, render_template, session, url_for, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from functools import wraps
import sqlite3
import os
load_dotenv()

app =Flask(__name__)

app.secret_key=os.environ.get("FLASK_SECRET_KEY")

@app.route("/")
def home():
    return render_template("register.html")


class User:
    
    def __init__(self,user_id, username, password_hash):
        self.user_id=user_id
        self.username=username
        self.password_hash=password_hash

    @staticmethod
    def get_connection():
        return sqlite3.connect("users.db")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_user(cls, username, password):
        password_hash=generate_password_hash(password)
        with cls.get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, password_hash))
            conn.commit()
            user_id=cursor.lastrowid
        return cls(user_id, username, password_hash)

    @classmethod
    def find_by_username(cls, username):
        with cls.get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            row=cursor.fetchone()
        if row:
            return cls(row[0], row[1], row[2])
        return None

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method =="POST":
        username=request.form.get("username","").strip()
        password=request.form.get("password","")

        #none textbox should be empty
        if not username or not password:
            flash("Username or password cannot be empty")
            return redirect(url_for("register"))
        
        #no space at start and end of the password
        if password!=password.strip():
            flash("Password cannot start and end with space")
            return redirect(url_for("register"))

        #length should be 6
        if len(password)<6:
            flash("Password must be atleast 6 characters")
            return redirect(url_for("register"))

        try:
            user=User.create_user(username, password)

            session['username']=username
            session.permanent=True
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("User already exists, choose another name")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        username=request.form.get("username","").strip()
        password=request.form.get("password","")

        #username and password should not be empty
        if not username or not password:
            flash("Username and password can not be empty")
            return redirect(url_for("login"))

        #password should not start and end with space
        if password!=password.strip():
            flash("Password can not start and end with space")
            return redirect(url_for("login"))

        #password must be of minimum 6 len
        if len(password)<6:
            flash("Password must be of minimum 6 characters")
            return redirect(url_for("login"))
        
        user=User.find_by_username(username)

        if user:
            if user.check_password(password):
                session['username']=user.username
                session.permanent=True
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid password")
                return redirect(url_for("login"))
        else:
            flash("User nto found")
            return redirect(url_for("login"))
    
    return render_template("login.html")

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not session.get("username"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


@app.route("/dashboard")
@login_required
def dashboard():
    user=User.find_by_username(session['username'])
    if user is None:
        session.pop("username", None)
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=user.username)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

if __name__ =="__main__":
    app.run(debug=True)
