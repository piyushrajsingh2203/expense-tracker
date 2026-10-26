# Expense Tracker

A personal income and expense tracker built with Flask and SQLite. Add your daily transactions, set monthly budgets, and see where your money is going through charts on the dashboard.

Every user has their own account, their own categories and their own data.

## Features

**Transactions**
- Add, edit and delete income or expense entries
- Each entry has an amount, category, date and an optional note
- Filter the list by date range, type and category
- "Save and add another" for quick entry of multiple records

**Budgets**
- Set a limit for the whole month, or a separate limit for any expense category
- Progress bar shows how much of each limit is used
- Warning at 80% and an alert when a limit is crossed
- Copy last month's budget in one click

**Categories**
- Common categories like Food, Travel, Bills and Salary are created automatically on sign up
- Add your own categories for income or expense
- A category with transactions cannot be deleted, so old records stay correct

**Dashboard**
- Balance left for the selected month, with an income vs spent split bar
- Doughnut chart of spending by category
- Bar chart of day-wise spending
- Last 6 months income vs expense comparison
- Recent transactions list

**Accounts**
- Register and log in, with "keep me logged in"
- Passwords are stored as hashes, never as plain text
- Forgot password works through a 6-digit OTP, valid for 10 minutes
- OTP is limited to 5 attempts, with a 60 second wait before a new one can be sent

## Tech stack

| Part | Used |
|------|------|
| Backend | Python, Flask |
| Database | SQLite |
| Login | Flask-Login, Werkzeug password hashing |
| Templates | Jinja2, loaded from `templates.py` |
| Frontend | Bootstrap 5, Chart.js |
| Email | Gmail SMTP for OTP |

## Project structure

```
expense_tracker/
├── app.py            # routes, database schema, all the logic
├── templates.py      # every HTML page, kept as strings
├── config.py         # OTP mode and Gmail settings
├── requirements.txt
└── expense.db        # created on first run
```

The HTML pages are kept in `templates.py` instead of a `templates/` folder, and loaded with Jinja2 `DictLoader`.

## Setup

**1. Clone the project**

```
git clone https://github.com/piyushrajsingh2203/expense-tracker.git
cd expense-tracker
```

**2. Create a virtual environment**

```
python -m venv .venv
.venv\Scripts\activate
```

On Mac or Linux use `source .venv/bin/activate`.

**3. Install the packages**

```
pip install -r requirements.txt
```

**4. Set the secret key**

Open `app.py` and change this line to any long random text:

```python
app.config["SECRET_KEY"] = "change-this-to-any-long-random-text"
```

**5. Run it**

```
python app.py
```

Open http://127.0.0.1:5000 in the browser. The database is created on the first run, so there is no separate migration step.

## OTP settings

`config.py` decides how the OTP for forgot password is sent.

**Terminal mode (default, nothing to set up)**

```python
OTP_MODE = "terminal"
```

The OTP is printed in the terminal where the app is running. Good enough while testing.

**Gmail mode**

```python
OTP_MODE = "gmail"
MAIL_USER = "yourmail@gmail.com"
MAIL_PASS = "your 16 character app password"
```

The app password is not your normal Gmail password. Turn on 2-step verification in your Google account, then create an app password from Google Account > Security > App passwords.

## Database

Four tables, all created by `init_db()` in `app.py`.

| Table | Holds |
|-------|-------|
| `users` | name, email, password hash |
| `categories` | user's income and expense categories |
| `transactions` | every income and expense entry |
| `budgets` | monthly limits, overall or category wise |
| `password_resets` | OTP hash, expiry and attempt count |

In `budgets`, a `category_id` of NULL means the limit is for the whole month.

## Notes

- `expense.db` is in `.gitignore`, so your data stays on your machine only
- Amounts are shown in rupees through a small `inr` Jinja filter
- Debug mode is on in `app.py` for local use. Turn it off before putting this anywhere public

## Author

Piyush Raj Singh
[github.com/piyushrajsingh2203](https://github.com/piyushrajsingh2203)