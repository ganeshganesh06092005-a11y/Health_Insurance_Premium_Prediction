"""Train, test, compare, and report insurance premium regression models.

Run: python train.py
Outputs: models/premium_model.joblib, models/evaluation_metrics.json,
and models/training_testing_report.md.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from model import FEATURES, MODEL_PATH, read_data


RANDOM_STATE = 42
TEST_SIZE = 0.20
REPORT_PATH = Path("models") / "training_testing_report.md"
METRICS_PATH = Path("models") / "evaluation_metrics.json"


def make_pipeline(regressor) -> Pipeline:
    """Use identical preprocessing across candidates for a fair comparison."""
    preprocessor = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), ["sex", "smoker", "region"]),
        ("numeric", "passthrough", ["age", "bmi", "children", "salary"]),
    ])
    return Pipeline([("preprocessor", preprocessor), ("regressor", regressor)])


def evaluate_model(name, pipeline, x_train, x_test, y_train, y_test):
    pipeline.fit(x_train, y_train)
    predicted = pipeline.predict(x_test)
    mse = float(mean_squared_error(y_test, predicted))
    metrics = {
        "model": name,
        "MAE": round(float(mean_absolute_error(y_test, predicted)), 2),
        "MSE": round(mse, 2),
        "RMSE": round(mse ** 0.5, 2),
        "R2": round(float(r2_score(y_test, predicted)), 4),
    }
    samples = pd.DataFrame({
        "actual_charge": y_test.to_numpy(),
        "predicted_charge": predicted,
        "absolute_error": abs(y_test.to_numpy() - predicted),
    }).head(10).round(2)
    return pipeline, metrics, samples


def markdown_table(frame: pd.DataFrame) -> str:
    headers = list(frame.columns)
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def write_report(dataset_rows, train_rows, test_rows, results, best_result, sample_rows) -> None:
    metrics_table = pd.DataFrame(results)[["model", "MAE", "MSE", "RMSE", "R2"]]
    report = f"""# ML Training and Testing Report

**Generated:** {datetime.now(timezone.utc).strftime('%d %B %Y, %H:%M UTC')}  
**Dataset:** Medical Cost Personal Dataset (`data/insurance.csv`)  
**Target variable:** `charges`

## Dataset and split

| Item | Value |
|---|---:|
| Total records | {dataset_rows} |
| Training records | {train_rows} |
| Testing records | {test_rows} |
| Test ratio | {int(TEST_SIZE * 100)}% |
| Random state | {RANDOM_STATE} |

Features: age, sex, BMI, number of children, smoker status, region, and salary. The public source dataset does not include salary, so this educational project derives a documented academic proxy. It is not an actual salary measure.

## Models tested

{markdown_table(metrics_table)}

## Selected model

**{best_result['model']}** was selected because it had the lowest test MAE: **{best_result['MAE']:,.2f}**. Its test R² score is **{best_result['R2']:.4f}**. The selected model is saved as `models/premium_model.joblib`.

## Example test predictions

{markdown_table(sample_rows)}

## Metric definitions

- **MAE:** Average absolute prediction error; lower is better.
- **MSE:** Average squared error; lower is better.
- **RMSE:** Square root of MSE in the target's units; lower is better.
- **R²:** Variation in charges explained by the model; closer to 1 is better.

## Limitation

This is an educational model using a small anonymized dataset. It must not be used for actual insurance underwriting, pricing, eligibility, or any other high-impact decision without fairness testing, validation, governance, and regulatory review.
"""
    REPORT_PATH.write_text(report.replace("  \n", "\n"), encoding="utf-8")


def main() -> None:
    data = read_data()
    x_train, x_test, y_train, y_test = train_test_split(
        data[FEATURES], data["charges"], test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    candidates = [
        ("Linear Regression", make_pipeline(LinearRegression())),
        ("Random Forest Regressor", make_pipeline(RandomForestRegressor(
            n_estimators=350, min_samples_leaf=2, random_state=RANDOM_STATE, n_jobs=-1
        ))),
        ("Gradient Boosting Regressor", make_pipeline(GradientBoostingRegressor(
            n_estimators=250, learning_rate=0.04, max_depth=3, random_state=RANDOM_STATE
        ))),
    ]
    try:
        from xgboost import XGBRegressor
        candidates.append(("XGBoost Regressor", make_pipeline(XGBRegressor(
            n_estimators=400, learning_rate=0.05, max_depth=3,
            objective="reg:squarederror", random_state=RANDOM_STATE, n_jobs=-1,
        ))))
    except ImportError:
        print("XGBoost is not installed; using Linear Regression and Random Forest.")

    runs = [evaluate_model(name, pipeline, x_train, x_test, y_train, y_test)
            for name, pipeline in candidates]
    best_pipeline, best_result, best_samples = min(runs, key=lambda run: run[1]["MAE"])

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(best_pipeline, MODEL_PATH)
    all_results = [metrics for _, metrics, _ in runs]
    METRICS_PATH.write_text(json.dumps({
        "dataset_rows": len(data), "training_rows": len(x_train), "testing_rows": len(x_test),
        "best_model": best_result["model"], "results": all_results,
    }, indent=2), encoding="utf-8")
    write_report(len(data), len(x_train), len(x_test), all_results, best_result, best_samples)

    print("Training and testing complete.")
    for result in all_results:
        print(f"{result['model']}: MAE={result['MAE']}, RMSE={result['RMSE']}, R²={result['R2']}")
    print(f"Selected model: {best_result['model']}")
    print(f"Report saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
