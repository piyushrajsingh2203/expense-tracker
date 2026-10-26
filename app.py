import calendar
import os
import secrets
import smtplib
import sqlite3
from datetime import date, datetime, timedelta
from email.message import EmailMessage

from flask import Flask, g, session, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from jinja2 import DictLoader
from werkzeug.security import generate_password_hash, check_password_hash

import config
from templates import TEMPLATES

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expense.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE (user_id, name, type)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
    amount REAL NOT NULL CHECK (amount > 0),
    category_id INTEGER NOT NULL,
    txn_date TEXT NOT NULL,
    note TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- category_id NULL means overall monthly budget
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    category_id INTEGER,
    limit_amount REAL NOT NULL CHECK (limit_amount > 0),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE INDEX IF NOT EXISTS idx_txn_user_date ON transactions (user_id, txn_date);
CREATE INDEX IF NOT EXISTS idx_budget_user_month ON budgets (user_id, month);

CREATE TABLE IF NOT EXISTS password_resets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    otp_hash TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    attempts INTEGER DEFAULT 0,
    used INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

app = Flask(__name__)
app.jinja_loader = DictLoader(TEMPLATES)
app.config["SECRET_KEY"] = "change-this-to-any-long-random-text"


# ---------- database ----------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    # Creates tables only if they do not exist
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)

    # older databases may have password_resets without created_at
    cols = [r[1] for r in conn.execute("PRAGMA table_info(password_resets)")]
    if "created_at" not in cols:
        conn.execute("ALTER TABLE password_resets ADD COLUMN created_at TEXT")

    conn.commit()
    conn.close()


login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "warning"

# OTP settings, kept in config.py
OTP_MODE = getattr(config, "OTP_MODE", "terminal")
MAIL_USER = getattr(config, "MAIL_USER", "").strip()
MAIL_PASS = getattr(config, "MAIL_PASS", "").replace(" ", "")
OTP_VALID_MINUTES = 10
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_SECONDS = 60

DEFAULT_CATEGORIES = [
    ("Food", "expense"), ("Travel", "expense"), ("Shopping", "expense"),("Bills", "expense"), ("Health", "expense"), ("Education", "expense"),
    ("Entertainment", "expense"), ("Other", "expense"),("Salary", "income"), ("Pocket Money", "income"),("Freelance", "income"), ("Other", "income"),
]

class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]
        self.name = row["name"]
        self.email = row["email"]


@login_manager.user_loader
def load_user(user_id):
    row = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return User(row) if row else None


@app.template_filter("inr")
def inr(value):
    return "₹{:,.2f}".format(value or 0)


def current_month():
    return date.today().strftime("%Y-%m")


def valid_month(value):
    try:
        datetime.strptime(value, "%Y-%m")
        return value
    except (TypeError, ValueError):
        return current_month()


def valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def shift_month(month, offset):
    year, mon = map(int, month.split("-"))
    mon += offset
    while mon < 1:
        mon += 12
        year -= 1
    while mon > 12:
        mon -= 12
        year += 1
    return f"{year:04d}-{mon:02d}"


def month_label(month):
    return datetime.strptime(month, "%Y-%m").strftime("%b %Y")


def get_categories(txn_type=None):
    sql = "SELECT * FROM categories WHERE user_id = ?"
    params = [current_user.id]
    if txn_type:
        sql += " AND type = ?"
        params.append(txn_type)
    sql += " ORDER BY type, name"
    return get_db().execute(sql, params).fetchall()


def get_spent(user_id, month, category_id=None):
    sql = """SELECT COALESCE(SUM(amount), 0) FROM transactions
             WHERE user_id = ? AND type = 'expense'
             AND strftime('%Y-%m', txn_date) = ?"""
    params = [user_id, month]
    if category_id:
        sql += " AND category_id = ?"
        params.append(category_id)
    return get_db().execute(sql, params).fetchone()[0]


def get_budget_status(user_id, month):
    rows = get_db().execute("""
        SELECT b.id, b.category_id, b.limit_amount, c.name AS category_name
        FROM budgets b
        LEFT JOIN categories c ON c.id = b.category_id
        WHERE b.user_id = ? AND b.month = ?
        ORDER BY b.category_id IS NOT NULL, c.name
    """, (user_id, month)).fetchall()

    result = []
    for row in rows:
        spent = get_spent(user_id, month, row["category_id"])
        percent = spent / row["limit_amount"] * 100
        if percent >= 100:
            level = "danger"
        elif percent >= 80:
            level = "warning"
        else:
            level = "success"
        result.append({
            "id": row["id"],
            "category_id": row["category_id"],
            "name": row["category_name"] or "Overall",
            "limit": row["limit_amount"],
            "spent": spent,
            "left": row["limit_amount"] - spent,
            "percent": percent,
            "level": level,
        })
    return result


def check_budget_alerts(txn_date, category_id):
    month = txn_date[:7]
    for item in get_budget_status(current_user.id, month):
        # only overall budget and the budget of this category
        if item["category_id"] and str(item["category_id"]) != str(category_id):
            continue
        if item["level"] == "danger":
            flash(f"Budget crossed: {item['name']} is at {item['percent']:.0f}% "
                  f"({inr(item['spent'])} of {inr(item['limit'])}).", "danger")
        elif item["level"] == "warning":
            flash(f"Careful: {item['name']} budget is at {item['percent']:.0f}%. "
                  f"Only {inr(item['left'])} left.", "warning")


def read_txn_form():
    form = {
        "type": request.form.get("type", ""),
        "amount": request.form.get("amount", "").strip(),
        "category_id": request.form.get("category_id", ""),
        "txn_date": request.form.get("txn_date", ""),
        "note": request.form.get("note", "").strip(),
    }
    errors = []

    if form["type"] not in ("income", "expense"):
        errors.append("Choose income or expense.")

    try:
        form["amount"] = round(float(form["amount"]), 2)
        if form["amount"] <= 0:
            raise ValueError
    except ValueError:
        errors.append("Enter an amount greater than 0.")

    if not valid_date(form["txn_date"]):
        errors.append("Choose a valid date.")

    category = get_db().execute(
        "SELECT id FROM categories WHERE id = ? AND user_id = ? AND type = ?",
        (form["category_id"], current_user.id, form["type"])).fetchone()
    if not category:
        errors.append("Choose a category that matches the type.")

    return form, errors


def get_own_transaction(txn_id):
    row = get_db().execute("SELECT * FROM transactions WHERE id = ? AND user_id = ?",
                           (txn_id, current_user.id)).fetchone()
    if row is None:
        abort(404)
    return row


# ---------- authentication ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        error = None
        if not name or not email or not password:
            error = "Fill in all fields."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm:
            error = "Passwords do not match."

        db = get_db()
        if not error and db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone():
            error = "This email is already registered. Log in instead."

        if error:
            flash(error, "danger")
            return render_template("register.html", name=name, email=email)

        cur = db.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                         (name, email, generate_password_hash(password)))
        user_id = cur.lastrowid
        db.executemany("INSERT INTO categories (user_id, name, type) VALUES (?, ?, ?)",
                       [(user_id, n, t) for n, t in DEFAULT_CATEGORIES])
        db.commit()
        flash("Account created. Log in to start tracking.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        row = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

        if row and check_password_hash(row["password_hash"], password):
            login_user(User(row), remember=bool(request.form.get("remember")))
            return redirect(request.args.get("next") or url_for("dashboard"))

        flash("Email or password is wrong.", "danger")
        return render_template("login.html", email=email)

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ---------- forgot password Logic ----------

def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def send_otp_email(to_email, name, otp):
    msg = EmailMessage()
    msg["Subject"] = "Your Expense Tracker OTP"
    msg["From"] = MAIL_USER
    msg["To"] = to_email
    msg.set_content(
        f"Hi {name},\n\n"
        f"Your OTP to reset your Expense Tracker password is: {otp}\n\n"
        f"It is valid for {OTP_VALID_MINUTES} minutes. "
        f"If you did not ask for this, you can ignore this email.\n"
    )
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as server:
        server.login(MAIL_USER, MAIL_PASS)
        server.send_message(msg)


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email:
            flash("Enter your registered email.", "danger")
            return render_template("forgot.html")

        if OTP_MODE == "gmail" and (not MAIL_USER or not MAIL_PASS):
            flash("Email sending is not set up. Add your Gmail and app password in config.py.", "danger")
            return render_template("forgot.html", email=email)

        db = get_db()
        user = db.execute("SELECT id, name FROM users WHERE email = ?", (email,)).fetchone()

        if user:
            last = db.execute("""SELECT created_at FROM password_resets
                                 WHERE user_id = ? ORDER BY id DESC LIMIT 1""",
                              (user["id"],)).fetchone()
            if last:
                wait_till = datetime.strptime(last["created_at"], "%Y-%m-%d %H:%M:%S") \
                    + timedelta(seconds=OTP_RESEND_SECONDS)
                if datetime.now() < wait_till:
                    seconds = int((wait_till - datetime.now()).total_seconds()) + 1
                    flash(f"Please wait {seconds} seconds before asking for a new OTP.", "warning")
                    session["reset_email"] = email
                    return redirect(url_for("reset_password"))

            otp = f"{secrets.randbelow(1000000):06d}"
            expires_at = (datetime.now() + timedelta(minutes=OTP_VALID_MINUTES)).strftime("%Y-%m-%d %H:%M:%S")

            if OTP_MODE == "gmail":
                try:
                    send_otp_email(email, user["name"], otp)
                except Exception as e:
                    app.logger.error("OTP mail failed: %s", e)
                    flash("Could not send the email. Check your internet and Gmail app password.", "danger")
                    return render_template("forgot.html", email=email)
            else:
                print("\n" + "=" * 45)
                print(f"  OTP for {email}: {otp}")
                print(f"  Valid for {OTP_VALID_MINUTES} minutes")
                print("=" * 45 + "\n", flush=True)

            # ----------------   old OTPs stop working once a new one is sent ----------------

            db.execute("UPDATE password_resets SET used = 1 WHERE user_id = ?", (user["id"],))
            db.execute("""INSERT INTO password_resets (user_id, otp_hash, expires_at, created_at) VALUES (?, ?, ?, ?)""",
                       (user["id"], generate_password_hash(otp), expires_at, now_text()))
            db.commit()

        session["reset_email"] = email
        if OTP_MODE == "gmail":
            flash("If this email is registered, an OTP has been sent to it. Check inbox and Spam.", "Success")
        else:
            flash("If this email is registered, the OTP is shown in the VS Code terminal.", "Success")
        return redirect(url_for("reset_password"))

    return render_template("forgot.html")


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    email = session.get("reset_email")
    if not email:
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        otp = request.form.get("otp", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        db = get_db()

        row = db.execute("""SELECT r.* FROM password_resets r
                            JOIN users u ON u.id = r.user_id
                            WHERE u.email = ? AND r.used = 0
                            ORDER BY r.id DESC LIMIT 1""", (email,)).fetchone()

        if not row or row["expires_at"] < now_text():
            flash("This OTP has expired. Ask for a new one.", "danger")
            return redirect(url_for("reset_password"))

        if row["attempts"] >= OTP_MAX_ATTEMPTS:
            flash("Too many wrong attempts. Ask for a new OTP.", "danger")
            return redirect(url_for("reset_password"))

        if not check_password_hash(row["otp_hash"], otp):
            db.execute("UPDATE password_resets SET attempts = attempts + 1 WHERE id = ?", (row["id"],))
            db.commit()
            left = OTP_MAX_ATTEMPTS - row["attempts"] - 1
            flash(f"Wrong OTP. {left} attempt{'' if left == 1 else 's'} left.", "danger")
            return redirect(url_for("reset_password"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("reset_password"))
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("reset_password"))

        db.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                   (generate_password_hash(password), row["user_id"]))
        db.execute("UPDATE password_resets SET used = 1 WHERE user_id = ?", (row["user_id"],))
        db.commit()

        session.pop("reset_email", None)
        flash("Password changed. Log in with your new password.", "Success")
        return redirect(url_for("login"))

    return render_template("reset.html", email=email)


# ---------- dashboard ----------

@app.route("/")
@login_required
def dashboard():
    month = valid_month(request.args.get("month"))
    db = get_db()

    totals = {"income": 0, "expense": 0}
    rows = db.execute("""
        SELECT type, SUM(amount) AS total FROM transactions
        WHERE user_id = ? AND strftime('%Y-%m', txn_date) = ?
        GROUP BY type
    """, (current_user.id, month)).fetchall()
    for row in rows:
        totals[row["type"]] = row["total"]

    recent = db.execute("""
        SELECT t.*, c.name AS category FROM transactions t
        JOIN categories c ON c.id = t.category_id
        WHERE t.user_id = ? AND strftime('%Y-%m', t.txn_date) = ?
        ORDER BY t.txn_date DESC, t.id DESC LIMIT 5
    """, (current_user.id, month)).fetchall()

    return render_template(
        "dashboard.html",
        month=month,
        month_name=month_label(month),
        income=totals["income"],
        expense=totals["expense"],
        balance=totals["income"] - totals["expense"],
        budgets=get_budget_status(current_user.id, month),
        recent=recent,
    )


@app.route("/api/chart-data")
@login_required
def chart_data():
    month = valid_month(request.args.get("month"))
    db = get_db()

    by_category = db.execute("""
        SELECT c.name, SUM(t.amount) AS total FROM transactions t
        JOIN categories c ON c.id = t.category_id
        WHERE t.user_id = ? AND t.type = 'expense' AND strftime('%Y-%m', t.txn_date) = ?
        GROUP BY c.name ORDER BY total DESC
    """, (current_user.id, month)).fetchall()

    year, mon = map(int, month.split("-"))
    days_in_month = calendar.monthrange(year, mon)[1]
    daily = [0] * days_in_month
    for row in db.execute("""
        SELECT CAST(strftime('%d', txn_date) AS INTEGER) AS day, SUM(amount) AS total
        FROM transactions
        WHERE user_id = ? AND type = 'expense' AND strftime('%Y-%m', txn_date) = ?
        GROUP BY day
    """, (current_user.id, month)).fetchall():
        daily[row["day"] - 1] = row["total"]

    months = [shift_month(month, -i) for i in range(5, -1, -1)]
    trend = {m: {"income": 0, "expense": 0} for m in months}
    for row in db.execute("""
        SELECT strftime('%Y-%m', txn_date) AS m, type, SUM(amount) AS total
        FROM transactions
        WHERE user_id = ? AND strftime('%Y-%m', txn_date) BETWEEN ? AND ?
        GROUP BY m, type
    """, (current_user.id, months[0], months[-1])).fetchall():
        trend[row["m"]][row["type"]] = row["total"]

    return jsonify({
        "category": {
            "labels": [r["name"] for r in by_category],
            "values": [r["total"] for r in by_category],
        },
        "daily": {
            "labels": list(range(1, days_in_month + 1)),
            "values": daily,
        },
        "trend": {
            "labels": [month_label(m) for m in months],
            "income": [trend[m]["income"] for m in months],
            "expense": [trend[m]["expense"] for m in months],
        },
    })


# ---------- transactions details ----------

@app.route("/transactions")
@login_required
def transactions():
    filters = {
        "from_date": request.args.get("from_date", ""),
        "to_date": request.args.get("to_date", ""),
        "category_id": request.args.get("category_id", ""),
        "type": request.args.get("type", ""),
    }

    sql = """SELECT t.*, c.name AS category FROM transactions t
             JOIN categories c ON c.id = t.category_id
             WHERE t.user_id = ?"""
    params = [current_user.id]

    if valid_date(filters["from_date"]):
        sql += " AND t.txn_date >= ?"
        params.append(filters["from_date"])
    if valid_date(filters["to_date"]):
        sql += " AND t.txn_date <= ?"
        params.append(filters["to_date"])
    if filters["category_id"]:
        sql += " AND t.category_id = ?"
        params.append(filters["category_id"])
    if filters["type"] in ("income", "expense"):
        sql += " AND t.type = ?"
        params.append(filters["type"])

    sql += " ORDER BY t.txn_date DESC, t.id DESC"
    rows = get_db().execute(sql, params).fetchall()

    total_income = sum(r["amount"] for r in rows if r["type"] == "income")
    total_expense = sum(r["amount"] for r in rows if r["type"] == "expense")

    return render_template("transactions.html", rows=rows, filters=filters,
                           categories=get_categories(),
                           total_income=total_income, total_expense=total_expense)


@app.route("/transactions/add", methods=["GET", "POST"])
@login_required
def add_transaction():
    if request.method == "POST":
        form, errors = read_txn_form()
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("txn_form.html", txn=form, categories=get_categories(), mode="add")

        db = get_db()
        db.execute("""INSERT INTO transactions (user_id, type, amount, category_id, txn_date, note)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   (current_user.id, form["type"], form["amount"], form["category_id"],
                    form["txn_date"], form["note"]))
        db.commit()
        flash("Transaction saved.", "success")

        if form["type"] == "expense":
            check_budget_alerts(form["txn_date"], form["category_id"])

        if request.form.get("save_and_new"):
            return redirect(url_for("add_transaction", type=form["type"]))
        return redirect(url_for("transactions"))

    txn = {"type": request.args.get("type", "expense"), "amount": "",
           "category_id": "", "txn_date": date.today().isoformat(), "note": ""}
    return render_template("txn_form.html", txn=txn, categories=get_categories(), mode="add")


@app.route("/transactions/<int:txn_id>/edit", methods=["GET", "POST"])
@login_required
def edit_transaction(txn_id):
    row = get_own_transaction(txn_id)

    if request.method == "POST":
        form, errors = read_txn_form()
        if errors:
            for e in errors:
                flash(e, "danger")
            form["id"] = txn_id
            return render_template("txn_form.html", txn=form, categories=get_categories(), mode="edit")

        db = get_db()
        db.execute("""UPDATE transactions
                      SET type = ?, amount = ?, category_id = ?, txn_date = ?, note = ?
                      WHERE id = ? AND user_id = ?""",
                   (form["type"], form["amount"], form["category_id"], form["txn_date"],
                    form["note"], txn_id, current_user.id))
        db.commit()
        flash("Transaction updated.", "success")

        if form["type"] == "expense":
            check_budget_alerts(form["txn_date"], form["category_id"])
        return redirect(url_for("transactions"))

    return render_template("txn_form.html", txn=dict(row), categories=get_categories(), mode="edit")


@app.route("/transactions/<int:txn_id>/delete", methods=["POST"])
@login_required
def delete_transaction(txn_id):
    get_own_transaction(txn_id)
    db = get_db()
    db.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (txn_id, current_user.id))
    db.commit()
    flash("Transaction deleted.", "success")
    return redirect(request.referrer or url_for("transactions"))


# ---------- categories  Details ----------

@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        txn_type = request.form.get("type", "")
        if not name or txn_type not in ("income", "expense"):
            flash("Enter a name and choose a type.", "danger")
        elif db.execute("SELECT id FROM categories WHERE user_id = ? AND lower(name) = lower(?) AND type = ?",
                        (current_user.id, name, txn_type)).fetchone():
            flash("This category already exists.", "warning")
        else:
            db.execute("INSERT INTO categories (user_id, name, type) VALUES (?, ?, ?)",
                       (current_user.id, name, txn_type))
            db.commit()
            flash(f"Category '{name}' added.", "success")
        return redirect(url_for("categories"))

    rows = db.execute("""
        SELECT c.*, COUNT(t.id) AS used FROM categories c
        LEFT JOIN transactions t ON t.category_id = c.id
        WHERE c.user_id = ?
        GROUP BY c.id ORDER BY c.type, c.name
    """, (current_user.id,)).fetchall()
    return render_template("categories.html", rows=rows)


@app.route("/categories/<int:cat_id>/delete", methods=["POST"])
@login_required
def delete_category(cat_id):
    db = get_db()
    used = db.execute("SELECT COUNT(*) FROM transactions WHERE category_id = ? AND user_id = ?",
                      (cat_id, current_user.id)).fetchone()[0]
    if used:
        flash("This category has transactions, so it cannot be deleted.", "warning")
    else:
        db.execute("DELETE FROM budgets WHERE category_id = ? AND user_id = ?", (cat_id, current_user.id))
        db.execute("DELETE FROM categories WHERE id = ? AND user_id = ?", (cat_id, current_user.id))
        db.commit()
        flash("Category deleted.", "success")
    return redirect(url_for("categories"))


# ---------- budget Details ----------

@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    db = get_db()

    if request.method == "POST":
        month = valid_month(request.form.get("month"))
        category_id = request.form.get("category_id") or None
        try:
            limit_amount = round(float(request.form.get("limit_amount", "")), 2)
            if limit_amount <= 0:
                raise ValueError
        except ValueError:
            flash("Enter a budget amount greater than 0.", "danger")
            return redirect(url_for("budget", month=month))

        if category_id and not db.execute(
                "SELECT id FROM categories WHERE id = ? AND user_id = ? AND type = 'expense'",
                (category_id, current_user.id)).fetchone():
            flash("Choose a valid expense category.", "danger")
            return redirect(url_for("budget", month=month))

        existing = db.execute("""SELECT id FROM budgets
                                 WHERE user_id = ? AND month = ? AND category_id IS ?""",
                              (current_user.id, month, category_id)).fetchone()
        if existing:
            db.execute("UPDATE budgets SET limit_amount = ? WHERE id = ?", (limit_amount, existing["id"]))
            flash("Budget updated.", "success")
        else:
            db.execute("INSERT INTO budgets (user_id, month, category_id, limit_amount) VALUES (?, ?, ?, ?)",
                       (current_user.id, month, category_id, limit_amount))
            flash("Budget saved.", "success")
        db.commit()
        return redirect(url_for("budget", month=month))

    month = valid_month(request.args.get("month"))
    return render_template("budget.html", month=month, month_name=month_label(month),
                           budgets=get_budget_status(current_user.id, month),
                           categories=get_categories("expense"))


@app.route("/budget/copy", methods=["POST"])
@login_required
def copy_budget():
    month = valid_month(request.form.get("month"))
    prev = shift_month(month, -1)
    db = get_db()
    rows = db.execute("SELECT category_id, limit_amount FROM budgets WHERE user_id = ? AND month = ?",
                      (current_user.id, prev)).fetchall()
    if not rows:
        flash(f"No budget found for {month_label(prev)}.", "warning")
        return redirect(url_for("budget", month=month))

    for row in rows:
        exists = db.execute("SELECT id FROM budgets WHERE user_id = ? AND month = ? AND category_id IS ?",
                            (current_user.id, month, row["category_id"])).fetchone()
        if not exists:
            db.execute("INSERT INTO budgets (user_id, month, category_id, limit_amount) VALUES (?, ?, ?, ?)",
                       (current_user.id, month, row["category_id"], row["limit_amount"]))
    db.commit()
    flash(f"Budget copied from {month_label(prev)}.", "success")
    return redirect(url_for("budget", month=month))


@app.route("/budget/<int:budget_id>/delete", methods=["POST"])
@login_required
def delete_budget(budget_id):
    db = get_db()
    row = db.execute("SELECT month FROM budgets WHERE id = ? AND user_id = ?",
                     (budget_id, current_user.id)).fetchone()
    if row is None:
        abort(404)
    db.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
    db.commit()
    flash("Budget removed.", "success")
    return redirect(url_for("budget", month=row["month"]))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

