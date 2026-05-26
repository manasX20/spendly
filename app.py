import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Name is required.", name=name, email=email)
    if not email:
        return render_template("register.html", error="Email is required.", name=name, email=email)
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)

    try:
        user_id = create_user(name, email, password)
    except sqlite3.IntegrityError:
        return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

    session["user_id"] = user_id
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.", email=email)

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "January 2026",
    }

    stats = {
        "total_spent": 313.25,
        "transaction_count": 8,
        "top_category": "Bills",
    }

    transactions = [
        {"date": "2026-05-18", "description": "Lunch with friend",  "category": "Food",          "amount": 22.00},
        {"date": "2026-05-15", "description": "Miscellaneous",      "category": "Other",         "amount": 8.75},
        {"date": "2026-05-13", "description": "New shoes",          "category": "Shopping",      "amount": 60.00},
        {"date": "2026-05-10", "description": "Movie ticket",       "category": "Entertainment", "amount": 15.00},
        {"date": "2026-05-08", "description": "Pharmacy",           "category": "Health",        "amount": 30.00},
        {"date": "2026-05-05", "description": "Electricity bill",   "category": "Bills",         "amount": 120.00},
        {"date": "2026-05-03", "description": "Monthly bus pass",   "category": "Transport",     "amount": 45.00},
        {"date": "2026-05-01", "description": "Grocery run",        "category": "Food",          "amount": 12.50},
    ]

    categories = [
        {"name": "Bills",         "total": 120.00, "percent": 38},
        {"name": "Shopping",      "total": 60.00,  "percent": 19},
        {"name": "Transport",     "total": 45.00,  "percent": 14},
        {"name": "Food",          "total": 34.50,  "percent": 11},
        {"name": "Health",        "total": 30.00,  "percent": 10},
        {"name": "Entertainment", "total": 15.00,  "percent": 5},
        {"name": "Other",         "total": 8.75,   "percent": 3},
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
