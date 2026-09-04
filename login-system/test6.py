from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps
import os

app=Flask(__name__)

app.secret_key="govr_poly"

print("Current folder:", os.getcwd())
print("Database path:", os.path.abspath("users.db"))

@app.route("/")
def home():
    return render_template(
        "index.html",
        logged_in=('username' in session),
        username=session.get('username')
    )

class User:
    def __init__(self,id, username, password_hash):
        self.id=id
        self.username=username
        self.password_hash=password_hash
    
    @classmethod
    def from_row(cls, row):
        return cls(row[0],row[1],row[2])

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def get_connection():
        return sqlite3.connect("users.db")

    @property
    def display_name(self):
        return self.username.capitalize()

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        hash_password=User.hash_password(password)

        conn=User.get_connection()
        try: 
            cursor=conn.cursor()
            cursor.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", (username, hash_password))

            conn.commit()

            #create session after registration
            session["username"]=username
            session.permanent=True
            return redirect(url_for("dashboard"))

        except sqlite3.IntegrityError as e:
            return render_template("register.html", error="Username already exists. Please choose another username.")

        finally: 
            conn.close()

    return render_template("register.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        conn=User.get_connection()
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        conn.close()

        if user:
            user=User.from_row(user)

            if(user.check_password(password)):
                session['username']=user.username
                session.permanent=True

                return redirect(url_for("dashboard"))
            else:
                return render_template("login.html", error="Invalid password")
        else:
            return render_template("login.html", error="User not found")
    return render_template("login.html")

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        else:
            result=func(*args, **kwargs)
            return result
    return wrapper

@app.route("/dashboard")
@login_required
def dashboard():
    username = session["username"]

    conn=User.get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username =?", (username,))
    row=cursor.fetchone()

    conn.close()

    user=User.from_row(row)

    return render_template("dashboard.html", username=user.display_name)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")
    
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)