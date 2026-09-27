# ML Training and Testing Report

**Generated:** 27 September 2026, 18:00 UTC
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
| Linear Regression | 4195.37 | 33382061.37 | 5777.72 | 0.7966 |
| Random Forest Regressor | 2499.4 | 20678901.62 | 4547.41 | 0.874 |
| Gradient Boosting Regressor | 2552.66 | 19980332.24 | 4469.94 | 0.8783 |
| XGBoost Regressor | 2422.94 | 18251536.24 | 4272.18 | 0.8888 |

## Selected model

**XGBoost Regressor** was selected because it had the lowest test MAE: **2,422.94**. Its test R² score is **0.8888**. The selected model is saved as `models/premium_model.joblib`.

## Example test predictions

| actual_charge | predicted_charge | absolute_error |
|---|---|---|
| 9095.07 | 11831.169921875 | 2736.1 |
| 8021.91 | 9850.8095703125 | 1828.9 |
| 32819.9 | 34210.44140625 | 1390.54 |
| 9301.89 | 11010.509765625 | 1708.62 |
| 33750.29 | 34549.76953125 | 799.48 |
| 4536.26 | 5512.7998046875 | 976.54 |
| 2117.34 | 1471.8399658203125 | 645.5 |
| 14210.54 | 14906.1103515625 | 695.57 |
| 3732.63 | 3466.340087890625 | 266.29 |
| 10264.44 | 10460.4599609375 | 196.02 |

## Metric definitions

- **MAE:** Average absolute prediction error; lower is better.
- **MSE:** Average squared error; lower is better.
- **RMSE:** Square root of MSE in the target's units; lower is better.
- **R²:** Variation in charges explained by the model; closer to 1 is better.

## Limitation

This is an educational model using a small anonymized dataset. It must not be used for actual insurance underwriting, pricing, eligibility, or any other high-impact decision without fairness testing, validation, governance, and regulatory review.
