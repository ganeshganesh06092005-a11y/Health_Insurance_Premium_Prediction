from __future__ import annotations

import os
from datetime import datetime
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from werkzeug.security import check_password_hash, generate_password_hash

from model import FEATURE_RANGES, load_or_train_model, predict_premium


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-secret-in-production")
# Uses SQLite by default so the project runs immediately. Set DATABASE_URL to a
# MySQL URL, e.g. mysql+pymysql://user:password@localhost/insurance_db.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///predictions.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    children = db.Column(db.Integer, nullable=False)
    smoker = db.Column(db.String(5), nullable=False)
    region = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False, default="")
    salary = db.Column(db.Float, nullable=False, default=0)
    policy_duration = db.Column(db.Integer, nullable=False, default=5)
    plan_category = db.Column(db.String(20), nullable=False, default="silver")
    recommendation = db.Column(db.String(255), nullable=False, default="")
    estimated_benefit = db.Column(db.Float, nullable=False, default=0)
    estimated_premium = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    predictions = db.relationship("Prediction", backref="user", lazy=True)


with app.app_context():
    db.create_all()
    prediction_columns = {column["name"] for column in inspect(db.engine).get_columns("prediction")}
    migrations = {
        "user_id": "INTEGER NULL",
        "full_name": "VARCHAR(100) NOT NULL DEFAULT ''",
        "salary": "FLOAT NOT NULL DEFAULT 0",
        "policy_duration": "INTEGER NOT NULL DEFAULT 5",
        "plan_category": "VARCHAR(20) NOT NULL DEFAULT 'silver'",
        "recommendation": "VARCHAR(255) NOT NULL DEFAULT ''",
        "estimated_benefit": "FLOAT NOT NULL DEFAULT 0",
    }
    for column, definition in migrations.items():
        if column not in prediction_columns:
            db.session.execute(text(f"ALTER TABLE prediction ADD COLUMN {column} {definition}"))
    db.session.commit()
    load_or_train_model()


def parse_form(form):
    values = {
        "age": int(form["age"]),
        "sex": form["sex"],
        "bmi": float(form["bmi"]),
        "children": int(form["children"]),
        "smoker": form["smoker"],
        "region": form["region"],
        "full_name": form.get("full_name", "").strip(),
        "salary": float(form["salary"]),
    }
    if not values["full_name"]:
        raise ValueError("Full name is required.")
    if not FEATURE_RANGES["age"][0] <= values["age"] <= FEATURE_RANGES["age"][1]:
        raise ValueError("Age must be between 18 and 100.")
    if not FEATURE_RANGES["bmi"][0] <= values["bmi"] <= FEATURE_RANGES["bmi"][1]:
        raise ValueError("BMI must be between 10 and 60.")
    if not FEATURE_RANGES["children"][0] <= values["children"] <= FEATURE_RANGES["children"][1]:
        raise ValueError("Dependents must be between 0 and 10.")
    if not FEATURE_RANGES["salary"][0] <= values["salary"] <= FEATURE_RANGES["salary"][1]:
        raise ValueError("Annual salary must be between ₹1,00,000 and ₹1,00,00,000.")
    return values


def build_recommendation(premium, salary, plan, duration):
    plan_details = {
        "basic": ("Basic", 1.05, "A cost-conscious plan for essential protection."),
        "silver": ("Silver", 1.20, "A balanced plan for regular health protection."),
        "gold": ("Gold", 1.40, "A broader plan for higher financial protection."),
    }
    label, benefit_rate, description = plan_details[plan]
    affordability = premium / salary
    if affordability > 0.12:
        note = "Consider increasing the deductible or choosing a shorter duration."
    elif affordability < 0.05:
        note = "Your estimated premium is comfortably within the stated income."
    else:
        note = "The estimated premium is proportionate to the stated income."
    benefit = round(premium * duration * benefit_rate, 2)
    return {
        "plan": label,
        "description": f"{description} {note}",
        "benefit": benefit,
    }


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Name, email, and password are required.", "error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "error")
        else:
            user = User()
            user.name = name
            user.email = email
            user.password_hash = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect(url_for("dashboard"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "error")
        else:
            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.name
            destination = request.args.get("next")
            return redirect(destination if destination and destination.startswith("/") else url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and "user_id" not in session:
        return redirect(url_for("login", next=url_for("index")))
    result = None
    form_data = request.form.to_dict()
    if request.method == "POST":
        try:
            values = parse_form(request.form)
            result = predict_premium(values)
            duration = int(request.form.get("policy_duration", 5))
            plan = request.form.get("plan_category", "silver")
            if duration not in {5, 10, 15, 20}:
                raise ValueError("Choose a policy duration of 5, 10, 15, or 20 years.")
            if plan not in {"basic", "silver", "gold"}:
                raise ValueError("Choose a valid insurance plan.")
            recommendation = build_recommendation(result, values["salary"], plan, duration)
            prediction = Prediction()
            prediction.age = values["age"]
            prediction.sex = values["sex"]
            prediction.bmi = values["bmi"]
            prediction.children = values["children"]
            prediction.smoker = values["smoker"]
            prediction.region = values["region"]
            prediction.full_name = values["full_name"]
            prediction.salary = values["salary"]
            prediction.policy_duration = duration
            prediction.plan_category = plan
            prediction.recommendation = recommendation["description"]
            prediction.estimated_benefit = recommendation["benefit"]
            prediction.estimated_premium = result
            prediction.user_id = session["user_id"]
            db.session.add(prediction)
            db.session.commit()
            result = {**recommendation, "premium": result, "duration": duration}
        except (KeyError, TypeError, ValueError) as error:
            flash(str(error) or "Please enter valid values.", "error")
        except Exception:
            app.logger.exception("Prediction failed")
            flash("The prediction could not be completed. Please try again.", "error")
    return render_template("index.html", result=result, form_data=form_data)


@app.route("/dashboard")
@login_required
def dashboard():
    user = db.session.get(User, session["user_id"])
    records = (Prediction.query.filter_by(user_id=session["user_id"])
               .order_by(Prediction.created_at.desc()).limit(3).all())
    prediction_count = Prediction.query.filter_by(user_id=session["user_id"]).count()
    latest = records[0] if records else None
    return render_template(
        "dashboard.html",
        records=records,
        user=user,
        prediction_count=prediction_count,
        latest=latest,
    )


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email or "@" not in email:
            flash("Please enter a valid email address.", "error")
        else:
            flash(f"Password reset instructions have been sent to {email}.", "success")
            return redirect(url_for("forgot_password"))
    return render_template("forgot_password.html")


@app.route("/history")
@login_required
def history():
    records = (Prediction.query.filter_by(user_id=session["user_id"])
               .order_by(Prediction.created_at.desc()).limit(50).all())
    return render_template("history.html", records=records)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(debug=True)
