# ML Training and Testing Report

**Generated:** 17 November 2026, 00:50 IST  
**Dataset:** Indian Health Insurance Underwriting & Claims Dataset (`data/insurance.csv`)  
**Target variable:** `charges` (Actuarial Annual Premium in INR ₹)  

---

## 1. Dataset and Split

| Item | Value |
|---|---:|
| Total records | 8,000 |
| Training records | 6,400 |
| Testing records | 1,600 |
| Test ratio | 20% |
| Random state | 42 |

**Features Evaluated:** Age (18–85), Gender (`female`/`male`), BMI (15–44), Children (0–3), Smoker Status (`yes`/`no`), Geographic Region (`Delhi`, `Karnataka`, `Maharashtra`, `Tamil Nadu`, `Uttar Pradesh`, `West Bengal`), Alcohol Consumption (`yes`/`no`), and Annual Income (INR ₹).

---

## 2. Models Benchmarked

| Model Evaluated | Test MAE (INR ₹) | Test MSE | Test RMSE (INR ₹) | Test $R^2$ Score |
| :--- | :--- | :--- | :--- | :--- |
| **Linear Regression (Selected)** | **₹2,615.84** | **11,686,946.46** | **₹3,418.62** | **0.6492 (64.9%)** |
| **XGBoost Regressor** | ₹2,629.69 | 11,863,578.29 | ₹3,444.35 | 0.6439 (64.4%) |
| **Gradient Boosting Regressor** | ₹2,640.68 | 11,908,669.51 | ₹3,450.89 | 0.6425 (64.2%) |
| **Random Forest Regressor** | ₹2,776.21 | 13,262,480.05 | ₹3,641.77 | 0.6019 (60.2%) |

### Selected Production Model
**Linear Regression** was selected as the primary production regressor because it achieved the lowest test MAE (**₹2,615.84**) and the highest $R^2$ score (**0.6492**), while maintaining fast, deterministic inferences with high interpretability. The trained pipeline is serialized at `models/premium_model.joblib`.

---

## 3. Visual Performance Artifacts

The following evaluation plots have been generated and archived in the `models/` directory:
1. **Model Comparison Benchmark:** `model_comparison.png` (Comparison of MAE and $R^2$ variance across all regressors).
2. **Actual vs. Predicted Scatter:** `actual_vs_predicted.png` (Scatter plot of 1,600 test predictions against the $y = x$ reference line).
3. **Residuals Distribution:** `residuals_distribution.png` (Histogram and error spread demonstrating normal distribution centered at ₹0).
4. **Feature Attribution (XAI):** `feature_importance.png` (Relative attribution weights across clinical and demographic features).

---

## 4. Example Test Predictions

| Actual Premium (₹) | Predicted Premium (₹) | Absolute Error (₹) | Accuracy Rate |
|---|---|---|---|
| ₹28,421.80 | ₹29,138.65 | ₹716.85 | 97.5% |
| ₹21,205.71 | ₹21,606.05 | ₹400.34 | 98.1% |
| ₹24,685.92 | ₹26,670.21 | ₹1,984.29 | 92.0% |
| ₹23,008.26 | ₹20,936.48 | ₹2,071.78 | 91.0% |
| ₹20,014.42 | ₹22,208.08 | ₹2,193.66 | 89.0% |
| ₹29,215.70 | ₹26,541.73 | ₹2,673.97 | 90.8% |
| ₹17,694.59 | ₹21,376.07 | ₹3,681.48 | 79.2% |
| ₹32,766.45 | ₹28,642.17 | ₹4,124.28 | 87.4% |
| ₹40,296.16 | ₹32,834.52 | ₹7,461.64 | 81.5% |
| ₹36,183.27 | ₹28,616.51 | ₹7,566.76 | 79.1% |

---

## 5. Metric Definitions
* **MAE (Mean Absolute Error):** Average absolute deviation between actual and predicted annual premiums; lower is better.
* **RMSE (Root Mean Squared Error):** Square root of the mean squared error penalizing large outlier errors; lower is better.
* **$R^2$ (Coefficient of Determination):** Proportion of variance in annual premium explained by the model features (0.6492 = 64.9% variance explained).
