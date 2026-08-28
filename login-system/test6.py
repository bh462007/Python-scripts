from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
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
        return f"got it {username} your password: {hash_password}"
    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)