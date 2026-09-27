# HealthSecure &ndash; Smart Insurance Prediction System
**MCA Final-Year Project:** *Health Insurance Premium Prediction Using Machine Learning*  
**Brand:** HealthSecure &ndash; Smart Insurance Prediction

---

## 1. Project Overview & Architecture

**HealthSecure** is an enterprise-grade web application built to predict health insurance premiums using machine learning regression algorithms, recommend tailored health insurance plans, and provide explainability (XAI) and decision simulation for applicants and underwriters.

The project is built on the **Medical Cost Personal Dataset**, augmented with realistic actuarial liquor consumption indicators and financial affordability benchmarks, evaluating 8 core features:
1. **Age**: Chronological age (18 to 100).
2. **Gender**: Binary demographic indicator (Female / Male).
3. **Height & Weight (Dynamic BMI)**: Height in cm and Weight in kg used to compute Body Mass Index ($\text{BMI} = \text{Weight} / (\text{Height}/100)^2$) in real time.
4. **Smoking Status**: Tobacco usage status (Smoker / Non-smoker).
5. **Liquor / Alcohol Consumption**: Alcohol drinking status (Yes / No) with learned actuarial medical surcharge.
6. **Children / Dependents**: Number of dependents (0 to 10).
7. **Geographic Region**: 4-class regional classification (Northeast, Northwest, Southeast, Southwest).
8. **Annual Stated Salary**: Financial indicator used for affordability benchmarking.

- **Backend:** Python 3.10+, Flask 3.1, Flask-SQLAlchemy 3.1, PyMySQL
- **Database:** MySQL 8.0+ / MariaDB (InnoDB, utf8mb4)
- **Machine Learning & Data Science:** Scikit-Learn 1.4+, XGBoost 2.0+, Pandas 2.1+, NumPy 1.26+, Joblib 1.3+
- **Reporting Engine:** ReportLab 4.0+
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Chart.js (v4), Inter & Georgia Typography
- **Security:** Werkzeug password hashing (Scrypt/PBKDF2), HTTP sessions, role-based authorization (`user` vs `admin`), parameterized SQL.

---

## 3. Project Structure

```
health-insurance-project/
│
├── app.py                            # Flask application routes, session control & database models
├── model.py                          # ML model loading, preprocessing pipeline & Explainable AI (XAI)
├── train.py                          # Multi-model training, test evaluation & report generation
├── report_generator.py               # Professional ReportLab PDF generation engine
├── database.sql                      # MySQL schema, indexes, and administrator seed script
├── requirements.txt                  # Python dependencies
├── README.md                         # Complete project documentation & MCA viva guide
├── .env.example                      # Environment variables template
├── .env                              # Local configuration (database credentials & secret key)
│
├── data/
│   ├── insurance.csv                 # Medical Cost Personal Dataset (1,338 records)
│   └── README.md                     # Dataset documentation & source citations
│
├── models/
│   ├── premium_model.joblib          # Active production serialized ML pipeline
│   ├── evaluation_metrics.json       # Actual calculated test-set metrics (MAE, MSE, RMSE, R²)
│   └── training_testing_report.md    # Markdown test evaluation report
│
├── templates/
│   ├── index.html                    # Modern, unique AI health insurance landing page (18 sections)
│   ├── predict.html                  # Standalone premium calculator & recommendation output
│   ├── result.html                   # Automatic demo plan recommendations result view
│   ├── plan_details.html             # Individual demo policy specifications & difference metrics
│   ├── compare_plans.html            # Side-by-side 3-plan decision comparison matrix
│   ├── login.html                    # User authentication portal (deep teal aesthetic)
│   ├── register.html                 # User account creation
│   ├── forgot_password.html          # Password reset interface
│   ├── dashboard.html                # Member analytics dashboard with 6 Chart.js charts & recommended plans
│   ├── what_if.html                  # Feature 2: What-If / Scenario Simulator
│   ├── model_performance.html        # Feature 3: ML Model Comparison & Metrics Benchmark
│   ├── prediction_details.html       # Individual prediction details & Explainable AI breakdown
│   ├── history.html                  # Saved prediction history with direct action buttons
│   ├── plans.html                    # Insurance coverage tiers & active database catalog
│   ├── profile.html                  # User profile and credential management
│   ├── admin_dashboard.html          # Administrator control center & user directory
│   └── analytics.html                # Administrator system-wide analytics & telemetry
│
└── static/
    ├── css/
    │   ├── landing.css               # Dedicated landing page stylesheet (deep teal & mint)
    │   └── style.css                 # HealthSecure stylesheet (dark teal/navy theme)
    ├── js/
    │   ├── landing.js                # Landing page mobile drawer, FAQ accordion & preview simulator
    │   └── script.js                 # Interactive 6-chart filtering & reactive KPI calculations
    ├── auth.js                       # Password visibility toggle utility
    └── style.css                     # Root stylesheet reference
```

---

## 4. Summary of the Five Advanced Features

### Feature 1 &mdash; Explainable AI (XAI)
- **Problem Solved:** Machine learning models often function as opaque "black boxes," leaving applicants uncertain why their premium is high or low.
- **Implementation:** Extracts `feature_importances_` from the trained ensemble model (XGBoost / Random Forest) across one-hot encoded categories and numeric variables.
- **Visual Presentation:** Displays "Factors Influencing Premium Prediction" with percentage progress bars (Smoking Status ~84%, BMI ~5.6%, Region ~3.2%, Age ~2.9%, Salary ~2.4%, Dependents ~0.8%, Gender ~0.5%).
- **Natural Language Interpretation:** Generates a personalized section titled *"How the model interpreted your information"* analyzing applicant BMI classification (Normal vs Obese), smoking surcharge, demographic aging curve, and income affordability ratio.
- **Academic Disclaimer:** Explicitly clarifies that feature importance denotes statistical correlation within historical insurance data, not clinical medical causation.

### Feature 2 &mdash; What-If / Scenario Simulator (`/what-if`)
- **Problem Solved:** Enables applicants to evaluate lifestyle interventions (e.g. smoking cessation, weight management) before purchasing coverage.
- **Implementation:** Displays the applicant's current profile (Age, BMI, Smoking, Children, Salary, Baseline Premium) alongside editable input controls.
- **Instant Recalculation:** Submits modified parameters to `/what-if/predict`, runs the ML pipeline, and returns the new estimated premium.
- **Comparison Visualization:** Displays Original Premium vs What-If Premium, absolute difference in INR, percentage difference badge, and a Chart.js comparison bar chart.
- **Academic Disclaimer:** Prominently states that simulations represent algorithmic estimates and not binding price guarantees.

### Feature 3 &mdash; ML Model Comparison (`/model-performance`)
- **Problem Solved:** Compares multiple candidate algorithms under identical preprocessing to select the best production model empirically.
- **Models Evaluated:**
  1. Linear Regression (Baseline)
  2. Random Forest Regressor (Ensemble Bagging)
  3. Gradient Boosting Regressor (Ensemble Boosting)
  4. XGBoost Regressor (Extreme Gradient Boosting)
- **Evaluation Metrics (Held-Out 20% Test Split &ndash; 268 records):**
  - **MAE:** Mean Absolute Error (currency deviation in INR)
  - **MSE:** Mean Squared Error
  - **RMSE:** Root Mean Squared Error
  - **R² Score:** Coefficient of Determination (variance explained)
- **Model Selection Justification:** XGBoost Regressor was selected because it achieved the lowest test MAE (₹2,374.08) and highest test R² (0.8790).
- **Viva Note:** Explains why continuous regression problems rely on MAE, RMSE, and R² rather than unsupported classification "accuracy %".

### Feature 4 &mdash; Advanced Analytics Dashboard (`/dashboard` & `/admin/analytics`)
- **Problem Solved:** Provides data-driven visibility into historical predictions, clinical risk trends, and plan popularity.
- **Interactive KPI Cards:** Total Predictions, Average Predicted Premium, Latest Prediction, and Most Recommended Plan.
- **Interactive Filtering Toolbar:** Live filtering by Plan (All, Basic, Silver, Gold), Smoking Status, Gender, and Region with instant recalculation.
- **Six Responsive Chart.js Visualizations:**
  1. *Premium Distribution:* Histogram grouping predictions into cost brackets.
  2. *Age vs Predicted Premium:* Scatter plot illustrating actuarial aging curve.
  3. *BMI vs Predicted Premium:* Scatter plot highlighting the risk inflection point at BMI &ge; 30.
  4. *Smoking Status vs Predicted Premium:* Bar chart contrasting smoker vs non-smoker averages.
  5. *Plan Recommendation Distribution:* Doughnut chart of coverage tier selections.
  6. *Predictions by Month:* Trend line tracking evaluation volume over time.
- **Data Scoping:** Regular users see only their private estimates; administrators access system-wide aggregated telemetry.

### Feature 5 &mdash; Professional PDF Prediction Report (`/download-report/<id>`)
- **Problem Solved:** Generates an official, publication-quality A4 verification summary suitable for faculty review, project evaluation, or user download.
- **Technology:** Python `reportlab` library with customized corporate styling.
- **Contains All 10 Required Sections:**
  1. Header banner with HealthSecure branding, report reference ID, and date.
  2. Applicant Information (Full Name, Account Email, Age, Gender).
  3. Clinical & Health Profile (BMI, Smoking Status, Children, Region).
  4. Financial Analysis (Annual Stated Salary, Premium-to-Income Ratio).
  5. Machine Learning Prediction (Estimated Annual Premium).
  6. Selected Plan Tier & Duration (Basic / Silver / Gold & Policy Term).
  7. Actuarial Calculation (Total Cumulative Premium).
  8. Protective Benefit Calculation (Benefit Factor Rate & Estimated Benefit Amount).
  9. Explainable AI Insights (Feature importance bars & model explanation).
  10. Recommended Demo Insurance Plans (Automatic Matching table with Closest Match star).
  11. Official Academic Disclaimer callout box.

### Feature 6 &mdash; Automatic Demo Insurance Plan Recommendation
- **Problem Solved:** An ML continuous premium prediction alone (e.g. ₹28,500/yr) leaves users wondering which concrete insurance policy matches their financial estimation. This feature dynamically queries configurable demo policies in MySQL and presents the top 3 closest matches with visual indicator badges and comparative analysis.
- **Mathematical Matching Algorithm:**
  $$\text{Difference} = |\text{Demo Plan Annual Premium} - \text{Predicted Annual Premium}|$$
  $$\text{Percentage Difference} = \frac{\text{Difference}}{\text{Predicted Annual Premium}} \times 100\%$$
- **Match Indicator Rules:**
  - **Very Close Match** (`<= 5%` difference): High alignment with predicted risk.
  - **Close Match** (`<= 15%` difference): Suitable viable protection tier.
  - **Alternative** (`> 15%` difference): Broader coverage or budget option.
  - The plan with `MIN(Difference)` is marked with the **"★ Closest Match"** highlight badge and persisted into the database (`prediction.recommended_plan_id`).
- **Configurable Database Catalog (`insurance_plans` table):**
  1. *HealthSecure Basic:* ₹19,999/yr, ₹3 Lakhs coverage, 5 years term.
  2. *HealthSecure Standard:* ₹27,999/yr, ₹5 Lakhs coverage, 10 years term.
  3. *HealthSecure Plus:* ₹30,500/yr, ₹7.5 Lakhs coverage, 10 years term.
  4. *HealthSecure Family:* ₹31,999/yr, ₹10 Lakhs coverage, 15 years term.
  5. *HealthSecure Premium:* ₹49,999/yr, ₹15 Lakhs coverage, 20 years term.
- **Dedicated Routes & Touchpoints:**
  - `GET /result` & `GET /result/<id>`: Full recommendation view displaying the prediction banner, 3 plan cards, match badges, and XAI section.
  - `GET /plan/<id>`: Detailed plan specification page with Sum Insured, Duration, Annual Premium, Total Outlay, and live difference from the user's active prediction.
  - `GET /compare-plans`: Side-by-side comparison matrix evaluating up to 3 demo plans simultaneously with dynamic multi-plan selection.
  - `GET /dashboard`: "Recommended Plans Near Your Predicted Premium" panel linked to the member's latest estimate.
  - `GET /download-report/<id>`: Embeds matched demo plans in the downloaded official ReportLab PDF.
- **Academic Disclaimer:** Prominently clarifies that all demo insurance plans are mock educational packages stored in MySQL for academic demonstration and do not constitute real commercial insurance contracts.

---

## 5. Machine Learning Dataset & Salary Documentation

### Dataset Details
- **Source:** Medical Cost Personal Dataset ([Kaggle](https://www.kaggle.com/datasets/mirichoi0218/insurance))
- **Total Records:** 1,338 rows
- **Raw Features:** `age`, `sex`, `bmi`, `children`, `smoker`, `region`, `charges`

### Transparent Handling of Salary
- The raw Kaggle dataset does **not** natively contain an income or salary column.
- For this academic project, an annual income attribute is used to calculate **financial affordability ratios** (Premium-to-Income Ratio) and ensure recommended coverage does not exceed sustainable household limits (&le; 10%).
- To ensure mathematical consistency between training and runtime inference, a deterministic academic proxy is computed:
  $$\text{Salary} = \text{clip}(180000 + \text{age} \times 6500 + \text{bmi} \times 2500 + \text{children} \times 12000, 100000, 10000000)$$
- **Crucial Rule:** The model was trained with the exact same 7-feature schema as used in production prediction. An untrained feature is never passed to the model.

---

## 6. Installation & Execution Guide

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.14
- MySQL Server 8.0+ running on `127.0.0.1:3306`

### Step 1: Clone or Navigate to the Project Directory
```powershell
cd "c:\Users\Lenovo\.codex\.chatgpt-projects\g-p-6a96ce3b0f408191ac70be5a047ab4ba"
```

### Step 2: Set Up Virtual Environment & Dependencies
```powershell
# Activate existing virtual environment
.\venv\Scripts\Activate.ps1

# (Optional) Reinstall/update requirements
pip install -r requirements.txt
```

### Step 3: MySQL Database Setup
Open MySQL command prompt or MySQL Workbench and execute `database.sql`:
```powershell
mysql -u root -p < database.sql
```
Alternatively, the application automatically verifies schema integrity, runs column compatibility checks, and seeds the default administrator account at startup.

### Step 4: Configure Environment Variables
Verify `.env` has your MySQL credentials:
```ini
SECRET_KEY=27caefad8987def527c4bb869fc2fbbf63f37f9fad825fe56fa69ac4c1ed7820
BENEFIT_FACTOR=1.2

MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=health_insurance_db
```

### Step 5: (Optional) Re-Train & Benchmark Models
To execute the multi-model comparison suite and generate evaluation metrics:
```powershell
python train.py
```
This evaluates Linear Regression, Random Forest, Gradient Boosting, and XGBoost, selects the optimal pipeline based on lowest test MAE, and updates `models/evaluation_metrics.json`.

### Step 6: Start the Flask Application
```powershell
python app.py
```
Access the application in your browser:
**`http://127.0.0.1:5000`**

---

## 7. Default Credentials for Evaluation

| Role | Email Address | Password | Privileges |
|---|---|---|---|
| **System Administrator** | `admin@healthsecure.com` | `Admin@123` | System Analytics, Model Performance, User Directory, Audit Logs |
| **Test Member** | `mcatest@example.com` | `Password@123` | Private Prediction Portfolio, What-If Simulator, PDF Download |

*New members can also register directly at `/register`.*

---

## 8. Test Prediction Example

To test an applicant profile:
- **Full Name:** Ramesh Kumar
- **Age:** 35
- **Gender:** Male
- **BMI:** 28.5 (Overweight range)
- **Children / Dependents:** 2
- **Smoking Status:** Non-smoker
- **Geographic Region:** Northwest
- **Annual Salary:** ₹6,00,000
- **Policy Duration:** 5 Years
- **Plan Category:** Silver Plan

**Expected Results:**
- **Estimated Annual Premium:** ~₹5,000 &ndash; ₹11,000 / year (non-smoker baseline).
- **Premium-to-Income Ratio:** ~1.2% &ndash; 2.0% (Well within the &le; 10% sustainable threshold).
- **Explainable AI Top Factor:** Non-smoker status identified as the primary mitigating factor avoiding the tobacco surcharge.
- **What-If Test:** Changing Smoking Status to **Smoker** increases estimated premium to ~₹35,000 &ndash; ₹42,000 / year (+300% surcharge), illustrating real-time model sensitivity.

---

## 9. Viva Presentation & Evaluation Notes

### Q1: What machine learning algorithm was selected and why?
**Answer:** The production pipeline uses **XGBoost Regressor** (with Random Forest as fallback). In benchmark testing on an 80/20 train-test partition of 1,338 records, XGBoost achieved the lowest test Mean Absolute Error (**MAE = ₹2,374.08**) and highest variance explained (**R² = 0.8790**), outperforming Linear Regression (MAE = ₹4,181.19, R² = 0.7836) and Random Forest (MAE = ₹2,481.62, R² = 0.8662).

### Q2: Why is classification accuracy percentage not reported?
**Answer:** Predicting medical insurance premiums is a **continuous regression task**, not a discrete classification problem. In continuous prediction, an exact dollar match is virtually zero probability. True regression evaluation requires error-based metrics:
- **MAE** measures average absolute dollar error.
- **RMSE** penalizes large outlier errors quadratically.
- **R²** measures the proportion of variance explained by the model relative to a mean baseline.

### Q3: How is Explainable AI (XAI) implemented without heavy runtime overhead?
**Answer:** The system extracts native `feature_importances_` from the trained ensemble decision trees. One-hot encoded dummy variables (e.g. `smoker_yes`, `smoker_no`) are aggregated back to their parent domain variables, normalized to 100%, and paired with rule-based natural language interpreters that explain clinical BMI brackets, tobacco surcharges, and demographic aging factors.

### Q4: How is data privacy and multi-tenancy handled?
**Answer:** All database operations are scoped using parameterized SQLAlchemy ORM queries. Route authorization ensures normal users access strictly their own predictions (`user_id = session["user_id"]`), while administrators access aggregated, anonymized system telemetry without exposing user password hashes.

### Q5: How does the Automatic Demo Insurance Plan Recommendation algorithm work?
**Answer:** After the ML model outputs a continuous annual premium, the system executes an automated search query over all active demo plans in MySQL (`insurance_plans`). It computes the absolute financial difference:
$$\text{Difference} = |\text{Plan Annual Premium} - \text{Predicted Annual Premium}|$$
The plans are sorted by `Difference ASC` and the top 3 are returned. Percentage deviation is calculated to apply standardized visual indicator badges:
- **&le; 5%:** "Very Close Match"
- **&le; 15%:** "Close Match"
- **> 15%:** "Alternative"
The single closest plan (`MIN(Difference)`) is designated as "Closest Match" and saved as a foreign key (`recommended_plan_id`) on the prediction record.

### Q6: What is an example of the matching logic for an MCA evaluation demo?
**Answer:** If the ML predicted annual premium is **₹28,500**:
1. **HealthSecure Standard** (Annual: ₹27,999): Difference = ₹501 (1.76% deviation &le; 5%) &rarr; **Very Close Match &amp; Closest Match**.
2. **HealthSecure Plus** (Annual: ₹30,500): Difference = ₹2,000 (7.02% deviation &le; 15%) &rarr; **Close Match**.
3. **HealthSecure Family** (Annual: ₹31,999): Difference = ₹3,499 (12.28% deviation &le; 15%) &rarr; **Close Match**.
This provides immediate, actionable decision support for the applicant.
