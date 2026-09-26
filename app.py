from __future__ import annotations

import io
import json
import os
from datetime import datetime
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from werkzeug.security import check_password_hash, generate_password_hash

from model import (
    FEATURE_RANGES,
    FEATURES,
    explain_prediction,
    feature_insights,
    get_model_meta,
    load_or_train_model,
    predict_premium,
)
from report_generator import generate_pdf_report

BASE_DIR = Path(__file__).resolve().parent
METRICS_PATH = BASE_DIR / "models" / "evaluation_metrics.json"
load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "healthsecure-secret-key-change-in-production")
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    mysql_user = os.environ.get("MYSQL_USER", "root")
    mysql_password = os.environ.get("MYSQL_PASSWORD", "")
    mysql_host = os.environ.get("MYSQL_HOST", "127.0.0.1")
    mysql_port = os.environ.get("MYSQL_PORT", "3306")
    mysql_database = os.environ.get("MYSQL_DATABASE", "health_insurance_db")
    database_url = (
        f"mysql+pymysql://{mysql_user}:{mysql_password}"
        f"@{mysql_host}:{mysql_port}/{mysql_database}"
    )
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["BENEFIT_FACTOR"] = float(os.environ.get("BENEFIT_FACTOR", "1.2"))
db = SQLAlchemy(app)


class InsurancePlan(db.Model):
    __tablename__ = "insurance_plans"

    plan_id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(100), nullable=False)
    annual_premium = db.Column(db.Float, nullable=False)
    coverage_amount = db.Column(db.Float, nullable=False)
    policy_duration = db.Column(db.Integer, nullable=False, default=10)
    plan_description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Prediction(db.Model):
    __tablename__ = "prediction"

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
    premium_income_ratio = db.Column(db.Float, nullable=False, default=0)
    total_premium = db.Column(db.Float, nullable=False, default=0)
    benefit_factor = db.Column(db.Float, nullable=False, default=1.2)
    estimated_benefit = db.Column(db.Float, nullable=False, default=0)
    estimated_premium = db.Column(db.Float, nullable=False)
    recommended_plan_id = db.Column(db.Integer, db.ForeignKey("insurance_plans.plan_id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    recommended_demo_plan = db.relationship("InsurancePlan", foreign_keys=[recommended_plan_id], lazy=True)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(20), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    predictions = db.relationship("Prediction", backref="user", lazy=True)


class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey("prediction.id"), nullable=False, index=True)
    plan_name = db.Column(db.String(50), nullable=False)
    policy_years = db.Column(db.Integer, nullable=False)
    annual_premium = db.Column(db.Float, nullable=False)
    total_premium = db.Column(db.Float, nullable=False)
    estimated_benefit = db.Column(db.Float, nullable=False)
    benefit_factor = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


with app.app_context():
    db.create_all()
    prediction_columns = {column["name"] for column in inspect(db.engine).get_columns("prediction")}
    user_columns = {column["name"] for column in inspect(db.engine).get_columns("users")}

    migrations = {
        "user_id": "INTEGER NULL",
        "full_name": "VARCHAR(100) NOT NULL DEFAULT ''",
        "salary": "FLOAT NOT NULL DEFAULT 0",
        "policy_duration": "INTEGER NOT NULL DEFAULT 5",
        "plan_category": "VARCHAR(20) NOT NULL DEFAULT 'silver'",
        "recommendation": "VARCHAR(255) NOT NULL DEFAULT ''",
        "estimated_benefit": "FLOAT NOT NULL DEFAULT 0",
        "premium_income_ratio": "FLOAT NOT NULL DEFAULT 0",
        "total_premium": "FLOAT NOT NULL DEFAULT 0",
        "benefit_factor": "FLOAT NOT NULL DEFAULT 1.2",
        "recommended_plan_id": "INTEGER NULL",
    }
    for column, definition in migrations.items():
        if column not in prediction_columns:
            db.session.execute(text(f"ALTER TABLE prediction ADD COLUMN {column} {definition}"))

    user_migrations = {
        "phone": "VARCHAR(30) NULL",
        "dob": "DATE NULL",
        "role": "VARCHAR(20) NOT NULL DEFAULT 'user'",
        "created_at": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    }
    for column, definition in user_migrations.items():
        if column not in user_columns:
            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} {definition}"))
    db.session.commit()

    # Seed 5 Standard Demo Insurance Plans if table is empty
    if not InsurancePlan.query.first():
        demo_plans = [
            InsurancePlan(
                plan_name="HealthSecure Basic",
                annual_premium=19999.00,
                coverage_amount=300000.00,
                policy_duration=5,
                plan_description="Essential sample coverage plan designed for cost-conscious protection against acute hospitalization.",
                benefits="Hospitalization support, basic benefits, standard ambulance cover, daycare procedures",
                status="active",
            ),
            InsurancePlan(
                plan_name="HealthSecure Standard",
                annual_premium=27999.00,
                coverage_amount=500000.00,
                policy_duration=10,
                plan_description="Standard balanced protection plan providing comprehensive inpatient and outpatient support.",
                benefits="Inpatient treatment, daycare treatments, ambulance support, annual health checkup, pre/post hospitalization",
                status="active",
            ),
            InsurancePlan(
                plan_name="HealthSecure Plus",
                annual_premium=30500.00,
                coverage_amount=750000.00,
                policy_duration=10,
                plan_description="Enhanced health protection tier offering higher sum insured and critical illness cover.",
                benefits="Extended inpatient care, pre & post hospitalization (60/90 days), critical illness rider, restorative sum insured",
                status="active",
            ),
            InsurancePlan(
                plan_name="HealthSecure Family",
                annual_premium=31999.00,
                coverage_amount=1000000.00,
                policy_duration=15,
                plan_description="Family floater health protection offering extended duration and comprehensive pediatric/maternity coverage.",
                benefits="Maternity benefits, pediatric care, ICU cover, zero room-rent capping, family floater support",
                status="active",
            ),
            InsurancePlan(
                plan_name="HealthSecure Premium",
                annual_premium=49999.00,
                coverage_amount=1500000.00,
                policy_duration=20,
                plan_description="Comprehensive high-tier executive protection with worldwide emergency assistance and zero copays.",
                benefits="Zero copay nationwide, worldwide emergency evacuation, unlimited restoration, AYUSH cover, executive wellness suite",
                status="active",
            ),
        ]
        db.session.add_all(demo_plans)
        db.session.commit()

    # Seed default administrator if not present (Admin@123)
    admin_email = "admin@healthsecure.com"
    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin_user = User(
            name="System Administrator",
            email=admin_email,
            password_hash=generate_password_hash("Admin@123"),
            phone="+91 9876543210",
            role="admin",
        )
        db.session.add(admin_user)
        db.session.commit()

    # Backfill recommendations if table empty
    if not Recommendation.query.first():
        for record in Prediction.query.all():
            recommendation = Recommendation()
            recommendation.prediction_id = record.id
            recommendation.plan_name = record.plan_category.title()
            recommendation.policy_years = record.policy_duration
            recommendation.annual_premium = record.estimated_premium
            recommendation.total_premium = record.estimated_premium * record.policy_duration
            recommendation.estimated_benefit = record.estimated_benefit
            recommendation.benefit_factor = app.config["BENEFIT_FACTOR"]
            db.session.add(recommendation)
        db.session.commit()

    load_or_train_model()


def get_matching_plans(
    predicted_premium: float,
    limit: int = 3,
    selected_duration: int | None = None,
) -> list[dict]:
    """Retrieve active demo plans from MySQL and rank by smallest absolute premium difference.
    
    Formula:
        Difference = ABS(Demo Plan Annual Premium - Predicted Annual Premium)
    Sorted by:
        Difference ASC
    Matching indicators:
        <= 5% of predicted premium: "Very Close Match"
        <= 15% of predicted premium: "Close Match"
        Otherwise: "Alternative"
    """
    plans = InsurancePlan.query.filter_by(status="active").all()
    results = []
    for plan in plans:
        diff = round(abs(plan.annual_premium - predicted_premium), 2)
        diff_pct = (
            round(diff / predicted_premium * 100, 2)
            if predicted_premium
            else 0.0
        )

        if diff_pct <= 5.0:
            match_label = "Very Close Match"
            match_badge_class = "very-close"
        elif diff_pct <= 15.0:
            match_label = "Close Match"
            match_badge_class = "close"
        else:
            match_label = "Alternative"
            match_badge_class = "alternative"

        effective_duration = selected_duration if selected_duration else plan.policy_duration
        total_estimated = round(plan.annual_premium * effective_duration, 2)
        coverage_lakhs = plan.coverage_amount / 100000
        coverage_display = f"₹{coverage_lakhs:g} Lakhs"
        benefits_list = [b.strip() for b in plan.benefits.split(",") if b.strip()]

        results.append({
            "plan_id": plan.plan_id,
            "plan_name": plan.plan_name,
            "annual_premium": plan.annual_premium,
            "coverage_amount": plan.coverage_amount,
            "coverage_display": coverage_display,
            "policy_duration": plan.policy_duration,
            "effective_duration": effective_duration,
            "total_estimated_premium": total_estimated,
            "plan_description": plan.plan_description,
            "benefits": plan.benefits,
            "benefits_list": benefits_list,
            "difference": diff,
            "difference_pct": diff_pct,
            "match_label": match_label,
            "match_badge_class": match_badge_class,
            "is_closest": False,
        })

    results.sort(key=lambda x: x["difference"])
    if results:
        results[0]["is_closest"] = True

    return results[:limit]


def parse_form(form):
    """Validate and parse inputs from web forms."""
    try:
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
    except (KeyError, TypeError, ValueError):
        raise ValueError("Complete all prediction fields with valid values.")

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
    if values["sex"] not in {"female", "male"} or values["smoker"] not in {"yes", "no"}:
        raise ValueError("Choose valid gender and smoking values.")
    if values["region"] not in {"northeast", "northwest", "southeast", "southwest"}:
        raise ValueError("Choose a valid region.")
    return values


def build_recommendation(premium: float, salary: float, plan: str, duration: int) -> dict:
    """Generate plan-specific recommendation and estimated benefit calculations."""
    plan_details = {
        "basic": ("Basic", 1.05, "A cost-conscious plan for essential hospitalization protection."),
        "silver": ("Silver", 1.20, "A balanced plan providing comprehensive routine and critical care coverage."),
        "gold": ("Gold", 1.40, "A premium tier offering high sum insured, zero copay, and maximum coverage."),
    }
    label, benefit_rate, description = plan_details[plan]
    affordability = premium / salary if salary else 0
    if affordability > 0.12:
        note = "Notice: Estimated premium exceeds 12% of stated income. Consider selecting a higher deductible or adjusting coverage duration."
    elif affordability < 0.05:
        note = "Excellent affordability: Estimated premium represents less than 5% of stated income."
    else:
        note = "Healthy affordability: Estimated premium is proportionate to stated annual income."

    benefit = round(premium * duration * benefit_rate, 2)
    return {
        "plan": label,
        "description": f"{description} {note}",
        "benefit": benefit,
        "benefit_factor": benefit_rate,
    }


def load_metrics() -> dict:
    """Load train/test comparative model metrics from disk."""
    if not METRICS_PATH.exists():
        return {"results": [], "best_model": "Unavailable"}
    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        app.logger.warning("Unable to read model evaluation metrics", exc_info=True)
        return {"results": [], "best_model": "Unavailable"}


def analytics_payload(records: list[Prediction]) -> dict:
    """Aggregate actual database records into comprehensive metrics for all 6 required charts."""
    premiums = [float(record.estimated_premium) for record in records]
    smoking_totals = {}
    plan_counts = {}
    monthly_counts = {}
    records_data = []

    for record in records:
        prem = float(record.estimated_premium)
        smk = record.smoker.title()
        plan_cat = record.plan_category.title()
        month = record.created_at.strftime("%Y-%m")

        smoking_totals.setdefault(smk, []).append(prem)
        plan_counts[plan_cat] = plan_counts.get(plan_cat, 0) + 1
        monthly_counts[month] = monthly_counts.get(month, 0) + 1

        records_data.append({
            "id": record.id,
            "age": record.age,
            "sex": record.sex,
            "bmi": float(record.bmi),
            "children": record.children,
            "smoker": record.smoker,
            "region": record.region,
            "plan": record.plan_category,
            "salary": float(record.salary),
            "premium": prem,
            "ratio": float(record.premium_income_ratio),
            "created_at": record.created_at.strftime("%Y-%m-%d %H:%M"),
            "month": month,
        })

    # 1. Premium Distribution Bins
    if premiums:
        minimum, maximum = min(premiums), max(premiums)
        if maximum == minimum:
            distribution = [{"label": f"INR {minimum:,.0f}", "count": len(premiums)}]
        else:
            width = max((maximum - minimum) / 5, 1)
            distribution = []
            for index in range(5):
                lower = minimum + index * width
                upper = maximum if index == 4 else lower + width
                count = sum(lower <= p <= upper if index == 4 else lower <= p < upper for p in premiums)
                distribution.append({
                    "label": f"₹{lower:,.0f} - ₹{upper:,.0f}",
                    "count": count,
                })
    else:
        distribution = []

    most_rec_plan = max(plan_counts.items(), key=lambda x: x[1])[0] if plan_counts else "—"

    smoking_avg = [
        {"label": label, "premium": round(sum(values) / len(values), 2)}
        for label, values in sorted(smoking_totals.items())
    ]

    sorted_monthly = [
        {"label": label, "count": count}
        for label, count in sorted(monthly_counts.items())
    ]

    sorted_plans = [
        {"label": label, "count": count}
        for label, count in sorted(plan_counts.items())
    ]

    return {
        "total_count": len(records),
        "average_premium": round(sum(premiums) / len(premiums), 2) if premiums else None,
        "most_recommended_plan": most_rec_plan,
        "premium_distribution": distribution,
        "age_vs_premium": [
            {"age": r.age, "premium": float(r.estimated_premium), "smoker": r.smoker, "plan": r.plan_category}
            for r in records
        ],
        "bmi_vs_premium": [
            {"bmi": float(r.bmi), "premium": float(r.estimated_premium), "smoker": r.smoker, "plan": r.plan_category}
            for r in records
        ],
        "smoking_average": smoking_avg,
        "plan_counts": sorted_plans,
        "monthly_counts": sorted_monthly,
        "records_data": records_data,
    }


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = db.session.get(User, session.get("user_id"))
        if user is None or user.role != "admin":
            abort(403)
        return view(*args, **kwargs)

    return wrapped_view


def owned_prediction(prediction_id: int) -> Prediction:
    """Retrieve prediction ensuring user ownership or administrator privilege."""
    prediction = db.session.get(Prediction, prediction_id)
    if prediction is None:
        abort(404)
    user = db.session.get(User, session.get("user_id"))
    if prediction.user_id != session.get("user_id") and (user is None or user.role != "admin"):
        abort(403)
    return prediction


# =====================================================================
# AUTHENTICATION ROUTES
# =====================================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirm_password", request.form.get("confirmPassword", ""))

        if not name or not email or not password:
            flash("Name, email, and password are required.", "error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
        elif password != confirmation:
            flash("Passwords do not match.", "error")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "error")
        else:
            user = User()
            user.name = name
            user.email = email
            user.password_hash = generate_password_hash(password)
            user.phone = request.form.get("phone", "").strip() or None
            dob_value = request.form.get("dob", "").strip()
            if dob_value:
                try:
                    user.dob = datetime.strptime(dob_value, "%Y-%m-%d").date()
                except ValueError:
                    flash("Date of birth must be valid.", "error")
                    return render_template("register.html")
            db.session.add(user)
            db.session.commit()
            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_role"] = user.role
            flash("Registration successful! Welcome to HealthSecure.", "success")
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
            session["user_role"] = user.role
            destination = request.args.get("next")
            if user.role == "admin" and not destination:
                return redirect(url_for("admin_dashboard"))
            return redirect(destination if destination and destination.startswith("/") else url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email or "@" not in email:
            flash("Please enter a valid email address.", "error")
        else:
            flash(f"Password reset instructions have been dispatched to {email}.", "success")
            return redirect(url_for("forgot_password"))
    return render_template("forgot_password.html")


# =====================================================================
# PREDICTION & AUTOMATIC DEMO PLAN RECOMMENDATION
# =====================================================================

@app.route("/", methods=["GET", "POST"])
def index():
    """Modern AI health insurance landing page."""
    if request.method == "POST":
        return predict()
    metrics = load_metrics()
    plans = InsurancePlan.query.filter_by(status="active").all()
    insights = feature_insights()
    return render_template("index.html", metrics=metrics, plans=plans, insights=insights)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """Interactive multi-factor premium calculator and recommendation engine."""
    if request.method == "POST" and "user_id" not in session:
        return redirect(url_for("login", next=url_for("predict")))
    result = None
    form_data = request.form.to_dict()
    if request.method == "POST":
        try:
            values = parse_form(request.form)
            predicted_charge = predict_premium(values)
            duration = int(request.form.get("policy_duration", 5))
            plan = request.form.get("plan_category", "silver")
            if duration not in {5, 10, 15, 20}:
                raise ValueError("Choose a policy duration of 5, 10, 15, or 20 years.")
            if plan not in {"basic", "silver", "gold"}:
                raise ValueError("Choose a valid insurance plan.")

            recommendation = build_recommendation(predicted_charge, values["salary"], plan, duration)
            ratio = round(predicted_charge / values["salary"] * 100, 2)
            total_premium = round(predicted_charge * duration, 2)
            benefit_factor = recommendation["benefit_factor"]

            # AUTOMATIC DEMO PLAN MATCHING ALGORITHM
            matching_plans = get_matching_plans(predicted_charge, limit=3, selected_duration=duration)
            closest_plan = matching_plans[0] if matching_plans else None

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
            prediction.premium_income_ratio = ratio
            prediction.total_premium = total_premium
            prediction.benefit_factor = benefit_factor
            prediction.estimated_benefit = round(total_premium * benefit_factor, 2)
            prediction.estimated_premium = predicted_charge
            prediction.recommended_plan_id = closest_plan["plan_id"] if closest_plan else None
            prediction.user_id = session.get("user_id")
            db.session.add(prediction)
            db.session.commit()

            # Save recommendation records
            saved_recommendation = Recommendation()
            saved_recommendation.prediction_id = prediction.id
            saved_recommendation.plan_name = recommendation["plan"]
            saved_recommendation.policy_years = duration
            saved_recommendation.annual_premium = predicted_charge
            saved_recommendation.total_premium = total_premium
            saved_recommendation.estimated_benefit = prediction.estimated_benefit
            saved_recommendation.benefit_factor = benefit_factor
            db.session.add(saved_recommendation)
            db.session.commit()

            # Feature 1: Comprehensive Explainable AI (XAI) insights
            explanation = explain_prediction(values, predicted_charge)

            result = {
                **recommendation,
                "premium": predicted_charge,
                "duration": duration,
                "ratio": ratio,
                "total_premium": total_premium,
                "benefit": prediction.estimated_benefit,
                "prediction_id": prediction.id,
                "explanation": explanation,
                "insights": explanation["insights"],
                "matching_plans": matching_plans,
                "closest_plan": closest_plan,
            }
            flash("Prediction calculated! Matching demo plans found.", "success")
        except (KeyError, TypeError, ValueError) as error:
            flash(str(error) or "Please enter valid values.", "error")
        except Exception:
            app.logger.exception("Prediction calculation failed")
            flash("The prediction could not be completed. Please try again.", "error")
    return render_template("predict.html", result=result, form_data=form_data)


@app.route("/result")
@app.route("/result/<int:prediction_id>")
@login_required
def result(prediction_id=None):
    """Direct result view displaying ML estimate, automatic matching demo plans, and XAI."""
    if prediction_id is None:
        prediction = (
            Prediction.query.filter_by(user_id=session["user_id"])
            .order_by(Prediction.created_at.desc())
            .first()
        )
        if not prediction:
            flash("Please make a prediction first to view results.", "error")
            return redirect(url_for("index"))
    else:
        prediction = owned_prediction(prediction_id)

    matching_plans = get_matching_plans(
        prediction.estimated_premium,
        limit=3,
        selected_duration=prediction.policy_duration,
    )
    closest_plan = matching_plans[0] if matching_plans else None

    pred_dict = {
        "age": prediction.age,
        "sex": prediction.sex,
        "bmi": prediction.bmi,
        "children": prediction.children,
        "smoker": prediction.smoker,
        "region": prediction.region,
        "salary": prediction.salary,
        "full_name": prediction.full_name,
    }
    explanation = explain_prediction(pred_dict, prediction.estimated_premium)

    return render_template(
        "result.html",
        prediction=prediction,
        matching_plans=matching_plans,
        closest_plan=closest_plan,
        explanation=explanation,
        insights=explanation["insights"],
    )


@app.route("/recommended-plans/<int:prediction_id>")
@login_required
def recommended_plans(prediction_id):
    """Dedicated route to inspect recommended demo plans for a prediction."""
    return redirect(url_for("result", prediction_id=prediction_id))


@app.route("/plan/<int:plan_id>")
def plan_details(plan_id):
    """Detailed specifications for an individual demo insurance plan."""
    plan = db.session.get(InsurancePlan, plan_id)
    if not plan:
        abort(404)

    prediction_id = request.args.get("prediction_id", type=int)
    prediction = None
    if prediction_id and "user_id" in session:
        prediction = owned_prediction(prediction_id)
    elif "user_id" in session:
        prediction = (
            Prediction.query.filter_by(user_id=session["user_id"])
            .order_by(Prediction.created_at.desc())
            .first()
        )

    diff = None
    diff_pct = None
    match_label = None
    match_badge_class = None
    effective_duration = plan.policy_duration

    if prediction:
        diff = round(abs(plan.annual_premium - prediction.estimated_premium), 2)
        diff_pct = (
            round(diff / prediction.estimated_premium * 100, 2)
            if prediction.estimated_premium
            else 0.0
        )
        if diff_pct <= 5.0:
            match_label = "Very Close Match"
            match_badge_class = "very-close"
        elif diff_pct <= 15.0:
            match_label = "Close Match"
            match_badge_class = "close"
        else:
            match_label = "Alternative"
            match_badge_class = "alternative"
        if prediction.policy_duration:
            effective_duration = prediction.policy_duration

    total_estimated = round(plan.annual_premium * effective_duration, 2)
    benefits_list = [b.strip() for b in plan.benefits.split(",") if b.strip()]
    all_plans = InsurancePlan.query.filter_by(status="active").all()

    return render_template(
        "plan_details.html",
        plan=plan,
        prediction=prediction,
        difference=diff,
        difference_pct=diff_pct,
        match_label=match_label,
        match_badge_class=match_badge_class,
        effective_duration=effective_duration,
        total_estimated_premium=total_estimated,
        benefits_list=benefits_list,
        all_plans=all_plans,
    )


@app.route("/compare-plans")
def compare_plans():
    """Side-by-side comparison for up to 3 demo insurance plans."""
    prediction_id = request.args.get("prediction_id", type=int)
    prediction = None
    if prediction_id and "user_id" in session:
        prediction = owned_prediction(prediction_id)
    elif "user_id" in session:
        prediction = (
            Prediction.query.filter_by(user_id=session["user_id"])
            .order_by(Prediction.created_at.desc())
            .first()
        )

    all_active_plans = InsurancePlan.query.filter_by(status="active").all()

    selected_plan_ids_raw = request.args.getlist("plans")
    if not selected_plan_ids_raw:
        # Check comma separated
        param = request.args.get("plans")
        if param:
            selected_plan_ids_raw = param.split(",")

    selected_ids = []
    for x in selected_plan_ids_raw:
        try:
            selected_ids.append(int(x))
        except (ValueError, TypeError):
            pass

    selected_ids = selected_ids[:3]

    if not selected_ids:
        if prediction:
            ranked = get_matching_plans(
                prediction.estimated_premium,
                limit=3,
                selected_duration=prediction.policy_duration,
            )
            selected_ids = [p["plan_id"] for p in ranked]
        else:
            selected_ids = [p.plan_id for p in all_active_plans[:3]]

    selected_plans = [p for p in all_active_plans if p.plan_id in selected_ids]

    compared_data = []
    for plan in selected_plans:
        effective_duration = (
            prediction.policy_duration
            if (prediction and prediction.policy_duration)
            else plan.policy_duration
        )
        total_estimated = round(plan.annual_premium * effective_duration, 2)
        diff = None
        diff_pct = None
        match_label = None
        match_badge_class = None

        if prediction:
            diff = round(abs(plan.annual_premium - prediction.estimated_premium), 2)
            diff_pct = (
                round(diff / prediction.estimated_premium * 100, 2)
                if prediction.estimated_premium
                else 0.0
            )
            if diff_pct <= 5.0:
                match_label = "Very Close Match"
                match_badge_class = "very-close"
            elif diff_pct <= 15.0:
                match_label = "Close Match"
                match_badge_class = "close"
            else:
                match_label = "Alternative"
                match_badge_class = "alternative"

        compared_data.append({
            "plan": plan,
            "coverage_display": f"₹{plan.coverage_amount / 100000:g} Lakhs",
            "effective_duration": effective_duration,
            "total_estimated": total_estimated,
            "difference": diff,
            "difference_pct": diff_pct,
            "match_label": match_label,
            "match_badge_class": match_badge_class,
            "benefits_list": [b.strip() for b in plan.benefits.split(",") if b.strip()],
            "is_closest": False,
        })

    if prediction and compared_data:
        sorted_by_diff = sorted(
            compared_data,
            key=lambda x: x["difference"] if x["difference"] is not None else 999999,
        )
        sorted_by_diff[0]["is_closest"] = True

    return render_template(
        "compare_plans.html",
        prediction=prediction,
        compared_data=compared_data,
        all_active_plans=all_active_plans,
        selected_ids=selected_ids,
    )


@app.route("/prediction/<int:prediction_id>")
@login_required
def prediction_details(prediction_id):
    """Comprehensive details, matched demo plans, and Explainable AI breakdown for a saved estimate."""
    prediction = owned_prediction(prediction_id)
    pred_dict = {
        "age": prediction.age,
        "sex": prediction.sex,
        "bmi": prediction.bmi,
        "children": prediction.children,
        "smoker": prediction.smoker,
        "region": prediction.region,
        "salary": prediction.salary,
        "full_name": prediction.full_name,
    }
    explanation = explain_prediction(pred_dict, prediction.estimated_premium)
    matching_plans = get_matching_plans(
        prediction.estimated_premium,
        limit=3,
        selected_duration=prediction.policy_duration,
    )
    return render_template(
        "prediction_details.html",
        prediction=prediction,
        insights=explanation["insights"],
        explanation=explanation,
        matching_plans=matching_plans,
        closest_plan=matching_plans[0] if matching_plans else None,
        active_tab="details",
    )


@app.route("/ai-insights")
@login_required
def ai_insights_latest():
    """Redirect to the AI insights for the user's latest prediction."""
    latest = (
        Prediction.query.filter_by(user_id=session["user_id"])
        .order_by(Prediction.created_at.desc())
        .first()
    )
    if not latest:
        flash("Create a prediction first to view AI insights.", "error")
        return redirect(url_for("index"))
    return redirect(url_for("ai_insights", prediction_id=latest.id))


@app.route("/ai-insights/<int:prediction_id>")
@login_required
def ai_insights(prediction_id):
    """Dedicated Explainable AI view for a specific prediction."""
    return prediction_details(prediction_id)


# =====================================================================
# FEATURE 2: WHAT-IF / SCENARIO SIMULATOR
# =====================================================================

@app.route("/what-if")
@login_required
def what_if():
    prediction_id = request.args.get("prediction_id", type=int)
    user_predictions = (
        Prediction.query.filter_by(user_id=session["user_id"])
        .order_by(Prediction.created_at.desc())
        .all()
    )
    if not user_predictions:
        flash("Create an initial prediction before opening the scenario simulator.", "error")
        return redirect(url_for("index"))

    prediction = (
        owned_prediction(prediction_id)
        if prediction_id
        else user_predictions[0]
    )
    return render_template(
        "what_if.html",
        prediction=prediction,
        user_predictions=user_predictions,
        scenario=None,
        changes=[],
        form_data={},
    )


@app.route("/what-if/predict", methods=["POST"])
@login_required
def what_if_predict():
    user_predictions = (
        Prediction.query.filter_by(user_id=session["user_id"])
        .order_by(Prediction.created_at.desc())
        .all()
    )
    try:
        prediction_id = int(request.form["prediction_id"])
        prediction = owned_prediction(prediction_id)
        form_data = request.form.to_dict()
        form_data["full_name"] = prediction.full_name
        values = parse_form(form_data)
        scenario_premium = predict_premium(values)
        difference = round(scenario_premium - prediction.estimated_premium, 2)
        percentage = (
            round(difference / prediction.estimated_premium * 100, 2)
            if prediction.estimated_premium
            else 0
        )

        changes = []
        if values["age"] != prediction.age:
            changes.append(f"Age: {prediction.age} → {values['age']} yrs")
        if values["sex"] != prediction.sex:
            changes.append(f"Gender: {prediction.sex.title()} → {values['sex'].title()}")
        if round(values["bmi"], 1) != round(prediction.bmi, 1):
            changes.append(f"BMI: {prediction.bmi:.1f} → {values['bmi']:.1f}")
        if values["children"] != prediction.children:
            changes.append(f"Children: {prediction.children} → {values['children']}")
        if values["smoker"] != prediction.smoker:
            changes.append(f"Smoker: {prediction.smoker.title()} → {values['smoker'].title()}")
        if values["region"] != prediction.region:
            changes.append(f"Region: {prediction.region.title()} → {values['region'].title()}")
        if values["salary"] != prediction.salary:
            changes.append(f"Salary: INR {prediction.salary:,.0f} → INR {values['salary']:,.0f}")

        scenario = {
            "premium": scenario_premium,
            "difference": difference,
            "percentage": percentage,
            "new_ratio": round(scenario_premium / values["salary"] * 100, 2) if values["salary"] else 0,
        }
    except (KeyError, TypeError, ValueError) as error:
        flash(str(error) or "Enter valid scenario values.", "error")
        return redirect(url_for("what_if", prediction_id=request.form.get("prediction_id")))

    return render_template(
        "what_if.html",
        prediction=prediction,
        user_predictions=user_predictions,
        scenario=scenario,
        changes=changes,
        form_data=form_data,
    )


# =====================================================================
# FEATURE 3: ML MODEL COMPARISON & PERFORMANCE
# =====================================================================

@app.route("/model-performance")
@login_required
def model_performance():
    return render_template(
        "model_performance.html",
        metrics=load_metrics(),
        model_meta=get_model_meta(),
        admin_view=False,
    )


@app.route("/admin/model-performance")
@login_required
@admin_required
def admin_model_performance():
    return render_template(
        "model_performance.html",
        metrics=load_metrics(),
        model_meta=get_model_meta(),
        admin_view=True,
    )


# =====================================================================
# FEATURE 4: ADVANCED ANALYTICS DASHBOARD
# =====================================================================

@app.route("/dashboard")
@login_required
def dashboard():
    user = db.session.get(User, session["user_id"])
    all_records = (
        Prediction.query.filter_by(user_id=session["user_id"])
        .order_by(Prediction.created_at.desc())
        .all()
    )
    records = all_records[:5]
    prediction_count = len(all_records)
    latest = all_records[0] if all_records else None

    latest_matching_plans = []
    if latest:
        latest_matching_plans = get_matching_plans(
            latest.estimated_premium,
            limit=3,
            selected_duration=latest.policy_duration,
        )

    return render_template(
        "dashboard.html",
        records=records,
        user=user,
        prediction_count=prediction_count,
        latest=latest,
        latest_matching_plans=latest_matching_plans,
        analytics=analytics_payload(all_records),
    )


@app.route("/admin/analytics")
@login_required
@admin_required
def admin_analytics():
    records = Prediction.query.order_by(Prediction.created_at.desc()).all()
    return render_template(
        "analytics.html",
        analytics=analytics_payload(records),
        admin_view=True,
    )


# =====================================================================
# FEATURE 5: PROFESSIONAL PDF PREDICTION REPORT
# =====================================================================

@app.route("/download-report/<int:prediction_id>")
@login_required
def download_report(prediction_id):
    prediction = owned_prediction(prediction_id)
    member = db.session.get(User, prediction.user_id) if prediction.user_id else None
    pred_dict = {
        "age": prediction.age,
        "sex": prediction.sex,
        "bmi": prediction.bmi,
        "children": prediction.children,
        "smoker": prediction.smoker,
        "region": prediction.region,
        "salary": prediction.salary,
        "full_name": prediction.full_name,
    }
    explanation = explain_prediction(pred_dict, prediction.estimated_premium)
    insights = explanation["insights"]
    matching_plans = get_matching_plans(
        prediction.estimated_premium,
        limit=3,
        selected_duration=prediction.policy_duration,
    )
    pdf_buffer = generate_pdf_report(
        prediction,
        member,
        insights,
        explanation,
        matching_plans=matching_plans,
    )

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"healthsecure-report-{prediction.id}.pdf",
        mimetype="application/pdf",
    )


# =====================================================================
# ADDITIONAL USER & ADMIN ROUTES
# =====================================================================

@app.route("/history")
@login_required
def history():
    records = (
        Prediction.query.filter_by(user_id=session["user_id"])
        .order_by(Prediction.created_at.desc())
        .limit(100)
        .all()
    )
    return render_template("history.html", records=records)


@app.route("/plans")
def insurance_plans():
    """Recommended insurance plan tiers and policy explanation."""
    all_plans = InsurancePlan.query.filter_by(status="active").all()
    return render_template("plans.html", demo_plans=all_plans)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = db.session.get(User, session["user_id"])
    if user is None:
        session.clear()
        flash("Your session has expired. Please log in again.", "error")
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        duplicate = User.query.filter(User.email == email, User.id != user.id).first()
        if not name or "@" not in email:
            flash("Name and a valid email are required.", "error")
        elif duplicate:
            flash("That email is already in use.", "error")
        else:
            user.name = name
            user.email = email
            user.phone = request.form.get("phone", "").strip() or None
            dob_value = request.form.get("dob", "").strip()
            try:
                user.dob = datetime.strptime(dob_value, "%Y-%m-%d").date() if dob_value else None
            except ValueError:
                flash("Date of birth must be valid.", "error")
                return render_template("profile.html", user=user)
            db.session.commit()
            session["user_name"] = user.name
            flash("Profile updated successfully.", "success")
    return render_template("profile.html", user=user)


@app.route("/change-password", methods=["POST"])
@login_required
def change_password():
    user = db.session.get(User, session["user_id"])
    if user is None:
        session.clear()
        flash("Your session has expired. Please log in again.", "error")
        return redirect(url_for("login"))
    current = request.form.get("current_password", "")
    password = request.form.get("password", "")
    confirmation = request.form.get("confirm_password", "")
    if not check_password_hash(user.password_hash, current) or len(password) < 8 or password != confirmation:
        flash("Password change failed. Check current password and confirmation (minimum 8 characters).", "error")
    else:
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        flash("Password updated successfully.", "success")
    return redirect(url_for("profile"))


@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    predictions = Prediction.query.order_by(Prediction.created_at.desc()).limit(15).all()
    all_predictions = Prediction.query.order_by(Prediction.created_at.desc()).all()
    return render_template(
        "admin_dashboard.html",
        users=User.query.order_by(User.id.desc()).limit(15).all(),
        predictions=predictions,
        user_count=User.query.count(),
        prediction_count=Prediction.query.count(),
        recommendation_count=Recommendation.query.count(),
        analytics=analytics_payload(all_predictions),
    )


@app.route("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}, 200


if __name__ == "__main__":
    app.run(debug=True)
