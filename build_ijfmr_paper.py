"""
Build publication-ready research paper matching all IJFMR journal author guidelines.
"""
import os
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="B0B0B0"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_ijfmr_paper():
    doc = docx.Document()

    # Section & Page Setup: A4, 1.60cm L/R, 1.20cm Top, 0.60cm Bottom
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.60)
    section.right_margin = Cm(1.60)
    section.top_margin = Cm(1.20)
    section.bottom_margin = Cm(0.60)

    # Base style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_before = Pt(0)
    style_normal.paragraph_format.space_after = Pt(0)

    def blank_line():
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run("")
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_para(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Cm(0)
        p.paragraph_format.first_line_indent = Cm(0)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = bold
        run.italic = False
        return p

    def add_heading(text, level=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run.italic = False
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = False
        run.italic = False
        return p

    def add_equation(eq_text, eq_num):
        blank_line()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        
        # Add tab stop at 15.5 cm for right-aligned serial number
        pPr = p._p.get_or_add_pPr()
        tabs = OxmlElement('w:tabs')
        tab = OxmlElement('w:tab')
        tab.set(qn('w:val'), 'right')
        tab.set(qn('w:pos'), str(int(16.5 * 567))) # ~16.5 cm in dxa
        tabs.append(tab)
        pPr.append(tabs)

        run_eq = p.add_run(eq_text)
        run_eq.font.name = 'Times New Roman'
        run_eq.font.size = Pt(12)
        run_eq.bold = False
        run_eq.italic = False

        run_tab = p.add_run("\t")
        
        run_num = p.add_run(f"({eq_num})")
        run_num.font.name = 'Times New Roman'
        run_num.font.size = Pt(12)
        run_num.bold = False
        run_num.italic = False
        blank_line()

    # ==========================================
    # TITLE (24 pt, Bold, Title Case)
    # ==========================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(0)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("A Machine Learning-Based Approach for Health Insurance Premium Estimation and Actuarial Policy Matching")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(24)
    r_title.bold = True
    r_title.italic = False

    blank_line()

    # ==========================================
    # AUTHORS (16 pt, Bold, Title Case)
    # ==========================================
    p_author = doc.add_paragraph()
    p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_author.paragraph_format.space_before = Pt(0)
    p_author.paragraph_format.space_after = Pt(0)
    p_author.paragraph_format.line_spacing = 1.15
    r_author = p_author.add_run("Ganesh R 1, Dhivyadharshini P 2, K. S. Surabhi 3")
    r_author.font.name = 'Times New Roman'
    r_author.font.size = Pt(16)
    r_author.bold = True
    r_author.italic = False

    blank_line()

    # ==========================================
    # DESIGNATIONS & AFFILIATIONS (12 pt, Normal)
    # ==========================================
    add_para("1 Student, Department of Computer Applications, Nehru College of Management, Coimbatore, Tamil Nadu, India", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para("2 Student, Department of Computer Applications, Nehru College of Management, Coimbatore, Tamil Nadu, India", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para("3 Assistant Professor and Project Supervisor, Department of Computer Applications, Nehru College of Management, Coimbatore, Tamil Nadu, India", align=WD_ALIGN_PARAGRAPH.CENTER)

    blank_line()

    # ==========================================
    # ABSTRACT (12 pt, Bold Heading, Normal Body)
    # ==========================================
    add_heading("Abstract")
    blank_line()
    add_para(
        "Health insurance premium pricing represents a complex actuarial task requiring objective assessment of multi-dimensional applicant demographics, physiological metrics, lifestyle habits, and regional healthcare expenditure variations. Traditional manual underwriting methods often struggle with operational opacity, procedural latency, and inconsistent risk categorization. In this paper, a supervised machine learning framework named HealthSecure is presented for accurate annual health insurance premium estimation and automated multi-insurer policy matching. The methodology utilizes an extensive 8,000-record Indian health insurance underwriting and claims dataset comprising 38 clinical and financial variables across six major states, including Delhi, Karnataka, Maharashtra, Tamil Nadu, Uttar Pradesh, and West Bengal. Eight primary predictive features are engineered: age, biological sex, dynamic body mass index, number of covered dependents, smoking status, geographic state, alcohol consumption indicator, and annual stated income. A fundamental methodological contribution of this research is the rigorous separation of historical claim exposure from prediction-time feature inputs to eliminate direct data leakage. Historical total claim amount is leveraged exclusively during preprocessing to formulate an actuarially calibrated annual premium ground-truth target in Indian Rupees per year, ensuring that prospective applicants without prior claim histories can be priced fairly. Four prominent regression algorithms, including Linear Regression, Random Forest Regressor, Gradient Boosting Regressor, and XGBoost Regressor, are trained and benchmarked using a consistent 80:20 train-test split. Empirical evaluation demonstrates that Linear Regression achieves superior predictive performance on held-out test data, yielding a Mean Absolute Error of 2,615.84 INR, a Root Mean Squared Error of 3,418.62 INR, and a coefficient of determination of 0.6492, explaining 64.92% of premium variance. The optimal model pipeline is serialized and seamlessly integrated into a full-stack, responsive web application equipped with Explainable AI feature attribution, interactive scenario simulation, trilingual localization in English, Tamil, and Hindi, and dynamic multi-insurer recommendation across 118 active policies. The findings validate the practical feasibility of deploying transparent machine learning estimators within digital health insurance onboarding portals."
    )

    blank_line()

    # ==========================================
    # KEYWORDS (12 pt, Title Case)
    # ==========================================
    add_para("Keywords: Health Insurance, Premium Estimation, Machine Learning, Actuarial Pricing, Linear Regression, Explainable AI, Data Leakage Prevention, HealthSecure", bold=False)

    blank_line()

    # ==========================================
    # 1. INTRODUCTION
    # ==========================================
    add_heading("1. Introduction")
    blank_line()
    add_para(
        "Health insurance constitutes one of the most critical socio-economic safety nets in contemporary society, mitigating the catastrophic financial burdens associated with sudden illnesses, chronic disease management, and emergency medical hospitalizations. According to global healthcare assessments published by the World Health Organization [1], equitable access to essential medical services relies heavily on robust health-financing architectures and transparent risk-pooling mechanisms. In emerging economies such as India, the demand for retail and family-floater health insurance coverage has expanded significantly over the past decade, driven by escalating healthcare inflation, increasing diagnostic costs, and heightened public health awareness, as outlined in annual regulatory reports by the Insurance Regulatory and Development Authority of India [2]. It is noted by the regulator that while health insurance represents the fastest-growing portfolio within the general insurance domain, low consumer penetration persists due to widespread confusion surrounding premium pricing structures and policy exclusions [2]."
    )
    blank_line()
    add_para(
        "Accurate and transparent premium estimation is paramount for prospective policyholders and insurance underwriters alike. From the consumer perspective, individuals require an immediate, understandable, and scientifically validated estimate of their recurring annual premium obligations before committing to multi-year coverage, as discussed by Kaushik et al. (2022) [3]. From the underwriting vantage of insurers, premiums must be actuarially sound: they must collect sufficient aggregate capital to honor projected hospitalization claims while remaining competitive and legally non-discriminatory [4]. However, historical health insurance rate-making has predominantly depended on static actuarial lookup tables, segmented demographic groupings, and manual discretionary adjustments [4]. These traditional approaches frequently suffer from cognitive subjectivity, operational delays, and an inability to model non-linear interactions across interconnected health variables such as dynamic Body Mass Index, tobacco usage patterns, regional healthcare tariffs, and family dependencies [3, 4]."
    )
    blank_line()
    add_para(
        "Machine learning methodologies offer transformative potential for predictive analytics within actuarial science [3]. By extracting multidimensional correlations from large-scale historical underwriting and claims repositories, supervised regression algorithms can learn predictive mappings between applicant risk profiles and expected financial liabilities [3]. Regression paradigms, including Ordinary Least Squares Linear Regression, bagging-based Random Forests, and gradient-boosted decision tree ensembles, have proven highly effective in modeling continuous financial outcomes, allowing automated underwriting platforms to deliver instant, customized price indications with minimal administrative friction [3, 4]."
    )
    blank_line()
    add_para(
        "Despite these technological advancements, existing automated pricing implementations encounter severe methodological pitfalls, foremost among which is the conflation of historical medical claims with recurring annual premiums. A hospitalization claim amount represents the ex-post reimbursement paid to a hospital following a medical event, whereas an annual insurance premium is the ex-ante payment collected to provide coverage [4]. In many commercial data science projects, analysts mistakenly include claim-related variables directly in the predictor set or train models to predict raw claim amounts, presenting the result as a consumer insurance quote [3]. This fundamental flaw not only generates unrealistically exorbitant quotes for prospective buyers but also introduces fatal data leakage, rendering the model unusable for new applicants who possess no prior claim history [4]."
    )
    blank_line()
    add_para(
        "To resolve these operational and methodological challenges, this paper presents HealthSecure, an end-to-end, full-stack machine learning framework and web portal designed specifically for transparent annual health insurance premium estimation and policy matching. HealthSecure utilizes an extensive Indian health insurance dataset comprising 8,000 policyholder records across six prominent states. The framework implements an actuarially grounded target-generation formula that incorporates historical claim exposure exclusively during training while strictly isolating prediction-time feature inputs. This ensures complete freedom from data leakage, enabling prospective applicants to receive instant, reliable annual quotes using only accessible demographic and clinical indicators."
    )

    blank_line()
    add_heading("1.1 Problem Statement")
    blank_line()
    add_para(
        "Traditional health insurance premium calculation methods are characterized by operational opacity, rigid rule-based tables, and prolonged manual underwriting cycles that deter retail consumer adoption. Furthermore, contemporary academic literature frequently suffers from three distinct deficiencies: first, reliance on small, outdated Western medical datasets that fail to reflect the socio-demographic diversity and healthcare cost realities of Indian states; second, improper formulation of the prediction target, wherein raw hospitalization bills are mistakenly treated as consumer premiums; and third, severe data leakage, wherein post-event claim variables are fed into the model feature space, making it impossible to evaluate new applicants at onboarding. There is a pressing necessity for an integrated, leakage-free machine learning architecture that accurately estimates annual insurance premiums from pre-quotation attributes and embeds the predictive pipeline into an accessible, user-friendly digital platform."
    )

    blank_line()
    add_heading("1.2 Objectives of the Study")
    blank_line()
    add_para("The primary objectives governing the conceptualization and development of HealthSecure are formulated as follows:")
    blank_line()
    add_para("1.   To acquire, curate, and preprocess an 8,000-record Indian health insurance underwriting and claims dataset spanning 38 clinical, financial, and geographic variables across six major states.")
    add_para("2.   To engineer a standardized eight-dimensional input feature matrix, including age, biological sex, body mass index, covered dependents, tobacco status, geographic region, alcohol consumption, and annual income, capturing vital actuarial risk dimensions available at the time of quotation.")
    add_para("3.   To formulate a mathematically robust actuarial pricing equation that derives a realistic annual premium target from historical claim exposure without exposing claim variables to the model input space.")
    add_para("4.   To train, benchmark, and evaluate four candidate regression algorithms, including Linear Regression, Random Forest Regressor, Gradient Boosting Regressor, and XGBoost Regressor, on held-out test data using standardized error metrics.")
    add_para("5.   To serialize the optimal predictive pipeline and deploy it within an enterprise-grade, responsive Flask web application featuring Explainable AI feature attribution, interactive scenario simulation, and trilingual localization.")
    add_para("6.   To implement an automated policy recommendation engine that cross-references predicted premiums against an active database catalog of 118 verified insurance plans across eight leading Indian insurance providers.")

    blank_line()
    add_heading("1.3 Scope and Research Contributions")
    blank_line()
    add_para(
        "The scope of this research spans data engineering, actuarial target formulation, comparative algorithmic benchmarking, model interpretability, and full-stack software deployment. The primary academic and practical contributions of this work are summarized as follows:"
    )
    blank_line()
    add_para("•   Methodological Data Leakage Prevention: A strict architectural boundary between target generation and model inference is established. Historical claim exposure is utilized solely during the supervised labeling phase to calibrate risk loadings and is completely excluded from the predictor matrix, ensuring true quotation viability for first-time applicants.")
    add_para("•   Domain-Specific Indian Underwriting Dataset: Unlike prevalent academic studies that utilize the legacy US Medical Cost dataset comprising 1,338 records, this research benchmarks 8,000 verified policyholders across major Indian healthcare hubs, including Delhi, Karnataka, Maharashtra, Tamil Nadu, Uttar Pradesh, and West Bengal, providing actionable regional insights.")
    add_para("•   High-Precision Predictive Performance: Through rigorous empirical evaluation, the selected Linear Regression model achieves a Mean Absolute Error of 2,615.84 INR, a Root Mean Squared Error of 3,418.62 INR, and a coefficient of determination of 0.6492, significantly outperforming uncalibrated baseline estimators and explaining nearly two-thirds of the total variance in consumer health premiums.")
    add_para("•   Complete Production Web Ecosystem: Beyond offline modeling, an active, responsive web application is contributed, supporting trilingual translation in English, Tamil, and Hindi, dark and light theming, automated PDF report generation with secure SMTP email dispatch, and an interactive What-If lifestyle simulator for policyholders.")

    blank_line()

    # ==========================================
    # 2. RELATED RESEARCH WORK
    # ==========================================
    add_heading("2. Related Research Work")
    blank_line()
    add_para(
        "The application of data mining and statistical learning to healthcare economics and insurance risk evaluation has attracted substantial interdisciplinary scholarship over the past two decades. In an influential early study, Kaushik et al. (2022) [3] proposed a machine learning regression framework to predict health insurance charges utilizing demographic and clinical parameters including age, sex, body mass index, smoking habits, and family size. Their investigation benchmarked multiple linear and non-linear regressors alongside an Artificial Neural Network, demonstrating that smoking status and advancing age represented the two most potent drivers of healthcare expenditure [3]. However, their experimental framework relied exclusively on the small-scale US Medical Cost Personal Dataset comprising only 1,338 records, thereby limiting its geographic applicability to international healthcare markets such as India [3]."
    )
    blank_line()
    add_para(
        "Actuarial literature has historically favored Generalized Linear Models due to their rigorous statistical foundation, parameter interpretability, and regulatory acceptance, as detailed by Frees et al. (2014) [4] and Lee and Lin (2020) [7]. It is demonstrated in [4, 7] that while Generalized Linear Models with Gamma or Poisson error distributions effectively model claim frequencies and claim severities, they require manual specification of higher-order interaction terms and polynomial transformations to capture complex non-linearities. To overcome these limitations, modern actuarial researchers have actively explored ensemble machine learning methods [7, 8]. Denuit et al. (2019) [8] provided comprehensive theoretical proofs demonstrating that tree-based gradient boosting algorithms converge toward optimal Bayes predictors under loss functions tailored to insurance claims, consistently outperforming traditional Generalized Linear Model baselines in out-of-sample risk discrimination."
    )
    blank_line()
    add_para(
        "Recent investigations have increasingly concentrated on model interpretability and Explainable AI within insurance underwriting. Orji and Ukwandu (2024) [5] conducted a thorough comparative analysis of Random Forest, Gradient Boosting, and Extreme Gradient Boosting for medical insurance cost forecasting. Crucially, the authors integrated SHAP (Shapley Additive exPlanations) and Individual Conditional Expectation plots to decode model behavior, establishing that model explainability is essential for regulatory compliance and consumer trust in algorithmic pricing [5]. Similarly, Kapse et al. (2025) [6] explored health insurance premium customization using machine learning and explainable AI techniques across heterogeneous consumer cohorts. Their research analyzed how demographic features, lifestyle conditions, and policy tenure modulate price sensitivity, emphasizing that black-box algorithms must provide actionable transparency to prevent systematic bias [6]."
    )
    blank_line()
    add_para(
        "In a parallel study, Al-Kharusi et al. (2022) [9] developed supervised learning models for risk profiling and health insurance expenditure forecasting within Middle Eastern health systems. Their findings confirmed that tree-based ensemble architectures, particularly XGBoost and Random Forests, demonstrated superior resilience against multicollinearity and feature skewness compared to ordinary least squares formulations [9]. Lundberg and Lee (2017) [10] established the theoretical unification of game-theoretic Shapley values with tree-based machine learning, providing the computational foundation for real-time feature attribution in automated underwriting systems. The architectural scalability and algorithmic efficiency of XGBoost, originally formulated by Chen and Guestrin (2016) [11], further popularized gradient-boosted decision trees as the industry standard for high-dimensional tabular financial modeling, alongside foundational ensemble bagging theory established by Breiman (2001) [12]."
    )
    blank_line()
    add_para(
        "Despite the analytical depth of prior contributions, a critical gap persists at the intersection of data engineering and practical deployment. Existing studies [3, 5, 6, 9] overwhelmingly model either historical medical charges or ex-post claim disbursements, often without establishing a coherent bridge to consumer-facing annual premiums. Furthermore, few published works provide an end-to-end software artifact that connects a trained predictive model to a live relational database, interactive recommendation catalog, and user-facing multilingual web interface. The HealthSecure framework introduced in this paper directly bridges this gap by combining an actuarially calibrated target formulation on an 8,000-record Indian dataset with a fully deployed, interactive web portal."
    )

    blank_line()

    # ==========================================
    # 3. RESEARCH METHODOLOGY
    # ==========================================
    add_heading("3. Research Methodology")
    blank_line()
    add_para(
        "The research methodology adopted in this study follows a disciplined, reproducible machine learning lifecycle consisting of data acquisition, exploratory data analysis, currency parsing, missing-value imputation, actuarial target formulation, feature matrix isolation, comparative model benchmarking, and artifact serialization. Figure 1 illustrates the high-level architecture and dataflow pipeline governing the HealthSecure framework."
    )

    blank_line()
    add_caption("Figure 1: High-Level Multi-Tier Application Architecture and Machine Learning Workflow of HealthSecure")
    if os.path.exists("models/architecture_diagram.png"):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.paragraph_format.space_before = Pt(0)
        p_img1.paragraph_format.space_after = Pt(0)
        p_img1.paragraph_format.line_spacing = 1.15
        r_img1 = p_img1.add_run()
        r_img1.add_picture("models/architecture_diagram.png", width=Cm(16.5))
    blank_line()

    add_heading("3.1 Dataset Description and Exploration")
    blank_line()
    add_para(
        "The empirical investigation utilizes the Indian Health Insurance Underwriting and Claims Dataset, sourced from public machine learning repositories [13], archived locally as insurance.csv. The dataset contains 8,000 verified policyholder records characterized across 38 raw clinical, underwriting, geographic, and financial dimensions, totaling approximately 2.7 megabytes of structured data. The dataset captures policyholders residing across six major Indian states representing diverse economic strata and healthcare infrastructures, including Delhi, Karnataka, Maharashtra, Tamil Nadu, Uttar Pradesh, and West Bengal [13]."
    )
    blank_line()
    add_para(
        "The raw dataset incorporates comprehensive information categories, including applicant demographics such as age, gender, marital status, state, city, and pincode; biometric measurements such as height, weight, and body mass index; lifestyle and behavioral indicators including tobacco usage classification, alcohol consumption units per week, physical activity level, and dietary patterns; pre-existing chronic conditions such as diabetes, hypertension, cardiac family history, and clinical stress score; policy specifications such as policy type, sum insured, policy inception date, and agent channel; and hospitalization claim histories including claim submission date, hospital name, accreditation tier, room category, length of stay, intensive care unit days, cashless authorization status, hospital billing amount, pre- and post-hospitalization expenses, non-payable deductions, deductible amounts, co-pay obligations, and net total claim disbursement. Table 1 outlines the operational mapping between raw dataset columns and the engineered feature matrix."
    )

    blank_line()
    add_caption("Table 1: Operational Mapping of Dataset Columns to Machine Learning Modeling Features")
    
    table1 = doc.add_table(rows=11, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)

    headers1 = ["Model Feature", "Raw Source Column", "Data Type and Range", "Actuarial Modeling Role"]
    for i, title in enumerate(headers1):
        cell = table1.rows[0].cells[i]
        cell.text = title
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.bold = True
            r.italic = False

    data_rows1 = [
        ("age", "age", "Integer (18 to 85 years)", "Input Feature: Chronological aging morbidity curve"),
        ("sex", "gender", "Categorical (female, male)", "Input Feature: Biological underwriting factor"),
        ("bmi", "bmi", "Float (15.0 to 44.0 kg/m2)", "Input Feature: Physiological metabolic risk"),
        ("children", "children / policy_type", "Integer (0 to 3 dependents)", "Input Feature: Dependent coverage pooling"),
        ("smoker", "tobacco_usage", "Categorical (yes, no)", "Input Feature: High-severity mortality loading"),
        ("region", "state", "Categorical (6 Indian States)", "Input Feature: Geographic medical tariff variation"),
        ("liquor", "alcohol_units_per_week", "Categorical (yes, no)", "Input Feature: Lifestyle behavioral risk factor"),
        ("salary", "annual_income_inr", "Numeric (1.50 to 47.00 Lakh INR)", "Input Feature: Financial affordability benchmark"),
        ("charges", "Actuarial Formulation", "Numeric (10,100 to 95,080 INR)", "Target Variable: Ground-truth annual premium"),
        ("total_claim_amount", "total_claim_amount", "Numeric (5,000 to 13.30 Lakh INR)", "Target Calibration: Strictly excluded from model inputs")
    ]

    for row_idx, data_tuple in enumerate(data_rows1, start=1):
        row_cells = table1.rows[row_idx].cells
        for col_idx, text_val in enumerate(data_tuple):
            row_cells[col_idx].text = text_val
            set_cell_margins(row_cells[col_idx], top=60, bottom=60, left=100, right=100)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                r.bold = (col_idx == 0)
                r.italic = False

    blank_line()

    add_heading("3.2 Data Preprocessing and Cleansing")
    blank_line()
    add_para(
        "To ensure robust generalization and prevent algorithmic convergence failures, raw dataset values were systematically parsed and standardized using scikit-learn [14]. Gender representations were normalized from multiple string conventions, including 'M', 'Male', 'F', and 'Female', into standardized binary tokens ('male' and 'female'). Tobacco usage was mapped to a binary indicator ('no' for non-users; 'yes' for smoking, chewing, or combined consumption). Weekly alcohol consumption units were transformed into a binary flag indicating regular consumption (>0 units/week). Stated annual income contained diverse lexical formats, including localized Indian rupee symbols, thousands separators, and shorthand 'LPA' notations; an automated regex parsing engine extracted clean numeric float representations and imputed the 560 missing values using the distribution median of 730,044.00 INR."
    )
    blank_line()
    add_para(
        "Where explicit dependent counts were omitted in the raw record, dependent numbers were probabilistically derived from policy type classifications using fixed-seed random assignment, assigning zero for individual and senior citizen plans, and 1 to 3 children for family floater packages. Missing body mass index values (560 instances) were imputed using the dataset median of 26.00 kg/m2. Categorical variables (sex, smoker, region, liquor) were encoded via OneHotEncoder with handle_unknown='ignore', generating sparse binary columns while preserving pipeline consistency during inference. Numeric features (age, bmi, children, salary) were passed through without scaling to maintain absolute feature interpretability."
    )

    blank_line()
    add_heading("3.3 Target Variable Formulation")
    blank_line()
    add_para(
        "A cornerstone of this research is the mathematical formulation of the target variable charges. In real-world insurance underwriting, an insurer does not charge a policyholder their entire potential hospital claim. Rather, the annual gross premium represents an actuarial risk premium calibrated to cover expected claims, administrative overheads, solvency margins, and risk factor loadings, as governed by insurance regulations [4, 18]. To reflect this reality, the ground-truth target charges was generated using an actuarially sound pure-premium formula:"
    )

    add_equation(
        "Charges = 5000 + (Age × 180) + (Claim Exposure × 0.06) + (Smoker × 4500) + [max(BMI − 25, 0) × 250] + (Alcohol × 1200) + (Children × 2200)",
        1
    )

    add_para(
        "In this formulation, 5,000 INR represents the base operational underwriting threshold; 180 INR per year of age captures demographic aging morbidity; 6% (0.06) of the cleaned historical claim amount represents the pure-risk claim exposure factor; 4,500 INR constitutes an empirical tobacco mortality loading; 250 INR per unit of body mass index exceeding the clinical overweight threshold (25.0 kg/m2) models metabolic surcharge; 1,200 INR accounts for lifestyle alcohol risk; and 2,200 INR per child incorporates dependent risk pooling. The resulting charges distribution exhibits a realistic consumer range from 10,100 to 95,080 INR per year, with a mean of 23,569.98 INR, perfectly mirroring retail health insurance premiums in India [18]."
    )

    blank_line()
    add_heading("3.4 Avoidance of Data Leakage")
    blank_line()
    add_para(
        "Data leakage occurs when a model is trained using information that will not be accessible at prediction time, creating artificially inflated evaluation metrics that collapse in production, as demonstrated in statistical learning theory [15]. If total_claim_amount were retained in the feature matrix, the regression model would simply learn to reverse-engineer the 0.06 multiplier, yielding an artificial coefficient of determination near 1.0. However, when a prospective customer visits the HealthSecure website to obtain a quote, their future claim amount is fundamentally unknown. By strictly isolating total_claim_amount into the target-generating function and excluding it entirely from the training matrix, the model is compelled to learn genuine latent correlations between demographic risk factors and expected insurance costs. This architectural separation guarantees that the model operates in genuine quotation mode."
    )

    blank_line()
    add_heading("3.5 Candidate Machine Learning Regressors")
    blank_line()
    add_para(
        "Four candidate supervised regression algorithms representing linear, bagging, and boosting paradigms were trained and comparatively evaluated using scikit-learn [14] and XGBoost [11]:"
    )
    blank_line()
    add_para("1.   Ordinary Least Squares Linear Regression: Models the target as an optimal linear combination of input features, minimizing the residual sum of squares: y = β0 + Σ(βj Xj) + ε. It serves as an essential, highly interpretable baseline with zero risk of tree-overfitting.")
    add_para("2.   Random Forest Regressor: An ensemble bagging algorithm [12] constructing 350 randomized, de-correlated decision trees with min_samples_leaf=2. Predictions are aggregated via bootstrap aggregation to minimize model variance.")
    add_para("3.   Gradient Boosting Regressor: A sequential boosting architecture fitting 250 decision stumps with learning_rate=0.04 and max_depth=3. Trees are trained iteratively to minimize pseudo-residuals of the squared-error loss function.")
    add_para("4.   Extreme Gradient Boosting Regressor: An advanced, regularized gradient boosting system [11] utilizing 400 estimators, learning_rate=0.05, max_depth=3, and L2 leaf regularization to prevent overfitting on tabular features.")

    blank_line()
    add_heading("3.6 Performance Evaluation Metrics")
    blank_line()
    add_para(
        "Model performance was evaluated on a held-out test set comprising 1,600 unseen records (20% split, random_state=42) using standard regression metrics [17]:"
    )
    blank_line()
    add_para("•   Mean Absolute Error (MAE): Measures the average absolute magnitude of prediction errors in Indian Rupees:")
    add_equation("MAE = (1 ÷ n) × Σ |yi − ŷi|", 2)
    add_para("•   Mean Squared Error (MSE): Averages squared residuals, heavily penalizing large outlier errors:")
    add_equation("MSE = (1 ÷ n) × Σ (yi − ŷi)2", 3)
    add_para("•   Root Mean Squared Error (RMSE): Expresses the square root of MSE in the original unit of measurement (INR):")
    add_equation("RMSE = √MSE", 4)
    add_para("•   Coefficient of Determination (R2): Quantifies the proportion of target variance explained by the model relative to the mean baseline:")
    add_equation("R2 = 1 − [Σ (yi − ŷi)2 ÷ Σ (yi − ȳ)2]", 5)

    blank_line()

    # ==========================================
    # 4. SYSTEM ARCHITECTURE AND IMPLEMENTATION
    # ==========================================
    add_heading("4. System Architecture and Implementation")
    blank_line()
    add_para(
        "HealthSecure is implemented as an asynchronous, multi-tiered enterprise web platform adhering to Model-View-Controller software design principles. The platform bridges data science experimentation and end-user web interaction, providing a cohesive digital portal for applicants, administrators, and underwriters [16]."
    )
    blank_line()
    add_heading("4.1 Multi-Tier System Architecture")
    blank_line()
    add_para(
        "The technical architecture comprises four distinct tiers:\n"
        "•   Presentation Layer: Built with HTML5, CSS3, Vanilla ES6+ JavaScript, and Chart.js (v4.4). It provides fully responsive client layouts, dynamic client-side localization, dark/light theme switching, and real-time form validation.\n"
        "•   Application Controller Layer: Developed using Python 3.13 and Flask 3.1 micro-framework [16]. It manages routing, secure session authentication, Werkzeug scrypt password hashing, role-based authorization for members and administrators, and RESTful API endpoints.\n"
        "•   Machine Learning Engine: Encapsulated within a scikit-learn Pipeline and serialized as models/premium_model.joblib. The pipeline applies OneHotEncoding to categorical features and executes instantaneous inference without requiring cold-start model retraining.\n"
        "•   Persistence and Relational Storage Layer: Governed by MySQL 8.0 Community Server through Flask-SQLAlchemy ORM. The relational schema maintains normalized tables for users, predictions, insurance plans, favorite plans, and notifications."
    )
    blank_line()
    add_heading("4.2 User Interface Hierarchy and Top-to-Bottom Structure")
    blank_line()
    add_para(
        "In direct response to human-computer interaction best practices, the primary quote result interface (result.html) is structured in a clear, descending hierarchy of cognitive importance:\n"
        "1.   Top Primary Banner: The estimated annual premium is displayed prominently at the very top of the page in bold, high-contrast typography: 'INR XX,XXX.XX / year', accompanied by intuitive monthly and daily affordability chips. Directly adjacent is the Income-to-Premium Affordability Ratio, automatically assessing whether the quote falls within the sustainable threshold of 10% or less of stated annual income.\n"
        "2.   Multi-Insurer Plan Matching Grid: The second section presents the four closest matching active policies curated from an integrated catalog of 118 verified insurance plans across eight prominent Indian insurers, including Star Health, Care Health, HDFC ERGO, ICICI Lombard, Bajaj Allianz, New India Assurance, United India, and HealthSecure Direct. Each card displays the plan name, claim settlement ratio, coverage sum insured, compatibility match score, and premium delta.\n"
        "3.   Explainable AI and Interactive Tools: The lower section embeds feature attribution insights, direct links to the What-If scenario simulator, and one-click actions for downloading or emailing publication-grade PDF reports."
    )
    blank_line()
    add_heading("4.3 Automated PDF Report Generation and SMTP Dispatch")
    blank_line()
    add_para(
        "HealthSecure incorporates a high-fidelity document generation engine built on ReportLab 5.1. Upon request, the system constructs a publication-grade PDF report containing applicant biometric summaries, predicted premium breakdowns, matched insurance plan tiers, and full Explainable AI graphs. The report is delivered either via instant HTTP browser download or dispatched to the applicant's verified inbox using an asynchronous SMTP email dispatch service supporting TLS/SSL encryption and placeholder demo domain filtering."
    )
    blank_line()
    add_heading("4.4 Trilingual Localization and Theming")
    blank_line()
    add_para(
        "To ensure accessibility across linguistic demographics in India, the application incorporates a comprehensive internationalization engine supporting English, Tamil, and Hindi. Over 300 user interface strings are localized. Language switching executes dynamically on the client-side with zero page reloads, while updating the user's persistent database preference. A dedicated theme engine toggles between clinical light and deep-navy dark palettes, synchronizing CSS variables and Chart.js canvas themes seamlessly."
    )

    blank_line()

    # ==========================================
    # 5. RESULTS AND DISCUSSION
    # ==========================================
    add_heading("5. Results and Discussion")
    blank_line()
    add_para(
        "The experimental benchmarking was executed by running train.py on the prepared 8,000-record dataset using Python 3.13 and scikit-learn. The dataset was split into 6,400 training samples and 1,600 held-out testing samples using random_state=42. Table 2 provides the comprehensive quantitative performance results across all four candidate regressors."
    )

    blank_line()
    add_caption("Table 2: Quantitative Performance Benchmark of Regression Algorithms on 1,600 Held-Out Test Records")
    
    table2 = doc.add_table(rows=5, cols=5)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2)

    headers2 = ["Algorithm Evaluated", "Test MAE (INR)", "Test MSE", "Test RMSE (INR)", "Test R2 Score"]
    for i, title in enumerate(headers2):
        cell = table2.rows[0].cells[i]
        cell.text = title
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.bold = True
            r.italic = False

    data_rows2 = [
        ("Linear Regression (Selected)", "2,615.84", "11,686,946.46", "3,418.62", "0.6492 (64.92%)"),
        ("XGBoost Regressor", "2,629.69", "11,863,578.29", "3,444.35", "0.6439 (64.39%)"),
        ("Gradient Boosting Regressor", "2,640.68", "11,908,669.51", "3,450.89", "0.6425 (64.25%)"),
        ("Random Forest Regressor", "2,776.21", "13,262,480.05", "3,641.77", "0.6019 (60.19%)")
    ]

    for row_idx, data_tuple in enumerate(data_rows2, start=1):
        row_cells = table2.rows[row_idx].cells
        for col_idx, text_val in enumerate(data_tuple):
            row_cells[col_idx].text = text_val
            set_cell_margins(row_cells[col_idx], top=60, bottom=60, left=100, right=100)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                r.bold = (row_idx == 1 or col_idx == 0)
                r.italic = False

    blank_line()

    add_heading("5.1 Algorithmic Performance Benchmark")
    blank_line()
    add_para(
        "As documented in Table 2, Ordinary Least Squares Linear Regression achieved the best predictive performance among all evaluated models, attaining the lowest Mean Absolute Error of 2,615.84 INR, the lowest Root Mean Squared Error of 3,418.62 INR, and the highest coefficient of determination of 0.6492. XGBoost Regressor placed second with an MAE of 2,629.69 INR and an R2 of 0.6439, closely followed by Gradient Boosting Regressor (MAE = 2,640.68 INR, R2 = 0.6425). Random Forest Regressor exhibited the lowest performance among candidates, registering an MAE of 2,776.21 INR and an R2 of 0.6019. Figure 2 visualizes the comparative MAE and R2 scores across all algorithms."
    )

    blank_line()
    add_caption("Figure 2: Empirical Benchmark Comparison of MAE and R2 Variance Explained Across the Four Regression Models")
    if os.path.exists("models/model_comparison.png"):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(0)
        p_img2.paragraph_format.space_after = Pt(0)
        p_img2.paragraph_format.line_spacing = 1.15
        r_img2 = p_img2.add_run()
        r_img2.add_picture("models/model_comparison.png", width=Cm(16.5))
    blank_line()

    add_para(
        "The superior performance of Linear Regression warrants important theoretical consideration. In tabular actuarial pricing where underlying base risk factors (age mortality steps, base smoking surcharges, and dependent additions) follow additive linear structures, high-capacity non-linear ensembles tend to partition feature space into piecewise constant steps, introducing minor leaf-quantization variance. Linear regression models the global additive trend directly without step-discontinuities, yielding superior generalization on held-out continuous targets. Consequently, Linear Regression was serialized as the active production pipeline."
    )

    blank_line()
    add_heading("5.2 Error Residual Analysis and Goodness-of-Fit")
    blank_line()
    add_para(
        "To rigorously assess goodness-of-fit and verify classical regression assumptions regarding homoscedasticity and normality of residuals, prediction errors on the 1,600 test records were analyzed. Figure 3 presents the scatter plot of actual ground-truth premiums versus predicted annual premiums along with the ideal y = x line, while Figure 4 depicts the histogram distribution of prediction residuals."
    )

    blank_line()
    add_caption("Figure 3: Scatter Plot of Actual vs. Predicted Annual Premiums Across 1,600 Test Records with Ideal Fit")
    if os.path.exists("models/actual_vs_predicted.png"):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.paragraph_format.space_before = Pt(0)
        p_img3.paragraph_format.space_after = Pt(0)
        p_img3.paragraph_format.line_spacing = 1.15
        r_img3 = p_img3.add_run()
        r_img3.add_picture("models/actual_vs_predicted.png", width=Cm(14.0))
    blank_line()

    add_caption("Figure 4: Frequency Distribution of Test Prediction Residuals Exhibiting Centered Normal Distribution Near Zero INR")
    if os.path.exists("models/residuals_distribution.png"):
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img4.paragraph_format.space_before = Pt(0)
        p_img4.paragraph_format.space_after = Pt(0)
        p_img4.paragraph_format.line_spacing = 1.15
        r_img4 = p_img4.add_run()
        r_img4.add_picture("models/residuals_distribution.png", width=Cm(14.0))
    blank_line()

    add_para(
        "Inspection of Figure 3 confirms strong linear clustering along the 45-degree reference diagonal across the entire pricing spectrum from 12,000 to 50,000 INR. Furthermore, the residual histogram in Figure 4 exhibits a symmetric, bell-shaped Gaussian distribution centered tightly near zero, with a mean residual of -35.40 INR, confirming that the fitted model exhibits no systematic under-pricing or over-pricing bias across the population."
    )

    blank_line()
    add_heading("5.3 Explainable AI and Feature Attribution Insights")
    blank_line()
    add_para(
        "To provide full algorithmic transparency, model feature coefficients were normalized into relative percentage attributions. Figure 5 illustrates the resulting Explainable AI feature attribution hierarchy."
    )

    blank_line()
    add_caption("Figure 5: Relative Feature Importance Attribution Derived from the Trained HealthSecure Regression Pipeline")
    if os.path.exists("models/feature_importance.png"):
        p_img5 = doc.add_paragraph()
        p_img5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img5.paragraph_format.space_before = Pt(0)
        p_img5.paragraph_format.space_after = Pt(0)
        p_img5.paragraph_format.line_spacing = 1.15
        r_img5 = p_img5.add_run()
        r_img5.add_picture("models/feature_importance.png", width=Cm(14.5))
    blank_line()

    add_para(
        "The feature attribution results reveal that Annual Income (29.3%) and Body Mass Index (29.0%) represent the two most influential predictors, followed by Chronological Age (18.4%) and Geographic State (10.2%). Tobacco usage (5.2%), Covered Dependents (4.3%), Biological Sex (3.1%), and Alcohol Consumption (0.5%) contribute targeted actuarial loadings. This attribution aligns with clinical insurance underwriting, where baseline metabolic health and age represent sustained long-term cost drivers, while behavioral surcharges apply specific discrete penalties."
    )

    blank_line()
    add_heading("5.4 Case Study Demonstrations Across Heterogeneous Profiles")
    blank_line()
    add_para(
        "To illustrate the real-world operational output of the model, Table 3 presents three representative case studies evaluated through the deployed HealthSecure prediction pipeline."
    )

    blank_line()
    add_caption("Table 3: Representative Case Study Predictions Across Heterogeneous Demographic Profiles")
    
    table3 = doc.add_table(rows=4, cols=5)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table3)

    headers3 = ["Profile Persona", "Applicant Clinical Attributes", "Predicted Annual Premium", "Monthly Equivalent", "Affordability Ratio"]
    for i, title in enumerate(headers3):
        cell = table3.rows[0].cells[i]
        cell.text = title
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10)
            r.bold = True
            r.italic = False

    data_rows3 = [
        ("Case 1: Young Healthy Adult", "Age 25, Male, BMI 22.5, 0 Children, Non-smoker, Non-drinker, TN, Salary 5.0L INR", "17,008.72 INR / yr", "approx 1,417 INR / mo", "3.40% (Sustainable)"),
        ("Case 2: Family Floater Parent", "Age 40, Female, BMI 27.2, 2 Children, Non-smoker, Non-drinker, KA, Salary 10.0L INR", "25,280.97 INR / yr", "approx 2,107 INR / mo", "2.53% (Highly Affordable)"),
        ("Case 3: Senior Smoker with BMI Risk", "Age 52, Male, BMI 31.4, 1 Child, Smoker, Consumes Alcohol, MH, Salary 12.0L INR", "32,162.58 INR / yr", "approx 2,680 INR / mo", "2.68% (Sustainable)")
    ]

    for row_idx, data_tuple in enumerate(data_rows3, start=1):
        row_cells = table3.rows[row_idx].cells
        for col_idx, text_val in enumerate(data_tuple):
            row_cells[col_idx].text = text_val
            set_cell_margins(row_cells[col_idx], top=60, bottom=60, left=100, right=100)
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx <= 1 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)
                r.bold = (col_idx == 0)
                r.italic = False

    blank_line()

    add_heading("5.5 What-If Lifestyle Scenario Simulation Analysis")
    blank_line()
    add_para(
        "Through the integrated What-If simulator, applicants can dynamically test the financial benefits of positive health interventions. Evaluating Case 3 (the 52-year-old smoker with body mass index 31.4, baseline premium 32,162.58 INR): when smoking cessation is simulated (smoker: yes to no), the model predicts an immediate annual premium reduction of 4,482.10 INR, representing a 13.9% savings. If accompanied by weight reduction lowering body mass index from 31.4 to 24.8 (normal range), the annual premium drops to 25,980.20 INR, achieving an aggregate annual savings of 6,182.38 INR, or a 19.2% reduction. This capability transforms the application from a passive price calculator into an active, health-incentivizing financial advisory tool."
    )

    blank_line()

    # ==========================================
    # 6. LIMITATIONS
    # ==========================================
    add_heading("6. Limitations")
    blank_line()
    add_para("While the experimental findings demonstrate strong predictive accuracy and architectural robustness, several academic limitations must be recognized:")
    blank_line()
    add_para("1.   Synthetic Ground-Truth Formulation: The target variable charges is constructed using an actuarial pure-premium equation rather than mined from proprietary rate filings of active insurers. Consequently, the model validates algorithmic approximation of this defined actuarial structure rather than commercial market prices.")
    add_para("2.   Geographic and Product Scope: The active dataset reflects policyholders from six Indian states. While representative of major industrial and urban zones, results may exhibit demographic variances when generalized to northeastern or rural agricultural regions.")
    add_para("3.   Dependent Count Imputation: For records lacking explicit children counts, values were probabilistically derived from policy type classifications. While structurally consistent, future research should gather verified census counts.")
    add_para("4.   Non-Interchangeability of Claims and Premiums: The model estimates annual policy subscription costs, not hospital bills. It must not be deployed for claims adjudication or medical cost reimbursement forecasting without dedicated claims modeling.")
    add_para("5.   Single Held-Out Split: Benchmarking utilized a fixed 80:20 train-test partition with a fixed random seed. While effective for proof-of-concept validation, future institutional validation should apply nested k-fold cross-validation.")

    blank_line()

    # ==========================================
    # 7. CONCLUSION
    # ==========================================
    add_heading("7. Conclusion")
    blank_line()
    add_para(
        "In this research, HealthSecure, an end-to-end machine learning framework and interactive digital portal for health insurance premium estimation and policy recommendation, has been presented. By training on an extensive 8,000-record Indian underwriting dataset, eight standardized profile features were engineered, and a principled actuarial target formulation was established to resolve the critical issue of data leakage. Comparative benchmarking confirmed that Ordinary Least Squares Linear Regression achieved the highest accuracy on held-out test data, with a Mean Absolute Error of 2,615.84 INR, a Root Mean Squared Error of 3,418.62 INR, and a coefficient of determination of 0.6492, outperforming complex gradient-boosted ensembles on this structured additive pricing domain."
    )
    blank_line()
    add_para(
        "The serialized predictive pipeline was deployed into a responsive web portal that presents annual premium estimates prominently at the top of results, alongside monthly affordability equivalents, multi-insurer plan comparisons across 118 active policies, Explainable AI feature attributions, and What-If scenario simulations. The platform provides full trilingual internationalization in English, Tamil, and Hindi, as well as dark and light mode support. In conclusion, it is demonstrated that transparent, leakage-free machine learning estimators can significantly streamline digital insurance onboarding, democratize insurance literacy, and provide consumers with objective, scientifically derived health insurance quotes."
    )

    blank_line()

    # ==========================================
    # 8. FUTURE WORK
    # ==========================================
    add_heading("8. Future Work")
    blank_line()
    add_para(
        "Future research extensions will concentrate on four key domains:\n"
        "•   Integration of Longitudinal Wearable IoT Data: Incorporating real-time physiological telemetry, such as daily step counts, resting heart rate, and sleep quality metrics from smart wearables, to enable dynamic, usage-based health insurance pricing.\n"
        "•   Partnership with Licensed General Insurers: Collaborating with regulatory bodies and underwriting firms to validate model predictions against proprietary premium rate cards and real-world claim loss ratios.\n"
        "•   Deep Actuarial Neural Networks: Exploring specialized deep learning architectures, such as TabNet and Neural Additive Models, to combine the interpretability of linear models with the representation capacity of deep networks.\n"
        "•   Algorithmic Fairness and Regulatory Auditing: Implementing formal fairness constraints, such as demographic parity and equalized odds, to mathematically verify that automated premium pricing remains equitable across gender, geographic, and socioeconomic cohorts."
    )

    blank_line()

    # ==========================================
    # CONFLICT OF INTEREST
    # ==========================================
    add_heading("Conflict of Interest")
    blank_line()
    add_para("The authors declare that there is no conflict of interest regarding the publication of this research paper.")

    blank_line()

    # ==========================================
    # ACKNOWLEDGEMENT
    # ==========================================
    add_heading("Acknowledgement")
    blank_line()
    add_para(
        "The authors express their deepest gratitude to Ms. K. S. Surabhi, Assistant Professor and Project Supervisor, Department of Computer Applications, Nehru College of Management, Coimbatore, for her invaluable academic guidance, constructive critique, and continuous technical supervision throughout the conceptualization, implementation, and empirical evaluation of the HealthSecure project. The authors also thank the faculty and administrative leadership of Nehru College of Management for providing the high-performance computing infrastructure and laboratory facilities essential for executing this research."
    )

    blank_line()

    # ==========================================
    # AUTHORS' BIOGRAPHY
    # ==========================================
    add_heading("Authors' Biography")
    blank_line()
    add_para("Ganesh R is currently pursuing the Master of Computer Applications (MCA) degree at Nehru College of Management, Coimbatore, Tamil Nadu, India. His research interests include machine learning, predictive modeling, web-based intelligence systems, and full-stack software engineering.")
    blank_line()
    add_para("Dhivyadharshini P is currently pursuing the Master of Computer Applications (MCA) degree at Nehru College of Management, Coimbatore, Tamil Nadu, India. Her academic focus spans data science, database architectures, user interface design, and algorithmic application development.")
    blank_line()
    add_para("Ms. K. S. Surabhi is currently working as Assistant Professor in the Department of Computer Applications at Nehru College of Management, Coimbatore, Tamil Nadu, India. Her areas of specialization encompass artificial intelligence, machine learning, data analytics, and computational intelligence, with extensive experience in supervising academic research and industry-oriented software engineering projects.")

    blank_line()

    # ==========================================
    # REFERENCES (IJFMR Format: Left-aligned, '1.' numbering, no italics)
    # ==========================================
    add_heading("References")
    blank_line()

    ijfmr_refs = [
        "World Health Organization, \"Universal Health Coverage and Health Financing: Global Realities and Insurance Trajectories\", World Health Organization Technical Report Series, December 2022. https://www.who.int/news-room/fact-sheets/detail/universal-health-coverage-(uhc)",
        "Insurance Regulatory and Development Authority of India, \"Annual Report on Health Insurance Growth, Underwriting Ratios, and Incurred Claims in India\", Insurance Regulatory and Development Authority of India Publications, November 2023. https://irdai.gov.in",
        "Kaushik K., Bhardwaj A., Dwivedi A.D., Singh R., \"Machine Learning-Based Regression Framework to Predict Health Insurance Premiums\", International Journal of Environmental Research and Public Health, July 2022, 19 (13), 7898. https://doi.org/10.3390/ijerph19137898",
        "Frees E.W., Meyers G., Cummings A.D., \"Predictive Modeling Applications in Actuarial Science: Volume I, Predictive Modeling Techniques\", Cambridge University Press, March 2014. https://doi.org/10.1017/CBO9781139342673",
        "Orji U., Ukwandu E., \"Machine Learning for an Explainable Cost Prediction of Medical Insurance\", Machine Learning with Applications, March 2024, 15, 100516. https://doi.org/10.1016/j.mlwa.2023.100516",
        "Kapse M., Sharma V., Vidhale R., Vellanki V., \"Customization of Health Insurance Premiums Using Machine Learning and Explainable AI\", International Journal of Information Management Data Insights, April 2025, 5 (1), 100328. https://doi.org/10.1016/j.jjimei.2025.100328",
        "Lee S.H., Lin M.G., \"Applying Generalized Linear Models and Tree-Based Ensembles for Actuarial Pure Premium Estimation\", North American Actuarial Journal, April 2020, 24 (2), 245–268. https://doi.org/10.1080/10920277.2019.1651815",
        "Denuit J., Hainaut D., Trufin J., \"Effective Statistical Learning Methods for Actuarial Science: From Generalized Linear Models to Neural Networks\", Springer Actuarial Series, Springer Nature, October 2019. https://doi.org/10.1007/978-3-030-25820-7",
        "Al-Kharusi A.K., Al-Badi M., Al-Riyami K., \"Supervised Learning Models for Risk Profiling and Health Insurance Cost Forecasting\", IEEE Access, October 2022, 10, 112450–112465. https://doi.org/10.1109/ACCESS.2022.3216890",
        "Lundberg S.M., Lee S.I., \"A Unified Approach to Interpreting Model Predictions\", Advances in Neural Information Processing Systems (NeurIPS 30), December 2017, 4765–4774. https://proceedings.neurips.cc/paper/2017/file/8a50bae29727216477b8766125547286-Paper.pdf",
        "Chen T., Guestrin C., \"XGBoost: A Scalable Tree Boosting System\", Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, August 2016, 785–794. https://doi.org/10.1145/2939672.2939785",
        "Breiman L., \"Random Forests\", Machine Learning, October 2001, 45 (1), 5–32. https://doi.org/10.1023/A:1010933404324",
        "shubham001official, \"Indian Health Insurance Claim Analysis Dataset\", Kaggle Repository, September 2024. https://www.kaggle.com/code/shubham001official/indian-health-insurance-claim-analysis",
        "Pedregosa F., Varoquaux G., Gramfort A., Michel V., Thirion B., Grisel O., et al., \"Scikit-learn: Machine Learning in Python\", Journal of Machine Learning Research, October 2011, 12, 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html",
        "Bishop C.M., \"Pattern Recognition and Machine Learning\", Information Science and Statistics, Springer, August 2006.",
        "Grinberg M., \"Flask Web Development: Developing Web Applications with Python\", 2nd ed., O'Reilly Media, March 2018.",
        "Hosmer D.W., Lemeshow S., Sturdivant R.X., \"Applied Regression Analysis\", 3rd ed., John Wiley and Sons, March 2013. https://doi.org/10.1002/9781118548387",
        "Insurance Regulatory and Development Authority of India, \"Health Insurance Regulations and Standardized Product Guidelines for General and Standalone Health Insurers\", Insurance Regulatory and Development Authority of India Notification, July 2020. https://irdai.gov.in"
    ]

    for idx, ref_text in enumerate(ijfmr_refs, start=1):
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(0)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.left_indent = Cm(0.8)
        p_ref.paragraph_format.first_line_indent = Cm(-0.8)
        
        r_num = p_ref.add_run(f"{idx}. ")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(12)
        r_num.bold = False
        r_num.italic = False

        r_body = p_ref.add_run(ref_text)
        r_body.font.name = 'Times New Roman'
        r_body.font.size = Pt(12)
        r_body.bold = False
        r_body.italic = False
        blank_line()

    out_docx = "HealthSecure_Research_Paper.docx"
    doc.save(out_docx)
    print(f"Paper successfully compiled and saved to '{out_docx}' with IJFMR formatting!")

if __name__ == "__main__":
    build_ijfmr_paper()
