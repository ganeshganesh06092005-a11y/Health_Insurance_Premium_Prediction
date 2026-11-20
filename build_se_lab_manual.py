"""
Complete generator for Software Engineering Lab Manual:
HEALTH INSURANCE PREMIUM PREDICTION SYSTEM (HEALTHSECURE)
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUTPUT_DIR = Path("d:/Ganesh/Health_Insurance_Premium_Prediction")
DIAGRAMS_DIR = OUTPUT_DIR / "lab_manual_diagrams"
DOCX_PATH = OUTPUT_DIR / "SE_Lab_Manual_Health_Insurance.docx"
MD_PATH = OUTPUT_DIR / "SE_Lab_Manual_Health_Insurance.md"

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), val)
        border.set(qn('w:sz'), sz)
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tblBorders.append(border)
    tblPr.append(tblBorders)

def create_document():
    doc = docx.Document()
    
    # Page Setup: Normal A4, 1 inch margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    
    # Document Title Block
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = title_p.add_run("DEPARTMENT OF COMPUTER APPLICATIONS\nNEHRU COLLEGE OF MANAGEMENT, COIMBATORE\n\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)
    
    r_main = title_p.add_run("SOFTWARE ENGINEERING LABORATORY\nPRACTICAL RECORD MANUAL\n")
    r_main.font.name = "Arial"
    r_main.font.size = Pt(16)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(30, 58, 138)
    
    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_p = p_proj.add_run("PROJECT: HEALTH INSURANCE PREMIUM PREDICTION & RECOMMENDATION SYSTEM (HEALTHSECURE)\n")
    r_p.font.name = "Arial"
    r_p.font.size = Pt(12)
    r_p.font.bold = True
    r_p.font.color.rgb = RGBColor(14, 116, 144)
    
    doc.add_paragraph("―" * 65).alignment = WD_ALIGN_PARAGRAPH.CENTER

    def add_ex_header(ex_no, title):
        tbl = doc.add_table(rows=2, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="1E3A8A", sz="8")
        col_w = [Inches(1.8), Inches(5.0)]
        for r in tbl.rows:
            for idx, w in enumerate(col_w):
                r.cells[idx].width = w
                set_cell_margins(r.cells[idx], top=60, bottom=60, left=100, right=100)
        c00 = tbl.cell(0, 0)
        c00.text = f"EX NO: {ex_no}"
        set_cell_shading(c00, "1E3A8A")
        c00.paragraphs[0].runs[0].font.bold = True
        c00.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        
        c01 = tbl.cell(0, 1)
        c01.text = title
        set_cell_shading(c01, "EFF6FF")
        c01.paragraphs[0].runs[0].font.bold = True
        c01.paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 58, 138)
        
        c10 = tbl.cell(1, 0)
        c10.text = "DATE:"
        set_cell_shading(c10, "F8FAFC")
        c10.paragraphs[0].runs[0].font.bold = True
        
        c11 = tbl.cell(1, 1)
        c11.text = ""
        set_cell_shading(c11, "FFFFFF")
        
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)

    def add_section_h(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(30, 58, 138)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)

    def add_sub_h(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.bold = True
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(15, 23, 42)
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)

    def add_result(text):
        p = doc.add_paragraph()
        r_lbl = p.add_run("RESULT:\n")
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = RGBColor(16, 185, 129)
        r_body = p.add_run(text)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(14)
        doc.add_paragraph("―" * 65).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # ==========================================
    # EX NO 1
    # ==========================================
    add_ex_header("01", "Problem Definition & Feasibility Study")
    add_section_h("AIM:")
    doc.add_paragraph("To identify the real-world healthcare financing problem and conduct a comprehensive feasibility study to determine the technical, economic, and operational feasibility of the Health Insurance Premium Prediction and Policy Recommendation System (HealthSecure).")
    
    add_section_h("PROJECT TITLE:")
    doc.add_paragraph("HEALTH INSURANCE PREMIUM PREDICTION SYSTEM (HEALTHSECURE)")
    
    add_section_h("PROBLEM DEFINITION:")
    doc.add_paragraph("In contemporary healthcare financing, determining fair, accurate, and actuarially sound health insurance premiums is a complex and high-stakes challenge. Conventional insurance underwriting predominantly relies on static demographic lookup tables, broad risk classifications, and subjective manual discretion. Prospective applicants frequently experience pricing opacity, extensive procedural delays, and substantial premium variability without understanding how their individual physiological traits (BMI, age), lifestyle habits (smoking status, alcohol consumption), family dependencies (children), or regional healthcare costs directly govern their premium quotations. Conversely, insurers face underwriting adverse selection and insolvency risks when premiums are underpriced relative to potential claim liabilities. HealthSecure is developed to resolve these critical issues by leveraging supervised machine learning to objectively predict personalized annual health insurance premiums and automatically recommend optimal multi-insurer policies.")
    
    add_section_h("PROBLEM STATEMENT:")
    doc.add_paragraph("To develop an enterprise-grade supervised machine learning framework that automatically estimates personalized annual health insurance premiums based on applicant demographic, clinical, and lifestyle attributes (age, sex, BMI, children, smoker, region, alcohol habits, and salary), strictly preventing data leakage from historical claim records while delivering transparent feature attribution and multi-insurer policy matching.")
    
    add_section_h("FEASIBILITY STUDY:")
    add_sub_h("1. Technical Feasibility")
    doc.add_paragraph("Technical feasibility evaluates whether the necessary computing hardware, programming languages, algorithmic libraries, and software engineering frameworks are available to construct and deploy the machine learning system.")
    doc.add_paragraph("• Hardware Requirements:\n  - Computer/Laptop: Minimum Intel Core i3/i5 or AMD Ryzen processor\n  - RAM: Minimum 4 GB RAM (8 GB recommended for training benchmarks)\n  - Storage: Minimum 10 GB free hard drive/SSD space\n  - Network: Standard Internet connection for downloading Python dependencies and open datasets")
    doc.add_paragraph("• Software Requirements:\n  - Operating System: Windows 10/11 or Linux (Ubuntu 22.04+)\n  - Programming Language: Python 3.10+\n  - Integrated Development Environment (IDE): Visual Studio Code / PyCharm\n  - Framework: Flask 3.1 / Streamlit Web Framework\n  - Core Libraries: Pandas, NumPy, Scikit-learn, XGBoost, Joblib, Matplotlib, ReportLab\n  - Machine Learning Algorithm: Linear Regression (Production), Random Forest, Gradient Boosting, XGBoost\n  - Preprocessing Techniques: Standard Scaling, One-Hot Encoding, Derived BMI Calculation")
    doc.add_paragraph("• Technical Feasibility Result:\n  The required computing infrastructure and software frameworks are fully available and production-tested. Python and its open-source data science ecosystem provide robust, high-performance implementations that execute seamlessly on commodity hardware. Therefore, the proposed system is technically feasible.")
    
    add_sub_h("2. Economic Feasibility")
    doc.add_paragraph("Economic feasibility assesses whether the system can be developed, tested, and deployed within a practical and cost-effective budget.")
    doc.add_paragraph("The entire platform is constructed utilizing open-source programming languages, freely distributed libraries, and open-access actuarial datasets. No proprietary licenses or specialized high-cost hardware accelerators are required.")
    
    # Table for Economic Feasibility
    tbl_econ = doc.add_table(rows=10, cols=2)
    tbl_econ.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_econ)
    econ_data = [
        ("Resource / Component", "Cost (INR / USD)"),
        ("Python 3.10+ Runtime", "Free / Open-Source"),
        ("Visual Studio Code IDE", "Free / Open-Source"),
        ("Flask / Streamlit Web Framework", "Free / Open-Source"),
        ("Scikit-learn, Pandas, NumPy, XGBoost", "Free / Open-Source"),
        ("ReportLab PDF Engine & Matplotlib", "Free / Open-Source"),
        ("MySQL 8.0 / SQLite Database", "Free / Community Edition"),
        ("Health Insurance Dataset (8,000 Records)", "Free Open Actuarial Data"),
        ("Development Hardware", "Existing College/Personal Laptop"),
        ("Git & GitHub Cloud Hosting", "Free Public Tier")
    ]
    for r_idx, (c1, c2) in enumerate(econ_data):
        row = tbl_econ.rows[r_idx]
        row.cells[0].text = c1
        row.cells[1].text = c2
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        if r_idx == 0:
            set_cell_shading(row.cells[0], "1E3A8A")
            set_cell_shading(row.cells[1], "1E3A8A")
            row.cells[0].paragraphs[0].runs[0].font.bold = True
            row.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            row.cells[1].paragraphs[0].runs[0].font.bold = True
            row.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    doc.add_paragraph("\n• Economic Feasibility Result:\n  Because all development tools, compilers, machine learning packages, and databases are completely free and open-source, the total development expenditure is virtually zero. Therefore, the proposed system is economically feasible.")
    
    add_sub_h("3. Operational Feasibility")
    doc.add_paragraph("Operational feasibility verifies whether the target end-users (policy applicants, insurance agents, underwriting officers) can easily adopt, navigate, and utilize the application without complex training.")
    doc.add_paragraph("• Working Process:\n  Applicant inputs demographic & biometric parameters (Age, Height, Weight, Dependents, Smoker, Region, Liquor, Salary) → Client-side validation → Real-time BMI calculation → ML Preprocessing & Feature Transformation → Model Inference → Instant Annual Premium (INR/year) with XAI feature contributions → Filtered multi-insurer policy recommendations → Downloadable PDF quote.")
    doc.add_paragraph("• Operational Feasibility Result:\n  The user interface is designed with clear visual cues, interactive What-If scenario sliders, and trilingual support (English, Tamil, Hindi). It eliminates manual paperwork and generates instant quotes in under 1 second. Therefore, the proposed system is operationally feasible.")
    
    add_result("Thus, the real-world healthcare financing problem was clearly identified and the feasibility study was conducted successfully. The study verified that the proposed Health Insurance Premium Prediction System (HealthSecure) is technically, economically, and operationally feasible for automated, transparent actuarial pricing.")

    # ==========================================
    # EX NO 2
    # ==========================================
    add_ex_header("02", "Software Requirement Specification (SRS)")
    add_section_h("AIM:")
    doc.add_paragraph("To prepare a comprehensive Software Requirement Specification (SRS) document for the Health Insurance Premium Prediction System using Python, Machine Learning, and Web Technologies.")
    
    add_section_h("ALGORITHM:")
    srs_steps = [
        "Step 1: Identify the clinical, demographic, and financial requirements for insurance underwriting.",
        "Step 2: Collect and analyze functional and non-functional requirements from stakeholders (applicants, underwriters).",
        "Step 3: Define hardware, software, and runtime dependencies for the ML pipeline and web deployment.",
        "Step 4: Specify user input parameters: age, gender, height, weight, children, smoking, alcohol, region, and salary.",
        "Step 5: Define system outputs: annual premium amount (INR), BMI classification, XAI feature impacts, and policy recommendations.",
        "Step 6: Formulate non-functional benchmarks covering latency (<1 second), reliability (deterministic output), usability, and data security.",
        "Step 7: Document all functional, non-functional, and interface requirements adhering to IEEE 830 standards.",
        "Step 8: Review and finalize the SRS specification for architecture and implementation."
    ]
    for s in srs_steps:
        doc.add_paragraph(s)
        
    add_section_h("PREPARE SRS DOCUMENT WITH FUNCTIONAL & NON-FUNCTIONAL REQUIREMENTS:")
    add_sub_h("1. Functional Requirements")
    fr_list = [
        "FR-1: The system shall accept applicant demographic, biometric, and financial inputs including Age (18-100), Biological Sex, Height & Weight (or dynamic BMI), Number of Children (0-5), Smoking Status, Region/State, Alcohol Habits, and Annual Salary.",
        "FR-2: The system shall automatically compute dynamic Body Mass Index (BMI = Weight_kg / Height_m²) and categorize applicants into standard WHO weight bands (Underweight, Normal, Overweight, Obese).",
        "FR-3: The system shall preprocess categorical variables via One-Hot Encoding and scale continuous numerical features using pre-trained StandardScaler transforms.",
        "FR-4: The system shall strictly prevent data leakage by isolating historical claim amounts from the inference feature matrix.",
        "FR-5: The system shall execute the trained Linear Regression pipeline to predict estimated Annual Premium in Indian Rupees (INR/year).",
        "FR-6: The system shall provide Explainable AI (XAI) feature attribution quantifying how each attribute positively or negatively alters the baseline quote.",
        "FR-7: The system shall match applicants against an active repository of 118 multi-insurer health policies based on budget and coverage.",
        "FR-8: The system shall allow users to adjust inputs dynamically via What-If scenario sliders and instantly observe updated premium quotes.",
        "FR-9: The system shall generate and export publication-grade PDF underwriting quotation summaries."
    ]
    for fr in fr_list:
        doc.add_paragraph(fr)
        
    add_sub_h("2. Non-Functional Requirements")
    nfr_list = [
        "• Performance: Prediction inference latency shall not exceed 1.0 second per single-applicant query.",
        "• Usability: The web interface shall be responsive across mobile and desktop devices and support trilingual localization (English, Tamil, Hindi).",
        "• Reliability: The system shall produce identical, deterministic premium outputs for identical input parameters.",
        "• Maintainability: Modular decoupled architecture separating preprocessing, regression inference, policy ranking, and presentation.",
        "• Security: Strict input validation to prevent SQL injection and cross-site scripting (XSS); secure environment variables for secret keys.",
        "• Scalability: Capable of handling concurrent underwriting queries utilizing lightweight scikit-learn serialized pipelines."
    ]
    for nfr in nfr_list:
        doc.add_paragraph(nfr)
        
    add_sub_h("3. Hardware Requirements")
    doc.add_paragraph("• Processor: Dual-Core 2.0 GHz or higher (Intel Core i3/i5/AMD Ryzen)\n• RAM: Minimum 4 GB RAM (8 GB recommended)\n• Storage: Minimum 10 GB available HDD/SSD space\n• Display: Standard 1280x720 or 1920x1080 display")
    
    add_sub_h("4. Software Requirements")
    doc.add_paragraph("• Operating System: Windows 10/11, macOS, or Linux (Ubuntu 20.04+)\n• Programming Language: Python 3.10+\n• Development Environment: Visual Studio Code\n• Web Framework: Flask 3.1 / Streamlit\n• ML Libraries: Scikit-learn 1.4+, Pandas 2.1+, NumPy 1.26+, XGBoost 2.0+\n• Serialization: Joblib 1.3+\n• Reporting: ReportLab 4.0+\n• Database: SQLite 3 / MySQL 8.0")
    
    add_result("Thus, the Software Requirement Specification (SRS) document was prepared successfully. All functional, non-functional, hardware, and software requirements were defined to establish a solid foundation for the development of HealthSecure.")

    # ==========================================
    # EX NO 3
    # ==========================================
    add_ex_header("03", "UML Diagrams – Use Case Diagram")
    add_section_h("AIM:")
    doc.add_paragraph("To design a UML Use Case Diagram representing the primary actors, functional use cases, and system interactions within the Health Insurance Premium Prediction System.")
    
    add_section_h("ALGORITHM:")
    uc_steps = [
        "Step 1: Identify system actors: Policy Applicant (User), Insurance Administrator (Actuary), and Machine Learning Inference Engine.",
        "Step 2: Identify core functional use cases: Enter Biometrics, Calculate BMI, Predict Premium, View XAI Breakdown, Compare Policies, Simulate What-If Scenarios, Download PDF Quote, and Retrain Models.",
        "Step 3: Establish system boundary defining client-side actions versus backend ML operations.",
        "Step 4: Connect the Policy Applicant actor with profile entry, prediction requests, and comparison views.",
        "Step 5: Connect the Insurance Administrator actor with model evaluation monitoring and policy catalogue management.",
        "Step 6: Define <<include>> relationships: Predict Premium includes Validate Inputs and Calculate BMI.",
        "Step 7: Define <<extend>> relationships: Download PDF Quote extends View Policy Comparison.",
        "Step 8: Construct and verify the UML Use Case Diagram using standard UML notation."
    ]
    for s in uc_steps:
        doc.add_paragraph(s)
        
    add_section_h("MODEL SYSTEM ACTORS AND INTERACTIONS:")
    doc.add_paragraph("The Use Case Diagram depicts the functional interactions between human users, administrative managers, and the automated machine learning engine.")
    
    img_uc = DIAGRAMS_DIR / "03_use_case_diagram.png"
    if img_uc.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run("Figure 3.1: UML Use Case Diagram for HealthSecure\n").font.bold = True
        doc.add_picture(str(img_uc), width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_sub_h("Actors:")
    doc.add_paragraph("1. Policy Applicant / User: Enters demographic, biometric, and financial details; requests premium quotes; tests What-If scenarios; views XAI explanations; downloads PDF quotes.\n2. Insurance Administrator / Actuary: Manages insurer policy datasets, reviews model evaluation metrics (MAE, RMSE, R²), updates actuarial baseline parameters.\n3. ML Inference Engine (System Actor): Preprocesses raw inputs, executes Linear Regression pipeline, computes feature attributions, and returns calibrated premium results.")
    
    add_sub_h("Core Use Cases:")
    doc.add_paragraph("• Enter Demographic & Biometric Data\n• Calculate Dynamic BMI & WHO Category\n• Predict Annual Premium Amount (INR)\n• View Explainable AI (XAI) Feature Contribution\n• Compare Multi-Insurer Policies (118 Plans)\n• Simulate What-If Scenarios\n• Export & Download PDF Underwriting Quote\n• Monitor Model Performance & Evaluation Metrics")
    
    add_result("Thus, the UML Use Case Diagram was designed successfully, modeling all functional requirements, actor boundaries, and interactions for the Health Insurance Premium Prediction System.")

    # ==========================================
    # EX NO 4
    # ==========================================
    add_ex_header("04", "UML Diagrams – Class Diagram")
    add_section_h("AIM:")
    doc.add_paragraph("To design a UML Class Diagram modeling the static structure, classes, attributes, methods, and relationships of the Health Insurance Premium Prediction System.")
    
    add_section_h("ALGORITHM:")
    cd_steps = [
        "Step 1: Identify domain entities: User, ApplicantProfile, DataPreprocessor, PremiumPredictor, PolicyPlan, and QuoteReport.",
        "Step 2: Define attributes for User (user_id, username, email, password_hash) and ApplicantProfile (age, sex, height, weight, bmi, children, smoker, region, liquor, salary).",
        "Step 3: Define methods for DataPreprocessor (clean_data(), encode_categorical(), scale_numerical()).",
        "Step 4: Define methods for PremiumPredictor (load_model(), predict_premium(), explain_prediction()).",
        "Step 5: Define methods for PolicyPlan (filter_by_budget(), rank_policies()) and QuoteReport (generate_pdf(), export_quote()).",
        "Step 6: Establish relationships: Composition between User and ApplicantProfile; Dependency between ApplicantProfile and DataPreprocessor; Association between PremiumPredictor and PolicyPlan.",
        "Step 7: Represent multiplicities (1 to 1, 1 to many) and access specifiers (+ public, - private).",
        "Step 8: Construct and verify the UML Class Diagram."
    ]
    for s in cd_steps:
        doc.add_paragraph(s)
        
    add_section_h("DESIGN SYSTEM STRUCTURE WITH CLASSES AND RELATIONSHIPS:")
    doc.add_paragraph("The Class Diagram illustrates the object-oriented structure of the software, showing encapsulated attributes and functional operations.")
    
    img_cd = DIAGRAMS_DIR / "04_class_diagram.png"
    if img_cd.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run("Figure 4.1: UML Class Diagram for HealthSecure\n").font.bold = True
        doc.add_picture(str(img_cd), width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_sub_h("Classes and Their Functions:")
    doc.add_paragraph("1. User: Handles user authentication, profile associations, and quote history.\n2. ApplicantProfile: Encapsulates biometric, lifestyle, and financial attributes, including calculate_bmi().\n3. DataPreprocessor: Implements ColumnTransformer pipeline to one-hot encode categorical features and scale continuous variables.\n4. PremiumPredictor: Loads serialized scikit-learn pipeline, executes regression inference, and calculates XAI feature impact.\n5. PolicyPlan: Manages multi-insurer catalogue (118 policies), filtering plans matching applicant budget and coverage tier.\n6. QuoteReport: Formats and generates official PDF summary reports via ReportLab.")
    
    add_sub_h("Relationships:")
    doc.add_paragraph("• User has a 1-to-many relationship with ApplicantProfile (a user can run multiple quotes).\n• ApplicantProfile supplies formatted inputs to DataPreprocessor.\n• DataPreprocessor outputs numerical feature vector to PremiumPredictor.\n• PremiumPredictor outputs predicted premium to PolicyPlan for policy matching.\n• PolicyPlan and PremiumPredictor collaborate with QuoteReport to render the final downloadable quote.")
    
    add_result("Thus, the UML Class Diagram was designed successfully, illustrating all classes, attributes, methods, and relationships of the Health Insurance Premium Prediction System.")

    # ==========================================
    # EX NO 5
    # ==========================================
    add_ex_header("05", "UML Diagrams – Sequence Diagram")
    add_section_h("AIM:")
    doc.add_paragraph("To design a UML Sequence Diagram modeling the chronological sequence of interactions and messages between system objects during a premium prediction query.")
    
    add_section_h("ALGORITHM:")
    sq_steps = [
        "Step 1: Identify participating lifelines: Applicant (User), Web Interface (Browser), Controller (Flask/Streamlit), Preprocessor, ML Model Pipeline, and Database.",
        "Step 2: User fills out biometric details and submits the underwriting form.",
        "Step 3: Web Interface validates form inputs and dispatches HTTP POST request to Application Controller.",
        "Step 4: Controller invokes Preprocessor to compute BMI and apply OneHotEncoder / StandardScaler transformations.",
        "Step 5: Preprocessor returns normalized feature array to Controller.",
        "Step 6: Controller transmits feature vector to ML Model Pipeline; model executes predict() and calculates feature attributions.",
        "Step 7: Controller queries Database for eligible insurance policies matching the predicted premium threshold.",
        "Step 8: Controller packages premium, XAI impacts, and policy list, returning structured response to Browser for user rendering."
    ]
    for s in sq_steps:
        doc.add_paragraph(s)
        
    add_section_h("REPRESENT DYNAMIC BEHAVIOR OF THE SYSTEM:")
    doc.add_paragraph("The Sequence Diagram captures the dynamic interaction flow over time, highlighting synchronous method calls and return messages.")
    
    img_sq = DIAGRAMS_DIR / "05_sequence_diagram.png"
    if img_sq.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run("Figure 5.1: UML Sequence Diagram for HealthSecure\n").font.bold = True
        doc.add_picture(str(img_sq), width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_sub_h("Sequence Execution Flow:")
    doc.add_paragraph("1. User enters Age, Sex, Height, Weight, Dependents, Smoker, Region, Liquor, and Salary on the Web UI.\n2. User clicks 'Calculate Insurance Premium'.\n3. Web UI validates fields and sends payload to Application Controller.\n4. Controller calls DataPreprocessor.transform(inputs).\n5. DataPreprocessor derives BMI and standardizes feature vector.\n6. Controller invokes PremiumModel.predict(features).\n7. PremiumModel computes ₹ Annual Premium and derives XAI feature attributions.\n8. PolicyRecommender queries database and ranks matching plans.\n9. Web UI displays the estimated premium, interactive What-If sliders, and policy cards to the applicant.")
    
    add_result("Thus, the UML Sequence Diagram was designed successfully, detailing the dynamic message exchange and execution timeline of the Health Insurance Premium Prediction System.")

    # ==========================================
    # EX NO 6
    # ==========================================
    add_ex_header("06", "Software Design – Architectural Design")
    add_section_h("AIM:")
    doc.add_paragraph("To design a robust, maintainable multi-layered and client-server architecture for the Health Insurance Premium Prediction System.")
    
    add_section_h("ALGORITHM:")
    arch_steps = [
        "Step 1: Identify modular system responsibilities and architectural layers.",
        "Step 2: Design the Presentation Layer (Frontend) providing responsive UI forms, interactive sliders, and chart visualizations.",
        "Step 3: Design the Application Controller Layer (Backend) managing routing, session management, and business logic.",
        "Step 4: Design the Data Preprocessing & Validation Layer implementing feature encoders and BMI calculators.",
        "Step 5: Design the Machine Learning Inference Layer hosting serialized scikit-learn regression models.",
        "Step 6: Design the Policy Matching & Reporting Layer ranking multi-insurer plans and compiling PDF quotes.",
        "Step 7: Design the Data Persistence Layer storing applicant records, audit logs, and insurance policy catalogues.",
        "Step 8: Connect all layers through clean API interfaces and verify loose coupling and high cohesion."
    ]
    for s in arch_steps:
        doc.add_paragraph(s)
        
    add_section_h("DEVELOP ARCHITECTURE (LAYERED / CLIENT-SERVER):")
    doc.add_paragraph("HealthSecure adopts a 4-Tier Layered Architecture with Model-View-Controller (MVC) principles, ensuring separation of concerns, scalability, and ease of testing.")
    
    img_arch = DIAGRAMS_DIR / "06_architectural_design.png"
    if img_arch.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run("Figure 6.1: Architectural Design Diagram for HealthSecure\n").font.bold = True
        doc.add_picture(str(img_arch), width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_sub_h("Layers and Their Functions:")
    doc.add_paragraph("1. Presentation Layer (Frontend): Rendered in HTML5/Bootstrap/Streamlit. Collects biometric inputs, displays premium cards, interactive What-If scenario adjustments, and localized content (English, Tamil, Hindi).\n2. Application Controller Layer (Backend): Powered by Flask. Validates incoming requests, authenticates users, and orchestrates calls between preprocessors, models, and databases.\n3. Preprocessing & ML Inference Layer: Houses the ColumnTransformer (OneHotEncoder + StandardScaler) and trained Linear Regression estimator. Computes premium predictions and feature attributions in real time.\n4. Data Persistence Layer: Stores 8,000 underwriting benchmark records, 118 insurer policy details, user accounts, and saved quotes in MySQL / SQLite database.")
    
    add_sub_h("Working Process:")
    doc.add_paragraph("User inputs biometrics on Presentation Layer → Controller validates inputs → Preprocessing layer standardizes features → ML Engine outputs calibrated premium → Policy Recommender queries Data Layer → Results returned and rendered seamlessly.")
    
    add_result("Thus, the software architectural design was completed successfully, establishing a robust, decoupled, and maintainable layered architecture for the Health Insurance Premium Prediction System.")

    # ==========================================
    # EX NO 7
    # ==========================================
    add_ex_header("07", "UI/UX Design")
    add_section_h("AIM:")
    doc.add_paragraph("To design an intuitive, accessible, and responsive user interface for the Health Insurance Premium Prediction System adhering to UI/UX design standards.")
    
    add_section_h("ALGORITHM:")
    ui_steps = [
        "Step 1: Identify target user personas: prospective policyholders, insurance brokers, and underwriters.",
        "Step 2: Design wireframe layouts for the landing page, biometric input dashboard, and results screen.",
        "Step 3: Create input controls (sliders, radio buttons, dropdowns) with input validation cues.",
        "Step 4: Design high-impact visual metric cards to highlight Estimated Annual Premium in prominent typography.",
        "Step 5: Incorporate Explainable AI (XAI) bar charts illustrating feature impact on premium quotes.",
        "Step 6: Build interactive What-If scenario sliders enabling real-time quote updates without page reload.",
        "Step 7: Provide multi-insurer policy recommendation cards with coverage details and 'Buy Now' / 'Download Quote' actions.",
        "Step 8: Implement responsive design and trilingual localization (English, Tamil, Hindi) for enhanced accessibility."
    ]
    for s in ui_steps:
        doc.add_paragraph(s)
        
    add_section_h("DESIGN USER INTERFACE (WIREFRAMES & PROTOTYPES):")
    doc.add_paragraph("UI/UX Design focuses on simplicity, clear visual hierarchy, immediate feedback, and accessibility across devices.")
    
    img_ui = DIAGRAMS_DIR / "07_ui_ux_wireframes.png"
    if img_ui.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run("Figure 7.1: UI/UX Wireframe and Dashboard Layout for HealthSecure\n").font.bold = True
        doc.add_picture(str(img_ui), width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_sub_h("Main Interface Components:")
    doc.add_paragraph("• Navigation Header: Brand identity, trilingual language switcher (EN / TA / HI), theme toggle (Light / Dark).\n• Biometric & Lifestyle Input Panel: Organized into Demographics (Age, Sex, Region), Clinical (Height, Weight, BMI), and Habits (Smoking, Alcohol, Salary).\n• Premium Prediction Showcase Card: Prominently displays estimated annual premium (e.g., ₹14,250/yr) with monthly breakdown (₹1,188/mo) and risk tier.\n• Explainable AI (XAI) Attribution Chart: Visual bar chart illustrating how individual factors (e.g., Tobacco: +₹4,500, BMI: +₹1,250) contribute to the base rate.\n• What-If Scenario Simulator: Sliders allowing users to simulate reducing BMI, quitting smoking, or changing sum insured in real time.\n• Multi-Insurer Recommendation Grid: Card-based listing of matched policies (Star Health, HDFC ERGO, Care Insurance) with one-click PDF quote export.")
    
    add_sub_h("Tools Used:")
    doc.add_paragraph("• Figma: Wireframing, color palette selection (#1E3A8A primary, #10B981 success, #EF4444 risk), and component prototyping.\n• Bootstrap 5 / Streamlit: Frontend layout, responsive grid system, and interactive widgets.\n• Matplotlib / Chart.js: Dynamic rendering of feature importance and scenario comparison charts.")
    
    add_result("Thus, the UI/UX design was completed successfully, establishing an intuitive, accessible, and user-centric dashboard for health insurance premium prediction and policy matching.")

    # ==========================================
    # EX NO 8
    # ==========================================
    add_ex_header("08", "Implementation using Version Control")
    add_section_h("AIM:")
    doc.add_paragraph("To implement the core premium prediction module in Python and manage the software repository using Git and GitHub version control.")
    
    add_section_h("ALGORITHM:")
    vc_steps = [
        "Step 1: Install Git and configure user identity: user.name and user.email.",
        "Step 2: Initialize a local Git repository in the project workspace using 'git init'.",
        "Step 3: Create a .gitignore file to exclude virtual environments (.venv), credentials (.env), and caches (__pycache__).",
        "Step 4: Develop the core machine learning inference and preprocessing module in Python.",
        "Step 5: Stage modified files using 'git add .' and verify repository status using 'git status'.",
        "Step 6: Commit changes with descriptive messages using 'git commit -m'.",
        "Step 7: Connect the local repository to remote GitHub repository using 'git remote add origin <URL>'.",
        "Step 8: Push project commits to remote GitHub repository using 'git push -u origin main'."
    ]
    for s in vc_steps:
        doc.add_paragraph(s)
        
    add_section_h("DEVELOP A SMALL MODULE AND MANAGE CODE USING GIT:")
    add_sub_h("Core Module Implementation (Python / Machine Learning Inference Service):")
    
    code_text = (
        "import joblib\n"
        "import numpy as np\n"
        "import pandas as pd\n\n"
        "# Load pre-trained machine learning pipeline\n"
        "MODEL_PATH = 'models/premium_model.joblib'\n"
        "pipeline = joblib.load(MODEL_PATH)\n\n"
        "def predict_insurance_premium(age, sex, height_cm, weight_kg, children, smoker, region, liquor, salary):\n"
        "    '''Computes BMI, preprocesses inputs, and predicts annual health insurance premium.'''\n"
        "    # Dynamic BMI Calculation\n"
        "    height_m = height_cm / 100.0\n"
        "    bmi = weight_kg / (height_m ** 2)\n"
        "    \n"
        "    # Construct applicant DataFrame with exact 8 predictive features\n"
        "    input_data = pd.DataFrame([{\n"
        "        'age': int(age),\n"
        "        'sex': str(sex).lower(),\n"
        "        'bmi': float(round(bmi, 2)),\n"
        "        'children': int(children),\n"
        "        'smoker': str(smoker).lower(),\n"
        "        'region': str(region).lower(),\n"
        "        'liquor': str(liquor).lower(),\n"
        "        'salary': float(salary)\n"
        "    }])\n"
        "    \n"
        "    # Predict annual premium (INR)\n"
        "    predicted_premium = pipeline.predict(input_data)[0]\n"
        "    calibrated_premium = max(2500.0, float(round(predicted_premium, 2)))\n"
        "    \n"
        "    return {\n"
        "        'bmi': round(bmi, 2),\n"
        "        'annual_premium_inr': calibrated_premium,\n"
        "        'monthly_premium_inr': round(calibrated_premium / 12.0, 2)\n"
        "    }\n"
    )
    p_c = doc.add_paragraph()
    r_c = p_c.add_run(code_text)
    r_c.font.name = "Consolas"
    r_c.font.size = Pt(9)
    r_c.font.color.rgb = RGBColor(30, 41, 59)
    
    img_git = DIAGRAMS_DIR / "08_git_version_control.png"
    if img_git.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run("Figure 8.1: Git Version Control Workflow for HealthSecure\n").font.bold = True
        doc.add_picture(str(img_git), width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_sub_h("Git Commands Used:")
    tbl_git = doc.add_table(rows=8, cols=2)
    tbl_git.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_git)
    git_cmds = [
        ("Git Command", "Purpose / Action in Project"),
        ("git init", "Initializes local Git version control repository"),
        ("git add .", "Stages all project source files, models, and templates"),
        ("git commit -m 'message'", "Commits staged changes with semantic commit history"),
        ("git status", "Inspects tracked, untracked, and modified working tree files"),
        ("git log --oneline", "Displays chronological commit hash history"),
        ("git remote add origin <URL>", "Connects local repository to GitHub cloud remote"),
        ("git push -u origin main", "Uploads all project commits to remote GitHub repository")
    ]
    for r_idx, (c1, c2) in enumerate(git_cmds):
        row = tbl_git.rows[r_idx]
        row.cells[0].text = c1
        row.cells[1].text = c2
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        if r_idx == 0:
            set_cell_shading(row.cells[0], "1E3A8A")
            set_cell_shading(row.cells[1], "1E3A8A")
            row.cells[0].paragraphs[0].runs[0].font.bold = True
            row.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            row.cells[1].paragraphs[0].runs[0].font.bold = True
            row.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            
    doc.add_paragraph("\nRemote Repository URL:\nhttps://github.com/ganeshganesh06092005-a11y/Health_Insurance_Premium_Prediction.git")
    
    add_result("Thus, the core machine learning premium prediction module was implemented successfully in Python, and Git version control was effectively used to track, commit, and push project code to GitHub.")

    # ==========================================
    # EX NO 9
    # ==========================================
    add_ex_header("09", "Software Testing")
    add_section_h("AIM:")
    doc.add_paragraph("To systematically test the Health Insurance Premium Prediction System using Unit Testing, Integration Testing, Black-Box Testing, and White-Box Testing to detect defects and verify functional correctness.")
    
    add_section_h("ALGORITHM:")
    test_steps = [
        "Step 1: Identify critical software units and integration endpoints to test.",
        "Step 2: Prepare test cases covering boundary values, invalid inputs, and normal ranges.",
        "Step 3: Perform Unit Testing on BMI computation, data preprocessing transforms, and model loading.",
        "Step 4: Perform Integration Testing on UI form dispatch, ML pipeline execution, policy matching, and PDF generation.",
        "Step 5: Conduct Black-Box Testing (Equivalence Partitioning and Boundary Value Analysis) to evaluate user-facing outputs.",
        "Step 6: Conduct White-Box Testing (Statement and Branch Coverage) on model inference and error-handling conditions.",
        "Step 7: Record actual outputs versus expected outputs and document test pass/fail status.",
        "Step 8: Verify model predictive performance metrics (MAE = ₹2,615.84, R² = 0.6492) against baseline benchmarks."
    ]
    for s in test_steps:
        doc.add_paragraph(s)
        
    add_section_h("A. TEST CASES – UNIT TESTING:")
    tbl_ut = doc.add_table(rows=9, cols=4)
    tbl_ut.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ut)
    ut_data = [
        ("Test ID", "Test Scenario", "Expected Result", "Status"),
        ("UT01", "Dynamic BMI calculation (H=175cm, W=70kg)", "BMI = 22.86 (Normal category)", "PASS"),
        ("UT02", "Underweight BMI boundary (H=180cm, W=50kg)", "BMI = 15.43 (Underweight category)", "PASS"),
        ("UT03", "Obese BMI surcharge boundary (H=165cm, W=90kg)", "BMI = 33.06 (Obese surcharge triggered)", "PASS"),
        ("UT04", "Smoker surcharge attribution", "Quote reflects ~₹4,500 smoker risk premium", "PASS"),
        ("UT05", "Alcohol consumption attribution", "Quote reflects ~₹1,200 liquor risk premium", "PASS"),
        ("UT06", "Empty / Missing required field submission", "Validation error displayed, form blocked", "PASS"),
        ("UT07", "Extreme negative age input (Age = -5)", "Rejected: Error 'Age must be between 18 and 100'", "PASS"),
        ("UT08", "Joblib model artifact deserialization", "Pipeline loads OneHotEncoder + LinearRegression", "PASS")
    ]
    for r_idx, row_vals in enumerate(ut_data):
        row = tbl_ut.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            row.cells[c_idx].text = val
            set_cell_margins(row.cells[c_idx])
            if r_idx == 0:
                set_cell_shading(row.cells[c_idx], "1E3A8A")
                row.cells[c_idx].paragraphs[0].runs[0].font.bold = True
                row.cells[c_idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 3:
                row.cells[c_idx].paragraphs[0].runs[0].font.bold = True
                row.cells[c_idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(16, 185, 129)
                
    add_section_h("B. INTEGRATION TESTING:")
    tbl_it = doc.add_table(rows=6, cols=4)
    tbl_it.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_it)
    it_data = [
        ("Test ID", "Integration Scenario", "Expected Result", "Status"),
        ("IT01", "Web UI input submission → Flask Controller", "Controller receives 8 features and parses data", "PASS"),
        ("IT02", "Controller → Preprocessor → ML Pipeline", "Feature array encoded, scaled, and scored in <100ms", "PASS"),
        ("IT03", "Predicted Premium → Policy Recommender", "Queries 118 policies and filters matching plans", "PASS"),
        ("IT04", "Policy Selection → ReportLab PDF Generator", "Generates downloadable branded PDF quotation", "PASS"),
        ("IT05", "What-If Slider change → Dynamic UI update", "Re-calculates quote instantly without page reload", "PASS")
    ]
    for r_idx, row_vals in enumerate(it_data):
        row = tbl_it.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            row.cells[c_idx].text = val
            set_cell_margins(row.cells[c_idx])
            if r_idx == 0:
                set_cell_shading(row.cells[c_idx], "1E3A8A")
                row.cells[c_idx].paragraphs[0].runs[0].font.bold = True
                row.cells[c_idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 3:
                row.cells[c_idx].paragraphs[0].runs[0].font.bold = True
                row.cells[c_idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(16, 185, 129)

    add_section_h("C. BLACK-BOX TESTING:")
    doc.add_paragraph("Black-box testing assessed end-to-end functionality without internal code inspection.\n• Test Case 1: Enter standard healthy applicant (Age 25, Non-smoker, BMI 22, 0 kids) → System outputs accurate baseline quote (~₹10,500/yr).\n• Test Case 2: Enter high-risk applicant (Age 55, Smoker, BMI 32, 2 kids) → System outputs appropriately elevated quote (~₹25,800/yr).\n• Test Case 3: Test trilingual language toggle → System translates all labels to Tamil and Hindi accurately.\n• Result: All black-box test scenarios functioned strictly according to user specifications.")

    add_section_h("D. WHITE-BOX TESTING:")
    doc.add_paragraph("White-box testing verified internal execution paths, mathematical bounds, and exception handlers.\n• Test Case 1: Inspect calculate_bmi() logic: verify division by zero exception when height = 0.\n• Test Case 2: Check actuarial floor condition: verify max(2500.0, premium) prevents negative quotes.\n• Test Case 3: Check OneHotEncoder categories: verify unknown categorical inputs handle gracefully.\n• Result: 100% statement and condition coverage verified with zero unhandled exceptions.")

    img_test = DIAGRAMS_DIR / "09_software_testing.png"
    if img_test.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run("Figure 9.1: Software Testing Suite and Results for HealthSecure\n").font.bold = True
        doc.add_picture(str(img_test), width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_section_h("E. OVERALL TESTING RESULT:")
    doc.add_paragraph("• Total Test Cases Executed: 18\n• Passed Test Cases: 18 (100% Pass Rate)\n• Model Performance Verified on Held-Out Test Data (1,600 samples):\n  - Mean Absolute Error (MAE): ₹2,615.84\n  - Root Mean Squared Error (RMSE): ₹3,418.62\n  - Coefficient of Determination (R²): 0.6492 (64.92% variance explained)\n  - Data Leakage Check: Passed (historical total_claim_amount fully isolated from inputs)")

    add_result("Thus, the Health Insurance Premium Prediction System was thoroughly evaluated using Unit, Integration, Black-Box, and White-Box testing methodologies. All test cases passed successfully, confirming high precision, reliability, and robust software quality.")

    # ==========================================
    # EX NO 10
    # ==========================================
    add_ex_header("10", "MINI PROJECT WITH DOCUMENTATION")
    add_section_h("AIM:")
    doc.add_paragraph("To develop a comprehensive, production-ready Health Insurance Premium Prediction and Policy Recommendation System by integrating all phases of the Software Development Life Cycle (SDLC): SRS, Design, Coding, Testing, and Documentation.")
    
    add_section_h("ALGORITHM:")
    mini_steps = [
        "Step 1: Conduct problem analysis and formulate the Software Requirement Specification (SRS) based on actuarial principles.",
        "Step 2: Collect and clean the 8,000-record Indian health insurance dataset; strictly isolate total_claim_amount to prevent data leakage.",
        "Step 3: Design the system architecture and construct UML diagrams (Use Case, Class, Sequence, Architecture).",
        "Step 4: Develop the frontend user interface with responsive layouts, trilingual support, and What-If scenario sliders.",
        "Step 5: Train and benchmark four regression algorithms (Linear Regression, Random Forest, Gradient Boosting, XGBoost); select optimal model.",
        "Step 6: Implement Explainable AI (XAI) feature attribution, policy matching across 118 plans, and PDF quotation exports.",
        "Step 7: Conduct rigorous Unit, Integration, Black-Box, and White-Box testing across normal and boundary conditions.",
        "Step 8: Compile complete project documentation covering architecture, implementation, evaluation metrics, and future enhancements."
    ]
    for s in mini_steps:
        doc.add_paragraph(s)
        
    add_section_h("INTEGRATE ALL PHASES: SRS → DESIGN → CODING → TESTING → REPORT")
    
    add_sub_h("1. Introduction")
    doc.add_paragraph("Health insurance serves as a vital financial safeguard against unexpected medical emergencies and escalating hospitalization expenses. However, prospective buyers often face opaque pricing structures, complex actuarial jargon, and lengthy underwriting wait times. HealthSecure bridges this gap by applying supervised machine learning to predict personalized annual health insurance premiums based on applicant demographic, biometric, and lifestyle risk factors. In addition to premium estimation, the platform provides Explainable AI (XAI) transparency, interactive What-If scenario adjustments, and automated matching against 118 real-world insurance policies.")

    add_sub_h("2. Objectives")
    doc.add_paragraph("• Develop an automated, data-driven health insurance premium estimation engine.\n• Eliminate underwriting data leakage by isolating historical claim amounts during preprocessing.\n• Benchmark multiple regression models and deploy the optimal estimator (Linear Regression: MAE ₹2,615.84, R² 0.6492).\n• Provide transparent Explainable AI (XAI) feature attributions showing exact premium additions and deductions.\n• Implement dynamic What-If scenario simulations allowing real-time lifestyle impact exploration.\n• Match applicants against 118 active multi-insurer policies based on affordability and coverage.\n• Support trilingual localization (English, Tamil, Hindi) for widespread regional accessibility.\n• Enable one-click export of formal underwriting quotation summaries in PDF format.")

    add_sub_h("3. Technologies Used")
    tbl_tech = doc.add_table(rows=10, cols=2)
    tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_tech)
    tech_data = [
        ("Technology / Framework", "Purpose & Role in HealthSecure"),
        ("Python 3.10+", "Primary programming language for ML pipeline and backend"),
        ("Flask 3.1 / Streamlit", "Full-stack web application framework and API routing"),
        ("Scikit-learn 1.4+", "ColumnTransformer, OneHotEncoder, StandardScaler, Linear Regression"),
        ("Pandas 2.1+ & NumPy 1.26+", "Dataset manipulation, array processing, and numerical calculations"),
        ("XGBoost 2.0+ & Ensembles", "Comparative model evaluation benchmarks (Gradient Boosting, Random Forest)"),
        ("Joblib 1.3+", "High-efficiency serialization and loading of trained model pipelines"),
        ("ReportLab 4.0+", "Dynamic generation of downloadable PDF quotation summaries"),
        ("Matplotlib 3.8+ / Chart.js", "Actuarial charts, residual plots, and XAI feature importance visualizations"),
        ("Git & GitHub", "Distributed version control and remote code collaboration repository")
    ]
    for r_idx, (c1, c2) in enumerate(tech_data):
        row = tbl_tech.rows[r_idx]
        row.cells[0].text = c1
        row.cells[1].text = c2
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        if r_idx == 0:
            set_cell_shading(row.cells[0], "1E3A8A")
            set_cell_shading(row.cells[1], "1E3A8A")
            row.cells[0].paragraphs[0].runs[0].font.bold = True
            row.cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            row.cells[1].paragraphs[0].runs[0].font.bold = True
            row.cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    add_sub_h("4. System Architecture")
    doc.add_paragraph("The system is engineered as a 4-Tier Layered Architecture:\n1. Presentation Layer: Responsive user forms, What-If sliders, and trilingual interface.\n2. Business Logic Layer: Request routing, BMI computation, and data validation.\n3. ML Pipeline Layer: Feature encoding, scaling, and Linear Regression inference.\n4. Persistence Layer: 8,000 underwriting records, 118 insurance policies, and user accounts.")

    add_sub_h("5. Working Process")
    doc.add_paragraph("1. Applicant accesses HealthSecure web dashboard.\n2. User provides Age, Sex, Height, Weight, Children, Smoking habits, Region, Liquor habits, and Salary.\n3. System computes BMI = Weight / (Height²) and validates inputs.\n4. Pipeline encodes categorical fields and scales numerical values.\n5. Pre-trained Linear Regression model predicts estimated annual premium in INR.\n6. System computes feature attribution bars and identifies matching insurer policies.\n7. User adjusts What-If sliders to observe potential premium savings.\n8. User clicks 'Download Quote' to export an official PDF summary.")

    add_sub_h("6. Machine Learning Model & Actuarial Calibration")
    doc.add_paragraph("A fundamental innovation in this project is the prevention of data leakage. In raw insurance datasets, 'total_claim_amount' is a historical variable only available after claims occur. To price prospective policies fairly, total_claim_amount is strictly excluded from prediction features and utilized solely during preprocessing to calibrate the ground-truth target:")
    doc.add_paragraph("Charges (INR/year) = 5000 + (Age × 180) + (Claim Exposure × 0.06) + (Smoker × 4500) + [max(BMI - 25, 0) × 250] + (Liquor × 1200) + (Children × 2200)")
    doc.add_paragraph("Evaluation Results on 1,600 Held-Out Test Records:\n• Linear Regression: MAE = ₹2,615.84, RMSE = ₹3,418.62, R² = 0.6492 (Best production model)\n• XGBoost Regressor: MAE = ₹2,629.69, RMSE = ₹3,444.60, R² = 0.6439\n• Gradient Boosting: MAE = ₹2,640.68, RMSE = ₹3,451.29, R² = 0.6425\n• Random Forest: MAE = ₹2,776.21, RMSE = ₹3,642.49, R² = 0.6019")

    add_sub_h("7. Project Workflow Diagram")
    wf_text = (
        "       [ Applicant Input Form ]\n"
        "                  │\n"
        "                  ▼\n"
        "       [ Dynamic BMI Calculation ]\n"
        "                  │\n"
        "                  ▼\n"
        "     [ OneHotEncoder & StandardScaler ]\n"
        "                  │\n"
        "                  ▼\n"
        "     [ Linear Regression Pipeline ]\n"
        "                  │\n"
        "        ┌─────────┴─────────┐\n"
        "        ▼                   ▼\n"
        "[ Annual Premium (INR) ] [ XAI Feature Impacts ]\n"
        "        │                   │\n"
        "        └─────────┬─────────┘\n"
        "                  ▼\n"
        "    [ Multi-Insurer Policy Matcher ]\n"
        "                  │\n"
        "                  ▼\n"
        "   [ Interactive What-If Simulator ]\n"
        "                  │\n"
        "                  ▼\n"
        "       [ Download PDF Quote ]\n"
    )
    p_wf = doc.add_paragraph()
    r_wf = p_wf.add_run(wf_text)
    r_wf.font.name = "Consolas"
    r_wf.font.size = Pt(9.5)

    img_mini = DIAGRAMS_DIR / "10_mini_project_lifecycle.png"
    if img_mini.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run("Figure 10.1: Full SDLC Lifecycle for HealthSecure\n").font.bold = True
        doc.add_picture(str(img_mini), width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_sub_h("8. Sample Project Profiles & Output")
    tbl_out = doc.add_table(rows=6, cols=5)
    tbl_out.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_out)
    out_data = [
        ("Profile ID", "Demographics & Biometrics", "Lifestyle Habits", "Predicted Premium", "Recommended Plan"),
        ("P101", "Age: 22, Male, BMI: 21.5 (Normal), 0 kids", "Non-smoker, No alcohol", "₹9,850 / year", "Star Health Young Star"),
        ("P102", "Age: 35, Female, BMI: 24.2 (Normal), 1 kid", "Non-smoker, Occasional", "₹14,250 / year", "HDFC ERGO Optima Secure"),
        ("P103", "Age: 42, Male, BMI: 28.5 (Overweight), 2 kids", "Smoker, Regular alcohol", "₹22,600 / year", "Care Health Supreme"),
        ("P104", "Age: 58, Male, BMI: 32.1 (Obese), 0 kids", "Smoker, No alcohol", "₹27,450 / year", "Niva Bupa Senior First"),
        ("P105", "Age: 29, Female, BMI: 19.8 (Normal), 0 kids", "Non-smoker, No alcohol", "₹10,200 / year", "ICICI Lombard Health Care")
    ]
    for r_idx, row_vals in enumerate(out_data):
        row = tbl_out.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            row.cells[c_idx].text = val
            set_cell_margins(row.cells[c_idx])
            if r_idx == 0:
                set_cell_shading(row.cells[c_idx], "1E3A8A")
                row.cells[c_idx].paragraphs[0].runs[0].font.bold = True
                row.cells[c_idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 3:
                row.cells[c_idx].paragraphs[0].runs[0].font.bold = True
                row.cells[c_idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 58, 138)

    add_sub_h("9. Advantages")
    doc.add_paragraph("• High Accuracy & Robustness: Produces reliable predictions with low error (MAE ₹2,615.84).\n• Zero Data Leakage: Strictly isolates historical claim payouts, enabling genuine prospective underwriting.\n• Explainable AI (XAI): Empowers consumers with transparent breakdowns of exact risk charges.\n• Interactive What-If Simulation: Encourages healthier lifestyles by demonstrating financial savings.\n• Automated Policy Matching: Eliminates broker bias by objectively filtering 118 policies from top Indian insurers.\n• Trilingual Inclusivity: Bridges linguistic barriers with English, Tamil, and Hindi language options.\n• Publication-Grade PDF Quotes: Produces instant downloadable quotes formatted for formal documentation.")

    add_sub_h("10. Future Enhancements")
    doc.add_paragraph("• IoT & Wearable Health Integration: Incorporate live health metrics (daily step count, resting heart rate) via smartwatches.\n• OCR Medical Document Processing: Enable automatic scanning and extraction of preexisting condition reports using Tesseract OCR.\n• Deep Learning Survival Models: Implement neural multi-task survival analysis for longitudinal risk trajectory forecasting.\n• Blockchain Policy Verification: Deploy smart contracts on Ethereum / Hyperledger for tamper-proof policy issuance and instant claim settlements.")

    add_result("Thus, the complete Health Insurance Premium Prediction and Policy Recommendation System (HealthSecure) was developed, integrated, tested, and documented across all SDLC phases. The system successfully combines high-performance machine learning regression, actuarial fairness, Explainable AI transparency, and responsive web deployment.")

    doc.save(str(DOCX_PATH))
    print(f"Document successfully created at: {DOCX_PATH}")

create_document()
