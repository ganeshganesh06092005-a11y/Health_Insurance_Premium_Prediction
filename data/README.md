# HealthSecure Dataset Documentation

## Active Dataset: Indian Health Insurance Underwriting & Claims Dataset
* **Filename:** `insurance.csv`
* **Records:** 8,000 policyholders
* **Raw Schema:** 38 clinical, underwriting, financial, and claim attributes
* **File Size:** ~2.7 MB

---

## 1. Domain & Scope
This dataset reflects retail health insurance policyholders and hospitalization claims across major Indian states (`Delhi`, `Karnataka`, `Maharashtra`, `Tamil Nadu`, `Uttar Pradesh`, `West Bengal`). It provides multi-dimensional health metrics, lifestyle habits, hospital billing records, and claims experience.

---

## 2. Core Feature Mapping for Machine Learning

| Model Feature | Source Column | Description | Valid Range / Values |
| :--- | :--- | :--- | :--- |
| **`age`** | `age` | Applicant chronological age | 18 &ndash; 85 years |
| **`sex`** | `gender` | Standardized biological sex | `female`, `male` |
| **`bmi`** | `bmi` | Body Mass Index (kg/m²) | 15.0 &ndash; 44.0 |
| **`children`** | `policy_type` / `children` | Number of covered dependents | 0 &ndash; 3 children |
| **`smoker`** | `tobacco_usage` | Tobacco consumption status | `no` (none), `yes` (smoking/chewing) |
| **`region`** | `state` | Indian state of residence | `Delhi`, `Karnataka`, `Maharashtra`, `Tamil Nadu`, `Uttar Pradesh`, `West Bengal` |
| **`liquor`** | `alcohol_units_per_week` | Alcohol consumption indicator | `no` (0 units), `yes` (&gt;0 units/wk) |
| **`salary`** | `annual_income_inr` | Annual stated income (INR ₹) | ₹1,50,000 &ndash; ₹47,00,000 |
| **`charges`** *(Target)* | Actuarial Formula | Actuarial Annual Premium (INR/year) | ₹10,100 &ndash; ₹95,000 (Mean: ~₹23,570/yr) |

---

## 3. Actuarial Annual Premium Target Formulation
In insurance underwriting, medical expenses (`total_claim_amount`) represent potential risk exposure, whereas **Annual Premium** represents the recurring policy cost paid by the policyholder.

The target variable `charges` is calibrated using standard actuarial pure-premium principles:

$$\begin{aligned}
\text{Annual Premium (₹/year)} = &\ 5,000 + (\text{Age} \times 180) + (\text{Total Claim Exposure} \times 6\%) \\
&+ (\text{Smoker Surcharge: ₹4,500}) + (\max(\text{BMI} - 25, 0) \times 250) \\
&+ (\text{Alcohol Factor: ₹1,200}) + (\text{Children Cover: ₹2,200/child})
\end{aligned}$$

This ensures the ML model predicts realistic, consumer-grade annual premiums (₹12,000 &ndash; ₹35,000/year) rather than full hospital bill amounts.
