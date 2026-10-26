# All HTML pages of the app, loaded by app.py

TEMPLATES = {}

TEMPLATES["base.html"] = r"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Expense Tracker{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <style>
:root {
    --ink: #1d2b4f;
    --paper: #f3f5f9;
    --card: #ffffff;
    --line: #dde3ee;
    --muted: #66708a;
    --income: #1f8a5b;
    --expense: #c43d5a;
    --warn: #d99a00;

    --bs-primary: #1d2b4f;
    --bs-primary-rgb: 29, 43, 79;
    --bs-body-color: #1d2b4f;
    --bs-link-color: #2d4a8a;
    --bs-link-color-rgb: 45, 74, 138;
    --bs-success-rgb: 31, 138, 91;
    --bs-danger-rgb: 196, 61, 90;
    --bs-warning-rgb: 217, 154, 0;
}

body {
    background: var(--paper);
    font-family: "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif;
    padding-bottom: 5rem;
}

.amount,
.balance-value,
.amount-input {
    font-variant-numeric: tabular-nums;
}

.text-income { color: var(--income) !important; }
.text-expense { color: var(--expense) !important; }

/* buttons */
.btn-primary {
    --bs-btn-bg: var(--ink);
    --bs-btn-border-color: var(--ink);
    --bs-btn-hover-bg: #2a3d6b;
    --bs-btn-hover-border-color: #2a3d6b;
    --bs-btn-active-bg: #15203b;
    --bs-btn-active-border-color: #15203b;
}

.btn-outline-primary {
    --bs-btn-color: var(--ink);
    --bs-btn-border-color: var(--ink);
    --bs-btn-hover-bg: var(--ink);
    --bs-btn-hover-border-color: var(--ink);
    --bs-btn-active-bg: var(--ink);
}

.form-control:focus,
.form-select:focus {
    border-color: #6f84b8;
    box-shadow: 0 0 0 0.2rem rgba(29, 43, 79, 0.15);
}

:focus-visible {
    outline: 2px solid #2d4a8a;
    outline-offset: 2px;
}

/* navbar */
.app-nav {
    background: var(--ink);
}

.app-nav .navbar-brand,
.app-nav .nav-link,
.app-nav .nav-user {
    color: #fff;
}

.app-nav .nav-link {
    opacity: 0.75;
}

.app-nav .nav-link:hover,
.app-nav .nav-link.active {
    opacity: 1;
    color: #fff;
}

.app-nav .nav-link.active {
    box-shadow: inset 0 -2px 0 #fff;
}

.app-nav .navbar-toggler {
    border-color: rgba(255, 255, 255, 0.4);
}

.app-nav .navbar-toggler-icon {
    filter: invert(1);
}

.nav-user {
    font-size: 0.9rem;
    opacity: 0.85;
}

.brand-mark {
    display: inline-grid;
    place-items: center;
    width: 1.8rem;
    height: 1.8rem;
    border-radius: 50%;
    background: #fff;
    color: var(--ink);
    font-weight: 700;
    margin-right: 0.35rem;
}

/* page layout */
.page-head {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.page-title {
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0;
}

.month-picker .form-control {
    width: auto;
}

.panel {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 0.75rem;
    padding: 1.25rem;
}

.panel-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.75rem;
}

.panel-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
}

.panel-head .panel-title {
    margin-bottom: 0;
}

/* balance panel: the main highlight of the dashboard */
.balance-panel {
    background: var(--ink);
    color: #fff;
    border-radius: 1rem;
    padding: 1.75rem 1.5rem 1.5rem;
}

.balance-label {
    font-size: 0.95rem;
    opacity: 0.75;
}

.balance-value {
    font-size: clamp(2.2rem, 7vw, 3.5rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 1.25rem;
}

.balance-value.is-negative {
    color: #ff9fb2;
}

.split-bar {
    height: 0.75rem;
    border-radius: 999px;
    background: var(--income);
    overflow: hidden;
}

.split-expense {
    display: block;
    height: 100%;
    background: var(--expense);
    transition: width 0.6s ease;
}

.balance-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 2rem;
    margin-top: 0.85rem;
    font-size: 0.95rem;
}

.balance-legend strong {
    margin-left: 0.25rem;
    font-variant-numeric: tabular-nums;
}

.balance-legend .text-muted {
    color: rgba(255, 255, 255, 0.65) !important;
}

.dot {
    display: inline-block;
    width: 0.65rem;
    height: 0.65rem;
    border-radius: 50%;
    margin-right: 0.25rem;
}

.dot-income { background: var(--income); }
.dot-expense { background: var(--expense); }

/* budget rows */
.budget-row {
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--line);
}

.budget-row:last-of-type {
    border-bottom: 0;
}

.budget-row .progress {
    height: 0.6rem;
    margin: 0.4rem 0 0.3rem;
    background: #e8ecf3;
}

/* lists and tables */
.txn-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.txn-list li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--line);
}

.txn-list li:last-child {
    border-bottom: 0;
}

.txn-list .amount {
    font-weight: 600;
    white-space: nowrap;
}

.txn-table thead th {
    font-size: 0.85rem;
    color: var(--muted);
    font-weight: 600;
    background: #f8f9fc;
}

.txn-table td.amount {
    font-weight: 600;
}

.filter-bar {
    margin-bottom: 1rem;
}

.filter-bar .form-label {
    font-size: 0.85rem;
    color: var(--muted);
    margin-bottom: 0.25rem;
}

.totals-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1.5rem;
    margin-bottom: 1rem;
    color: var(--muted);
    font-size: 0.95rem;
}

/* charts */
.chart-box {
    position: relative;
    height: 260px;
}

.chart-box-sm {
    height: 240px;
}

.chart-empty {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    margin: 0;
}

/* forms */
.form-narrow {
    max-width: 560px;
    margin: 0 auto;
}

.type-toggle {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
}

.type-toggle .btn {
    border: 1px solid var(--line);
    background: #fff;
    font-weight: 600;
    padding: 0.6rem;
}

.btn-check:checked + .btn-toggle-expense {
    background: var(--expense);
    border-color: var(--expense);
    color: #fff;
}

.btn-check:checked + .btn-toggle-income {
    background: var(--income);
    border-color: var(--income);
    color: #fff;
}

.otp-input {
    font-size: 1.5rem;
    letter-spacing: 0.4em;
    text-align: center;
}

.amount-input {
    font-size: 1.6rem;
    font-weight: 600;
}

/* auth pages */
.auth-wrap {
    min-height: 80vh;
    display: grid;
    place-items: center;
}

.auth-card {
    width: 100%;
    max-width: 420px;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 1rem;
    padding: 2rem 1.75rem;
}

.auth-brand {
    font-weight: 700;
    margin-bottom: 1.5rem;
}

.auth-brand .brand-mark {
    background: var(--ink);
    color: #fff;
}

.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    background: var(--card);
    border: 1px dashed var(--line);
    border-radius: 0.75rem;
}

/* floating add button */
.fab {
    position: fixed;
    right: 1.25rem;
    bottom: 1.25rem;
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 50%;
    background: var(--expense);
    color: #fff;
    font-size: 2rem;
    line-height: 1;
    display: grid;
    place-items: center;
    text-decoration: none;
    box-shadow: 0 6px 18px rgba(196, 61, 90, 0.35);
    z-index: 1000;
}

.fab:hover {
    color: #fff;
    background: #a83049;
}

@media (max-width: 575.98px) {
    .page-title {
        font-size: 1.35rem;
    }

    .panel {
        padding: 1rem;
    }

    .balance-panel {
        padding: 1.25rem 1rem;
    }
}

@media (prefers-reduced-motion: reduce) {
    .split-expense {
        transition: none;
    }
}
    </style>
</head>
<body>
{% if current_user.is_authenticated %}
<nav class="navbar navbar-expand-md app-nav">
    <div class="container">
        <a class="navbar-brand" href="{{ url_for('dashboard') }}">
            <span class="brand-mark">₹</span> Expense Tracker
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav"
                aria-controls="mainNav" aria-expanded="false" aria-label="Toggle menu">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="mainNav">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}"
                       href="{{ url_for('dashboard') }}">Dashboard</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint in ['transactions', 'add_transaction', 'edit_transaction'] %}active{% endif %}"
                       href="{{ url_for('transactions') }}">Transactions</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint == 'budget' %}active{% endif %}"
                       href="{{ url_for('budget') }}">Budget</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link {% if request.endpoint == 'categories' %}active{% endif %}"
                       href="{{ url_for('categories') }}">Categories</a>
                </li>
            </ul>
            <div class="d-flex align-items-center gap-3">
                <span class="nav-user">Hi, {{ current_user.name }}</span>
                <a class="btn btn-sm btn-outline-light" href="{{ url_for('logout') }}">Log out</a>
            </div>
        </div>
    </div>
</nav>
{% endif %}

<main class="container py-4">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        {% endfor %}
    {% endwith %}

    {% block content %}{% endblock %}
</main>

{% if current_user.is_authenticated and request.endpoint not in ['add_transaction', 'edit_transaction'] %}
<a href="{{ url_for('add_transaction') }}" class="fab" aria-label="Add transaction" title="Add transaction">+</a>
{% endif %}

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
// Ask before submitting delete forms
document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
        if (!confirm(form.dataset.confirm)) {
            e.preventDefault();
        }
    });
});

// Show only categories that match the selected type
var categorySelect = document.querySelector("select#category_id option[data-type]");
var typeRadios = document.querySelectorAll("input[name='type'][type='radio']");

function filterCategories() {
    var checked = document.querySelector("input[name='type'][type='radio']:checked");
    if (!checked) return;
    var select = document.getElementById("category_id");

    select.querySelectorAll("option[data-type]").forEach(function (opt) {
        var show = opt.dataset.type === checked.value;
        opt.hidden = !show;
        opt.disabled = !show;
    });

    var selected = select.options[select.selectedIndex];
    if (selected && selected.disabled) {
        select.value = "";
    }
}

if (categorySelect && typeRadios.length) {
    typeRadios.forEach(function (radio) {
        radio.addEventListener("change", filterCategories);
    });
    filterCategories();
}

// Hide success messages after a few seconds
setTimeout(function () {
    document.querySelectorAll(".alert-success").forEach(function (el) {
        bootstrap.Alert.getOrCreateInstance(el).close();
    });
}, 4000);
</script>
{% block scripts %}{% endblock %}
</body>
</html>
"""

TEMPLATES["login.html"] = r"""{% extends "base.html" %}
{% block title %}Log in - Expense Tracker{% endblock %}
{% block content %}
<div class="auth-wrap">
    <div class="auth-card">
        <div class="auth-brand"><span class="brand-mark">₹</span> Expense Tracker</div>
        <h1 class="h4 mb-1">Welcome back</h1>
        <p class="text-muted mb-4">Log in to see where your money went this month.</p>

        <form method="post" novalidate>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" name="email"
                       value="{{ email or '' }}" required autofocus>
            </div>
            <div class="mb-3">
                <div class="d-flex justify-content-between">
                    <label for="password" class="form-label">Password</label>
                    <a href="{{ url_for('forgot_password') }}" class="small">Forgot password?</a>
                </div>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <div class="form-check mb-4">
                <input class="form-check-input" type="checkbox" id="remember" name="remember" value="1">
                <label class="form-check-label" for="remember">Keep me logged in</label>
            </div>
            <button type="submit" class="btn btn-primary w-100">Log in</button>
        </form>

        <p class="mt-4 mb-0 text-center">New here? <a href="{{ url_for('register') }}">Create an account</a></p>
    </div>
</div>
{% endblock %}
"""

TEMPLATES["register.html"] = r"""{% extends "base.html" %}
{% block title %}Create account - Expense Tracker{% endblock %}
{% block content %}
<div class="auth-wrap">
    <div class="auth-card">
        <div class="auth-brand"><span class="brand-mark">₹</span> Expense Tracker</div>
        <h1 class="h4 mb-1">Create your account</h1>
        <p class="text-muted mb-4">Common categories like Food, Travel and Bills are added for you.</p>

        <form method="post" novalidate>
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" name="name"
                       value="{{ name or '' }}" required autofocus>
            </div>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" name="email"
                       value="{{ email or '' }}" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" name="password"
                       minlength="6" required>
                <div class="form-text">At least 6 characters.</div>
            </div>
            <div class="mb-4">
                <label for="confirm" class="form-label">Confirm password</label>
                <input type="password" class="form-control" id="confirm" name="confirm" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Create account</button>
        </form>

        <p class="mt-4 mb-0 text-center">Already have an account? <a href="{{ url_for('login') }}">Log in</a></p>
    </div>
</div>
{% endblock %}
"""

TEMPLATES["dashboard.html"] = r"""{% extends "base.html" %}
{% block title %}Dashboard - Expense Tracker{% endblock %}
{% block content %}
<div class="page-head">
    <h1 class="page-title">{{ month_name }}</h1>
    <form method="get" class="month-picker">
        <label for="month" class="visually-hidden">Month</label>
        <input type="month" id="month" name="month" value="{{ month }}"
               class="form-control" onchange="this.form.submit()">
    </form>
</div>

{% set used = (expense / income * 100) if income else (100 if expense else 0) %}
<section class="balance-panel">
    <div class="balance-main">
        <div class="balance-label">Left this month</div>
        <div class="balance-value {% if balance < 0 %}is-negative{% endif %}">{{ balance | inr }}</div>
    </div>
    <div class="split-bar" role="img"
         aria-label="You spent {{ '%.0f' % used }} percent of your income">
        <span class="split-expense" style="width: {{ [used, 100] | min }}%"></span>
    </div>
    <div class="balance-legend">
        <div>
            <span class="dot dot-income"></span> Income
            <strong>{{ income | inr }}</strong>
        </div>
        <div>
            <span class="dot dot-expense"></span> Spent
            <strong>{{ expense | inr }}</strong>
            {% if income %}<span class="text-muted">({{ '%.0f' % used }}% of income)</span>{% endif %}
        </div>
    </div>
</section>

<div class="row g-4 mt-1">
    <div class="col-12 col-lg-5">
        <section class="panel h-100">
            <div class="panel-head">
                <h2 class="panel-title">Budget</h2>
                <a href="{{ url_for('budget', month=month) }}" class="small">Set budget</a>
            </div>
            {% if budgets %}
                {% for b in budgets %}
                <div class="budget-row">
                    <div class="d-flex justify-content-between">
                        <span class="fw-semibold">{{ b.name }}</span>
                        <span class="amount">{{ b.spent | inr }} / {{ b.limit | inr }}</span>
                    </div>
                    <div class="progress" role="progressbar" aria-valuenow="{{ '%.0f' % b.percent }}"
                         aria-valuemin="0" aria-valuemax="100" aria-label="{{ b.name }} budget used">
                        <div class="progress-bar bg-{{ b.level }}" style="width: {{ [b.percent, 100] | min }}%"></div>
                    </div>
                    <div class="small {% if b.level == 'danger' %}text-danger{% else %}text-muted{% endif %}">
                        {% if b.left >= 0 %}{{ b.left | inr }} left{% else %}Over by {{ (-b.left) | inr }}{% endif %}
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <p class="text-muted mb-2">No budget set for this month.</p>
                <a href="{{ url_for('budget', month=month) }}" class="btn btn-sm btn-outline-primary">Set a budget</a>
            {% endif %}
        </section>
    </div>

    <div class="col-12 col-lg-7">
        <section class="panel h-100">
            <h2 class="panel-title">Where the money went</h2>
            <div class="chart-box chart-box-sm">
                <canvas id="categoryChart"></canvas>
                <p class="chart-empty text-muted" hidden>No expenses in this month yet.</p>
            </div>
        </section>
    </div>

    <div class="col-12 col-lg-6">
        <section class="panel">
            <h2 class="panel-title">Daily spending</h2>
            <div class="chart-box"><canvas id="dailyChart"></canvas></div>
        </section>
    </div>

    <div class="col-12 col-lg-6">
        <section class="panel">
            <h2 class="panel-title">Last 6 months</h2>
            <div class="chart-box"><canvas id="trendChart"></canvas></div>
        </section>
    </div>

    <div class="col-12">
        <section class="panel">
            <div class="panel-head">
                <h2 class="panel-title">Recent transactions</h2>
                <a href="{{ url_for('transactions', from_date=month ~ '-01') }}" class="small">See all</a>
            </div>
            {% if recent %}
            <ul class="txn-list">
                {% for t in recent %}
                <li>
                    <div>
                        <div class="fw-semibold">{{ t.category }}</div>
                        <div class="small text-muted">{{ t.txn_date }}{% if t.note %} - {{ t.note }}{% endif %}</div>
                    </div>
                    <div class="amount {{ 'text-income' if t.type == 'income' else 'text-expense' }}">
                        {{ '+' if t.type == 'income' else '-' }}{{ t.amount | inr }}
                    </div>
                </li>
                {% endfor %}
            </ul>
            {% else %}
            <p class="text-muted mb-2">Nothing added for this month.</p>
            <a href="{{ url_for('add_transaction') }}" class="btn btn-sm btn-primary">Add first transaction</a>
            {% endif %}
        </section>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js"></script>
<script data-url="{{ url_for('chart_data', month=month) }}">
(function () {
    var script = document.currentScript;
    var dataUrl = script.dataset.url;

    var incomeColor = "#1f8a5b";
    var expenseColor = "#c43d5a";
    var palette = ["#1d2b4f", "#c43d5a", "#d99a00", "#1f8a5b", "#5b7bc0",
                   "#8e5bc0", "#2a9d9d", "#e07a3f", "#7a8599", "#b8578a"];

    Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
    Chart.defaults.color = "#66708a";

    function rupees(value) {
        return "\u20B9" + Number(value).toLocaleString("en-IN", { maximumFractionDigits: 2 });
    }

    var moneyTooltip = {
        callbacks: {
            label: function (ctx) {
                var value = ctx.parsed.y !== undefined ? ctx.parsed.y : ctx.parsed;
                return (ctx.dataset.label ? ctx.dataset.label + ": " : ctx.label + ": ") + rupees(value);
            }
        }
    };

    fetch(dataUrl)
        .then(function (res) { return res.json(); })
        .then(function (data) {
            drawCategory(data.category);
            drawDaily(data.daily);
            drawTrend(data.trend);
        })
        .catch(function (err) {
            console.error("Could not load chart data", err);
        });

    function drawCategory(d) {
        var canvas = document.getElementById("categoryChart");
        if (!d.values.length) {
            canvas.hidden = true;
            canvas.parentElement.querySelector(".chart-empty").hidden = false;
            return;
        }
        new Chart(canvas, {
            type: "doughnut",
            data: {
                labels: d.labels,
                datasets: [{ data: d.values, backgroundColor: palette, borderWidth: 2 }]
            },
            options: {
                maintainAspectRatio: false,
                cutout: "62%",
                plugins: {
                    legend: { position: window.innerWidth < 576 ? "bottom" : "right", labels: { boxWidth: 12 } },
                    tooltip: moneyTooltip
                }
            }
        });
    }

    function drawDaily(d) {
        new Chart(document.getElementById("dailyChart"), {
            type: "bar",
            data: {
                labels: d.labels,
                datasets: [{ label: "Spent", data: d.values, backgroundColor: expenseColor, borderRadius: 3 }]
            },
            options: {
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: moneyTooltip },
                scales: {
                    x: { grid: { display: false }, ticks: { maxTicksLimit: 10 } },
                    y: { beginAtZero: true, ticks: { callback: rupees } }
                }
            }
        });
    }

    function drawTrend(d) {
        new Chart(document.getElementById("trendChart"), {
            type: "bar",
            data: {
                labels: d.labels,
                datasets: [
                    { label: "Income", data: d.income, backgroundColor: incomeColor, borderRadius: 3 },
                    { label: "Spent", data: d.expense, backgroundColor: expenseColor, borderRadius: 3 }
                ]
            },
            options: {
                maintainAspectRatio: false,
                plugins: { legend: { position: "bottom", labels: { boxWidth: 12 } }, tooltip: moneyTooltip },
                scales: {
                    x: { grid: { display: false } },
                    y: { beginAtZero: true, ticks: { callback: rupees } }
                }
            }
        });
    }
})();
</script>
{% endblock %}
"""

TEMPLATES["transactions.html"] = r"""{% extends "base.html" %}
{% block title %}Transactions - Expense Tracker{% endblock %}
{% block content %}
<div class="page-head">
    <h1 class="page-title">Transactions</h1>
    <a href="{{ url_for('add_transaction') }}" class="btn btn-primary d-none d-md-inline-block">Add transaction</a>
</div>

<form method="get" class="panel filter-bar">
    <div class="row g-2 align-items-end">
        <div class="col-6 col-md-3">
            <label for="from_date" class="form-label">From</label>
            <input type="date" id="from_date" name="from_date" class="form-control" value="{{ filters.from_date }}">
        </div>
        <div class="col-6 col-md-3">
            <label for="to_date" class="form-label">To</label>
            <input type="date" id="to_date" name="to_date" class="form-control" value="{{ filters.to_date }}">
        </div>
        <div class="col-6 col-md-2">
            <label for="type" class="form-label">Type</label>
            <select id="type" name="type" class="form-select">
                <option value="">All</option>
                <option value="expense" {% if filters.type == 'expense' %}selected{% endif %}>Expense</option>
                <option value="income" {% if filters.type == 'income' %}selected{% endif %}>Income</option>
            </select>
        </div>
        <div class="col-6 col-md-2">
            <label for="category_id" class="form-label">Category</label>
            <select id="category_id" name="category_id" class="form-select">
                <option value="">All</option>
                {% for c in categories %}
                <option value="{{ c.id }}" {% if filters.category_id == c.id|string %}selected{% endif %}>
                    {{ c.name }} ({{ c.type }})
                </option>
                {% endfor %}
            </select>
        </div>
        <div class="col-12 col-md-2 d-flex gap-2">
            <button type="submit" class="btn btn-primary flex-fill">Filter</button>
            <a href="{{ url_for('transactions') }}" class="btn btn-outline-secondary flex-fill">Clear</a>
        </div>
    </div>
</form>

<div class="totals-strip">
    <span>{{ rows | length }} record{{ '' if rows | length == 1 else 's' }}</span>
    <span>Income <strong class="text-income">{{ total_income | inr }}</strong></span>
    <span>Spent <strong class="text-expense">{{ total_expense | inr }}</strong></span>
</div>

{% if rows %}
<div class="panel p-0">
    <div class="table-responsive">
        <table class="table align-middle mb-0 txn-table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Category</th>
                    <th class="d-none d-md-table-cell">Note</th>
                    <th class="text-end">Amount</th>
                    <th class="text-end">Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for t in rows %}
                <tr>
                    <td class="text-nowrap">{{ t.txn_date }}</td>
                    <td>
                        {{ t.category }}
                        {% if t.note %}<div class="small text-muted d-md-none">{{ t.note }}</div>{% endif %}
                    </td>
                    <td class="d-none d-md-table-cell text-muted">{{ t.note or '' }}</td>
                    <td class="text-end amount text-nowrap {{ 'text-income' if t.type == 'income' else 'text-expense' }}">
                        {{ '+' if t.type == 'income' else '-' }}{{ t.amount | inr }}
                    </td>
                    <td class="text-end text-nowrap">
                        <a href="{{ url_for('edit_transaction', txn_id=t.id) }}" class="btn btn-sm btn-outline-primary">Edit</a>
                        <form method="post" action="{{ url_for('delete_transaction', txn_id=t.id) }}"
                              class="d-inline" data-confirm="Delete this transaction?">
                            <button type="submit" class="btn btn-sm btn-outline-danger">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% else %}
<div class="empty-state">
    <p class="mb-3">No transactions match these filters.</p>
    <a href="{{ url_for('add_transaction') }}" class="btn btn-primary">Add transaction</a>
</div>
{% endif %}
{% endblock %}
"""

TEMPLATES["txn_form.html"] = r"""{% extends "base.html" %}
{% block title %}{{ 'Edit' if mode == 'edit' else 'Add' }} transaction - Expense Tracker{% endblock %}
{% block content %}
<div class="form-narrow">
    <h1 class="page-title mb-4">{{ 'Edit transaction' if mode == 'edit' else 'Add transaction' }}</h1>

    <form method="post" class="panel" novalidate>
        <div class="type-toggle mb-4" role="group" aria-label="Transaction type">
            <input type="radio" class="btn-check" name="type" id="typeExpense" value="expense"
                   {% if txn.type != 'income' %}checked{% endif %}>
            <label class="btn btn-toggle-expense" for="typeExpense">Expense</label>

            <input type="radio" class="btn-check" name="type" id="typeIncome" value="income"
                   {% if txn.type == 'income' %}checked{% endif %}>
            <label class="btn btn-toggle-income" for="typeIncome">Income</label>
        </div>

        <div class="mb-3">
            <label for="amount" class="form-label">Amount (₹)</label>
            <input type="number" step="0.01" min="0.01" inputmode="decimal" id="amount" name="amount"
                   class="form-control form-control-lg amount-input" value="{{ txn.amount }}" required autofocus>
        </div>

        <div class="mb-3">
            <label for="category_id" class="form-label">Category</label>
            <select id="category_id" name="category_id" class="form-select" required>
                <option value="">Choose category</option>
                {% for c in categories %}
                <option value="{{ c.id }}" data-type="{{ c.type }}"
                        {% if txn.category_id|string == c.id|string %}selected{% endif %}>{{ c.name }}</option>
                {% endfor %}
            </select>
            <div class="form-text">Need another one? <a href="{{ url_for('categories') }}">Add a category</a></div>
        </div>

        <div class="mb-3">
            <label for="txn_date" class="form-label">Date</label>
            <input type="date" id="txn_date" name="txn_date" class="form-control" value="{{ txn.txn_date }}" required>
        </div>

        <div class="mb-4">
            <label for="note" class="form-label">Note <span class="text-muted">(optional)</span></label>
            <input type="text" id="note" name="note" class="form-control" maxlength="200"
                   value="{{ txn.note or '' }}" placeholder="e.g. Lunch with friends">
        </div>

        <div class="d-flex flex-wrap gap-2">
            <button type="submit" class="btn btn-primary">{{ 'Save changes' if mode == 'edit' else 'Save' }}</button>
            {% if mode == 'add' %}
            <button type="submit" name="save_and_new" value="1" class="btn btn-outline-primary">Save and add another</button>
            {% endif %}
            <a href="{{ url_for('transactions') }}" class="btn btn-link text-muted ms-auto">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
"""

TEMPLATES["budget.html"] = r"""{% extends "base.html" %}
{% block title %}Budget - Expense Tracker{% endblock %}
{% block content %}
<div class="page-head">
    <h1 class="page-title">Budget for {{ month_name }}</h1>
    <form method="get" class="month-picker">
        <label for="month" class="visually-hidden">Month</label>
        <input type="month" id="month" name="month" value="{{ month }}"
               class="form-control" onchange="this.form.submit()">
    </form>
</div>

<div class="row g-4">
    <div class="col-12 col-lg-5">
        <form method="post" class="panel" novalidate>
            <h2 class="panel-title">Set a limit</h2>
            <input type="hidden" name="month" value="{{ month }}">
            <div class="mb-3">
                <label for="category_id" class="form-label">Apply to</label>
                <select id="category_id" name="category_id" class="form-select">
                    <option value="">Whole month (all expenses)</option>
                    {% for c in categories %}
                    <option value="{{ c.id }}">{{ c.name }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="mb-3">
                <label for="limit_amount" class="form-label">Limit (₹)</label>
                <input type="number" step="0.01" min="1" inputmode="decimal" id="limit_amount"
                       name="limit_amount" class="form-control" required>
                <div class="form-text">Setting it again for the same item updates the old limit.</div>
            </div>
            <button type="submit" class="btn btn-primary w-100">Save budget</button>
        </form>

        <form method="post" action="{{ url_for('copy_budget') }}" class="mt-3">
            <input type="hidden" name="month" value="{{ month }}">
            <button type="submit" class="btn btn-outline-secondary w-100">Copy last month's budget</button>
        </form>
    </div>

    <div class="col-12 col-lg-7">
        <section class="panel">
            <h2 class="panel-title">This month</h2>
            {% if budgets %}
                {% for b in budgets %}
                <div class="budget-row">
                    <div class="d-flex justify-content-between align-items-center gap-2">
                        <span class="fw-semibold">{{ b.name }}</span>
                        <form method="post" action="{{ url_for('delete_budget', budget_id=b.id) }}"
                              data-confirm="Remove the {{ b.name }} budget?">
                            <button type="submit" class="btn btn-sm btn-link text-danger p-0">Remove</button>
                        </form>
                    </div>
                    <div class="progress" role="progressbar" aria-valuenow="{{ '%.0f' % b.percent }}"
                         aria-valuemin="0" aria-valuemax="100" aria-label="{{ b.name }} budget used">
                        <div class="progress-bar bg-{{ b.level }}" style="width: {{ [b.percent, 100] | min }}%"></div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span class="amount">{{ b.spent | inr }} of {{ b.limit | inr }} ({{ '%.0f' % b.percent }}%)</span>
                        <span class="{% if b.left < 0 %}text-danger{% else %}text-muted{% endif %}">
                            {% if b.left >= 0 %}{{ b.left | inr }} left{% else %}Over by {{ (-b.left) | inr }}{% endif %}
                        </span>
                    </div>
                </div>
                {% endfor %}
                <p class="small text-muted mb-0 mt-3">
                    You get a warning at 80% and an alert when a limit is crossed.
                </p>
            {% else %}
                <p class="text-muted mb-0">No limits set yet. Start with a whole-month limit, then add limits for categories like Food or Shopping.</p>
            {% endif %}
        </section>
    </div>
</div>
{% endblock %}
"""

TEMPLATES["categories.html"] = r"""{% extends "base.html" %}
{% block title %}Categories - Expense Tracker{% endblock %}
{% block content %}
<h1 class="page-title mb-4">Categories</h1>

<div class="row g-4">
    <div class="col-12 col-lg-4">
        <form method="post" class="panel" novalidate>
            <h2 class="panel-title">Add category</h2>
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" id="name" name="name" class="form-control" maxlength="40" required>
            </div>
            <div class="mb-3">
                <label for="type" class="form-label">Type</label>
                <select id="type" name="type" class="form-select">
                    <option value="expense">Expense</option>
                    <option value="income">Income</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary w-100">Add category</button>
        </form>
    </div>

    <div class="col-12 col-lg-8">
        {% for group in ['expense', 'income'] %}
        <section class="panel mb-4">
            <h2 class="panel-title">{{ 'Expense' if group == 'expense' else 'Income' }} categories</h2>
            <ul class="txn-list">
                {% for c in rows if c.type == group %}
                <li>
                    <div>
                        <span class="fw-semibold">{{ c.name }}</span>
                        <span class="small text-muted ms-2">{{ c.used }} transaction{{ '' if c.used == 1 else 's' }}</span>
                    </div>
                    {% if c.used == 0 %}
                    <form method="post" action="{{ url_for('delete_category', cat_id=c.id) }}"
                          data-confirm="Delete the {{ c.name }} category?">
                        <button type="submit" class="btn btn-sm btn-link text-danger p-0">Delete</button>
                    </form>
                    {% endif %}
                </li>
                {% endfor %}
            </ul>
        </section>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""

TEMPLATES["404.html"] = r"""{% extends "base.html" %}
{% block title %}Page not found{% endblock %}
{% block content %}
<div class="empty-state">
    <h1 class="h4">This page does not exist</h1>
    <p class="text-muted">The link may be wrong, or the record was deleted.</p>
    <a class="btn btn-primary" href="{{ url_for('dashboard') }}">Go to dashboard</a>
</div>
{% endblock %}
"""

TEMPLATES["forgot.html"] = r"""{% extends "base.html" %}
{% block title %}Forgot password - Expense Tracker{% endblock %}
{% block content %}
<div class="auth-wrap">
    <div class="auth-card">
        <div class="auth-brand"><span class="brand-mark">₹</span> Expense Tracker</div>
        <h1 class="h4 mb-1">Forgot password</h1>
        <p class="text-muted mb-4">Enter your registered email. We will send a 6-digit OTP to reset your password.</p>

        <form method="post" novalidate>
            <div class="mb-4">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" name="email"
                       value="{{ email or '' }}" required autofocus>
            </div>
            <button type="submit" class="btn btn-primary w-100">Send OTP</button>
        </form>

        <p class="mt-4 mb-0 text-center"><a href="{{ url_for('login') }}">Back to log in</a></p>
    </div>
</div>
{% endblock %}
"""

TEMPLATES["reset.html"] = r"""{% extends "base.html" %}
{% block title %}Reset password - Expense Tracker{% endblock %}
{% block content %}
<div class="auth-wrap">
    <div class="auth-card">
        <div class="auth-brand"><span class="brand-mark">₹</span> Expense Tracker</div>
        <h1 class="h4 mb-1">Reset password</h1>
        <p class="text-muted mb-4">Enter the OTP sent to <strong>{{ email }}</strong> and choose a new password.</p>

        <form method="post" novalidate>
            <div class="mb-3">
                <label for="otp" class="form-label">OTP</label>
                <input type="text" class="form-control otp-input" id="otp" name="otp"
                       inputmode="numeric" maxlength="6" autocomplete="one-time-code" required autofocus>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">New password</label>
                <input type="password" class="form-control" id="password" name="password" minlength="6" required>
                <div class="form-text">At least 6 characters.</div>
            </div>
            <div class="mb-4">
                <label for="confirm" class="form-label">Confirm new password</label>
                <input type="password" class="form-control" id="confirm" name="confirm" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Change password</button>
        </form>

        <form method="post" action="{{ url_for('forgot_password') }}" class="mt-3">
            <input type="hidden" name="email" value="{{ email }}">
            <button type="submit" class="btn btn-outline-secondary w-100">Resend OTP</button>
        </form>

        <p class="mt-4 mb-0 text-center"><a href="{{ url_for('forgot_password') }}">Use a different email</a></p>
    </div>
</div>
{% endblock %}
"""