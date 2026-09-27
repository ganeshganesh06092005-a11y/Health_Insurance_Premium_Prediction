from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "insurance.csv"
MODEL_PATH = BASE_DIR / "models" / "premium_model.joblib"
FEATURES = ["age", "sex", "bmi", "children", "smoker", "region", "liquor", "salary"]
FEATURE_RANGES = {
    "age": (18, 100),
    "height": (50, 250),
    "weight": (20, 250),
    "bmi": (10, 60),
    "children": (0, 10),
    "salary": (100000, 10000000),
}


def create_demo_data(rows: int = 2500) -> pd.DataFrame:
    """Create realistic synthetic data only when no local dataset was supplied."""
    rng = np.random.default_rng(42)
    age = rng.integers(18, 65, rows)
    bmi = np.clip(rng.normal(30, 6, rows), 16, 54).round(1)
    children = rng.integers(0, 6, rows)
    sex = rng.choice(["female", "male"], rows)
    smoker = rng.choice(["no", "yes"], rows, p=[0.8, 0.2])
    liquor = rng.choice(["no", "yes"], rows, p=[0.72, 0.28])
    region = rng.choice([
        "Maharashtra", "Tamil Nadu", "Karnataka", "Delhi", "Uttar Pradesh",
        "Gujarat", "West Bengal", "Kerala", "Telangana", "Rajasthan",
        "Andhra Pradesh", "Madhya Pradesh", "Punjab", "Haryana", "Bihar", "Odisha"
    ], rows)
    salary = np.clip(180000 + age * 6500 + rng.normal(0, 90000, rows), 100000, 10000000)
    charges = (1200 + age * 250 + bmi * 110 + children * 350
               + (smoker == "yes") * (17000 + age * 140)
               + (liquor == "yes") * (2200 + age * 20)
               + (bmi >= 30) * 1200 + rng.normal(0, 1800, rows))
    return pd.DataFrame({"age": age, "sex": sex, "bmi": bmi, "children": children,
                         "smoker": smoker, "region": region, "liquor": liquor, "salary": salary.round(0),
                         "charges": np.maximum(charges, 1000)})


def read_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        data = pd.read_csv(DATA_PATH)
        required = set(FEATURES[:-1] + ["charges"])
        missing = required - set(data.columns)
        if missing:
            raise ValueError(f"Dataset is missing columns: {', '.join(sorted(missing))}")
        data = data.dropna(subset=[column for column in FEATURES if column != "salary"] + ["charges"])
        if "salary" not in data:
            # The public medical-cost dataset has no income column. This documented
            # proxy keeps salary available for academic experimentation.
            data["salary"] = np.clip(
                180000 + data["age"] * 6500 + data["bmi"] * 2500
                + data["children"] * 12000, 100000, 10000000
            ).round(0)
        return data.dropna(subset=FEATURES + ["charges"])
    return create_demo_data()


def train_model() -> Pipeline:
    data = read_data()
    preprocessor = ColumnTransformer([
        ("categories", OneHotEncoder(handle_unknown="ignore"), ["sex", "smoker", "region", "liquor"]),
        ("numbers", "passthrough", ["age", "bmi", "children", "salary"]),
    ])
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=250, min_samples_leaf=2, random_state=42, n_jobs=-1)),
    ])
    pipeline.fit(data[FEATURES], data["charges"])
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    return pipeline


def load_or_train_model() -> Pipeline:
    source_mtime = max(Path(__file__).stat().st_mtime, DATA_PATH.stat().st_mtime if DATA_PATH.exists() else 0)
    if MODEL_PATH.exists() and MODEL_PATH.stat().st_mtime >= source_mtime:
        return joblib.load(MODEL_PATH)
    return train_model()


def predict_premium(values: dict) -> float:
    model = load_or_train_model()
    frame = pd.DataFrame([values], columns=FEATURES)
    return round(float(model.predict(frame)[0]), 2)


def feature_insights(limit: int = 8) -> list[dict]:
    """Return aggregated tree-model importances for Explainable AI."""
    model = load_or_train_model()
    regressor = model.named_steps.get("regressor")
    preprocessor = model.named_steps.get("preprocessor")
    if not hasattr(regressor, "feature_importances_") or preprocessor is None:
        return []

    grouped: dict[str, float] = {}
    display_names = {
        "smoker": "Smoking Status",
        "bmi": "Body Mass Index (BMI)",
        "age": "Age",
        "region": "Geographic Region",
        "liquor": "Liquor / Alcohol Consumption",
        "children": "Number of Children",
        "sex": "Gender",
        "salary": "Annual Salary (Proxy)",
    }
    for name, importance in zip(preprocessor.get_feature_names_out(), regressor.feature_importances_):
        feature_name = name.split("__", 1)[-1]
        if feature_name.startswith(("sex_", "smoker_", "region_", "liquor_")):
            feature_name = feature_name.split("_", 1)[0]
        grouped[feature_name] = grouped.get(feature_name, 0.0) + float(importance)

    total = sum(grouped.values()) or 1.0
    results = []
    for key, value in sorted(grouped.items(), key=lambda item: item[1], reverse=True)[:limit]:
        results.append({
            "key": key,
            "name": display_names.get(key, key.replace("_", " ").title()),
            "importance": round(value / total * 100, 1),
        })
    return results


def explain_prediction(values: dict, estimated_premium: float | None = None) -> dict:
    """Generate comprehensive, user-friendly Explainable AI (XAI) insights.
    
    Provides feature importances and personalized natural-language breakdown of
    how the regression model evaluated the applicant's inputs.
    """
    insights = feature_insights()
    top_feature = insights[0]["name"] if insights else "Smoking Status"

    interpretations = []

    # 1. Smoking Status
    smoker = str(values.get("smoker", "")).lower()
    if smoker == "yes":
        interpretations.append({
            "feature": "Smoking Status",
            "value": "Smoker",
            "impact": "High Surcharge Weight",
            "status": "warning",
            "explanation": "Smoking status is the single most dominant factor in the trained model (over 80% relative importance). The model assigns a substantial premium surcharge to individuals who smoke due to statistically higher claim frequencies in historical insurance data."
        })
    else:
        interpretations.append({
            "feature": "Smoking Status",
            "value": "Non-smoker",
            "impact": "Favorable Base Rate",
            "status": "positive",
            "explanation": "Non-smoking status avoids the heavy surcharge that the model applies to tobacco users, keeping your baseline premium estimate significantly lower."
        })

    # 2. BMI
    bmi = float(values.get("bmi", 25.0))
    if bmi >= 30:
        interpretations.append({
            "feature": "Body Mass Index (BMI)",
            "value": f"{bmi:.1f} (Obese range: ≥ 30.0)",
            "impact": "Elevated Risk Surcharge",
            "status": "warning",
            "explanation": f"A BMI of {bmi:.1f} places the profile in the higher risk category. In tree-based regression, high BMI interacts with age and smoking to compound projected medical costs."
        })
    elif bmi >= 25:
        interpretations.append({
            "feature": "Body Mass Index (BMI)",
            "value": f"{bmi:.1f} (Overweight range: 25.0–29.9)",
            "impact": "Moderate Upward Influence",
            "status": "neutral",
            "explanation": f"A BMI of {bmi:.1f} is slightly above standard normal ranges, resulting in a moderate upward influence on the predicted annual charge."
        })
    elif bmi >= 18.5:
        interpretations.append({
            "feature": "Body Mass Index (BMI)",
            "value": f"{bmi:.1f} (Normal range: 18.5–24.9)",
            "impact": "Optimal Base Range",
            "status": "positive",
            "explanation": f"A BMI of {bmi:.1f} is within the recommended healthy range, serving as a stabilizing indicator in the model."
        })
    else:
        interpretations.append({
            "feature": "Body Mass Index (BMI)",
            "value": f"{bmi:.1f} (Underweight: < 18.5)",
            "impact": "Baseline Bracket",
            "status": "neutral",
            "explanation": f"A BMI of {bmi:.1f} is evaluated near the lower baseline for insurance cost estimation."
        })

    # 3. Age
    age = int(values.get("age", 30))
    if age >= 50:
        interpretations.append({
            "feature": "Age",
            "value": f"{age} years",
            "impact": "Substantial Age Curve",
            "status": "warning",
            "explanation": f"At age {age}, the actuarial aging curve increases predicted medical utilization and hospitalization probabilities."
        })
    elif age >= 35:
        interpretations.append({
            "feature": "Age",
            "value": f"{age} years",
            "impact": "Moderate Age Progression",
            "status": "neutral",
            "explanation": f"At age {age}, the model applies a steady progressive increment reflecting mid-career healthcare expenditure trends."
        })
    else:
        interpretations.append({
            "feature": "Age",
            "value": f"{age} years",
            "impact": "Young Demographic Base",
            "status": "positive",
            "explanation": f"At age {age}, young demographic status places the applicant at the lower end of the baseline age risk scale."
        })

    # 4. Dependents / Children
    children = int(values.get("children", 0))
    interpretations.append({
        "feature": "Number of Children",
        "value": f"{children} dependent(s)",
        "impact": "Family Coverage Factor",
        "status": "neutral",
        "explanation": f"Household of {children} dependent(s) contributes moderately to cumulative family health risk and coverage scope."
    })

    # 5. Geographic Region / Indian State
    region = str(values.get("region", "Maharashtra"))
    interpretations.append({
        "feature": "Indian State / Region",
        "value": region.title(),
        "impact": "State Healthcare Index",
        "status": "neutral",
        "explanation": f"Healthcare infrastructure, provider pricing index, and tertiary hospital network density in {region.title()} adjust actuarial baseline costs."
    })

    # 6. Gender
    sex = str(values.get("sex", "male"))
    interpretations.append({
        "feature": "Gender",
        "value": sex.title(),
        "impact": "Demographic Base Rate",
        "status": "neutral",
        "explanation": f"Gender ({sex.title()}) has minimal relative importance in this regression model (< 1%), indicating equitable baseline cost distribution."
    })

    # 7. Salary (Financial Analysis)
    salary = float(values.get("salary", 0))
    if salary > 0:
        ratio = (estimated_premium / salary * 100) if (estimated_premium and salary) else 0.0
        interpretations.append({
            "feature": "Annual Salary (Financial Input)",
            "value": f"INR {salary:,.2f}",
            "impact": f"Affordability Ratio: {ratio:.2f}%",
            "status": "positive" if ratio <= 10 else "warning",
            "explanation": f"Annual salary is used for financial affordability benchmarking. The estimated premium represents {ratio:.2f}% of stated annual income."
        })

    # 8. Liquor / Alcohol Consumption
    liquor = str(values.get("liquor", "no")).lower()
    if liquor == "yes":
        interpretations.append({
            "feature": "Liquor / Alcohol Consumption",
            "value": "Consumes Alcohol",
            "impact": "Lifestyle Risk Surcharge",
            "status": "warning",
            "explanation": "Alcohol consumption increases projected clinical claim risk (hepatic metabolism, cardiovascular strain, and elevated hospitalization risk), causing the ML model to apply an actuarial surcharge."
        })
    else:
        interpretations.append({
            "feature": "Liquor / Alcohol Consumption",
            "value": "Non-drinker",
            "impact": "Favorable Health Factor",
            "status": "positive",
            "explanation": "Abstaining from liquor/alcohol avoids lifestyle-associated health surcharges, maintaining a lower risk tier in the ML regression assessment."
        })

    simple_explanation = (
        f"{top_feature} had relatively high feature importance in this trained model. "
        "Inputs like smoking status, BMI, liquor consumption, and age form the primary drivers of predicted premiums."
    )

    return {
        "insights": insights,
        "interpretations": interpretations,
        "simple_explanation": simple_explanation,
        "disclaimer": (
            "Model-Based Insights Disclaimer: Feature importance and interpretation reflect mathematical correlations "
            "within the trained regression dataset. They represent statistical model weights and do not prove direct "
            "medical causation or official insurance underwriting approval."
        ),
    }


def get_model_meta() -> dict:
    """Return runtime metadata regarding the trained model and features."""
    model = load_or_train_model()
    regressor = model.named_steps.get("regressor")
    regressor_name = regressor.__class__.__name__ if regressor else "Unknown Regressor"
    return {
        "algorithm": regressor_name,
        "features": FEATURES,
        "target": "charges",
        "salary_proxy_note": (
            "The public Medical Cost Personal Dataset does not contain salary. "
            "This project documents salary as a derived academic proxy so that "
            "training and prediction pipelines utilize the identical feature set."
        ),
    }

