from flask import Flask, render_template, session, url_for, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime
import sqlite3
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("register.html")


# ---------------- USER CLASS ----------------

class User:

    def __init__(self, user_id, username, password_hash):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get_connection():
        db_path = os.path.abspath("users.db")
        print("DATABASE:", db_path)
        return sqlite3.connect("users.db")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create_user(cls, username, password):

        password_hash = generate_password_hash(password)

        with cls.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )

            conn.commit()

            user_id = cursor.lastrowid

        return cls(user_id, username, password_hash)

    @classmethod
    def find_by_username(cls, username):

        with cls.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )

            row = cursor.fetchone()

        if row:
            return cls(row[0], row[1], row[2])

        return None

    @classmethod
    def find_by_id(cls, user_id):

        with cls.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM users WHERE id = ?",
                (user_id,)
            )

            row = cursor.fetchone()

        if row:
            return cls(row[0], row[1], row[2])

        return None

    @classmethod
    def update_password(cls, username, new_password):

        new_password_hash = generate_password_hash(new_password)

        with cls.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (new_password_hash, username)
            )

            conn.commit()


# ---------------- TASK CLASS ----------------

class Task:

    @staticmethod
    def get_connection():
        return sqlite3.connect("users.db")

    @classmethod
    def add_task(cls, user_id, task_name, description, start, end, priority):

        with cls.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO tasks
                (task_name, description, start, end, priority, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (task_name, description, start, end, priority, user_id)
            )

            conn.commit()

    @classmethod
    def get_tasks(cls, user_id, status=None, priority=None):

        query = "SELECT * FROM tasks WHERE user_id = ?"
        params = [user_id]

        if status is not None:
            query += " AND status = ?"
            params.append(status)

        if priority is not None:
            query += " AND priority = ?"
            params.append(priority)

        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

        return rows

    @classmethod
    def get_task(cls, task_id, user_id):

        with cls.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM tasks WHERE user_id = ? AND task_id = ?",
                (user_id, task_id)
            )

            row = cursor.fetchone()

        return row

    @classmethod
    def remove_task(cls, task_id, user_id):

        with cls.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM tasks WHERE task_id = ? AND user_id = ?",
                (task_id, user_id)
            )

            conn.commit()

    @classmethod
    def update_task(cls, task_id, user_id, **fields):

        allowed_fields = {
            "task_name",
            "description",
            "start",
            "end",
            "priority"
        }

        fields = {
            key: value
            for key, value in fields.items()
            if key in allowed_fields
        }

        if not fields:
            return

        set_clause = ", ".join(
            field + " = ?" for field in fields
        )

        params = list(fields.values())
        params.extend([task_id, user_id])

        query = f"""
            UPDATE tasks
            SET {set_clause}
            WHERE task_id = ? AND user_id = ?
        """

        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    @classmethod
    def task_exists(cls, user_id, task_name):

        with cls.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT 1
                FROM tasks
                WHERE user_id = ? AND task_name = ?
                LIMIT 1
                """,
                (user_id, task_name)
            )

            return cursor.fetchone() is not None


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username or password cannot be empty")
            return redirect(url_for("register"))

        if password != password.strip():
            flash("Password cannot start or end with space")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters")
            return redirect(url_for("register"))

        try:

            user = User.create_user(username, password)

            session["user_id"] = user.user_id
            session.permanent = True

            return redirect(url_for("dashboard"))

        except sqlite3.IntegrityError:

            flash("User already exists, choose another name")
            return redirect(url_for("register"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password cannot be empty")
            return redirect(url_for("login"))

        if password != password.strip():
            flash("Password cannot start or end with space")
            return redirect(url_for("login"))

        user = User.find_by_username(username)

        if user and user.check_password(password):

            session["user_id"] = user.user_id
            session.permanent = True

            return redirect(url_for("dashboard"))

        flash("Invalid username or password")
        return redirect(url_for("login"))

    return render_template("login.html")


# ---------------- LOGIN REQUIRED DECORATOR ----------------

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not session.get("user_id"):
            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
@login_required
def dashboard():

    user = User.find_by_id(session["user_id"])

    if user is None:

        session.clear()

        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=user.username
    )


# ---------------- PROFILE ----------------

@app.route("/profile")
@login_required
def profile():

    user = User.find_by_id(session["user_id"])

    if user is None:

        session.clear()

        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        username=user.username,
        user_id=user.user_id
    )


# ---------------- CHANGE PASSWORD ----------------

@app.route("/change_password", methods=["POST"])
@login_required
def change_password():

    old_password = request.form.get("password", "")
    new_password = request.form.get("new-password", "")
    confirm_password = request.form.get("check-new-password", "")

    if not old_password or not new_password or not confirm_password:

        flash("All fields are required")

        return redirect(url_for("profile"))

    user = User.find_by_id(session["user_id"])

    if user is None:

        session.clear()

        return redirect(url_for("login"))

    if not user.check_password(old_password):

        flash("Old password is incorrect")

        return redirect(url_for("profile"))

    if new_password != new_password.strip():

        flash("New password cannot start or end with space")

        return redirect(url_for("profile"))

    if new_password != confirm_password:

        flash("New passwords do not match")

        return redirect(url_for("profile"))

    if len(new_password) < 6:

        flash("New password must be at least 6 characters")

        return redirect(url_for("profile"))

    User.update_password(user.username, new_password)

    flash("Password updated successfully")

    return redirect(url_for("profile"))


# ---------------- TASKS ----------------

@app.route("/tasks")
@login_required
def tasks():

    user_id = session["user_id"]

    tasks = Task.get_tasks(user_id)

    print("USER ID:", user_id)
    print("TASKS:", tasks)

    return render_template(
        "tasks.html",
        tasks=tasks
    )


# ---------------- ADD TASK ----------------

@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():

    user_id = session["user_id"]

    if request.method == "POST":

        task_name = request.form.get("task_name", "").strip()
        description = request.form.get("description", "").strip()
        start = request.form.get("start", "")
        end = request.form.get("end", "")
        priority = request.form.get("priority", "")

        allowed_priorities = {"Low", "Medium", "High"}

        # Task name validation

        if not task_name:

            flash("Task must have a name")

            return redirect(url_for("add_task"))

        if Task.task_exists(user_id, task_name):

            flash("A task with this name already exists!")

            return redirect(url_for("dashboard"))

        if len(task_name) > 100:

            flash("Task name must be less than 100 characters")

            return redirect(url_for("add_task"))

        # Description validation

        if len(description) > 1000:

            flash("Description is too long")

            return redirect(url_for("add_task"))

        # Start validation

        if not start:

            flash("Start date and time are required")

            return redirect(url_for("add_task"))

        # End validation

        if not end:

            flash("End date and time are required")

            return redirect(url_for("add_task"))

        # Priority validation

        if priority not in allowed_priorities:

            flash("Invalid priority")

            return redirect(url_for("add_task"))

        # Convert dates

        try:

            start_time = datetime.strptime(
                start,
                "%Y-%m-%dT%H:%M"
            )

            end_time = datetime.strptime(
                end,
                "%Y-%m-%dT%H:%M"
            )

        except ValueError:

            flash("Invalid date or time")

            return redirect(url_for("add_task"))

        # End must be after start

        if end_time <= start_time:

            flash(
                "Oops! Please make sure your end time comes after your start time"
            )

            return redirect(url_for("add_task"))

        Task.add_task(
            user_id,
            task_name,
            description,
            start,
            end,
            priority
        )

        flash("Task added successfully!")

        return redirect(url_for("tasks"))

    return render_template("add_task.html")


# ---------------- EDIT TASK ----------------

@app.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):

    user_id = session["user_id"]

    current_task = Task.get_task(task_id, user_id)

    if current_task is None:

        flash("Task does not exist")

        return redirect(url_for("tasks"))

    if request.method == "POST":

        task_name = request.form.get("task_name", "").strip()
        description = request.form.get("description", "").strip()
        start = request.form.get("start", "").strip()
        end = request.form.get("end", "").strip()
        priority = request.form.get("priority", "").strip()

        # Validation

        if not task_name:

            flash("Task name is required")

            return render_template(
                "edit_task.html",
                task=current_task
            )

        if len(description) > 1000:

            flash("Description must be 1000 characters or less")

            return render_template(
                "edit_task.html",
                task=current_task
            )

        if not start or not end:

            flash("Start and end time are required")

            return render_template(
                "edit_task.html",
                task=current_task
            )

        if priority not in ["Low", "Medium", "High"]:

            flash("Invalid priority")

            return render_template(
                "edit_task.html",
                task=current_task
            )

        try:

            start_datetime = datetime.strptime(
                start,
                "%Y-%m-%dT%H:%M"
            )

            end_datetime = datetime.strptime(
                end,
                "%Y-%m-%dT%H:%M"
            )

        except ValueError:

            flash("Invalid date/time format")

            return render_template(
                "edit_task.html",
                task=current_task
            )

        if end_datetime <= start_datetime:

            flash("End time must be after start time")

            return render_template(
                "edit_task.html",
                task=current_task
            )

        Task.update_task(
            task_id,
            user_id,
            task_name=task_name,
            description=description,
            start=start,
            end=end,
            priority=priority
        )

        flash("Task updated successfully")

        return redirect(url_for("tasks"))

    return render_template(
        "edit_task.html",
        task=current_task
    )


# ---------------- DELETE TASK ----------------

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):

    user_id = session["user_id"]

    Task.remove_task(task_id, user_id)

    flash("Task deleted successfully")

    return redirect(url_for("tasks"))


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)