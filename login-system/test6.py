from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

import os

app=Flask(__name__)

app.secret_key="abc"

print("Current folder:", os.getcwd())
print("Database path:", os.path.abspath("users.db"))

@app.route("/")
def home():
    return render_template(
        "index.html",
        logged_in=('username' in session),
        username=session.get('username')
    )

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        hash_password=generate_password_hash(password)

        conn=sqlite3.connect("users.db")

        try: 
            
            cursor=conn.cursor()

            cursor.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", (username, hash_password))

            conn.commit()

            return "registration done successfully"

        except sqlite3.IntegrityError as e:
            return f"failed: {e}"

        finally: 
            conn.close()

    return render_template("register.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        conn=sqlite3.connect("users.db")
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        conn.close()

        if user:
            stored_hash=user[2]

            if(check_password_hash(stored_hash, password)):
                session['username']=username
                session.permanent=True

                return redirect(url_for('home'))
            else:
                return "Invalid password"
            
        else:
            return "user not found"

        

    return render_template("login.html")
        
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)