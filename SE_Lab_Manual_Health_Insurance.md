# Software Engineering Laboratory Manual
## Health Insurance Premium Prediction and Policy Recommendation System (HealthSecure)

**Department of Computer Applications**  
**Nehru College of Management, Coimbatore, Tamil Nadu, India**  
**Student Authors:** Ganesh R, Dhivyadharshini P  
**Project Supervisor:** Ms. K. S. Surabhi, Assistant Professor  

---

## Exercise 1: Problem Definition and Feasibility Analysis

### Aim
To analyze the operational challenges in manual health insurance pricing and carry out technical, economic, and operational feasibility assessments for building our automated predictive platform, HealthSecure.

### Project Title
Health Insurance Premium Prediction and Multi-Policy Recommendation System (HealthSecure)

### Problem Identification
Underwriting health policies through traditional insurance workflows is slow, non-transparent, and prone to subjective human error. Most existing insurers still compute annual quotes using rigid demographic lookups and coarse risk brackets. As a consequence, prospective policyholders cannot see how specific biological metrics such as Body Mass Index (BMI), tobacco use, alcohol habits, dependents, or geographic hospital pricing indices influence their quotes. 

On the insurer side, mispriced plans introduce underwriting risks. Setting rates too low leads to financial deficits when claims arrive, while pricing policies too high drives away healthy, low-risk applicants. HealthSecure tackles both problems by using a supervised machine learning regression pipeline that calculates actuarially sound annual premiums in real time and matches applicants with suitable policies.

### Problem Statement
To build and deploy an end-to-end web system that accurately estimates annual medical insurance charges from eight core applicant attributes (age, sex, height, weight, dependent children, smoking status, alcohol use, region, and annual salary) while keeping training data strictly separated from past claims to prevent leakage, providing transparent factor breakdowns and matching available multi-insurer policies.

### Feasibility Study

#### 1. Technical Feasibility
Technical feasibility determines whether our target hardware, programming languages, libraries, and runtime frameworks can support development and local execution.

- **Hardware Specifications:**
  - Standard laptop equipped with an Intel Core i3 or AMD Ryzen 3 processor (2.0 GHz or higher).
  - 8 GB system RAM (4 GB minimum required).
  - 10 GB of available hard disk space for repository files, libraries, and virtual environments.
  - Standard internet connection for package management and dependencies.
- **Software Specifications:**
  - Operating System: 64-bit Windows 11 (fully compatible with Ubuntu 22.04 LTS).
  - Core Language: Python 3.10 or newer (tested with Python 3.13).
  - Primary Frameworks: Flask 3.1 and Jinja2 templating.
  - Data Processing and Modeling: Pandas 2.2, NumPy 1.26, and Scikit-learn 1.6.
  - Visualization and Exports: Matplotlib 3.8 and ReportLab 5.1 for compiling PDF reports.
  - Relational Database: MySQL 8.0 community edition with SQLAlchemy ORM.
- **Outcome:**  
  All required runtime environments, libraries, and data science utilities are accessible, stable, and well-documented. System resource consumption during training and inference remains well within normal hardware thresholds, confirming complete technical feasibility.

#### 2. Economic Feasibility
Economic feasibility assesses whether the project can be completed without exceeding budgetary boundaries.

Our software stack relies exclusively on open-source packages and freely licensed developer tools. We trained and evaluated our models on an open-access actuarial dataset of 8,000 anonymized records. No commercial proprietary licenses, paid API keys, or specialized GPU cloud services were needed.

| Component | License Model | Estimated Expenditure |
| :--- | :--- | :--- |
| Python 3.13 Runtime | Open Source (PSF License) | Rs. 0.00 |
| Visual Studio Code Editor | Free Community License | Rs. 0.00 |
| Flask Web Framework & Extensions | Open Source (BSD-3-Clause) | Rs. 0.00 |
| Scikit-learn, Pandas, NumPy | Open Source (BSD License) | Rs. 0.00 |
| MySQL 8.0 Community Server | Free GPL License | Rs. 0.00 |
| ReportLab PDF Engine | Free Open-Source Edition | Rs. 0.00 |
| Actuarial Training Dataset (8,000 rows) | Open Access Public Domain | Rs. 0.00 |
| Development Machine | Personal Student Laptop | Rs. 0.00 |

- **Outcome:**  
  Because all compilers, frameworks, databases, and datasets carry zero licensing costs, the development budget is entirely manageable. The system is economically sound.

#### 3. Operational Feasibility
Operational feasibility evaluates how comfortably end-users—including everyday applicants, insurance agents, and actuaries—can navigate the software without specialized coaching.

- **Workflow Overview:**  
  An applicant accesses the clean web interface, enters basic personal details along with height and weight, and views their computed Body Mass Index. The system runs client-side validations, transforms the feature values, queries the pre-trained regression model, and displays the estimated premium in under one second. Along with the price, users see visual breakdowns of risk contributors, alternative scenario sliders, and matched plans with downloadable PDF quotes.
- **Outcome:**  
  With clear form hints, instant validation messages, and localized interfaces, users can calculate premiums and compare options without technical guidance. The application is operationally viable.

### Result
The problem definition was documented and the feasibility evaluation confirmed that HealthSecure is technically practical, economically viable, and operationally straightforward to deploy.

---

## Exercise 2: Software Requirements Specification (SRS)

### Aim
To write a structured Software Requirements Specification (SRS) document for HealthSecure following standard IEEE 830 guidelines.

### Procedure
1. Identify the clinical, demographic, and financial data inputs needed for actuarial calculation.
2. Outline specific functional requirements for data entry, validation, model scoring, and report exports.
3. Establish non-functional criteria regarding speed, accuracy, data security, and platform stability.
4. Detail hardware and software baseline requirements.
5. Review requirements against user personas (applicants, system administrators, and underwriting review staff).

### Functional Requirements (FR)
- **FR-1 (Data Input):** The system must accept applicant data including age (18 to 100), biological sex, height in centimeters (50 to 250), weight in kilograms (20 to 250), number of dependent children (0 to 5), tobacco smoking status, regional state, alcohol drinking habits, and stated annual income.
- **FR-2 (Dynamic BMI Computation):** The system must compute Body Mass Index on the fly using $\text{BMI} = \text{weight} / (\text{height} / 100)^2$ and assign the corresponding World Health Organization category (Underweight, Healthy, Overweight, or Obese).
- **FR-3 (Data Transformation):** The inference engine must encode categorical text using pre-fitted One-Hot encoders and pass numerical attributes through pre-calibrated feature scalers.
- **FR-4 (Data Leakage Isolation):** The pipeline must keep prospective underwriting inputs strictly isolated from retrospective variables, such as past total claim amounts, during feature construction.
- **FR-5 (Actuarial Regression):** The backend must run our trained model pipeline to predict estimated annual premiums in Indian Rupees (INR).
- **FR-6 (Explainable AI Attribution):** The system must provide percentage-based feature attribution, showing users how individual risk factors (such as tobacco use or elevated BMI) increase their premium relative to the baseline.
- **FR-7 (Policy Recommendation):** The system must match the predicted quote against our database of 12 cataloged insurance tiers, highlighting the closest plans by minimum absolute price difference.
- **FR-8 (Scenario Simulator):** The interface must provide interactive what-if controls so users can adjust habits (such as quitting smoking or lowering weight) and review projected savings immediately.
- **FR-9 (PDF Summary Export):** The application must generate and download an official, formatted A4 PDF summary detailing inputs, estimated charges, plan recommendations, and disclaimers.

### Non-Functional Requirements (NFR)
- **Performance:** End-to-end model inference and page rendering must finish within one second under typical home broadband connections.
- **Deterministic Reliability:** Given identical input parameters, the regression pipeline must consistently yield identical outputs without numerical drift.
- **Security:** User passwords must be stored using `scrypt` hashing. SQL queries must use parameterized bindings through SQLAlchemy, with database connection credentials escaped to prevent URI injection.
- **Maintainability:** Source modules must keep model training, HTTP routing, business logic, and UI templates clearly decoupled.
- **Cross-Platform Compatibility:** The web application must render reliably across modern desktop and mobile browsers, including Google Chrome, Mozilla Firefox, Microsoft Edge, and Apple Safari.

### Hardware Requirements
- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher.
- **Memory:** 4 GB RAM (8 GB recommended for simultaneous development and local server runs).
- **Storage:** 10 GB free space for virtual environments, dataset files, and database tables.
- **Display Resolution:** $1366 \times 768$ minimum; $1920 \times 1080$ recommended.

### Software Requirements
- **Operating Environment:** Windows 10/11 or Ubuntu Linux 20.04+.
- **Language & Runtime:** Python 3.10 through 3.13.
- **Web Application Stack:** Flask 3.1, Jinja2, and Werkzeug.
- **Scientific Libraries:** NumPy, Pandas, Scikit-learn, and Joblib.
- **Database Engine:** MySQL 8.0 Community Server.
- **Document Generation:** ReportLab 5.1.

### Result
The Software Requirements Specification was documented in accordance with IEEE 830 standards, establishing technical, operational, and interface targets for HealthSecure.

---

## Exercise 3: UML Use Case Modeling

### Aim
To construct a UML Use Case diagram mapping out the primary actors, system boundary, and core interaction use cases for HealthSecure.

### Procedure
1. Identify primary and secondary actors interacting with the system.
2. Define the main use cases across user management, biometrics entry, ML estimation, plan matching, and administration.
3. Set the system boundary separating browser actions from server-side ML and database tasks.
4. Establish `<<include>>` relationships for mandatory functional steps.
5. Establish `<<extend>>` relationships for optional user branches, such as what-if simulations or PDF downloads.
6. Assemble and review the diagram following standard UML conventions.

### Actors and Use Case Details
- **Policy Applicant (Primary Actor):** An unregistered guest or registered member who inputs clinical metrics, runs quotes, reviews risk factors, and explores insurance policies.
- **System Administrator (Secondary Actor):** Administrative staff responsible for managing accounts, reviewing system usage statistics, and checking model accuracy metrics.
- **Machine Learning Subsystem (System Actor):** The background service that loads serialized regression pipelines, computes inference values, and calculates feature contributions.
- **MySQL Database Subsystem (System Actor):** The relational persistence layer that records user profiles, historical estimates, and demo policy specifications.

![UML Use Case Diagram](lab_manual_diagrams/03_use_case_diagram.png)

### Key Relationships
- **`<<include>>` Dependencies:**
  - *Predict Actuarial Premium* includes *Auto-Calculate BMI*, because the ML pipeline requires a valid BMI value before scoring.
  - *Predict Actuarial Premium* includes *Explain Prediction (XAI)*, ensuring every quote displays transparent factor weights.
  - *Predict Actuarial Premium* includes *Match Active Demo Plans*, linking every price estimate to existing coverage options.
- **`<<extend>>` Extensions:**
  - *Simulate What-If Scenarios* extends *Predict Actuarial Premium*, allowing users to test lifestyle changes against their baseline quote.
  - *Download PDF Underwriting Report* extends *Predict Actuarial Premium*, creating an exportable summary only when requested by the applicant.

### Result
The UML Use Case model was designed, detailing actor roles, system boundaries, and functional dependencies across the HealthSecure platform.

---

## Exercise 4: UML Class Diagram

### Aim
To design an object-oriented UML Class diagram showing the classes, properties, method signatures, visibility markers, and structural relationships within HealthSecure.

### Procedure
1. Identify key domain entities: `User`, `Prediction`, `InsurancePlan`, `Recommendation`, `MLModelEngine`, and `ReportGenerator`.
2. Define data attributes, column data types, and primary/foreign key relationships.
3. Specify public (`+`) and private (`-`) methods for user authentication, data transformations, regression scoring, and reporting.
4. Model multiplicity constraints (e.g., one user to many predictions).
5. Identify structural relationships, including composition for tightly coupled records and dependencies for service calls.
6. Validate the class diagram against our SQLAlchemy models and service classes.

![UML Class Diagram](lab_manual_diagrams/04_class_diagram.png)

### Class Overview and Responsibilities
- **`User` (Entity):** Stores user identity data, email addresses, phone numbers, dates of birth, and `scrypt` password hashes, alongside role flags distinguishing regular members from administrators.
- **`Prediction` (Entity):** The central actuarial record storing biometric inputs (age, height, weight, BMI), lifestyle choices (smoking, alcohol use), dependents, location, stated salary, calculated annual premium, and financial affordability metrics.
- **`InsurancePlan` (Entity):** Catalogs available insurance policies, including plan names, base annual premiums, maximum coverage limits, policy terms, and covered medical benefits.
- **`Recommendation` (Entity):** Stores policy coverage advice, compounded terms, and multi-year benefit estimates linked directly to a parent prediction record.
- **`MLModelEngine` (Service):** Loads serialized pipelines (`premium_model.joblib`), feeds feature vectors into Scikit-learn regressors, and extracts tree or coefficient weights for Explainable AI output.
- **`ReportGenerator` (Utility):** Translates prediction dictionaries, applicant profiles, and matched plan tables into formatted, printable A4 PDF documents.

### Relationship Structure
- **Composition (`Prediction` $\blacklozenge\kern-0.5em\longrightarrow$ `Recommendation`):** A recommendation record cannot exist without its associated prediction. If a prediction is deleted, all related recommendations are dropped via cascade rules (`cascade="all, delete-orphan"`).
- **Association (`User` $1 \longrightarrow 0..*$ `Prediction`):** A registered user can generate and store multiple insurance estimates over time.
- **Association (`InsurancePlan` $0..1 \longleftarrow 0..*$ `Prediction`):** Links each prediction to the demo policy with the closest matching premium.
- **Dependency (`Prediction` $\dashrightarrow$ `MLModelEngine` and `ReportGenerator`):** The prediction workflow relies on the ML engine for scoring and the PDF generator for exports without persistent database ownership.

### Result
The static object model was designed and documented, specifying class responsibilities, attributes, methods, access levels, and multiplicity rules across the project.

---

## Exercise 5: UML Sequence Diagram

### Aim
To create a UML Sequence diagram tracing the chronological message flow, activation windows, and component interactions during the premium prediction process.

### Procedure
1. Define participating lifelines: Applicant, Web View (`predict.html`), Controller (`app.py`), Input Validator (`parse_form`), Core ML Engine (`model.py`), MySQL Database, and the XAI/PDF Engine.
2. Map the incoming HTTP `POST` submission carrying applicant biometric parameters.
3. Trace internal steps: form validation, dynamic BMI derivation, Scikit-learn model inference, database queries, and explainability calculations.
4. Model the commit phase for storing prediction records.
5. Capture the final HTTP response returning the rendered results template.

![UML Sequence Diagram](lab_manual_diagrams/05_sequence_diagram.png)

### Execution Trace
1. **Form Submission:** The applicant enters demographic and health values on `predict.html` and submits the form.
2. **Controller Routing:** The browser transmits an HTTP `POST /predict` request to `app.py`.
3. **Data Sanitization:** The controller calls `parse_form()`, checking range limits (such as age between 18 and 100) and calculating BMI from height and weight.
4. **Model Execution:** The controller passes the clean feature vector to `model.predict_premium()`, running the Scikit-learn pipeline to compute the annual charge in INR.
5. **Policy Retrieval:** The controller queries active rows from `insurance_plans` and sorts them by absolute price difference to find the closest match.
6. **Persistence:** The controller commits both `Prediction` and `Recommendation` entities into MySQL.
7. **Attribution:** The controller calls `explain_prediction()`, computing factor impact weights and clinical explanations.
8. **View Delivery:** The controller injects the prediction values, explanations, and matched policies into `result.html`, returning HTTP 200 OK.

### Result
The dynamic execution sequence was documented, illustrating message passing, component lifelines, and database persistence states for the HealthSecure prediction workflow.

---

## Exercise 6: Architectural Design

### Aim
To design a 4-tier layered and Model-View-Controller (MVC) architecture for HealthSecure that provides clear separation of concerns, reliable data validation, and modular ML model integration.

### Procedure
1. Identify functional domains across user interaction, server routing, machine learning inference, and data storage.
2. Structure the presentation layer using Jinja2 templates and a clean CSS design system.
3. Build the application controller layer using Flask routes, session protection, and validation routines.
4. Implement the machine learning subsystem using Scikit-learn preprocessing pipelines and serialized estimators.
5. Configure the data persistence layer using MySQL 8.0, connection pooling, and SQLAlchemy models.
6. Connect all tiers through explicit APIs and verify system modularity.

![Architectural Design](lab_manual_diagrams/06_architectural_design.png)

### Layer Descriptions
1. **Presentation Layer (Frontend Client):**  
   Built with semantic HTML5, custom responsive CSS3, and lightweight JavaScript. It collects applicant metrics, provides real-time BMI feedback, renders Chart.js factor charts, and displays matched policy options.
2. **Application Controller Layer (Flask Backend):**  
   Manages web routing, validates form data, manages session cookies, verifies roles (`user` vs `admin`), and computes financial ratios (such as annual premium relative to income).
3. **Machine Learning Subsystem Layer:**  
   Houses the `ColumnTransformer` preprocessing pipeline (using `OneHotEncoder` for categories like smoker status, region, and alcohol use) alongside the trained regressor (`LinearRegression` in production, with `RandomForest` and `XGBoost` for benchmarking). It also runs the XAI attribution logic.
4. **Data Persistence Layer (MySQL Database):**  
   Maintains four relational tables (`users`, `prediction`, `insurance_plans`, `recommendations`) designed in Third Normal Form (3NF). Handles foreign key constraints, indexing, and connection pooling through PyMySQL.
5. **Export & Utility Services:**  
   Integrates ReportLab Platypus to compile structured, multi-page A4 PDF policy summaries on demand.

### Result
The layered MVC architecture was designed and documented, separating concerns across presentation, routing logic, machine learning inference, and database persistence.

---

## Exercise 7: User Interface and Experience (UI/UX) Design

### Aim
To design clear, accessible, and responsive user interface wireframes and layout flows for the primary screens of HealthSecure.

### Procedure
1. Identify primary user tasks: discovering plans, calculating premiums, reviewing risk factors, and testing hypothetical adjustments.
2. Plan wireframe layouts for the landing page, prediction form, results summary, and scenario simulator.
3. Establish a cohesive design system using healthcare-oriented color palettes (deep navy `#0a2540`, medical teal `#0d9488`, slate gray `#334155`).
4. Add clear visual feedback, including dynamic BMI calculations and formatted risk badges.
5. Ensure layouts adjust cleanly across standard desktop, tablet, and mobile screens.

![UI/UX Wireframes](lab_manual_diagrams/07_ui_ux_wireframes.png)

### Screen Layouts
- **Screen 1: Landing Page (`index.html`):**  
  Features a top navigation bar, brand identity badge, hero section with a direct call to action, and a responsive grid showcasing available health insurance plans with annual pricing and coverage limits.
- **Screen 2: Multi-Factor Calculator (`predict.html`):**  
  Organized in a balanced two-column layout. Applicants enter height in centimeters and weight in kilograms to view their real-time calculated BMI alongside lifestyle toggles (tobacco, alcohol), state selections, and annual salary fields.
- **Screen 3: Prediction Results & Plan Matching (`result.html`):**  
  Displays the estimated annual premium in bold typography alongside an affordability ratio indicator. Below, the closest matching demo policy is highlighted with a "Very Close Match" badge ($\le 5\%$ difference), accompanied by an XAI bar chart showing risk weights.
- **Screen 4: What-If Scenario Simulator (`what_if.html`):**  
  Features an interactive comparison table contrasting baseline metrics against simulated changes. It shows immediate projected savings in Indian Rupees when users model quitting smoking or lowering their BMI.

### Result
The UI/UX layouts and interactive wireframe flows were produced, providing an accessible, responsive interface for premium prediction, plan evaluation, and scenario simulation.

---

## Exercise 8: Software Implementation using Version Control

### Aim
To develop the core machine learning inference and dynamic BMI module in Python and manage the repository using Git and GitHub version control.

### Procedure
1. Configure local Git identity (`user.name` and `user.email`).
2. Initialize the project repository and set up a comprehensive `.gitignore` to exclude temporary environments and credential files (`.env`, `__pycache__`).
3. Create feature branches to isolate new functional changes.
4. Implement the dynamic BMI calculation and inference routine in Python.
5. Stage and commit code changes with clear semantic messages.
6. Push commits to the remote GitHub repository.

![Git Version Control](lab_manual_diagrams/08_git_version_control.png)

### Core Inference Module (`model.py` / `app.py`)
```python
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = Path("models/premium_model.joblib")

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate Body Mass Index from metric height and weight."""
    if not (50.0 <= height_cm <= 250.0):
        raise ValueError("Height must fall between 50 cm and 250 cm.")
    if not (20.0 <= weight_kg <= 250.0):
        raise ValueError("Weight must fall between 20 kg and 250 kg.")
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 2)

def predict_insurance_premium(applicant_data: dict) -> dict:
    """Load model pipeline and generate calibrated premium prediction."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Trained model not found at {MODEL_PATH}")
    
    pipeline = joblib.load(MODEL_PATH)
    features_df = pd.DataFrame([applicant_data])
    predicted_charge = float(pipeline.predict(features_df)[0])
    calibrated_charge = max(2500.0, round(predicted_charge, 2))
    
    return {
        "annual_premium_inr": calibrated_charge,
        "monthly_premium_inr": round(calibrated_charge / 12.0, 2)
    }

if __name__ == "__main__":
    bmi_val = calculate_bmi(height_cm=175.0, weight_kg=70.0)
    sample_profile = {
        "age": 28, "sex": "male", "bmi": bmi_val,
        "children": 1, "smoker": "no", "region": "Maharashtra",
        "liquor": "no", "salary": 750000.0
    }
    quote = predict_insurance_premium(sample_profile)
    print(f"Computed BMI: {bmi_val} | Estimated Premium: Rs. {quote['annual_premium_inr']}/year")
```

### Git Command Reference
| Git Command | Functional Role in HealthSecure |
| :--- | :--- |
| `git init` | Initializes the local version control repository. |
| `git checkout -b feature/dynamic-bmi` | Creates and activates an isolated branch for developing the BMI module. |
| `git status` | Displays untracked, modified, and staged repository files. |
| `git add app.py model.py` | Stages modified source files for the next commit. |
| `git commit -m "feat: add dynamic BMI"` | Records an atomic snapshot of staged changes with a descriptive message. |
| `git checkout main && git merge feature/...`| Merges verified feature work into the main production branch. |
| `git push -u origin main` | Pushes local commit history to the remote GitHub repository. |

### Commit Audit Log
```text
* 0212d31 Enhance landing page light theme, single navbar, 12 demo plans, Indian states region
* 058d179 Add height and weight dynamic BMI calculation and liquor drinking ML feature across stack
* a8e335d feat: complete HealthSecure platform with modern landing page, XAI, simulator & demo matching
* eb20ba7 Second commit: Scikit-learn regression models & Flask routing
* 0dee44c Initial commit: Core project architecture & basic dataset setup
```

### Result
The core inference and BMI calculation module was implemented in Python and managed through Git version control, maintaining a clear, traceable commit history.

---

## Exercise 9: Software Testing and Quality Assurance

### Aim
To test the HealthSecure platform through White-Box Basis Path analysis, Black-Box Boundary Value Analysis, and automated integration tests.

### Procedure
1. Construct the Control Flow Graph (CFG) for the input parsing and validation function `parse_form()`.
2. Compute the Cyclomatic Complexity $V(G)$ to determine the number of independent execution paths.
3. Design test cases for each independent basis path.
4. Apply Equivalence Class Partitioning and Boundary Value Analysis (BVA) to user input fields.
5. Run the automated test suite across routing, regression scoring, database transactions, and PDF generation.
6. Verify and document model performance metrics on unseen test data.

![Software Testing Suite](lab_manual_diagrams/09_software_testing.png)

### White-Box Testing: Control Flow Graph and Cyclomatic Complexity
Let us analyze the validation function `parse_form()`:
- **Node 1:** Function entry.
- **Node 2:** Extract raw input values from the request dictionary.
- **Node 3 (Predicate):** Check if both `height` and `weight` are provided.
- **Node 4:** Check if `height` and `weight` fall within numerical bounds (50–250 cm, 20–250 kg).
- **Node 5:** Calculate `bmi = weight / (height / 100)^2`.
- **Node 6 (Predicate):** Check if an explicit `bmi` field exists in the form.
- **Node 7:** Raise a `ValueError` for missing biometric inputs.
- **Node 8 (Predicate):** Validate ranges for age, annual salary, smoker status, and state selection.
- **Node 9:** Raise a `ValueError` for invalid categorical or numerical ranges.
- **Node 10:** Function exit: return the sanitized feature dictionary.

#### Cyclomatic Complexity Calculation
$$V(G) = E - N + 2P$$
Where:
- $E = 13$ (Total edges in the graph)
- $N = 10$ (Total nodes in the graph)
- $P = 1$ (Single connected component)

$$V(G) = 13 - 10 + 2(1) = 5$$

Using the predicate node formula with $P_{\text{nodes}} = 4$:
$$V(G) = P_{\text{nodes}} + 1 = 4 + 1 = 5$$

#### Five Basis Paths
- **Path 1:** $1 \to 2 \to 3 \to 4 \to 5 \to 8 \to 10$ (Nominal flow: valid height and weight provided).
- **Path 2:** $1 \to 2 \to 3 \to 4 \to 9$ (Biometrics provided, but height out of bounds).
- **Path 3:** $1 \to 2 \to 3 \to 6 \to 8 \to 10$ (Height and weight omitted, valid direct BMI provided).
- **Path 4:** $1 \to 2 \to 3 \to 6 \to 7$ (Height, weight, and direct BMI all missing).
- **Path 5:** $1 \to 2 \to 3 \to 4 \to 5 \to 8 \to 9$ (Valid biometrics, but applicant age below 18).

### Black-Box Boundary Value Analysis (BVA)
| Parameter | Valid Input Range | Lower Boundary Tests | Upper Boundary Tests | Test Output |
| :--- | :--- | :--- | :--- | :--- |
| **Age** | $18 \le \text{age} \le 100$ | $17$ (Reject), $18$ (Accept) | $100$ (Accept), $101$ (Reject) | Error / Accepted / Accepted / Error |
| **Height** | $50 \le \text{height} \le 250$ cm | $49$ cm (Reject), $50$ cm (Accept) | $250$ cm (Accept), $251$ cm (Reject) | Error / Accepted / Accepted / Error |
| **Weight** | $20 \le \text{weight} \le 250$ kg | $19$ kg (Reject), $20$ kg (Accept) | $250$ kg (Accept), $251$ kg (Reject) | Error / Accepted / Accepted / Error |
| **BMI** | $10.0 \le \text{BMI} \le 60.0$ | $9.9$ (Reject), $10.0$ (Accept) | $60.0$ (Accept), $60.1$ (Reject) | Error / Accepted / Accepted / Error |
| **Salary** | Rs. 1 Lakh to Rs. 1 Crore | Rs. 99,999 (Reject) | Rs. 1,00,00,001 (Reject) | Error / Accepted / Error |
| **Smoker** | `'yes'`, `'no'` | Numerical inputs (Reject) | Arbitrary text (Reject) | Validation Error |

### Automated Integration Test Results
All 10 automated test cases completed successfully:
1. `TC-01`: Public GET routes (`/`, `/health`, `/plans`) $\to$ **PASS** (HTTP 200 OK).
2. `TC-02`: New user account registration and database persistence $\to$ **PASS** (`users` table updated).
3. `TC-03`: Administrator authentication (`admin@healthsecure.com`) $\to$ **PASS** (Admin role confirmed).
4. `TC-04`: Dynamic BMI calculation ($175\text{ cm}, 70\text{ kg} \to 22.86$) $\to$ **PASS** (Matches WHO formula).
5. `TC-05`: Machine learning regression inference $\to$ **PASS** (Calibrated premium calculated).
6. `TC-06`: Nearest demo policy matching (L1 distance) $\to$ **PASS** (Starter Shield selected).
7. `TC-07`: Explainable AI factor contribution scoring $\to$ **PASS** (Tobacco risk weighted appropriately).
8. `TC-08`: What-if simulation savings calculation $\to$ **PASS** (Premium delta matches expectation).
9. `TC-09`: PDF underwriting summary compilation $\to$ **PASS** (Valid A4 document delivered).
10. `TC-10`: Database connection with special password characters $\to$ **PASS** (`quote_plus` prevents parse errors).

### Result
Basis path testing confirmed a Cyclomatic Complexity of $V(G) = 5$. Boundary value checks verified input guards, and automated integration testing achieved a 100% pass rate.

---

## Exercise 10: Integrated Mini Project Documentation

### Aim
To assemble the complete project lifecycle documentation—spanning SRS, architectural design, modular implementation, multi-tier testing, and performance reporting—for HealthSecure.

### Project Summary
HealthSecure is an Explainable AI predictive platform developed to make retail health insurance underwriting transparent, fast, and accessible. In traditional insurance environments, applicants often face confusing actuarial jargon, unexplained pricing differences, and long underwriting delays. 

HealthSecure addresses this by using a calibrated Scikit-learn regression pipeline trained on 8,000 anonymized records. The platform calculates annual premiums in Indian Rupees, breaks down the impact of individual health factors using Explainable AI, simulates prospective savings through what-if adjustments, and pairs users with suitable policies from our catalog.

![Mini Project Lifecycle](lab_manual_diagrams/10_mini_project_lifecycle.png)

### Machine Learning Model Evaluation
To prevent data leakage, historical claim amounts (`total_claim_amount`) were completely excluded from the training feature set and used solely to establish ground-truth labels during preprocessing. We benchmarked four regression algorithms on a held-out test split of 1,600 records (20%):

| Regressor Algorithm | Test MAE (INR) | Test MSE | Test RMSE (INR) | Test $R^2$ Score | Evaluation Summary |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Regression** | **Rs. 2,603.32** | **11,570,814.72** | **Rs. 3,401.59** | **0.6527 (65.3%)** | **Selected for Production** |
| **XGBoost Regressor** | Rs. 2,629.69 | 11,863,578.29 | Rs. 3,444.35 | 0.6439 (64.4%) | Strong gradient-boosted candidate |
| **Gradient Boosting** | Rs. 2,640.68 | 11,908,669.51 | Rs. 3,451.12 | 0.6425 (64.2%) | Robust ensemble estimator |
| **Random Forest** | Rs. 2,776.42 | 13,252,803.11 | Rs. 3,640.44 | 0.6022 (60.2%) | Baseline decision tree ensemble |

*Linear Regression was selected for production because it achieved the lowest Mean Absolute Error (Rs. 2,603.32) and the highest $R^2$ score (0.6527) while offering fast, deterministic execution and clean interpretability.*

### Requirements Traceability Matrix
| Requirement ID | Design Artifact | Source File Location | Verification Test Case |
| :--- | :--- | :--- | :--- |
| **FR-1 (User Management)** | Class: `User`, Use Case: UC1 | `app.py`, lines 645–715 | `TC-02` (Registration Flow) |
| **FR-2 (ML Inference)** | Class: `MLModelEngine`, UC4 | `model.py`, lines 71–98 | `TC-05` (Premium Inference) |
| **FR-3 (Dynamic BMI)** | Sequence Diagram: Step 4, UC3 | `app.py`, lines 400–415 | `TC-04` (BMI Calculation) |
| **FR-4 (Explainable AI)** | Sequence Diagram: Step 7, UC5 | `model.py`, lines 136–304 | `TC-07` (XAI Attribution) |
| **FR-5 (Policy Matching)** | Architecture: Tier 2, UC7 | `app.py`, lines 320–385 | `TC-06` (Policy Matching) |
| **FR-6 (What-If Analysis)** | UI/UX Wireframe 4, UC6 | `app.py`, lines 1114–1200 | `TC-08` (Scenario Savings) |
| **FR-7 (Plan Comparison)** | UI/UX Wireframe 1, UC8 | `app.py`, lines 950–1050 | `TC-01` (Plan Exploration) |
| **FR-8 (PDF Generation)** | Architecture: Tier 5, UC9 | `report_generator.py`, lines 18–320 | `TC-09` (PDF Export) |

### Key Platform Strengths
- **Transparent Underwriting:** Explainable AI visualizations clarify why an applicant receives a specific quote, eliminating pricing guesswork.
- **Zero Data Leakage:** Keeps historical claim payouts strictly isolated during feature engineering.
- **Interactive Lifestyle Modeling:** Demonstrates the financial benefits of healthier habits by showing real-time savings when users lower their BMI or stop smoking.
- **Documented Code Quality:** Verified through Basis Path analysis ($V(G) = 5$), Boundary Value Analysis, and automated integration suites.

### Result
The complete Health Insurance Premium Prediction and Policy Recommendation System (HealthSecure) was implemented, tested, and documented across all phases of the software development lifecycle.

---

## Laboratory Viva Questions and Model Answers

**Q1: What is the operational difference between an `<<include>>` and an `<<extend>>` relationship in UML Use Case modeling?**  
*Answer:* An `<<include>>` relationship represents mandatory functionality that always executes whenever the base use case runs (such as *Predict Premium* always including *Calculate BMI*). In contrast, an `<<extend>>` relationship represents optional or conditional functionality that executes only when specific circumstances are met (such as a user choosing to launch the *What-If Simulator* or request a *Download PDF Quote*).

**Q2: Why is the relationship between `Prediction` and `Recommendation` modeled as a Composition rather than a simple Association?**  
*Answer:* Composition denotes strict lifecycle ownership. In HealthSecure, every recommendation record belongs entirely to a specific prediction. If an applicant's prediction is removed from the database, all linked recommendations become obsolete and are dropped automatically via cascade rules (`cascade="all, delete-orphan"`).

**Q3: How does Basis Path Testing establish that five test cases are sufficient for `parse_form()`?**  
*Answer:* By mapping all branches in `parse_form()` into a Control Flow Graph, we evaluate Cyclomatic Complexity as $V(G) = E - N + 2P = 13 - 10 + 2(1) = 5$. This proves that the method contains exactly five linearly independent execution paths. Testing these five paths achieves complete branch and statement coverage.

**Q4: Why was URL encoding necessary when building the MySQL database connection string?**  
*Answer:* Database connection URIs use the format `dialect://user:password@host:port/dbname`, treating the `@` symbol as the delimiter between credentials and network addresses. When passwords contain special characters—such as `@` in `Haris@128`—parsers misinterpret the password boundary, resulting in connection failures (`Errno 11003`). Passing the password through `urllib.parse.quote_plus` encodes `@` into `%40`, preventing connection errors.

**Q5: Why did Linear Regression outperform more complex ensemble algorithms like Random Forest in your benchmarks?**  
*Answer:* In our actuarial dataset, charges increase largely linearly with age, baseline medical factors, and binary risk switches (smoking status and alcohol consumption). Linear Regression captured these direct relationships cleanly without overfitting, yielding the lowest Mean Absolute Error (Rs. 2,603.32) and the highest $R^2$ score (0.6527), while executing with negligible latency.

---
*End of Laboratory Manual Record*
