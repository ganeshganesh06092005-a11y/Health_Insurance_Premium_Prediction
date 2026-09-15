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
FEATURES = ["age", "sex", "bmi", "children", "smoker", "region", "salary"]
FEATURE_RANGES = {
    "age": (18, 100),
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
    region = rng.choice(["northeast", "northwest", "southeast", "southwest"], rows)
    salary = np.clip(180000 + age * 6500 + rng.normal(0, 90000, rows), 100000, 10000000)
    charges = (1200 + age * 250 + bmi * 110 + children * 350
               + (smoker == "yes") * (17000 + age * 140)
               + (bmi >= 30) * 1200 + rng.normal(0, 1800, rows))
    return pd.DataFrame({"age": age, "sex": sex, "bmi": bmi, "children": children,
                         "smoker": smoker, "region": region, "salary": salary.round(0),
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
        ("categories", OneHotEncoder(handle_unknown="ignore"), ["sex", "smoker", "region"]),
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
