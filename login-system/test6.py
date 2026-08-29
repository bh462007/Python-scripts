from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        hash_password=generate_password_hash(password)

        try: 
            conn=sqlite3.connect("users.db")
            cursor=conn.cursor()

            cursor.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", (username, hash_password))

            conn.commit()

            return "registration done successfully"

        except sqlite3.IntegrityError as e:
            return f"failed: {e}"

        finally: 
            conn.close()

        

    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)