"""
Software Engineering Laboratory Manual Generator (Clean Black & White / Times New Roman / 12pt / Justified)
Project: HEALTH INSURANCE PREMIUM PREDICTION SYSTEM (HEALTHSECURE)
Department of Computer Applications, Nehru College of Management, Coimbatore
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
PDF_PATH = OUTPUT_DIR / "SE_Lab_Manual_Health_Insurance.pdf"
MD_PATH = OUTPUT_DIR / "SE_Lab_Manual_Health_Insurance.md"

BLACK = RGBColor(0, 0, 0)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="000000", sz="4", val="single"):
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

def build_manual():
    doc = docx.Document()
    
    # Page Setup: Standard A4, 1-inch margins
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        
    # Set Normal Style: Times New Roman, 12pt, Line Spacing 1.15, Black color
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    style.font.color.rgb = BLACK
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.space_before = Pt(0)
    
    # Helper to add standard justified paragraph with a tab indent (0.5 inch)
    def add_para(text, is_passage=True):
        p = doc.add_paragraph()
        if is_passage:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Inches(0.5)
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = BLACK
        return p

    # Helper for headings (Bold Times New Roman 12pt, Black, Left aligned, no tab indent)
    def add_heading(text, is_bold=True, is_center=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_center else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = is_bold
        r.font.color.rgb = BLACK
        return p

    # Helper for exercise header box (Default all side borders, black text, no background color)
    def add_ex_header(ex_no_str, title_str):
        tbl = doc.add_table(rows=2, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="000000", sz="6", val="single")
        col_w = [Inches(1.8), Inches(4.4)]
        for row in tbl.rows:
            for idx, w in enumerate(col_w):
                row.cells[idx].width = w
                set_cell_margins(row.cells[idx], top=80, bottom=80, left=120, right=120)
                
        # Cell 0,0
        c00 = tbl.cell(0, 0)
        c00.text = f"| EX NO: {ex_no_str}"
        p00 = c00.paragraphs[0]
        p00.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p00.runs[0].font.name = 'Times New Roman'
        p00.runs[0].font.size = Pt(12)
        p00.runs[0].font.bold = True
        p00.runs[0].font.color.rgb = BLACK
        
        # Cell 0,1
        c01 = tbl.cell(0, 1)
        c01.text = f"| {title_str} |"
        p01 = c01.paragraphs[0]
        p01.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p01.runs[0].font.name = 'Times New Roman'
        p01.runs[0].font.size = Pt(12)
        p01.runs[0].font.bold = True
        p01.runs[0].font.color.rgb = BLACK
        
        # Cell 1,0
        c10 = tbl.cell(1, 0)
        c10.text = "| DATE:"
        p10 = c10.paragraphs[0]
        p10.runs[0].font.name = 'Times New Roman'
        p10.runs[0].font.size = Pt(12)
        p10.runs[0].font.bold = True
        p10.runs[0].font.color.rgb = BLACK
        
        # Cell 1,1
        c11 = tbl.cell(1, 1)
        c11.text = "| |"
        p11 = c11.paragraphs[0]
        p11.runs[0].font.name = 'Times New Roman'
        p11.runs[0].font.size = Pt(12)
        p11.runs[0].font.color.rgb = BLACK
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(4)
        p_sp.paragraph_format.space_after = Pt(4)

    # Helper for adding image with caption (all black, Times New Roman 12)
    def add_image_figure(img_path, caption_text):
        if Path(img_path).exists():
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.first_line_indent = Inches(0)
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            run = p_img.add_run()
            run.add_picture(str(img_path), width=Inches(5.8))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.first_line_indent = Inches(0)
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            rc = p_cap.add_run(caption_text)
            rc.font.name = 'Times New Roman'
            rc.font.size = Pt(11)
            rc.font.bold = True
            rc.font.color.rgb = BLACK

    # Helper for result block
    def add_result_block(result_text):
        add_heading("RESULT")
        add_para(result_text, is_passage=True)
        doc.add_page_break()

    # =========================================================================
    # EX NO 1: Problem Definition & Feasibility Study
    # =========================================================================
    add_ex_header("01", "Problem Definition & Feasibility Study")
    add_heading("AIM")
    add_para("To identify the real-world healthcare financing problem and conduct a feasibility study to determine the technical, economic, and operational feasibility of the Health Insurance Premium Prediction System (HealthSecure).")
    
    add_heading("Project title : HEALTH INSURANCE PREMIUM PREDICTION SYSTEM")
    
    add_heading("Problem Definition:")
    add_para("In the retail health insurance sector, prospective policyholders face significant challenges in estimating accurate and transparent annual premiums prior to submitting detailed formal applications. Traditional actuarial underwriting processes predominantly rely on static demographic lookup tables, broad risk classifications, and subjective manual discretion. As a consequence, applicants frequently experience procedural delays, pricing opacity, and inconsistent risk categorization. Furthermore, applicants lack clarity regarding how specific physiological attributes such as dynamic Body Mass Index (BMI), lifestyle habits including tobacco usage and alcohol consumption, familial dependencies, and regional healthcare tariffs interact to influence their required premium charges. HealthSecure is developed to resolve these issues by automating annual health insurance premium estimation and policy matching using supervised machine learning algorithms.")
    
    add_heading("Problem Statement")
    add_para("To develop a machine learning-based system that automatically evaluates applicant demographic, clinical, and lifestyle risk factors to accurately estimate personalized annual health insurance premiums, strictly avoiding data leakage from historical claim amounts, thereby reducing manual underwriting latency and providing transparent, scientifically grounded premium quotations.")
    
    add_heading("Feasibility study:")
    add_heading("Technical Feasibility")
    add_para("Technical feasibility determines whether the required hardware, software, tools, and technologies are available for developing the system.")
    
    add_heading("Hardware Requirements", is_bold=False)
    add_para("Computer/Laptop\nMinimum 4 GB RAM\nMinimum 10 GB free storage\nInternet connection for downloading required libraries and datasets", is_passage=False)
    
    add_heading("Software Requirements", is_bold=False)
    add_para("Operating System: Windows/Linux\nProgramming Language: Python\nIDE: Visual Studio Code / PyCharm\nFramework: Flask / Streamlit\nLibraries:\nPandas\nNumPy\nScikit-learn\nMatplotlib\nJoblib\nMachine Learning Algorithm: Linear Regression (Calibrated against Random Forest, Gradient Boosting, XGBoost)\nFeature Processing Technique: StandardScaler and OneHotEncoder", is_passage=False)
    
    add_heading("Technical Feasibility Result")
    add_para("The required hardware and software are easily available. Python and the required data science and web libraries are open-source and can run efficiently on a normal commodity computer. Therefore, the proposed system is technically feasible.")
    
    add_heading("Economic Feasibility")
    add_para("Economic feasibility determines whether the project can be developed within a reasonable cost.")
    add_para("The proposed system mainly uses open-source software and freely available tools. No expensive hardware or licensed software is required.")
    
    # Economic Feasibility Table: All borders, Black text, No background color
    tbl_econ = doc.add_table(rows=9, cols=2)
    tbl_econ.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_econ, color="000000", sz="4", val="single")
    econ_rows = [
        ("Resource", "Cost"),
        ("Python", "Free"),
        ("VS Code", "Free"),
        ("Flask / Streamlit", "Free"),
        ("Scikit-learn", "Free"),
        ("Pandas & NumPy", "Free"),
        ("Matplotlib & Joblib", "Free"),
        ("Dataset", "Free/Available dataset (8,000 records)"),
        ("Hardware", "Existing computer/laptop")
    ]
    for r_idx, (c1, c2) in enumerate(econ_rows):
        row = tbl_econ.rows[r_idx]
        row.cells[0].width = Inches(3.2)
        row.cells[1].width = Inches(3.0)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        row.cells[0].text = c1
        row.cells[1].text = c2
        for cell in row.cells:
            p = cell.paragraphs[0]
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
            p.runs[0].font.color.rgb = BLACK
            if r_idx == 0:
                p.runs[0].font.bold = True
                
    add_heading("Economic Feasibility Result")
    add_para("Since most of the software tools and libraries are freely available, the development cost is very low. Therefore, the proposed system is economically feasible.")
    
    add_heading("Operational Feasibility")
    add_para("Operational feasibility determines whether the proposed system can be easily used by its intended users.")
    add_para("The system provides a simple user interface where the user can enter demographic, biometric, and lifestyle attributes. The system processes the underwriting parameters and displays the predicted annual premium along with Explainable AI feature attributions.")
    
    add_heading("Working Process")
    add_para("User enters biometric and lifestyle data → Input validation → BMI computation → Feature encoding and scaling → Machine Learning model → Premium prediction → Result displayed", is_passage=False)
    add_para("The system does not require advanced technical knowledge from the user. It can be used by prospective policyholders, insurance sales agents, underwriting officers, and actuarial analysts who need to determine transparent premium estimations.")
    
    add_heading("Operational Feasibility Result")
    add_para("The system is simple, user-friendly, and easy to operate. It reduces the time required for manual underwriting analysis and provides quick, scientifically grounded results in under one second. Therefore, the proposed system is operationally feasible.")
    
    add_result_block("Thus, the problem was identified and the feasibility study was completed successfully. The study confirmed that the proposed system is technically, economically, and operationally feasible for automatically evaluating applicant risk factors and estimating fair, transparent health insurance premiums.")

    # =========================================================================
    # EX NO 2: Software Requirement Specification (SRS)
    # =========================================================================
    add_ex_header("02", "Software Requirement Specification (SRS)")
    add_heading("AIM:")
    add_para("To develop a Health Insurance Premium Prediction System using Python and Machine Learning to estimate annual insurance premiums and recommend matching policies based on applicant risk attributes.")
    
    add_heading("ALGORITHM:")
    srs_steps = [
        "Step 1: Identify the requirements of the Health Insurance Premium Prediction System.",
        "Step 2: Collect the functional and non-functional requirements of the system.",
        "Step 3: Identify the software and hardware requirements needed to develop the system.",
        "Step 4: Define the system features, such as biometric input, dynamic BMI calculation, feature scaling, and premium prediction.",
        "Step 5: Specify the input and output requirements of the system.",
        "Step 6: Define the system performance, reliability, usability, and security requirements.",
        "Step 7: Document all the gathered requirements in the SRS document adhering to IEEE standards.",
        "Step 8: Review and finalize the SRS document for system development."
    ]
    for s in srs_steps:
        add_para(s, is_passage=False)
        
    add_heading("Prepare SRS document with functional & non-functional requirements")
    add_heading("Functional Requirements")
    frs = [
        "• The system should accept applicant risk parameters from users (Age, Gender, Height, Weight, Children, Smoking Status, Region, Alcohol Habits, Annual Salary).",
        "• The system should dynamically calculate Body Mass Index (BMI = Weight_kg / Height_m²) and categorize applicants into standard WHO weight categories.",
        "• The system should preprocess categorical features using OneHotEncoder and continuous features using StandardScaler.",
        "• The system should prevent data leakage by isolating historical claim amounts from the feature inputs.",
        "• The system should predict the estimated annual premium in Indian Rupees (INR/year) using the trained machine learning model.",
        "• The system should display Explainable AI (XAI) feature impact breakdowns indicating additions and deductions.",
        "• The system should recommend matching insurance policies from the active repository of 118 policies.",
        "• The system should provide an interactive What-If scenario simulation slider tool.",
        "• The system should generate and allow download of a formal PDF underwriting quote."
    ]
    for f in frs:
        add_para(f, is_passage=False)
        
    add_heading("Non-Functional Requirements")
    nfrs = [
        "• Performance: The system should provide premium predictions in less than 1.0 second.",
        "• Usability: The interface should be simple, responsive across devices, and offer trilingual localization (English, Tamil, Hindi).",
        "• Reliability: The system should provide consistent, deterministic results for identical input parameters.",
        "• Maintainability: The codebase should be modular, separating preprocessing, model inference, and web presentation.",
        "• Security: Form inputs must be validated to prevent SQL injection and cross-site scripting attacks.",
        "• Compatibility: The system should run on Windows or Linux environments with standard Python 3.10+ runtimes."
    ]
    for n in nfrs:
        add_para(n, is_passage=False)
        
    add_heading("Hardware Requirements")
    add_para("Computer or laptop\nMinimum 4 GB RAM\nSufficient storage space (Minimum 10 GB free)\nInternet connection for installing software and downloading datasets", is_passage=False)
    
    add_heading("Software Requirements")
    add_para("Operating System: Windows or Linux\nProgramming Language: Python 3.10+\nIDE: Visual Studio Code\nFramework: Flask / Streamlit\nLibraries: Pandas, NumPy, Scikit-learn, XGBoost, Joblib, Matplotlib, ReportLab\nFeature Processing Technique: ColumnTransformer (StandardScaler, OneHotEncoder)\nMachine Learning Algorithm: Linear Regression (Production), Random Forest, XGBoost\nDatabase: SQLite / MySQL", is_passage=False)
    
    add_result_block("Thus, the functional, non-functional, hardware, and software requirements of the Health Insurance Premium Prediction System were identified successfully. The system is designed to provide fast, reliable, transparent, and user-friendly premium estimations.")

    # =========================================================================
    # EX NO 3: UML Diagrams – Use Case Diagram
    # =========================================================================
    add_ex_header("03", "UML Diagrams – Use Case Diagram")
    add_heading("AIM:")
    add_para("To design a UML Use Case Diagram that represents the interaction between the user, administrator, machine learning engine, and the Health Insurance Premium Prediction System.")
    
    add_heading("ALGORITHM:")
    uc_steps = [
        "Step 1: Identify the actors involved in the system, such as Policy Applicant (User), Insurance Administrator (Actuary), and ML Inference Subsystem.",
        "Step 2: Identify the main use cases of the system.",
        "Step 3: Define user activities, such as entering demographic and biometric parameters.",
        "Step 4: Connect the User actor with the profile input, prediction request, and comparison use cases.",
        "Step 5: Connect the system inference engine with the feature scaling and premium prediction use cases.",
        "Step 6: Define include relationships (Predict Premium includes Validate Inputs and Calculate BMI).",
        "Step 7: Represent relationships between actors and use cases using standard UML symbols.",
        "Step 8: Draw and verify the Use Case Diagram."
    ]
    for s in uc_steps:
        add_para(s, is_passage=False)
        
    add_heading("Model system actors and interactions:")
    add_para("A Use Case Diagram represents the interaction between external actors and the system boundaries.")
    
    add_image_figure(DIAGRAMS_DIR / "03_use_case_diagram.png", "Figure 3.1: UML Use Case Diagram for Health Insurance Premium Prediction System")
    
    add_heading("Actors:")
    add_para("• User (Policy Applicant): Enters demographic and biometric details, views predicted premium, simulates scenarios, and downloads PDF quotes.\n• System Administrator (Actuary): Manages insurer policy datasets and monitors model evaluation metrics (MAE, RMSE, R²).\n• ML Inference Subsystem: Preprocesses raw inputs, executes Linear Regression inference, and computes feature attributions.", is_passage=False)
    
    add_heading("Use Cases:")
    add_para("• Enter Biometric and Demographic Profile\n• Validate Form Inputs\n• Calculate Dynamic BMI and WHO Category\n• Preprocess and Scale Features\n• Predict Annual Premium using Linear Regression Pipeline\n• View Explainable AI (XAI) Feature Contributions\n• Compare Multi-Insurer Policies (118 Plans)\n• Simulate What-If Scenarios\n• Generate and Download PDF Quotation\n• Monitor Model Performance and Retrain Pipeline", is_passage=False)
    
    add_result_block("Thus, the Use Case Diagram was designed successfully to represent the user activities, administrative functions, and core machine learning capabilities of the Health Insurance Premium Prediction System.")

    # =========================================================================
    # EX NO 4: UML Diagrams – Class Diagram
    # =========================================================================
    add_ex_header("04", "UML Diagrams – Class Diagram")
    add_heading("AIM:")
    add_para("To design a UML Class Diagram representing the classes, attributes, methods, and relationships of the Health Insurance Premium Prediction System.")
    
    add_heading("ALGORITHM:")
    cd_steps = [
        "Step 1: Identify the main classes required for the system, such as User, ApplicantProfile, DataPreprocessor, PremiumPredictor, PolicyPlan, and QuoteReport.",
        "Step 2: Define attributes for each class.",
        "Step 3: Define methods and operations for each class.",
        "Step 4: Create the User and ApplicantProfile classes to manage user authentication and underwriting attributes.",
        "Step 5: Create the DataPreprocessor class to calculate BMI and apply OneHotEncoder and StandardScaler transforms.",
        "Step 6: Create the PremiumPredictor class to execute regression inference and calculate XAI feature attributions.",
        "Step 7: Create the PolicyPlan and QuoteReport classes to manage policy filtering and PDF rendering.",
        "Step 8: Establish associations, compositions, and dependencies between classes and draw the Class Diagram."
    ]
    for s in cd_steps:
        add_para(s, is_passage=False)
        
    add_heading("Design system structure with classes and relationships")
    add_para("A Class Diagram represents the object-oriented structure of the Health Insurance Premium Prediction System by detailing its classes, attributes, operations, and relationships.")
    
    add_image_figure(DIAGRAMS_DIR / "04_class_diagram.png", "Figure 4.1: UML Class Diagram for Health Insurance Premium Prediction System")
    
    add_heading("Classes and Their Functions:")
    add_para("• User: Manages user account credentials, authentication, and saved quotation history.\n• ApplicantProfile: Stores biometric and lifestyle attributes (age, sex, height, weight, bmi, children, smoker, region, liquor, salary).\n• DataPreprocessor: Cleans raw values, computes dynamic BMI, and transforms features using ColumnTransformer.\n• PremiumPredictor: Loads the serialized scikit-learn pipeline, computes annual premium quotes, and derives feature importances.\n• PolicyPlan: Represents insurer policy catalog entities, supporting filtering by budget and coverage.\n• QuoteReport: Compiles underwriting details into downloadable PDF documents using ReportLab.", is_passage=False)
    
    add_heading("Relationships:")
    add_para("• User has a 1-to-many relationship with ApplicantProfile.\n• ApplicantProfile supplies data to DataPreprocessor.\n• DataPreprocessor produces numerical feature vectors for PremiumPredictor.\n• PremiumPredictor passes predicted premium to PolicyPlan for recommendation matching.\n• PolicyPlan and PremiumPredictor collaborate with QuoteReport to render the final underwriting document.", is_passage=False)
    
    add_result_block("Thus, the Class Diagram was designed successfully to represent the system structure, encapsulated attributes, operations, and relationships between different domain classes.")

    # =========================================================================
    # EX NO 5: UML Diagrams – Sequence Diagram
    # =========================================================================
    add_ex_header("05", "UML Diagrams – Sequence Diagram")
    add_heading("AIM:")
    add_para("To design a UML Sequence Diagram representing the step-by-step chronological interaction between the user and system components during premium prediction and policy matching.")
    
    add_heading("ALGORITHM:")
    sq_steps = [
        "Step 1: Identify the objects involved in the system, such as User, Web Interface, Application Controller, Preprocessing Module, ML Regression Pipeline, and Database.",
        "Step 2: The user opens the HealthSecure underwriting application.",
        "Step 3: The system displays the biometric and lifestyle input form.",
        "Step 4: The user fills out parameters (Age, Height, Weight, Children, Smoker, Region, Liquor, Salary) and clicks Calculate.",
        "Step 5: The web interface dispatches the payload to the Application Controller.",
        "Step 6: The controller instructs the preprocessing module to calculate BMI and scale the numerical and categorical features.",
        "Step 7: The trained Linear Regression pipeline computes the estimated annual premium and feature impact values.",
        "Step 8: The controller retrieves matching insurer plans from the database and displays the final quote and recommendations."
    ]
    for s in sq_steps:
        add_para(s, is_passage=False)
        
    add_heading("Represent dynamic behavior of the system:")
    add_para("A Sequence Diagram captures the dynamic behavior of the Health Insurance Premium Prediction System, illustrating message lifelines and execution timing across components.")
    
    add_image_figure(DIAGRAMS_DIR / "05_sequence_diagram.png", "Figure 5.1: UML Sequence Diagram for Health Insurance Premium Prediction System")
    
    add_heading("Sequence Flow")
    add_para("1. User enters biometric and lifestyle details into the web form.\n2. Web application validates input constraints and dispatches an HTTP request.\n3. Application controller forwards input to the preprocessing module.\n4. Preprocessing module calculates BMI and normalizes features using OneHotEncoder and StandardScaler.\n5. Linear Regression pipeline predicts estimated annual premium in Indian Rupees.\n6. System derives Explainable AI (XAI) feature impact values.\n7. Controller queries the database to filter policies matching the applicant's risk and budget profile.\n8. Web interface renders the predicted annual premium, interactive What-If sliders, and policy recommendations.", is_passage=False)
    
    add_result_block("Thus, the Sequence Diagram was designed successfully to represent the dynamic behavior, chronological interactions, and message dispatch flow of the Health Insurance Premium Prediction System.")

    # =========================================================================
    # EX NO 6: Software Design – Architectural Design
    # =========================================================================
    add_ex_header("06", "Software Design – Architectural Design")
    add_heading("AIM:")
    add_para("To design a suitable layered and client-server architecture for the Health Insurance Premium Prediction System.")
    
    add_heading("ALGORITHM:")
    ar_steps = [
        "Step 1: Identify the main structural components and operational responsibilities of the system.",
        "Step 2: Design the Presentation Layer to provide a responsive user interface using HTML5, Bootstrap, and Streamlit.",
        "Step 3: Design the Application Layer to receive user inputs, manage routing, and enforce business rules.",
        "Step 4: Design the Preprocessing Layer to compute BMI and apply OneHotEncoder and StandardScaler transformations.",
        "Step 5: Design the Machine Learning Layer hosting the serialized Linear Regression pipeline to predict annual premiums.",
        "Step 6: Design the Policy Recommendation Layer to query and rank policies from the 118-plan insurance repository.",
        "Step 7: Design the Data Layer to store user profiles, quotation records, and policy catalogs in MySQL / SQLite.",
        "Step 8: Connect all layers and verify end-to-end communication and modular decoupling."
    ]
    for s in ar_steps:
        add_para(s, is_passage=False)
        
    add_heading("Develop architecture (Layered / Client-Server):")
    add_para("The Health Insurance Premium Prediction System follows a 4-Tier Layered Architecture with a Client-Server design. This architecture ensures high cohesion, loose coupling, and straightforward maintainability.")
    
    add_image_figure(DIAGRAMS_DIR / "06_architectural_design.png", "Figure 6.1: Architectural Design Diagram for Health Insurance Premium Prediction System")
    
    add_heading("Layers and Their Functions")
    add_para("• Presentation Layer: Provides the web interface for biometric inputs, interactive What-If scenario sliders, and trilingual display (English, Tamil, Hindi).\n• Application Layer: Handles HTTP requests, enforces input boundary validation, manages user sessions, and coordinates processing workflow.\n• Preprocessing & ML Layer: Computes dynamic BMI, applies ColumnTransformer feature transformations, and executes Linear Regression inference.\n• Data Layer: Persists user profiles, historical quotation logs, and the 118 multi-insurer health policy catalog in relational storage.", is_passage=False)
    
    add_heading("Working Process")
    add_para("User inputs biometrics on Presentation Layer → Application Layer validates data → Preprocessing Layer encodes and scales features → Machine Learning Layer predicts annual premium → Data Layer matches insurance policies → Complete quotation and recommendation view displayed.", is_passage=False)
    
    add_result_block("Thus, the architectural design was completed successfully by dividing the system into distinct operational layers for superior organization, robust performance, and simplified maintenance.")

    # =========================================================================
    # EX NO 7: UI/UX Design
    # =========================================================================
    add_ex_header("07", "UI/UX Design")
    add_heading("AIM:")
    add_para("To design a simple, intuitive, and user-friendly interface for the Health Insurance Premium Prediction System using UI/UX design principles.")
    
    add_heading("ALGORITHM:")
    ui_steps = [
        "Step 1: Identify the user interface requirements and target user personas (policyholders, insurance agents).",
        "Step 2: Design the home dashboard with prominent title branding and trilingual language toggle options.",
        "Step 3: Create input panels organized into Demographic, Clinical, and Lifestyle sections.",
        "Step 4: Add real-time input validation to prevent invalid entries (e.g., negative age or height).",
        "Step 5: Design high-impact visual result cards displaying estimated annual premium, monthly breakdown, and BMI status.",
        "Step 6: Display Explainable AI (XAI) feature impact bars illustrating individual premium additions and deductions.",
        "Step 7: Provide interactive What-If scenario sliders to simulate lifestyle changes in real time.",
        "Step 8: Test the interface across multiple screen viewports to ensure responsive, accessible operation."
    ]
    for s in ui_steps:
        add_para(s, is_passage=False)
        
    add_heading("Design user interface (wireframes/prototypes using tools like Figma)")
    add_para("UI/UX Design focuses on simplicity, immediate visual feedback, and effortless navigation for entering underwriting parameters and interpreting actuarial predictions.")
    
    add_image_figure(DIAGRAMS_DIR / "07_ui_ux_wireframes.png", "Figure 7.1: UI/UX Wireframes and Dashboard Layout for HealthSecure")
    
    add_heading("Main Interface Components")
    add_para("• Home Page & Navigation: Displays brand logo, trilingual language selector (English, Tamil, Hindi), and theme controls.\n• Input Panels: Biometric inputs (Height, Weight, Age), Demographic selectors (Gender, Region, Children), and Lifestyle controls (Smoking, Alcohol, Salary).\n• Calculate Button: Triggers form validation and model inference.\n• Prediction Showcase Card: Displays estimated Annual Premium (INR/year) with monthly breakdown (INR/month).\n• XAI Feature Impact Breakdown: Visual bar chart illustrating exact rupee additions (e.g., Smoker: +₹4,500, BMI: +₹1,250).\n• What-If Simulator: Interactive sliders for adjusting BMI, smoking status, or coverage limits.\n• Multi-Insurer Plan Cards: Grid of eligible insurance plans from Star Health, HDFC ERGO, and Care Health with PDF export options.", is_passage=False)
    
    add_heading("Tools Used")
    add_para("• Figma: Wireframe structuring, UI layout planning, and accessibility color contrast design.\n• HTML5, CSS3, Bootstrap 5, Streamlit: Building responsive user interface components.\n• Matplotlib / Chart.js: Dynamic client-side visualization of feature importance charts.", is_passage=False)
    
    add_result_block("Thus, the UI/UX design was completed successfully by planning the application layout and creating an intuitive, accessible interface for entering underwriting data and viewing premium estimations.")

    # =========================================================================
    # EX NO 8: Implementation using Version Control
    # =========================================================================
    add_ex_header("08", "Implementation using Version Control")
    add_heading("AIM:")
    add_para("To develop the core premium prediction module and manage the project source code using Git version control.")
    
    add_heading("ALGORITHM:")
    vc_steps = [
        "Step 1: Install Git and configure the Git username and email.",
        "Step 2: Create a project folder for the Health Insurance Premium Prediction System.",
        "Step 3: Initialize the Git repository using the git init command.",
        "Step 4: Add the project files, such as app.py, model.py, train.py, and insurance.csv.",
        "Step 5: Track the project files using the git add command.",
        "Step 6: Save changes using the git commit command with meaningful commit messages.",
        "Step 7: Create a GitHub remote repository and connect it using git remote add origin.",
        "Step 8: Upload project source files to GitHub using the git push command."
    ]
    for s in vc_steps:
        add_para(s, is_passage=False)
        
    add_heading("Develop a small module and manage code using Git:")
    add_heading("Implementation Using Version Control:")
    add_para("Version control is used to manage source code changes, track historical updates, and support collaborative development. Git and GitHub are used to maintain and manage the Health Insurance Premium Prediction System.")
    
    add_heading("Small Module Implementation:")
    add_para("The premium prediction service accepts applicant biometric details, calculates dynamic BMI, applies pre-trained ColumnTransformer scaling, and predicts estimated annual premium using the trained Linear Regression model.")
    
    add_heading("Sample Python Code:")
    sample_code = (
        "import joblib\n"
        "import pandas as pd\n\n"
        "# Load pre-trained machine learning pipeline\n"
        "model_pipeline = joblib.load('models/premium_model.joblib')\n\n"
        "def predict_health_premium(age, sex, height_cm, weight_kg, children, smoker, region, liquor, salary):\n"
        "    # Compute Body Mass Index (BMI)\n"
        "    height_m = height_cm / 100.0\n"
        "    bmi = round(weight_kg / (height_m ** 2), 2)\n"
        "    \n"
        "    # Format inputs into single-row DataFrame\n"
        "    applicant_data = pd.DataFrame([{\n"
        "        'age': int(age),\n"
        "        'sex': str(sex).lower(),\n"
        "        'bmi': float(bmi),\n"
        "        'children': int(children),\n"
        "        'smoker': str(smoker).lower(),\n"
        "        'region': str(region).lower(),\n"
        "        'liquor': str(liquor).lower(),\n"
        "        'salary': float(salary)\n"
        "    }])\n"
        "    \n"
        "    # Predict annual premium in INR\n"
        "    predicted_premium = model_pipeline.predict(applicant_data)[0]\n"
        "    annual_premium = max(2500.0, round(float(predicted_premium), 2))\n"
        "    monthly_premium = round(annual_premium / 12.0, 2)\n"
        "    \n"
        "    return {\n"
        "        'bmi': bmi,\n"
        "        'annual_premium_inr': annual_premium,\n"
        "        'monthly_premium_inr': monthly_premium\n"
        "    }\n"
    )
    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_code.paragraph_format.first_line_indent = Inches(0)
    p_code.paragraph_format.line_spacing = 1.0
    r_code = p_code.add_run(sample_code)
    r_code.font.name = 'Consolas'
    r_code.font.size = Pt(10)
    r_code.font.color.rgb = BLACK
    
    add_image_figure(DIAGRAMS_DIR / "08_git_version_control.png", "Figure 8.1: Git Version Control Workflow for HealthSecure")
    
    add_heading("Git Commands:")
    add_para("The following Git commands are used to manage the project repository:")
    
    tbl_git = doc.add_table(rows=7, cols=2)
    tbl_git.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_git, color="000000", sz="4", val="single")
    git_rows = [
        ("Git Command", "Purpose"),
        ("git init", "Initialize local repository"),
        ("git add .", "Add all project files to staging area"),
        ("git commit -m 'Initial commit'", "Save staged changes with commit description"),
        ("git status", "Check status of working tree and tracked files"),
        ("git log --oneline", "View abbreviated commit history"),
        ("git push -u origin main", "Upload project commits to remote GitHub repository")
    ]
    for r_idx, (c1, c2) in enumerate(git_rows):
        row = tbl_git.rows[r_idx]
        row.cells[0].width = Inches(2.8)
        row.cells[1].width = Inches(3.4)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        row.cells[0].text = c1
        row.cells[1].text = c2
        for cell in row.cells:
            p = cell.paragraphs[0]
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
            p.runs[0].font.color.rgb = BLACK
            if r_idx == 0:
                p.runs[0].font.bold = True
                
    add_heading("Version Control Process:")
    add_para("1. Create local project folder.\n2. Initialize Git using git init.\n3. Add source code using git add .\n4. Commit changes using git commit -m.\n5. Connect to remote repository using git remote add origin.\n6. Upload the project to GitHub using git push.", is_passage=False)
    
    add_result_block("Thus, the core premium prediction module was implemented successfully in Python, and Git version control was used to track, commit, and manage project code changes.")

    # =========================================================================
    # EX NO 9: Software Testing
    # =========================================================================
    add_ex_header("09", "Software Testing")
    add_heading("AIM:")
    add_para("To test the Health Insurance Premium Prediction System using Unit Testing, Integration Testing, Black-Box Testing, and White-Box Testing to identify errors and ensure the application works correctly.")
    
    add_heading("ALGORITHM:")
    st_steps = [
        "Step 1: Identify the modules and functionalities to be tested in the system.",
        "Step 2: Prepare test cases for entering applicant demographic, biometric, and lifestyle inputs.",
        "Step 3: Perform input validation to check whether values are within valid actuarial ranges.",
        "Step 4: Test dynamic BMI computation logic for standard, underweight, and obese boundary conditions.",
        "Step 5: Test the ColumnTransformer feature scaling and OneHotEncoder process.",
        "Step 6: Test the Linear Regression model to verify predicted annual premium values.",
        "Step 7: Perform unit testing and integration testing to check individual functions and their module interactions.",
        "Step 8: Verify output results across healthy and high-risk applicant profiles and correct any defects."
    ]
    for s in st_steps:
        add_para(s, is_passage=False)
        
    add_heading("A. Test Cases – Unit Testing:")
    add_para("Unit testing is used to test individual modules and functions of the application separately.")
    
    tbl_ut = doc.add_table(rows=8, cols=3)
    tbl_ut.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_ut, color="000000", sz="4", val="single")
    ut_rows = [
        ("TestCase ID", "Test Scenario", "Expected Result"),
        ("UT01", "Calculate normal BMI (H=175cm, W=70kg)", "BMI = 22.86 (Normal weight category)"),
        ("UT02", "Calculate underweight BMI (H=180cm, W=50kg)", "BMI = 15.43 (Underweight category)"),
        ("UT03", "Calculate obese BMI (H=165cm, W=90kg)", "BMI = 33.06 (Obese surcharge triggered)"),
        ("UT04", "Evaluate smoker surcharge attribution", "Display ~₹4,500 smoker risk premium addition"),
        ("UT05", "Evaluate liquor consumption attribution", "Display ~₹1,200 alcohol risk premium addition"),
        ("UT06", "Submit empty required input field", "Display input validation warning message"),
        ("UT07", "Load saved joblib model artifact", "Model pipeline loads successfully into memory")
    ]
    for r_idx, (c1, c2, c3) in enumerate(ut_rows):
        row = tbl_ut.rows[r_idx]
        row.cells[0].width = Inches(1.3)
        row.cells[1].width = Inches(2.6)
        row.cells[2].width = Inches(2.5)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        set_cell_margins(row.cells[2])
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        for cell in row.cells:
            p = cell.paragraphs[0]
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
            p.runs[0].font.color.rgb = BLACK
            if r_idx == 0:
                p.runs[0].font.bold = True
                
    add_heading("B. Integration Testing:")
    add_para("Integration testing checks whether different modules work together correctly.")
    
    tbl_it = doc.add_table(rows=6, cols=3)
    tbl_it.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_it, color="000000", sz="4", val="single")
    it_rows = [
        ("Test Case ID", "Test Scenario", "Expected Result"),
        ("IT01", "Connect Web UI with Application Controller", "Controller receives all 8 features correctly"),
        ("IT02", "Connect input validation with Preprocessing", "Features are converted and standardized"),
        ("IT03", "Connect Preprocessing with Linear Regression", "Model predicts annual premium correctly"),
        ("IT04", "Connect Prediction with Policy Recommender", "Matching plans are filtered and returned"),
        ("IT05", "Connect Policy Selection with PDF Generator", "Generates downloadable PDF quote report")
    ]
    for r_idx, (c1, c2, c3) in enumerate(it_rows):
        row = tbl_it.rows[r_idx]
        row.cells[0].width = Inches(1.4)
        row.cells[1].width = Inches(2.5)
        row.cells[2].width = Inches(2.5)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        set_cell_margins(row.cells[2])
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        for cell in row.cells:
            p = cell.paragraphs[0]
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
            p.runs[0].font.color.rgb = BLACK
            if r_idx == 0:
                p.runs[0].font.bold = True
                
    add_heading("C. Black-Box Testing:")
    add_para("Black-box testing checks application functionality without knowing its internal code logic.")
    add_para("Test cases:\n• Enter a standard young healthy profile and verify baseline quote (~₹9,850/yr).\n• Enter an elderly smoker profile and verify elevated risk quote (~₹27,450/yr).\n• Click Calculate without entering required fields and verify error prompt.\n• Switch language toggle to Tamil and Hindi and verify UI translations.\n• Result: The application accepts valid inputs, rejects invalid inputs, and displays expected premium quotes.", is_passage=False)
    
    add_heading("D. White-Box Testing:")
    add_para("White-box testing checks internal code structure, execution paths, and mathematical bounds.")
    add_para("Test cases:\n• Check dynamic calculate_bmi() logic for zero-division safety when height = 0.\n• Check premium boundary condition: verify max(2500.0, predicted) prevents negative outputs.\n• Verify StandardScaler transforms and OneHotEncoder category alignment.\n• Check model.predict() output format and float rounding.\n• Result: Internal branches, conditions, and calculations execute without errors or exceptions.", is_passage=False)
    
    add_image_figure(DIAGRAMS_DIR / "09_software_testing.png", "Figure 9.1: Software Testing Suite and Results for HealthSecure")
    
    add_heading("E. Overall Testing Result:")
    add_para("Testing completed successfully. The Health Insurance Premium Prediction System was thoroughly tested using unit testing, integration testing, black-box testing, and white-box testing. The application reliably calculates dynamic BMI, predicts personalized annual premiums, displays Explainable AI feature attributions, and exports official PDF quotes. On held-out test data (1,600 samples), the selected Linear Regression model achieved MAE = ₹2,615.84, RMSE = ₹3,418.62, and R² = 0.6492.")
    
    add_result_block("Thus, the Health Insurance Premium Prediction System was successfully tested. The application correctly estimates personalized health premiums and displays transparent feature contribution breakdowns.")

    # =========================================================================
    # EX NO 10: MINI PROJECT WITH DOCUMENTATION
    # =========================================================================
    add_ex_header("10", "MINI PROJECT WITH DOCUMENTATION")
    add_heading("Aim:")
    add_para("To develop a complete Health Insurance Premium Prediction System by integrating all phases of software development, including SRS, Design, Coding, Testing, and Documentation.")
    
    add_heading("Algorithm:")
    mini_steps = [
        "Step 1: Identify the problem and prepare the Software Requirement Specification (SRS).",
        "Step 2: Analyze the functional and non-functional requirements of the project.",
        "Step 3: Design the system using UML diagrams such as Use Case Diagram, Class Diagram, and Sequence Diagram.",
        "Step 4: Develop the system architecture and design the user interface using Flask / Streamlit.",
        "Step 5: Write Python code to implement the Health Insurance Premium Prediction System.",
        "Step 6: Train the machine learning model using StandardScaler, OneHotEncoder, and Linear Regression.",
        "Step 7: Test the application using diverse applicant risk profiles and verify prediction results.",
        "Step 8: Prepare complete project documentation, including SRS, Design, Implementation, Testing, Results, and Conclusion."
    ]
    for s in mini_steps:
        add_para(s, is_passage=False)
        
    add_heading("Integrate all phases: SRS → Design → Coding → Testing → Report")
    
    add_heading("1. Introduction")
    add_para("The Health Insurance Premium Prediction System (HealthSecure) is a machine learning-based application developed using Python. In contemporary healthcare financing, determining fair, accurate, and transparent health insurance premiums is a vital requirement. Prospective policyholders frequently encounter opaque rate calculations, lengthy underwriting waiting periods, and uncertainty regarding how their personal biometrics and lifestyle choices dictate required premium contributions.")
    add_para("This project automatically evaluates applicant risk parameters (age, sex, BMI, dependents, smoking status, region, alcohol habits, and salary) and predicts personalized annual health insurance premiums in Indian Rupees (INR/year). Furthermore, it provides Explainable AI (XAI) feature transparency, interactive What-If scenario simulations, and automated matching against 118 real-world insurance policies.")
    add_para("The application is developed with a responsive web interface supporting trilingual localization (English, Tamil, Hindi) for convenient access across regional demographics.")
    
    add_heading("2. Objectives")
    objs = [
        "• To develop an automated health insurance premium estimation system.",
        "• To eliminate data leakage by isolating historical claim amounts during preprocessing.",
        "• To predict annual premiums accurately using supervised machine learning algorithms.",
        "• To apply standard scaling and one-hot encoding for robust numerical feature representation.",
        "• To provide transparent Explainable AI (XAI) feature impact breakdowns.",
        "• To offer interactive What-If scenario sliders for prospective lifestyle planning.",
        "• To recommend suitable policies from an active repository of 118 health insurance plans.",
        "• To provide a simple, accessible, and user-friendly interface with trilingual support.",
        "• To generate publication-grade PDF quotation summaries for formal documentation."
    ]
    for ob in objs:
        add_para(ob, is_passage=False)
        
    add_heading("3. Technologies Used")
    tbl_tech = doc.add_table(rows=10, cols=2)
    tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_tech, color="000000", sz="4", val="single")
    tech_rows = [
        ("Technology", "Purpose"),
        ("Python", "Main programming language for data pipeline and web application"),
        ("Flask / Streamlit", "Frontend and application controller framework"),
        ("Pandas", "Dataset manipulation and tabular record handling"),
        ("Scikit-learn", "Machine learning pipeline, OneHotEncoder, StandardScaler, Regression"),
        ("Linear Regression", "Selected production regression algorithm for annual premium pricing"),
        ("Joblib", "Saving and loading trained machine learning model artifacts"),
        ("ReportLab", "Dynamic PDF underwriting quotation report generation"),
        ("Matplotlib", "Plotting model evaluation graphs and XAI feature attributions"),
        ("CSV & MySQL", "Underwriting dataset storage and user quote management")
    ]
    for r_idx, (c1, c2) in enumerate(tech_rows):
        row = tbl_tech.rows[r_idx]
        row.cells[0].width = Inches(2.2)
        row.cells[1].width = Inches(4.0)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        row.cells[0].text = c1
        row.cells[1].text = c2
        for cell in row.cells:
            p = cell.paragraphs[0]
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
            p.runs[0].font.color.rgb = BLACK
            if r_idx == 0:
                p.runs[0].font.bold = True
                
    add_heading("4. System Architecture")
    add_para("The project follows a layered architecture. Each layer performs a separate function in the insurance underwriting and premium prediction process.")
    
    add_image_figure(DIAGRAMS_DIR / "10_mini_project_lifecycle.png", "Figure 10.1: Full SDLC Lifecycle for Health Insurance Premium Prediction System")
    
    add_heading("Layers of the System:")
    add_para("• User Interface Layer: Applicants input biometric and lifestyle information through the web application.\n• Preprocessing Layer: Cleans inputs, calculates dynamic BMI, and converts categorical and numerical features into standard representations.\n• Machine Learning Layer: Serialized Linear Regression model computes estimated annual premium in Indian Rupees.\n• Policy Recommender Layer: Filters and matches plans from 118 insurer policies based on applicant budget.\n• Output Layer: Displays predicted premium, monthly breakdown, XAI feature attribution charts, and downloadable PDF quote.", is_passage=False)
    
    add_heading("5. Working Process")
    add_para("1. The user opens the Health Insurance Premium Prediction application.\n2. The user enters Age, Sex, Height, Weight, Dependents, Smoker, Region, Liquor, and Salary.\n3. The application receives and validates the input parameters.\n4. The preprocessing module calculates BMI = Weight / (Height²) and scales features.\n5. The trained Linear Regression model analyzes the input features.\n6. The model predicts the annual premium amount (INR/year).\n7. The application retrieves matching insurance policies from the active repository.\n8. The application displays the estimated premium, feature attributions, and policy cards.", is_passage=False)
    
    add_heading("6. Machine Learning Model")
    add_para("This project uses Linear Regression, a supervised machine learning regression algorithm, benchmarked against Random Forest, Gradient Boosting, and XGBoost.")
    add_para("A core actuarial principle implemented is data leakage prevention: historical total_claim_amount is strictly excluded from prediction-time feature inputs and used exclusively during preprocessing to formulate the ground-truth target:")
    add_para("Charges (INR/year) = 5000 + (Age × 180) + (Claim Exposure × 0.06) + (Smoker × 4500) + [max(BMI - 25, 0) × 250] + (Liquor × 1200) + (Children × 2200)", is_passage=True)
    add_para("Model Training Process:\n• Load the 8,000-record Indian health insurance dataset.\n• Isolate target charges from input features.\n• Split the dataset into 80% training data and 20% test data (1,600 samples).\n• Build ColumnTransformer with StandardScaler for numerical features and OneHotEncoder for categorical features.\n• Train Linear Regression, Random Forest, Gradient Boosting, and XGBoost models.\n• Evaluate model performance (Linear Regression achieved best test MAE = ₹2,615.84, R² = 0.6492).\n• Save the trained pipeline using Joblib.", is_passage=False)
    
    add_heading("7. Project Workflow Diagram")
    wf_text = (
        "        Start\n"
        "          |\n"
        "          v\n"
        "   Load Insurance Dataset\n"
        "          |\n"
        "          v\n"
        "   Data Preprocessing & BMI Calculation\n"
        "          |\n"
        "          v\n"
        "   ColumnTransformer (Scaler & OneHotEncoder)\n"
        "          |\n"
        "          v\n"
        "   Train Linear Regression Model\n"
        "          |\n"
        "          v\n"
        "    Model Evaluation (MAE: ₹2,615.84, R²: 0.6492)\n"
        "          |\n"
        "          v\n"
        "     Save Trained Pipeline\n"
        "          |\n"
        "          v\n"
        "    User Enters Biometrics & Lifestyle\n"
        "          |\n"
        "          v\n"
        "    Predict Annual Premium (INR)\n"
        "          |\n"
        "          v\n"
        "  Display Quote & Policy Recommendations\n"
        "          |\n"
        "          v\n"
        "         Stop\n"
    )
    p_wf = doc.add_paragraph()
    p_wf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_wf.paragraph_format.first_line_indent = Inches(0)
    p_wf.paragraph_format.line_spacing = 1.0
    r_wf = p_wf.add_run(wf_text)
    r_wf.font.name = 'Consolas'
    r_wf.font.size = Pt(10)
    r_wf.font.color.rgb = BLACK
    
    add_heading("8. Sample Project Output")
    add_heading("Sample Input and Output Profiles:")
    
    tbl_out = doc.add_table(rows=6, cols=3)
    tbl_out.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_out, color="000000", sz="4", val="single")
    out_rows = [
        ("Sample Applicant Profile", "Predicted Premium", "Recommended Plan"),
        ("Age: 22, Male, BMI: 21.5, Non-smoker, 0 kids", "₹9,850 / year", "Star Health Young Star"),
        ("Age: 35, Female, BMI: 24.2, Non-smoker, 1 kid", "₹14,250 / year", "HDFC ERGO Optima Secure"),
        ("Age: 42, Male, BMI: 28.5, Smoker, 2 kids", "₹22,600 / year", "Care Health Supreme"),
        ("Age: 58, Male, BMI: 32.1, Smoker, 0 kids", "₹27,450 / year", "Niva Bupa Senior First"),
        ("Age: 29, Female, BMI: 19.8, Non-smoker, 0 kids", "₹10,200 / year", "ICICI Lombard Health Care")
    ]
    for r_idx, (c1, c2, c3) in enumerate(out_rows):
        row = tbl_out.rows[r_idx]
        row.cells[0].width = Inches(2.8)
        row.cells[1].width = Inches(1.6)
        row.cells[2].width = Inches(2.0)
        set_cell_margins(row.cells[0])
        set_cell_margins(row.cells[1])
        set_cell_margins(row.cells[2])
        row.cells[0].text = c1
        row.cells[1].text = c2
        row.cells[2].text = c3
        for cell in row.cells:
            p = cell.paragraphs[0]
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
            p.runs[0].font.color.rgb = BLACK
            if r_idx == 0:
                p.runs[0].font.bold = True
                
    add_heading("Sample Application Output:")
    add_para("Health Insurance Premium Prediction System\nEnter your profile details:\nAge: 35 | Sex: Female | Height: 165 cm | Weight: 66 kg | BMI: 24.24 | Smoker: No | Region: Tamil Nadu | Salary: ₹7,50,000\nPredicted Annual Premium: ₹14,250 / year\nMonthly Breakdown: ₹1,187.50 / month\nTop Matching Policy: HDFC ERGO Optima Secure (Cover: ₹5,00,000)\nNote: Predicted results are based on supervised machine learning regression trained on 8,000 Indian health insurance records.", is_passage=False)
    
    add_heading("9. Advantages")
    advs = [
        "• Saves time by automatically calculating actuarially fair health insurance premiums in under one second.",
        "• Eliminates underwriting data leakage by isolating historical claim amounts during preprocessing.",
        "• Provides transparent Explainable AI (XAI) feature contribution breakdowns for prospective consumers.",
        "• Supports interactive What-If scenario simulations encouraging healthier lifestyles.",
        "• Matches applicants objectively against 118 multi-insurer health policies.",
        "• Simple and accessible web interface with trilingual localization (English, Tamil, Hindi).",
        "• Generates downloadable publication-grade PDF quotation reports for formal documentation."
    ]
    for ad in advs:
        add_para(ad, is_passage=False)
        
    add_heading("10. Future Enhancements")
    futs = [
        "• Wearable Health Integration: Incorporate real-time daily step counts and heart rates from smartwatches.",
        "• OCR Medical Records Parsing: Automatically scan and extract preexisting condition reports using Tesseract OCR.",
        "• Deep Learning Survival Models: Implement longitudinal neural survival analysis for multi-year risk trajectories.",
        "• Blockchain Policy Verification: Deploy smart contracts on Ethereum for tamper-proof policy issuance and instant claim settlements."
    ]
    for fu in futs:
        add_para(fu, is_passage=False)
        
    # Final Result
    add_heading("RESULT")
    add_para("Thus, the complete Health Insurance Premium Prediction System (HealthSecure) was developed, integrated, tested, and documented across all phases of the Software Development Life Cycle (SDLC). The system accurately evaluates applicant risk factors, estimates personalized annual premiums, provides Explainable AI transparency, and dynamically matches optimal insurance policies.")

    # Save DOCX
    doc.save(str(DOCX_PATH))
    print(f"Generated clean black & white Word Document: {DOCX_PATH}")

build_manual()
