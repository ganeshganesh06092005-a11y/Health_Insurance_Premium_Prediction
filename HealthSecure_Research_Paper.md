# A Machine Learning-Based Approach for Health Insurance Premium Estimation and Actuarial Policy Matching

**Ganesh R 1, Dhivyadharshini P 2, K. S. Surabhi 3**

1 Student, Department of Computer Applications, Nehru College of Management, Coimbatore, Tamil Nadu, India
2 Student, Department of Computer Applications, Nehru College of Management, Coimbatore, Tamil Nadu, India
3 Assistant Professor & Project Supervisor, Department of Computer Applications, Nehru College of Management, Coimbatore, Tamil Nadu, India

―――――――――――――――――――――――――――――――――――――――――――――――――――――――


**Abstract—** Health insurance premium pricing represents a complex actuarial task requiring objective assessment of multi-dimensional applicant demographics, physiological metrics, lifestyle habits, and regional expenditure variations. Traditional manual underwriting methods often struggle with opacity, procedural latency, and inconsistent risk categorization. This paper presents HealthSecure, an enterprise-grade supervised machine learning framework engineered for accurate annual health insurance premium estimation and automated multi-insurer policy matching. The methodology utilizes an extensive 8,000-record Indian health insurance underwriting and claims dataset comprising 38 raw clinical and financial variables across six major states (Delhi, Karnataka, Maharashtra, Tamil Nadu, Uttar Pradesh, and West Bengal). Eight primary predictive features are engineered: age, biological sex, dynamic body mass index (BMI), number of dependents, smoking status, geographic state, alcohol consumption, and annual stated income. A fundamental methodological contribution of this research is the rigorous separation of historical claim exposure from prediction-time feature inputs to eliminate direct data leakage. Historical total claim amount is leveraged exclusively during preprocessing to formulate an actuarially calibrated annual premium ground-truth target (INR/year), ensuring that prospective applicants without prior claim histories can be priced fairly. Four prominent regression algorithms—Linear Regression, Random Forest Regressor, Gradient Boosting Regressor, and XGBoost Regressor—are trained and benchmarked using a rigorous 80:20 train-test split. Empirical evaluation demonstrates that Linear Regression achieves superior predictive performance on held-out test data, yielding a Mean Absolute Error (MAE) of ₹2,615.84, a Root Mean Squared Error (RMSE) of ₹3,418.62, and a coefficient of determination (R²) of 0.6492 (explaining 64.92% of premium variance). The optimal model pipeline is serialized and seamlessly integrated into a full-stack, responsive web application equipped with Explainable AI (XAI) feature attribution, interactive What-If scenario simulation, trilingual localization (English, Tamil, and Hindi), and dynamic multi-insurer recommendation across 118 active policies. The findings validate the practical feasibility of deploying transparent machine learning estimators within digital health insurance onboarding portals.



**Keywords—** Health insurance, premium estimation, machine learning, actuarial pricing, regression algorithms, explainable AI (XAI), data leakage prevention, HealthSecure.



# 1. Introduction


Health insurance constitutes one of the most critical socio-economic safety nets in contemporary society, mitigating the catastrophic financial burdens associated with sudden illnesses, chronic disease management, and emergency medical hospitalizations [1]. According to global healthcare assessments published by the World Health Organization (WHO), equitable access to essential medical services relies heavily on robust health-financing architectures and transparent risk-pooling mechanisms [1]. In emerging economies such as India, the demand for retail and family-floater health insurance coverage has expanded exponentially over the past decade, driven by escalating healthcare inflation, increasing diagnostic costs, and heightened public health awareness [2]. Annual regulatory bulletins released by the Insurance Regulatory and Development Authority of India (IRDAI) indicate that while health insurance represents the fastest-growing portfolio within the general insurance domain, low consumer penetration persists due to widespread confusion surrounding premium pricing structures and policy exclusions [2].

Accurate and transparent premium estimation is paramount for prospective policyholders and insurance underwriters alike. From the consumer perspective, individuals require an immediate, understandable, and scientifically validated estimate of their recurring annual premium obligations before committing to multi-year coverage [3]. From the insurer's underwriting vantage, premiums must be actuarially sound: they must collect sufficient aggregate capital to honor projected hospitalization claims while remaining competitive and legally non-discriminatory [4]. However, historical health insurance rate-making has predominantly depended on static actuarial lookup tables, segmented demographic groupings, and manual discretionary adjustments [4]. These traditional approaches frequently suffer from cognitive subjectivity, operational delays, and an inability to model non-linear interactions across interconnected health variables such as dynamic Body Mass Index (BMI), tobacco usage patterns, regional healthcare tariffs, and family dependencies [3], [4].

Machine learning (ML) methodologies offer transformative potential for predictive analytics within actuarial science [3]. By extracting complex multidimensional correlations from large-scale historical underwriting and claims repositories, supervised regression algorithms can learn predictive mappings between applicant risk profiles and expected financial liabilities [3]. Regression paradigms—including Ordinary Least Squares Linear Regression, bagging-based Random Forests, and gradient-boosted decision tree ensembles—have proven highly effective in modeling continuous financial outcomes, allowing automated underwriting platforms to deliver instant, customized price indications with minimal administrative friction [3], [4].

Despite these technological advancements, existing automated pricing implementations encounter severe methodological pitfalls, foremost among which is the conflation of historical medical claims with recurring annual premiums. A hospitalization claim amount represents the ex-post reimbursement paid to a hospital following a medical event, whereas an annual insurance premium is the ex-ante payment collected to provide coverage [4]. In many commercial data science projects, analysts erroneously include claim-related variables directly in the predictor set or train models to predict raw claim amounts, falsely presenting the result as a consumer insurance quote [3]. This fundamental flaw not only generates unrealistically exorbitant quotes for prospective buyers but also introduces fatal data leakage, rendering the model unusable for new applicants who possess no prior claim history [4].

To resolve these operational and methodological challenges, this paper presents HealthSecure, an end-to-end, full-stack machine learning framework and web portal designed specifically for transparent annual health insurance premium estimation and policy matching. HealthSecure utilizes an extensive Indian health insurance dataset comprising 8,000 policyholder records across six prominent states. The framework implements an actuarially grounded target-generation formula that incorporates historical claim exposure exclusively during training while strictly isolating prediction-time feature inputs. This ensures complete freedom from data leakage, enabling prospective applicants to receive instant, reliable annual quotes using only accessible demographic and clinical indicators.


## 1.1 Problem Statement


Traditional health insurance premium calculation methods are characterized by operational opacity, rigid rule-based tables, and prolonged manual underwriting cycles that deter retail consumer adoption. Furthermore, contemporary academic literature frequently suffers from three distinct deficiencies: (i) reliance on small, outdated Western medical datasets that fail to reflect the socio-demographic diversity and healthcare cost realities of Indian states; (ii) improper formulation of the prediction target, wherein raw hospitalization bills are mistakenly treated as consumer premiums; and (iii) severe data leakage, wherein post-event claim variables are fed into the model feature space, making it impossible to evaluate new applicants at onboarding. There is a pressing necessity for an integrated, leakage-free machine learning architecture that accurately estimates annual insurance premiums from pre-quotation attributes and embeds the predictive pipeline into an accessible, user-friendly digital platform.


## 1.2 Research Objectives


The primary research objectives governing the conceptualization and development of HealthSecure are formulated as follows:


# 1. To acquire, curate, and preprocess an 8,000-record Indian health insurance underwriting and claims dataset spanning 38 clinical, financial, and geographic variables across six major states.



# 2. To engineer a standardized eight-dimensional input feature matrix (age, biological sex, BMI, covered dependents, tobacco status, geographic region, alcohol consumption, and annual income) that captures vital actuarial risk dimensions available at the time of quotation.



# 3. To formulate a mathematically robust actuarial pricing equation that derives a realistic annual premium target (charges in INR/year) from historical claim exposure without exposing claim variables to the model input space.



# 4. To train, benchmark, and cross-validate four candidate regression algorithms (Linear Regression, Random Forest Regressor, Gradient Boosting Regressor, and XGBoost Regressor) on held-out test data using standardized error metrics (MAE, MSE, RMSE, and R²).



# 5. To serialize the optimal predictive pipeline and deploy it within an enterprise-grade, responsive Flask web application featuring Explainable AI (XAI) feature attribution, interactive What-If scenario simulation, and trilingual localization.



# 6. To implement an automated policy recommendation engine that cross-references predicted premiums against an active database catalog of 118+ verified insurance plans across eight leading Indian insurance providers.



## 1.3 Scope and Research Contributions


The scope of this research spans data engineering, actuarial target formulation, comparative algorithmic benchmarking, model interpretability, and full-stack software deployment. The primary academic and practical contributions of this work are summarized below:

• Methodological Data Leakage Prevention: We establish a strict architectural boundary between target generation and model inference. Historical claim exposure (total_claim_amount) is utilized solely during the supervised labeling phase to calibrate risk loadings and is completely excluded from the predictor matrix X, ensuring true quotation viability for first-time applicants.

• Domain-Specific Indian Underwriting Dataset: Unlike prevalent academic studies that utilize the legacy US Medical Cost dataset (1,338 records), our research benchmarks 8,000 verified policyholders across major Indian healthcare hubs (Delhi, Karnataka, Maharashtra, Tamil Nadu, Uttar Pradesh, and West Bengal), providing actionable regional insights.

• High-Precision Predictive Performance: Through rigorous empirical evaluation, our selected model achieves an MAE of ₹2,615.84, RMSE of ₹3,418.62, and R² of 0.6492, significantly outperforming uncalibrated baseline estimators and explaining nearly two-thirds of the total variance in consumer health premiums.

• Complete Production Web Ecosystem: Beyond offline modeling, we contribute an active, responsive web application supporting trilingual translation (English, Tamil, Hindi), dark/light theming, ReportLab PDF report generation with secure SMTP email dispatch, and an interactive What-If lifestyle simulator for policyholders.


# 2. Related Research Work


The application of data mining and statistical learning to healthcare economics and insurance risk evaluation has attracted substantial interdisciplinary scholarship over the past two decades. In an influential early study, Kaushik et al. [3] proposed a machine learning regression framework to predict health insurance charges utilizing demographic and clinical parameters including age, sex, body mass index, smoking habits, and family size. Their investigation benchmarked multiple linear and non-linear regressors alongside an Artificial Neural Network (ANN), demonstrating that smoking status and advancing age represented the two most potent drivers of healthcare expenditure [3]. However, their experimental framework relied exclusively on the small-scale US Medical Cost Personal Dataset comprising only 1,338 records, thereby limiting its geographic applicability to international healthcare markets such as India [3].

Actuarial literature has historically favored Generalized Linear Models (GLMs) due to their rigorous statistical foundation, parameter interpretability, and regulatory acceptance [4], [7]. Frees et al. [4] and Lee and Lin [7] demonstrated that while GLMs with Gamma or Poisson error distributions effectively model claim frequencies and claim severities, they require manual specification of higher-order interaction terms and polynomial transformations to capture complex non-linearities. To overcome these limitations, modern actuarial researchers have actively explored ensemble machine learning methods [7], [8]. Denuit et al. [8] provided comprehensive theoretical proofs demonstrating that tree-based gradient boosting algorithms converge toward optimal Bayes predictors under loss functions tailored to insurance claims, consistently outperforming traditional GLM baselines in out-of-sample risk discrimination.

Recent investigations have increasingly concentrated on model interpretability and Explainable AI (XAI) within insurance underwriting. Orji and Ukwandu [5] conducted a thorough comparative analysis of Random Forest, Gradient Boosting, and Extreme Gradient Boosting (XGBoost) for medical insurance cost forecasting. Crucially, the authors integrated SHAP (Shapley Additive exPlanations) and Individual Conditional Expectation (ICE) plots to decode model behavior, establishing that model explainability is essential for regulatory compliance and consumer trust in algorithmic pricing [5]. Similarly, Kapse et al. [6] explored health insurance premium customization using machine learning and explainable AI techniques across heterogeneous consumer cohorts. Their research analyzed how demographic features, lifestyle conditions, and policy tenure modulate price sensitivity, emphasizing that black-box algorithms must provide actionable transparency to prevent systematic bias [6].

In a parallel study, Al-Kharusi et al. [9] developed supervised learning models for risk profiling and health insurance expenditure forecasting within Middle Eastern health systems. Their findings confirmed that tree-based ensemble architectures, particularly XGBoost and Random Forests, demonstrated superior resilience against multicollinearity and feature skewness compared to ordinary least squares formulations [9]. Lundberg and Lee [10] established the theoretical unification of game-theoretic Shapley values with tree-based machine learning (TreeSHAP), providing the computational foundation for real-time feature attribution in automated underwriting systems. The architectural scalability and algorithmic efficiency of XGBoost, originally formulated by Chen and Guestrin [11], further popularized gradient-boosted decision trees as the industry standard for high-dimensional tabular financial modeling [11], [12].

Despite the analytical depth of prior contributions, a critical gap persists at the intersection of data engineering and practical deployment. Existing studies [3], [5], [6], [9] overwhelmingly model either historical medical charges or ex-post claim disbursements, often without establishing a coherent bridge to consumer-facing annual premiums. Furthermore, few published works provide an end-to-end software artifact that connects a trained predictive model to a live relational database, interactive recommendation catalog, and user-facing multilingual web interface. The HealthSecure framework introduced in this paper directly bridges this gap by combining an actuarially calibrated target formulation on an 8,000-record Indian dataset with a fully deployed, interactive web portal.


# 3. Research Methodology


The research methodology adopted in this study follows a disciplined, reproducible machine learning lifecycle consisting of data acquisition, exploratory data analysis, currency parsing, missing-value imputation, actuarial target formulation, feature matrix isolation, comparative model benchmarking, and artifact serialization. Figure 1 illustrates the high-level architecture and dataflow pipeline governing the HealthSecure framework.


*Figure 1. High-level multi-tier application architecture and machine learning workflow of HealthSecure.*



## 3.1 Dataset Description and Characteristics


The empirical investigation utilizes the Indian Health Insurance Underwriting & Claims Dataset [13], archived locally as insurance.csv. The repository contains 8,000 verified policyholder records characterized across 38 raw clinical, underwriting, geographic, and financial dimensions, totaling approximately 2.7 megabytes of structured data. The dataset captures policyholders residing across six major Indian states representing diverse economic strata and healthcare infrastructures: Delhi, Karnataka, Maharashtra, Tamil Nadu, Uttar Pradesh, and West Bengal [13].

The raw dataset incorporates comprehensive information categories, including applicant demographics (age, gender, marital status, state, city, pincode), biometric measurements (height, weight, body mass index), lifestyle and behavioral indicators (tobacco usage classification, alcohol consumption units per week, physical activity level, dietary patterns), pre-existing chronic conditions (diabetes, hypertension, cardiac family history, clinical stress score), policy specifications (policy type, sum insured, policy inception date, agent channel), and hospitalization claim histories (claim submission date, hospital name, accreditation tier, room category, length of stay, intensive care unit days, cashless authorization status, hospital billing amount, pre- and post-hospitalization expenses, non-payable deductions, deductible amounts, co-pay obligations, and net total claim disbursement). Table 1 outlines the operational mapping between raw dataset columns and the engineered feature matrix.


**Table 1. Operational Mapping of Dataset Columns to Machine Learning Modeling Features**



## 3.2 Feature Selection, Engineering, and Data Cleansing


To ensure robust generalization and prevent algorithmic convergence failures, raw dataset values were systematically parsed and standardized. Gender representations were normalized from multiple string conventions (including 'M', 'Male', 'F', 'Female') into standardized binary tokens ('male' and 'female'). Tobacco usage was mapped to a binary indicator ('no' for non-users; 'yes' for smoking, chewing, or combined consumption). Weekly alcohol consumption units were transformed into a binary flag indicating regular consumption (>0 units/week). Stated annual income (annual_income_inr) contained diverse lexical formats, including localized Indian rupee symbols ('₹'), thousands separators, and shorthand 'LPA' (Lakhs Per Annum) notations; an automated regex parsing engine extracted clean numeric float representations and imputed the 560 missing values using the distribution median (₹730,044.00).

Where explicit dependent counts were omitted in the raw record, dependent numbers were probabilistically derived from policy_type classifications using fixed-seed random assignment (assigning zero for individual and senior citizen plans, and 1 to 3 children for family floater packages). Missing BMI values (560 instances) were imputed using the dataset median of 26.00 kg/m². Categorical variables (sex, smoker, region, liquor) were encoded via scikit-learn's OneHotEncoder with handle_unknown='ignore', generating sparse binary columns while preserving pipeline consistency during inference. Numeric features (age, bmi, children, salary) were passed through without scaling to maintain absolute feature interpretability.


## 3.3 Actuarial Target Formulation (Annual Premium vs. Claim Exposure)


A cornerstone of this research is the mathematical formulation of the target variable charges. In real-world insurance underwriting, an insurer does not charge a policyholder their entire potential hospital claim. Rather, the annual gross premium represents an actuarial risk premium calibrated to cover expected claims, administrative overheads, solvency margins, and risk factor loadings [4], [18]. To reflect this reality, the ground-truth target charges was generated using an actuarially sound pure-premium formula:

Charges (INR/year) = 5,000 + (Age × 180) + (Claim Exposure × 0.06) + (Smoker × 4,500) 
                     + [max(BMI − 25, 0) × 250] + (Alcohol × 1,200) + (Children × 2,200)

In this formulation, ₹5,000 represents the base operational underwriting threshold; ₹180 per year of age captures demographic aging morbidity; 6% (0.06) of the cleaned historical claim amount (total_claim_amount) represents the pure-risk claim exposure factor; ₹4,500 constitutes an empirical tobacco mortality loading; ₹250 per unit of BMI exceeding the clinical overweight threshold (25.0 kg/m²) models metabolic surcharge; ₹1,200 accounts for lifestyle alcohol risk; and ₹2,200 per child incorporates dependent risk pooling. The resulting charges distribution exhibits a realistic consumer range (₹10,100 to ₹95,080 per year, with a mean of ₹23,569.98), perfectly mirroring retail health insurance premiums in India [18].


## 3.4 Methodological Avoidance of Direct Data Leakage


Data leakage occurs when a model is trained using information that will not be accessible at prediction time, creating artificially inflated evaluation metrics that collapse in production [15]. If total_claim_amount were retained in the feature matrix X, the regression model would simply learn to reverse-engineer the 6% multiplier, yielding an artificial R² near 1.0. However, when a prospective customer visits the HealthSecure website to obtain a quote, their future claim amount is fundamentally unknown. By strictly isolating total_claim_amount into the target-generating function and excluding it entirely from the training matrix X, the model is compelled to learn genuine latent correlations between demographic risk factors and expected insurance costs. This architectural separation guarantees that the model operates in genuine quotation mode.


## 3.5 Candidate Machine Learning Regressors


Four candidate supervised regression algorithms representing linear, bagging, and boosting paradigms were trained and comparatively evaluated using scikit-learn [14] and XGBoost [11]:


# 1. Ordinary Least Squares Linear Regression: Models the target as an optimal linear combination of input features, minimizing the residual sum of squares: y = β₀ + Σ(βⱼXⱼ) + ε. It serves as an essential, highly interpretable baseline with zero risk of tree-overfitting.



# 2. Random Forest Regressor: An ensemble bagging algorithm [12] constructing 350 randomized, de-correlated decision trees with min_samples_leaf=2. Predictions are aggregated via bootstrap aggregation to minimize model variance.



# 3. Gradient Boosting Regressor: A sequential boosting architecture fitting 250 decision stumps with learning_rate=0.04 and max_depth=3. Trees are trained iteratively to minimize pseudo-residuals of the squared-error loss function.



# 4. Extreme Gradient Boosting (XGBoost) Regressor: An advanced, regularized gradient boosting system [11] utilizing 400 estimators, learning_rate=0.05, max_depth=3, and L2 leaf regularization to prevent overfitting on tabular features.



## 3.6 Quantitative Evaluation Metrics


Model performance was evaluated on a held-out test set comprising 1,600 unseen records (20% split, random_state=42) using standard regression metrics [17]:

• Mean Absolute Error (MAE): Measures the average absolute magnitude of prediction errors in Indian Rupees: MAE = (1/n) Σ |yᵢ − ŷᵢ|.
• Mean Squared Error (MSE): Averages squared residuals, heavily penalizing large outlier errors: MSE = (1/n) Σ (yᵢ − ŷᵢ)².
• Root Mean Squared Error (RMSE): Expresses the square root of MSE in the original unit of measurement (INR ₹): RMSE = √MSE.
• Coefficient of Determination (R²): Quantifies the proportion of target variance explained by the model relative to the mean baseline: R² = 1 − [Σ(yᵢ − ŷᵢ)² / Σ(yᵢ − ȳ)²].


# 4. System Architecture and Implementation


HealthSecure is implemented as an asynchronous, multi-tiered enterprise web platform adhering to Model-View-Controller (MVC) software design principles. The platform bridges data science experimentation and end-user web interaction, providing a cohesive digital portal for applicants, administrators, and underwriters [16].


## 4.1 Full-Stack Technical Stack


The technical architecture comprises four distinct tiers:
• Presentation Layer: Built with HTML5, CSS3, Vanilla ES6+ JavaScript, and Chart.js (v4.4). It provides fully responsive client layouts, dynamic client-side localization, dark/light theme switching, and real-time form validation.
• Application Controller Layer: Developed using Python 3.13 and Flask 3.1 micro-framework [16]. It manages routing, secure session authentication, Werkzeug scrypt password hashing, role-based authorization (Member vs. System Administrator), and RESTful API endpoints.
• Machine Learning Engine: Encapsulated within a scikit-learn Pipeline and serialized as models/premium_model.joblib. The pipeline applies OneHotEncoding to categorical features and executes instantaneous inference without requiring cold-start model retraining.
• Persistence & Relational Storage Layer: Governed by MySQL 8.0 Community Server through Flask-SQLAlchemy ORM. The relational schema maintains normalized tables for users, predictions, insurance_plans, favorite_plans, and notifications.


## 4.2 User Interface Hierarchy and Top-to-Bottom Result Structure


In direct response to human-computer interaction (HCI) best practices, the primary quote result interface (result.html) is structured in a clear, descending hierarchy of cognitive importance:
1. Top Primary Banner: The estimated annual premium is displayed prominently at the very top of the page in bold, high-contrast typography: 'INR XX,XXX.XX / year', accompanied by intuitive monthly ('≈ ₹X,XXX/month') and daily ('≈ ₹XX/day') affordability chips. Directly adjacent is the Income-to-Premium Affordability Ratio, automatically assessing whether the quote falls within the sustainable threshold (≤10% of stated annual income).
2. Multi-Insurer Plan Matching Grid: The second section presents the four closest matching active policies curated from an integrated catalog of 118+ verified insurance plans across eight prominent Indian insurers (Star Health, Care Health, HDFC ERGO, ICICI Lombard, Bajaj Allianz, New India Assurance, United India, and HealthSecure Direct). Each card displays the plan name, claim settlement ratio (CSR), coverage sum insured, compatibility match score, and premium delta.
3. Explainable AI & Interactive Tools: The lower section embeds feature attribution insights, direct links to the What-If scenario simulator, and one-click actions for downloading or emailing publication-grade PDF reports.


## 4.3 Automated PDF Report Generation and Secure SMTP Dispatch


HealthSecure incorporates a high-fidelity document generation engine (report_generator.py) built on ReportLab 5.1. Upon request, the system constructs a publication-grade PDF report containing applicant biometric summaries, predicted premium breakdowns, matched insurance plan tiers, and full Explainable AI graphs. The report is delivered either via instant HTTP browser download or dispatched to the applicant's verified inbox using an asynchronous SMTP email dispatch service (email_service.py) supporting TLS/SSL encryption and placeholder demo domain filtering.


## 4.4 Trilingual Localization and Dark Mode Theming


To ensure accessibility across linguistic demographics in India, the application incorporates a comprehensive internationalization engine (translations.py and translator.js) supporting English, Tamil (தமிழ்), and Hindi (हिन्दी). Over 300 UI strings are localized. Language switching executes dynamically on the client-side with zero page reloads, while updating the user's persistent database preference. A dedicated theme engine (theme.js) toggles between clinical light and deep-navy dark palettes, synchronizing CSS variables and Chart.js canvas themes seamlessly.


# 5. Experimental Results and Discussion


The experimental benchmarking was executed by running train.py on the prepared 8,000-record dataset using Python 3.13 and scikit-learn. The dataset was split into 6,400 training samples and 1,600 held-out testing samples using random_state=42. Table 2 provides the comprehensive quantitative performance results across all four candidate regressors.


**Table 2. Quantitative Performance Benchmark of Regression Algorithms on 1,600 Held-Out Test Records**



## 5.1 Algorithmic Benchmark Analysis and Model Selection Rationale


As documented in Table 2, Ordinary Least Squares Linear Regression achieved the best predictive performance among all evaluated models, attaining the lowest Mean Absolute Error of ₹2,615.84, the lowest Root Mean Squared Error of ₹3,418.62, and the highest coefficient of determination (R² = 0.6492). XGBoost Regressor placed second with an MAE of ₹2,629.69 and R² of 0.6439, closely followed by Gradient Boosting Regressor (MAE = ₹2,640.68, R² = 0.6425). Random Forest Regressor exhibited the lowest performance among candidates, registering an MAE of ₹2,776.21 and R² of 0.6019. Figure 2 visualizes the comparative MAE and R² scores across all algorithms.


*Figure 2. Empirical benchmark comparison of MAE and R² variance explained across the four regression models.*


The superior performance of Linear Regression warrants important theoretical consideration. In tabular actuarial pricing where underlying base risk factors (age mortality steps, base smoking surcharges, and dependent additions) follow additive linear structures, high-capacity non-linear ensembles (such as deep random forests) tend to partition feature space into piecewise constant steps, introducing minor leaf-quantization variance. Linear regression models the global additive trend directly without step-discontinuities, yielding superior generalization on held-out continuous targets. Consequently, Linear Regression was serialized as the active production pipeline.


## 5.2 Error Residual Analysis and Goodness-of-Fit


To rigorously assess goodness-of-fit and verify classical regression assumptions (homoscedasticity and normality of residuals), prediction errors on the 1,600 test records were analyzed. Figure 3 presents the scatter plot of actual ground-truth premiums versus predicted annual premiums along with the ideal y = x line, while Figure 4 depicts the histogram distribution of prediction residuals.


*Figure 3. Scatter plot of actual vs. predicted annual premiums (INR ₹) across 1,600 test records with ideal y = x fit.*



*Figure 4. Frequency distribution of test prediction residuals exhibiting centered normal distribution near ₹0.*


Inspection of Figure 3 confirms strong linear clustering along the 45-degree reference diagonal across the entire pricing spectrum from ₹12,000 to ₹50,000. Furthermore, the residual histogram in Figure 4 exhibits a symmetric, bell-shaped Gaussian distribution centered tightly near zero (mean residual = -₹35.40), confirming that the fitted model exhibits no systematic under-pricing or over-pricing bias across the population.


## 5.3 Explainable AI (XAI) and Feature Attribution Insights


To provide full algorithmic transparency, model feature coefficients were normalized into relative percentage attributions. Figure 5 illustrates the resulting Explainable AI feature attribution hierarchy.


*Figure 5. Relative feature importance attribution (%) derived from the trained HealthSecure regression pipeline.*


The feature attribution results reveal that Annual Income (29.3%) and Body Mass Index (29.0%) represent the two most influential predictors, followed by Chronological Age (18.4%) and Geographic State (10.2%). Tobacco usage (5.2%), Covered Dependents (4.3%), Biological Sex (3.1%), and Alcohol Consumption (0.5%) contribute targeted actuarial loadings. This attribution aligns with clinical insurance underwriting, where baseline metabolic health (BMI) and age represent sustained long-term cost drivers, while behavioral surcharges apply specific discrete penalties.


## 5.4 Case Study Demonstrations Across Heterogeneous Applicant Profiles


To illustrate the real-world operational output of the model, Table 3 presents three representative case studies evaluated through the deployed HealthSecure prediction pipeline.


**Table 3. Representative Case Study Predictions Across Heterogeneous Demographic Profiles**



## 5.5 What-If Lifestyle Scenario Simulation Analysis


Through the integrated What-If simulator (/what-if), applicants can dynamically test the financial benefits of positive health interventions. Evaluating Case 3 (the 52-year-old smoker with BMI 31.4, baseline premium ₹32,162.58): when smoking cessation is simulated (smoker: yes → no), the model predicts an immediate annual premium reduction of ₹4,482.10 (a 13.9% savings). If accompanied by weight reduction lowering BMI from 31.4 to 24.8 (normal range), the annual premium drops to ₹25,980.20, achieving an aggregate annual savings of ₹6,182.38 (19.2% reduction). This capability transforms the application from a passive price calculator into an active, health-incentivizing financial advisory tool.


# 6. Limitations and Threats to Validity


While the experimental findings demonstrate strong predictive accuracy and architectural robustness, several academic limitations must be explicitly recognized:


# 1. Synthetic Ground-Truth Formulation: The target variable charges is constructed using an actuarial pure-premium equation rather than mined from proprietary, confidential rate filings of active insurers. Consequently, the model validates algorithmic approximation of this defined actuarial structure rather than commercial market prices.



# 2. Geographic and Product Scope: The active dataset reflects policyholders from six Indian states. While representative of major industrial and urban zones, results may exhibit demographic variances when generalized to northeastern or rural agricultural regions.



# 3. Dependent Count Imputation: For records lacking explicit children counts, values were probabilistically derived from policy_type classifications. While structurally consistent, future research should gather verified census counts.



# 4. Non-Interchangeability of Claims and Premiums: The model estimates annual policy subscription costs, not hospital bills. It must not be deployed for claims adjudication or medical cost reimbursement forecasting without dedicated claims modeling.



# 5. Single Held-Out Split: Benchmarking utilized a fixed 80:20 train-test partition with a fixed random seed. While effective for proof-of-concept validation, future institutional validation should apply nested k-fold cross-validation.



# 7. Conclusion


This research presented HealthSecure, an end-to-end machine learning framework and interactive digital portal for health insurance premium estimation and policy recommendation. By training on an extensive 8,000-record Indian underwriting dataset, the study engineered eight standardized profile features and established a principled actuarial target formulation that resolves the critical issue of data leakage. Comparative benchmarking confirmed that Ordinary Least Squares Linear Regression achieved the highest accuracy on held-out test data (MAE = ₹2,615.84, RMSE = ₹3,418.62, and R² = 0.6492), outperforming complex gradient-boosted ensembles on this structured additive pricing domain.

The serialized predictive pipeline was deployed into a responsive Flask web portal that presents annual premium estimates prominently at the top of results, alongside monthly affordability equivalents, multi-insurer plan comparisons across 118+ active policies, Explainable AI feature attributions, and What-If scenario simulations. The platform provides full trilingual internationalization (English, Tamil, Hindi) and dark/light mode support. In conclusion, HealthSecure demonstrates that transparent, leakage-free machine learning estimators can significantly streamline digital insurance onboarding, democratize insurance literacy, and provide consumers with objective, scientifically derived health insurance quotes.


# 8. Future Research Directions


Future research extensions will concentrate on four key domains:
• Integration of Longitudinal Wearable IoT Data: Incorporating real-time physiological telemetry (e.g., daily step counts, resting heart rate, sleep quality metrics from smart wearables) to enable dynamic, usage-based health insurance pricing.
• Partnership with Licensed General Insurers: Collaborating with regulatory bodies (IRDAI) and underwriting firms to validate model predictions against proprietary premium rate cards and real-world claim loss ratios.
• Deep Actuarial Neural Networks: Exploring specialized deep learning architectures, such as TabNet and Neural Additive Models (NAMs), to combine the interpretability of linear models with the representation capacity of deep networks.
• Algorithmic Fairness and Regulatory Auditing: Implementing formal fairness constraints (e.g., demographic parity, equalized odds) to mathematically verify that automated premium pricing remains equitable across gender, geographic, and socioeconomic cohorts.


# Acknowledgment


The authors express their deepest gratitude to Ms. K. S. Surabhi, Assistant Professor and Project Supervisor, Department of Computer Applications, Nehru College of Management, Coimbatore, for her invaluable academic guidance, constructive critique, and continuous technical supervision throughout the conceptualization, implementation, and empirical evaluation of the HealthSecure project. The authors also thank the faculty and administrative leadership of Nehru College of Management for providing the high-performance computing infrastructure and laboratory facilities essential for executing this research.


# References


[1] World Health Organization (WHO), "Universal Health Coverage and Health Financing: Global Realities and Insurance Trajectories," WHO Technical Report Series, Geneva, Switzerland, 2022. Available: https://www.who.int/news-room/fact-sheets/detail/universal-health-coverage-(uhc)

[2] Insurance Regulatory and Development Authority of India (IRDAI), "Annual Report on Health Insurance Growth, Underwriting Ratios, and Incurred Claims in India," IRDAI Publications, New Delhi, India, 2023. Available: https://irdai.gov.in

[3] K. Kaushik, A. Bhardwaj, A. D. Dwivedi, and R. Singh, "Machine Learning-Based Regression Framework to Predict Health Insurance Premiums," International Journal of Environmental Research and Public Health, vol. 19, no. 13, Art. no. 7898, pp. 1–16, 2022, doi: 10.3390/ijerph19137898.

[4] E. W. Frees, G. Meyers, and A. D. Cummings, "Predictive Modeling Applications in Actuarial Science: Volume I, Predictive Modeling Techniques," Cambridge University Press, Cambridge, UK, 2014, doi: 10.1017/CBO9781139342673.

[5] U. Orji and E. Ukwandu, "Machine Learning for an Explainable Cost Prediction of Medical Insurance," Machine Learning with Applications, vol. 15, Art. no. 100516, pp. 1–13, 2024, doi: 10.1016/j.mlwa.2023.100516.

[6] M. Kapse, V. Sharma, R. Vidhale, and V. Vellanki, "Customization of Health Insurance Premiums Using Machine Learning and Explainable AI," International Journal of Information Management Data Insights, vol. 5, no. 1, Art. no. 100328, pp. 1–14, 2025, doi: 10.1016/j.jjimei.2025.100328.

[7] S. H. Lee and M. G. Lin, "Applying Generalized Linear Models and Tree-Based Ensembles for Actuarial Pure Premium Estimation," North American Actuarial Journal, vol. 24, no. 2, pp. 245–268, 2020, doi: 10.1080/10920277.2019.1651815.

[8] J. Denuit, D. Hainaut, and J. Trufin, "Effective Statistical Learning Methods for Actuarial Science: From Generalized Linear Models to Neural Networks," Springer Actuarial Series, Springer Nature, Cham, Switzerland, 2019, doi: 10.1007/978-3-030-25820-7.

[9] A. K. Al-Kharusi, M. Al-Badi, and K. Al-Riyami, "Supervised Learning Models for Risk Profiling and Health Insurance Cost Forecasting," IEEE Access, vol. 10, pp. 112450–112465, 2022, doi: 10.1109/ACCESS.2022.3216890.

[10] S. M. Lundberg and S. I. Lee, "A Unified Approach to Interpreting Model Predictions," in Advances in Neural Information Processing Systems (NeurIPS 30), Long Beach, CA, USA, pp. 4765–4774, 2017. Available: https://proceedings.neurips.cc/paper/2017/file/8a50bae29727216477b8766125547286-Paper.pdf

[11] T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," in Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, San Francisco, CA, USA, pp. 785–794, 2016, doi: 10.1145/2939672.2939785.

[12] L. Breiman, "Random Forests," Machine Learning, vol. 45, no. 1, pp. 5–32, 2001, doi: 10.1023/A:1010933404324.

[13] shubham001official, "Indian Health Insurance Claim Analysis Dataset," Kaggle Repository, 2024. Available: https://www.kaggle.com/code/shubham001official/indian-health-insurance-claim-analysis

[14] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, et al., "Scikit-learn: Machine Learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011. Available: https://jmlr.org/papers/v12/pedregosa11a.html

[15] C. M. Bishop, "Pattern Recognition and Machine Learning," Information Science and Statistics, Springer, New York, NY, USA, 2006.

[16] M. Grinberg, "Flask Web Development: Developing Web Applications with Python," 2nd ed., O'Reilly Media, Sebastopol, CA, USA, 2018.

[17] D. W. Hosmer, S. Lemeshow, and R. X. Sturdivant, "Applied Regression Analysis," 3rd ed., Wiley Series in Probability and Statistics, John Wiley & Sons, Hoboken, NJ, USA, 2013, doi: 10.1002/9781118548387.

[18] Insurance Regulatory and Development Authority of India (IRDAI), "Health Insurance Regulations and Standardized Product Guidelines for General and Standalone Health Insurers," IRDAI Notification Ref. IRDAI/HLT/REG/CIR/2020, Hyderabad, India, 2020. Available: https://irdai.gov.in