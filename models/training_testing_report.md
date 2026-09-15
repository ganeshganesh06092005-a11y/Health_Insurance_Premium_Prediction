# ML Training and Testing Report

**Generated:** 14 September 2026, 13:07 UTC  
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

Features: age, sex, BMI, number of children, smoker status, region, and salary. The public source dataset does not include salary, so this educational project derives a documented academic proxy. It is not an actual salary measure.

## Models tested

| model | MAE | MSE | RMSE | R2 |
|---|---|---|---|---|
| Linear Regression | 4181.19 | 33596915.82 | 5796.28 | 0.7836 |
| Random Forest Regressor | 2481.62 | 20769964.88 | 4557.41 | 0.8662 |
| XGBoost Regressor | 2374.08 | 18778544.88 | 4333.42 | 0.879 |

## Selected model

**XGBoost Regressor** was selected because it had the lowest test MAE: **2,374.08**. Its test R² score is **0.8790**. The selected model is saved as `models/premium_model.joblib`.

## Example test predictions

| actual_charge | predicted_charge | absolute_error |
|---|---|---|
| 9095.07 | 12096.0 | 3000.93 |
| 5272.18 | 5861.080078125 | 588.9 |
| 29330.98 | 29735.599609375 | 404.62 |
| 9301.89 | 10673.2802734375 | 1371.38 |
| 33750.29 | 33395.30078125 | 354.99 |
| 4536.26 | 5282.2099609375 | 745.95 |
| 2117.34 | 2110.469970703125 | 6.86 |
| 14210.54 | 16220.2099609375 | 2009.67 |
| 3732.63 | 4213.25 | 480.62 |
| 10264.44 | 10552.8896484375 | 288.44 |

## Metric definitions

- **MAE:** Average absolute prediction error; lower is better.
- **MSE:** Average squared error; lower is better.
- **RMSE:** Square root of MSE in the target's units; lower is better.
- **R²:** Variation in charges explained by the model; closer to 1 is better.

## Limitation

This is an educational model using a small anonymized dataset. It must not be used for actual insurance underwriting, pricing, eligibility, or any other high-impact decision without fairness testing, validation, governance, and regulatory review.
