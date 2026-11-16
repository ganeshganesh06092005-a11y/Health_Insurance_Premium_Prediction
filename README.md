# HealthSecure &ndash; Smart Insurance Prediction System
**MCA Final-Year Project:** *Health Insurance Premium Prediction Using Machine Learning*  
**Brand:** HealthSecure &ndash; Smart Insurance Prediction Powered by Machine Learning

---

## 1. Project Overview & Architecture

**HealthSecure** is an enterprise-grade AI web application engineered to predict health insurance premiums using machine learning regression algorithms, recommend tailored insurance policies, and provide actuarial explainability (XAI) and what-if decision simulation for policyholders and underwriters.

The system is trained on an **Indian Health Insurance Underwriting & Claims Dataset (8,000 records)** spanning 6 major states, evaluating 8 core clinical, demographic, and financial factors:
1. **Age**: Chronological age (18 to 85 years).
2. **Gender**: Binary demographic indicator (`female`, `male`).
3. **Height & Weight (Dynamic BMI)**: Height in cm and Weight in kg used to compute Body Mass Index ($\text{BMI} = \text{Weight} / (\text{Height}/100)^2$) in real time.
4. **Smoking Status**: Tobacco usage status (`yes` / `no`).
5. **Liquor / Alcohol Consumption**: Alcohol consumption indicator (`yes` / `no`).
6. **Children / Covered Dependents**: Number of dependents (0 to 3).
7. **Geographic Region**: State classification (`Delhi`, `Karnataka`, `Maharashtra`, `Tamil Nadu`, `Uttar Pradesh`, `West Bengal`).
8. **Annual Income (Salary)**: Stated annual income used for affordability benchmarking and underwriting tiers.

---

## 2. Technology Stack

- **Backend:** Python 3.10+, Flask 3.1, Flask-SQLAlchemy 3.1, PyMySQL
- **Database:** MySQL 8.0+ / MariaDB (InnoDB, utf8mb4)
- **Machine Learning & Data Science:** Scikit-Learn 1.6+, XGBoost 2.0+, Pandas 2.2+, NumPy 2.0+, Joblib 1.4+, Matplotlib 3.11+
- **Reporting Engine:** ReportLab 5.1+ (PDF report generation)
- **Email Service:** Python MIME & Secure SMTP Dispatch with TLS/SSL
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Chart.js (v4), Inter & Georgia Typography
- **Internationalization:** Multi-language system (English, Tamil `தமிழ்`, Hindi `हिन्दी`)
- **Theme:** Dynamic Light and Dark Mode system with persistent client storage

---

## 3. Project Structure

```
Health_Insurance_Premium_Prediction/
│
├── app.py                            # Flask application routes, session control & database models
├── model.py                          # ML model preprocessing pipeline, prediction & Explainable AI (XAI)
├── train.py                          # Multi-model benchmarking, training & report generation
├── email_service.py                  # SMTP email dispatch service for PDF reports
├── translations.py                   # Multi-language translation dictionaries (EN, TA, HI)
├── plans_data.py                     # Multi-insurer catalog (118+ demo policies across 8 leading insurers)
├── report_generator.py               # Professional ReportLab PDF generation engine
├── test_5_features.py                # Comprehensive 13-test automated test suite
├── database.sql                      # MySQL schema, indexes, and administrator seed script
├── migration_v2.sql                  # Database migration script for advanced features
├── requirements.txt                  # Python dependencies
├── README.md                         # Complete project documentation & guide
├── .env.example                      # Environment configuration template
├── .env                              # Local configuration (database & SMTP credentials, git-ignored)
│
├── data/
│   ├── insurance.csv                 # Active 8,000-record Indian Health Insurance dataset
│   └── README.md                     # Dataset documentation & actuarial schema mapping
│
├── models/
│   ├── premium_model.joblib          # Active production serialized ML pipeline
│   ├── evaluation_metrics.json       # Calculated test-set metrics (MAE, MSE, RMSE, R²)
│   ├── training_testing_report.md    # Markdown test evaluation report
│   ├── model_comparison.png          # Visual benchmark comparison (MAE and R²)
│   ├── actual_vs_predicted.png       # Scatter plot of actual vs. predicted annual premiums
│   ├── residuals_distribution.png    # Normal error distribution histogram
│   └── feature_importance.png        # Explainable AI feature attribution plot
│
├── templates/
│   ├── index.html                    # Modern AI health insurance landing page (18 sections)
│   ├── predict.html                  # Standalone premium calculator & recommendation output
│   ├── result.html                   # Automatic demo plan recommendations result view
│   ├── prediction_details.html       # Individual prediction details & Explainable AI breakdown
│   ├── plan_details.html             # Individual demo policy specifications & difference metrics
│   ├── compare_plans.html            # Side-by-side 3-plan decision comparison matrix
│   ├── plans.html                    # Insurance coverage catalog & active database directory
│   ├── favorites.html                # Bookmarked / favorite insurance plans
│   ├── notifications.html            # In-app notifications center
│   ├── history.html                  # Saved prediction history with direct action buttons
│   ├── what_if.html                  # What-If lifestyle scenario simulator
│   ├── model_performance.html        # Live ML model comparison & metrics benchmark
│   ├── dashboard.html                # Member analytics dashboard with 6 Chart.js charts
│   ├── profile.html                  # User profile and credential management
│   ├── admin_dashboard.html          # Administrator control center & user directory
│   ├── analytics.html                # System-wide analytics & telemetry
│   ├── login.html                    # User authentication portal with demo login
│   ├── register.html                 # User registration interface
│   └── forgot_password.html          # Password reset interface
│
└── static/
    ├── css/
    │   ├── landing.css               # Dedicated landing page stylesheet (deep teal & mint)
    │   └── style.css                 # HealthSecure main stylesheet
    ├── js/
    │   ├── landing.js                # Landing page interactive scripts & preview simulator
    │   ├── script.js                 # Interactive 6-chart filtering & reactive KPI calculations
    │   ├── theme.js                  # Dark / Light theme toggle engine
    │   └── translator.js             # Client-side dynamic language translation handler
    ├── images/                       # UI visual assets
    ├── auth.js                       # Password visibility toggle utility
    └── style.css                     # Root stylesheet reference
```

---

## 4. Key Advanced Features

### 1. Actuarial Annual Premium Machine Learning Engine
- **Algorithm:** Linear Regression with One-Hot Categorical Encoding and numeric passthrough.
- **Accuracy:** Test $R^2 = \mathbf{0.6492}$ (64.9% variance explained), Test $\text{MAE} = \mathbf{₹2,615.84}$.
- **Prominent Output:** Displays prominent **Annual Premium (INR/year)** at the very top of results, alongside monthly breakdown chips (`≈ ₹1,417/mo`) and daily affordability estimates.

### 2. Multi-Insurer Plan Recommendation System
- Curates from a catalog of **118+ demo insurance policies** across 8 leading insurers:
  1. Star Health & Allied Insurance
  2. Care Health Insurance
  3. HDFC ERGO General Insurance
  4. ICICI Lombard General Insurance
  5. Bajaj Allianz General Insurance
  6. The New India Assurance Co.
  7. United India Insurance
  8. HealthSecure AI Direct
- Automatically ranks plans by minimum premium difference, compatibility match score, and claim settlement ratio (CSR).

### 3. Explainable AI (XAI)
- Calculates feature attribution percentages showing exactly how clinical and demographic inputs contributed to the premium calculation.
- Generates natural language actuarial interpretations for BMI classification, age tiering, and smoking surcharge.

### 4. What-If Scenario Simulator (`/what-if`)
- Enables policyholders to evaluate potential savings from positive health interventions (e.g., smoking cessation, reducing BMI, or shifting policy duration).
- Interactive before-and-after premium comparison charts powered by Chart.js.

### 5. PDF Prediction Reports with Secure SMTP Email Dispatch
- Generates publication-grade, downloadable PDF reports using ReportLab.
- One-click **Email Report** button dispatches reports directly to applicant inboxes via secure SMTP.

### 6. Multi-Language System (`translations.py`, `translator.js`)
- Full trilingual support: **English**, **Tamil (`தமிழ்`)**, and **Hindi (`हिन्दी`)**.
- Instant in-browser language switching with zero page reloads.

### 7. Dark Mode & Responsive Theming (`theme.js`)
- Seamless toggle between light and dark themes with persistent `localStorage` state.

### 8. Bookmarks / Plan Favorites (`favorites.html`)
- Allows members to save and manage favorite policies for subsequent side-by-side comparison.

---

## 5. Getting Started & Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/ganeshganesh06092005-a11y/Health_Insurance_Premium_Prediction.git
cd Health_Insurance_Premium_Prediction
```

### Step 2: Configure Virtual Environment & Install Dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env` and fill in your MySQL credentials:
```ini
SECRET_KEY=your-random-secret-key
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=health_insurance_db

# SMTP Configuration (Optional, for email reports)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=HealthSecure AI <your-email@gmail.com>
```

### Step 4: Initialize MySQL Database
```powershell
mysql -u root -p < database.sql
mysql -u root -p health_insurance_db < migration_v2.sql
```

### Step 5: Retrain or Benchmark Models (Optional)
```powershell
python train.py
```

### Step 6: Start the Application
```powershell
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser!

---

## 6. Pre-seeded Demo Logins

| Role | Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Member** | `user@healthsecure.com` | `User@123` | Prediction calculator, What-If simulator, plan favorites, PDF report export |
| **Administrator** | `admin@healthsecure.com` | `Admin@123` | Full admin portal, telemetry, user governance, plan catalog management |

---

## 7. Running the Test Suite

Execute the 13-test automated test suite:
```powershell
python -m unittest test_5_features.py
```
```text
Ran 13 tests in 1.15s — OK (All tests passed)
```
