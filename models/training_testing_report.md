# ML Training and Testing Report

**Generated:** 27 September 2026, 17:27 UTC
**Dataset:** Medical Cost Personal Dataset (`data/insurance.csv`)
**Target variable:** `charges`

## Dataset and split

| Item | Value |
|---|---:|
| Total records | 1338 |
| Training records | 1070 |
| Testing records | 268 |
| Test ratio | 20% |
| Random state | 42 |

Features: age, sex, BMI, number of children, smoker status, region, liquor drinking, and salary. The public source dataset does not include salary, so this educational project derives a documented academic proxy. It is not an actual salary measure.

## Models tested

| model | MAE | MSE | RMSE | R2 |
|---|---|---|---|---|
| Linear Regression | 4178.66 | 33442558.88 | 5782.95 | 0.7963 |
| Random Forest Regressor | 2570.43 | 20892424.78 | 4570.82 | 0.8727 |
| Gradient Boosting Regressor | 2570.57 | 20094013.22 | 4482.63 | 0.8776 |
| XGBoost Regressor | 2476.26 | 19414850.55 | 4406.23 | 0.8817 |

## Selected model

**XGBoost Regressor** was selected because it had the lowest test MAE: **2,476.26**. Its test R² score is **0.8817**. The selected model is saved as `models/premium_model.joblib`.

## Example test predictions

| actual_charge | predicted_charge | absolute_error |
|---|---|---|
| 9095.07 | 12238.8203125 | 3143.75 |
| 8021.91 | 9142.1103515625 | 1120.2 |
| 32819.9 | 34330.76171875 | 1510.87 |
| 9301.89 | 11073.1396484375 | 1771.26 |
| 33750.29 | 33163.30078125 | 586.99 |
| 4536.26 | 5195.14990234375 | 658.89 |
| 2117.34 | 2051.4599609375 | 65.88 |
| 14210.54 | 15611.08984375 | 1400.55 |
| 3732.63 | 3878.840087890625 | 146.21 |
| 10264.44 | 10782.2099609375 | 517.77 |

## Metric definitions

- **MAE:** Average absolute prediction error; lower is better.
- **MSE:** Average squared error; lower is better.
- **RMSE:** Square root of MSE in the target's units; lower is better.
- **R²:** Variation in charges explained by the model; closer to 1 is better.

## Limitation

This is an educational model using a small anonymized dataset. It must not be used for actual insurance underwriting, pricing, eligibility, or any other high-impact decision without fairness testing, validation, governance, and regulatory review.
