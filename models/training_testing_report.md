# ML Training and Testing Report

**Generated:** 21 November 2026, 05:27 UTC
**Dataset:** Medical Cost Personal Dataset (`data/insurance.csv`)
**Target variable:** `charges`

## Dataset and split

| Item | Value |
|---|---:|
| Total records | 8000 |
| Training records | 6400 |
| Testing records | 1600 |
| Test ratio | 20% |
| Random state | 42 |

Features: age, sex, BMI, number of children, smoker status, region, liquor drinking, and salary. The public source dataset does not include salary, so this educational project derives a documented academic proxy. It is not an actual salary measure.

## Models tested

| model | MAE | MSE | RMSE | R2 |
|---|---|---|---|---|
| Linear Regression | 2615.84 | 11686946.46 | 3418.62 | 0.6492 |
| Random Forest Regressor | 2776.21 | 13262480.05 | 3641.77 | 0.6019 |
| Gradient Boosting Regressor | 2640.68 | 11908669.51 | 3450.89 | 0.6425 |
| XGBoost Regressor | 2629.69 | 11863578.29 | 3444.35 | 0.6439 |

## Selected model

**Linear Regression** was selected because it had the lowest test MAE: **2,615.84**. Its test R² score is **0.6492**. The selected model is saved as `models/premium_model.joblib`.

## Example test predictions

| actual_charge | predicted_charge | absolute_error |
|---|---|---|
| 28421.8 | 29138.65 | 716.85 |
| 36183.27 | 28616.51 | 7566.76 |
| 29215.7 | 26541.73 | 2673.97 |
| 24685.92 | 26670.21 | 1984.29 |
| 40296.16 | 32834.52 | 7461.64 |
| 21205.71 | 21606.05 | 400.34 |
| 20014.42 | 22208.08 | 2193.66 |
| 23008.26 | 20936.48 | 2071.78 |
| 17694.59 | 21376.07 | 3681.48 |
| 32766.45 | 28642.17 | 4124.28 |

## Metric definitions

- **MAE:** Average absolute prediction error; lower is better.
- **MSE:** Average squared error; lower is better.
- **RMSE:** Square root of MSE in the target's units; lower is better.
- **R²:** Variation in charges explained by the model; closer to 1 is better.

## Limitation

This is an educational model using a small anonymized dataset. It must not be used for actual insurance underwriting, pricing, eligibility, or any other high-impact decision without fairness testing, validation, governance, and regulatory review.
