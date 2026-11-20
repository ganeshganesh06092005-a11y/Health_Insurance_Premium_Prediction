"""
High-Resolution Diagram Generator for Software Engineering Lab Manual Programs
Programs 3 to 10 for HealthSecure (Health Insurance Premium Prediction System)
Outputs publication-quality 300 DPI diagrams with clean typography and alignment.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Arrow, FancyArrowPatch, Polygon
import numpy as np

OUTPUT_DIR = Path("d:/Ganesh/Health_Insurance_Premium_Prediction/lab_manual_diagrams")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Color Palette: Professional Academic & Medical Tech
NAVY = "#0a2540"
DARK_BLUE = "#1e3a8a"
TEAL = "#0d9488"
LIGHT_TEAL = "#ccfbf1"
SOFT_BLUE = "#e0f2fe"
ACCENT_BLUE = "#0284c7"
LIGHT_BG = "#f8fafc"
BORDER_COLOR = "#94a3b8"
CARD_BG = "#ffffff"
TEXT_DARK = "#0f172a"
TEXT_MUTED = "#475569"
GREEN = "#16a34a"
LIGHT_GREEN = "#dcfce7"
AMBER = "#d97706"
LIGHT_AMBER = "#fef3c7"
PURPLE = "#7c3aed"
LIGHT_PURPLE = "#f3e8ff"
ROSE = "#e11d48"
LIGHT_ROSE = "#ffe4e6"


def draw_header(ax, title, program_num, subtitle):
    """Draw a clean, uniform top header on every diagram."""
    ax.add_patch(FancyBboxPatch((0.02, 0.91), 0.96, 0.075, boxstyle="round,pad=0.012,rounding_size=0.015",
                               facecolor=NAVY, edgecolor="none", zorder=1))
    ax.text(0.04, 0.955, title, fontsize=14, fontweight="bold", color="#ffffff", va="center", zorder=2)
    ax.text(0.04, 0.925, f"SOFTWARE ENGINEERING LAB — PROGRAM {program_num}: {subtitle.upper()}",
            fontsize=9.5, fontweight="semibold", color="#38bdf8", va="center", zorder=2)
    ax.text(0.96, 0.94, "HealthSecure System", fontsize=11, fontweight="bold", color="#ffffff",
            ha="right", va="center", zorder=2)
    ax.text(0.96, 0.925, "Lab Record Documentation", fontsize=8.5, color="#cbd5e1",
            ha="right", va="center", zorder=2)


# =====================================================================
# PROGRAM 3: UML USE CASE DIAGRAM
# =====================================================================
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_header(ax, "HEALTHSECURE: SMART HEALTH INSURANCE PREDICTION — UML USE CASE DIAGRAM",
                "3", "System Actors and Interactions Modeling")

    # System Boundary Box
    boundary = FancyBboxPatch((0.24, 0.05), 0.52, 0.83, boxstyle="round,pad=0.01,rounding_size=0.02",
                              facecolor="#f8fafc", edgecolor="#0284c7", linewidth=2.2, linestyle="-", zorder=1)
    ax.add_patch(boundary)
    ax.text(0.50, 0.855, "System Boundary: HealthSecure Web Application Platform",
            fontsize=12, fontweight="bold", color=NAVY, ha="center", va="center", zorder=2)

    # Actor Helper
    def draw_actor(x, y, name, role="Actor"):
        # Head
        ax.add_patch(Circle((x, y + 0.04), 0.02, facecolor="#e0f2fe", edgecolor=NAVY, linewidth=2, zorder=4))
        # Body
        ax.plot([x, x], [y + 0.02, y - 0.02], color=NAVY, linewidth=2.2, zorder=4)
        # Arms
        ax.plot([x - 0.022, x + 0.022], [y + 0.005, y + 0.005], color=NAVY, linewidth=2.2, zorder=4)
        # Legs
        ax.plot([x, x - 0.018], [y - 0.02, y - 0.05], color=NAVY, linewidth=2.2, zorder=4)
        ax.plot([x, x + 0.018], [y - 0.02, y - 0.05], color=NAVY, linewidth=2.2, zorder=4)
        # Label Box
        ax.text(x, y - 0.07, name, fontsize=10, fontweight="bold", color=NAVY, ha="center", va="top", zorder=4)
        ax.text(x, y - 0.09, f"<<{role}>>", fontsize=8, fontstyle="italic", color=TEXT_MUTED, ha="center", va="top", zorder=4)

    # Left Actors
    draw_actor(0.10, 0.68, "Policy Applicant /\nUnregistered User", "Primary Actor")
    draw_actor(0.10, 0.32, "Registered User /\nPolicyholder", "Primary Actor")

    # Right Actors
    draw_actor(0.89, 0.68, "System Administrator\n(Role: Admin)", "Secondary Actor")
    draw_actor(0.89, 0.32, "Machine Learning &\nDatabase Subsystem", "External System")

    # Use Cases (Ovals) inside boundary
    use_cases = [
        # (id, x, y, label, type)
        ("UC1", 0.37, 0.78, "UC1: Register & Authenticate\nUser Account", "core"),
        ("UC2", 0.63, 0.78, "UC2: Manage Users & RBAC\n(admin@healthsecure.com)", "admin"),
        ("UC3", 0.37, 0.65, "UC3: Enter Biometrics &\nHealth Data (Height, Weight, ...)", "core"),
        ("UC4", 0.63, 0.65, "UC4: Auto-Calculate BMI\n[wt(kg) / (ht(m))^2]", "include"),
        ("UC5", 0.37, 0.51, "UC5: Predict Actuarial Annual\nPremium (charges)", "core"),
        ("UC6", 0.63, 0.51, "UC6: Explain Prediction (XAI)\nFeature Weights & Insights", "include"),
        ("UC7", 0.37, 0.37, "UC7: Match Active Demo Plans\n(Nearest L1 Premium Diff)", "include"),
        ("UC8", 0.63, 0.37, "UC8: Side-by-Side Compare\nInsurance Plans (Max 3)", "core"),
        ("UC9", 0.37, 0.23, "UC9: Scenario Simulator\n(What-If Analysis)", "extend"),
        ("UC10", 0.63, 0.23, "UC10: Download Detailed\nPDF Underwriting Report", "extend"),
        ("UC11", 0.37, 0.10, "UC11: View Historic Records\n& Financial Ratios", "core"),
        ("UC12", 0.63, 0.10, "UC12: Inspect Model Benchmark\nMetrics (MAE, RMSE, R^2)", "admin"),
    ]

    uc_centers = {}
    for ucid, x, y, label, uctype in use_cases:
        uc_centers[ucid] = (x, y)
        if uctype == "core":
            fc, ec = "#ffffff", "#0284c7"
        elif uctype == "admin":
            fc, ec = "#fef3c7", "#d97706"
        elif uctype == "include":
            fc, ec = "#ccfbf1", "#0d9488"
        else: # extend
            fc, ec = "#f3e8ff", "#7c3aed"

        ellipse = patches.Ellipse((x, y), 0.21, 0.08, facecolor=fc, edgecolor=ec, linewidth=1.8, zorder=3)
        ax.add_patch(ellipse)
        ax.text(x, y, label, fontsize=8.2, fontweight="semibold", color=NAVY, ha="center", va="center", zorder=4)

    # Actor Association Lines (Solid)
    def connect_actor_uc(ax_pt, uc_pt, color=NAVY):
        ax.plot([ax_pt[0], uc_pt[0]], [ax_pt[1], uc_pt[1]], color=color, linewidth=1.3, zorder=2)

    # Policy Applicant links
    connect_actor_uc((0.14, 0.68), (0.27, 0.78))
    connect_actor_uc((0.14, 0.68), (0.27, 0.65))
    connect_actor_uc((0.14, 0.68), (0.27, 0.51))

    # Registered User links
    connect_actor_uc((0.14, 0.32), (0.27, 0.65))
    connect_actor_uc((0.14, 0.32), (0.27, 0.51))
    connect_actor_uc((0.14, 0.32), (0.27, 0.37))
    connect_actor_uc((0.14, 0.32), (0.53, 0.37))
    connect_actor_uc((0.14, 0.32), (0.27, 0.23))
    connect_actor_uc((0.14, 0.32), (0.53, 0.23))
    connect_actor_uc((0.14, 0.32), (0.27, 0.10))

    # Admin links
    connect_actor_uc((0.85, 0.68), (0.73, 0.78))
    connect_actor_uc((0.85, 0.68), (0.73, 0.10))
    connect_actor_uc((0.85, 0.68), (0.73, 0.51))

    # Backend / ML links
    connect_actor_uc((0.85, 0.32), (0.73, 0.51))
    connect_actor_uc((0.85, 0.32), (0.73, 0.37))
    connect_actor_uc((0.85, 0.32), (0.73, 0.23))

    # <<include>> & <<extend>> relationships (Dashed with arrows)
    def draw_relationship(start, end, label, rel_type="include"):
        color = "#0d9488" if rel_type == "include" else "#7c3aed"
        arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12,
                                linestyle="--", linewidth=1.4, color=color, zorder=5)
        ax.add_patch(arrow)
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2 + 0.018
        ax.text(mid_x, mid_y, f"<<{rel_type}>>", fontsize=7.5, fontweight="bold",
                color=color, ha="center", va="center", bbox=dict(boxstyle="square,pad=0.1", fc="#ffffff", ec="none"), zorder=6)

    # UC3 includes UC4 (Biometrics -> BMI)
    draw_relationship((0.47, 0.65), (0.53, 0.65), "include", "include")
    # UC5 includes UC6 (Predict -> XAI)
    draw_relationship((0.47, 0.51), (0.53, 0.51), "include", "include")
    # UC5 includes UC7 (Predict -> Plan Matching)
    draw_relationship((0.37, 0.47), (0.37, 0.41), "include", "include")
    # UC9 extends UC5 (What-If extends Predict)
    draw_relationship((0.37, 0.27), (0.37, 0.47), "extend", "extend")
    # UC10 extends UC5 (Download PDF extends Predict)
    draw_relationship((0.63, 0.27), (0.47, 0.48), "extend", "extend")

    # Legend
    ax.add_patch(FancyBboxPatch((0.02, 0.04), 0.20, 0.16, boxstyle="round,pad=0.008", facecolor="#ffffff", edgecolor=BORDER_COLOR, linewidth=1, zorder=2))
    ax.text(0.03, 0.18, "Diagram Legend", fontsize=9, fontweight="bold", color=NAVY)
    ax.plot([0.035, 0.07], [0.15, 0.15], color=NAVY, linewidth=1.5)
    ax.text(0.08, 0.15, "Actor Association", fontsize=7.8, color=TEXT_DARK, va="center")
    ax.plot([0.035, 0.07], [0.12, 0.12], color="#0d9488", linewidth=1.5, linestyle="--")
    ax.text(0.08, 0.12, "<<include>> Mandatory Dependency", fontsize=7.8, color="#0d9488", va="center")
    ax.plot([0.035, 0.07], [0.09, 0.09], color="#7c3aed", linewidth=1.5, linestyle="--")
    ax.text(0.08, 0.09, "<<extend>> Optional Enhancement", fontsize=7.8, color="#7c3aed", va="center")
    ax.text(0.03, 0.06, "Scope: IEEE 830 Use Case Model", fontsize=7.5, fontstyle="italic", color=TEXT_MUTED)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "03_use_case_diagram.png"
    plt.savefig(out_path, dpi=300, facecolor="#ffffff", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {out_path}")


# =====================================================================
# PROGRAM 4: UML CLASS DIAGRAM
# =====================================================================
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_header(ax, "HEALTHSECURE: SMART HEALTH INSURANCE PREDICTION — UML CLASS DIAGRAM",
                "4", "Object Structure, Attributes, Methods and Relationships")

    def draw_class(x, y, w, h, class_name, stereotype, attributes, methods, header_color=DARK_BLUE):
        # Card Background
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                   facecolor="#ffffff", edgecolor="#334155", linewidth=1.6, zorder=2))
        # Header Box
        header_h = h * 0.18
        ax.add_patch(Rectangle((x, y + h - header_h), w, header_h,
                               facecolor=header_color, edgecolor="#334155", linewidth=1.6, zorder=3))
        ax.text(x + w/2, y + h - 0.015, f"<<{stereotype}>>", fontsize=7.5, fontstyle="italic",
                color="#bae6fd", ha="center", va="top", zorder=4)
        ax.text(x + w/2, y + h - 0.035, class_name, fontsize=10.5, fontweight="bold",
                color="#ffffff", ha="center", va="top", zorder=4)

        # Attributes Compartment
        attr_h = (h - header_h) * 0.50
        ax.add_patch(Rectangle((x, y + h - header_h - attr_h), w, attr_h,
                               facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=0.8, zorder=3))
        y_text = y + h - header_h - 0.015
        for attr in attributes:
            ax.text(x + 0.01, y_text, attr, fontsize=7.2, color=TEXT_DARK, va="top", fontfamily="monospace", zorder=4)
            y_text -= 0.018

        # Methods Compartment
        y_text = y + h - header_h - attr_h - 0.015
        for meth in methods:
            ax.text(x + 0.01, y_text, meth, fontsize=7.2, color=TEXT_DARK, va="top", fontfamily="monospace", zorder=4)
            y_text -= 0.018

    # 1. User Class
    draw_class(0.04, 0.52, 0.28, 0.35, "User", "Entity / ORM",
               ["- id: int [PK]",
                "- name: str",
                "- email: str [Unique]",
                "- password_hash: str",
                "- phone: str?",
                "- dob: date?",
                "- role: str = 'user' | 'admin'",
                "- created_at: datetime"],
               ["+ register(): User",
                "+ verify_password(pwd: str): bool",
                "+ update_profile(data: dict): bool",
                "+ change_password(new_pwd: str): bool"],
               header_color="#1e3a8a")

    # 2. Prediction Class
    draw_class(0.36, 0.44, 0.32, 0.43, "Prediction", "Entity / ORM",
               ["- id: int [PK]",
                "- user_id: int [FK -> users.id]",
                "- age: int, sex: str, region: str",
                "- height: float?, weight: float?",
                "- bmi: float, children: int",
                "- smoker: str, liquor: str",
                "- salary: float, policy_duration: int",
                "- plan_category: str",
                "- estimated_premium: float",
                "- recommended_plan_id: int [FK]",
                "- total_premium: float",
                "- estimated_benefit: float"],
               ["+ calculate_dynamic_bmi(): float",
                "+ compute_affordability_ratio(): float",
                "+ get_feature_dict(): dict",
                "+ to_dict(): dict"],
               header_color="#0e7490")

    # 3. InsurancePlan Class
    draw_class(0.72, 0.52, 0.25, 0.35, "InsurancePlan", "Entity / ORM",
               ["- plan_id: int [PK]",
                "- plan_name: str",
                "- annual_premium: float",
                "- coverage_amount: float",
                "- policy_duration: int",
                "- plan_description: text",
                "- benefits: text",
                "- status: str = 'active'"],
               ["+ calculate_diff(charge: float): float",
                "+ get_benefits_list(): list[str]",
                "+ evaluate_match_tier(): str"],
               header_color="#047857")

    # 4. Recommendation Class
    draw_class(0.36, 0.06, 0.32, 0.30, "Recommendation", "Entity / ORM",
               ["- id: int [PK]",
                "- prediction_id: int [FK -> prediction.id]",
                "- plan_name: str",
                "- policy_years: int",
                "- annual_premium: float",
                "- total_premium: float",
                "- estimated_benefit: float",
                "- benefit_factor: float = 1.20"],
               ["+ build_recommendation(prem, sal): dict",
                "+ format_summary(): str"],
               header_color="#b45309")

    # 5. MLModelEngine Class
    draw_class(0.04, 0.06, 0.28, 0.38, "MLModelEngine", "Core ML Service",
               ["+ FEATURES: list[str]",
                "+ FEATURE_RANGES: dict",
                "+ MODEL_PATH: Path",
                "- pipeline: Pipeline",
                "- regressor: LinearRegression | RF"],
               ["+ read_data(): DataFrame",
                "+ train_model(): Pipeline",
                "+ load_or_train_model(): Pipeline",
                "+ predict_premium(vals: dict): float",
                "+ feature_insights(k: int): list",
                "+ explain_prediction(vals, p): dict",
                "+ get_model_meta(): dict"],
               header_color="#6d28d9")

    # 6. ReportGenerator Class
    draw_class(0.72, 0.06, 0.25, 0.38, "ReportGenerator", "Utility / PDF",
               ["+ PRIMARY_NAVY: Color",
                "+ TEAL_MINT: Color",
                "+ PAGE_SIZE: A4",
                "- doc: SimpleDocTemplate",
                "- styles: StyleSheet"],
               ["+ generate_pdf_report(pred, user,",
                "   insights, expl, plans): BytesIO",
                "+ build_summary_table(): Table",
                "+ build_financial_breakdown(): Table",
                "+ render_disclaimer(): Paragraph"],
               header_color="#be123c")

    # Relationships & Multiplicity
    # User to Prediction (1 to 0..*)
    ax.plot([0.32, 0.36], [0.68, 0.68], color=NAVY, linewidth=2, zorder=5)
    ax.text(0.325, 0.69, "1", fontsize=9, fontweight="bold", color=NAVY)
    ax.text(0.345, 0.69, "0..*", fontsize=9, fontweight="bold", color=NAVY)
    ax.text(0.34, 0.655, "generates >", fontsize=7.5, fontstyle="italic", color=TEXT_MUTED)

    # Prediction to InsurancePlan (0..* to 0..1)
    ax.plot([0.68, 0.72], [0.68, 0.68], color=NAVY, linewidth=2, zorder=5)
    ax.text(0.685, 0.69, "0..*", fontsize=9, fontweight="bold", color=NAVY)
    ax.text(0.705, 0.69, "0..1", fontsize=9, fontweight="bold", color=NAVY)
    ax.text(0.685, 0.655, "matches >", fontsize=7.5, fontstyle="italic", color=TEXT_MUTED)

    # Prediction to Recommendation (Composition: filled diamond)
    ax.plot([0.52, 0.52], [0.44, 0.36], color=NAVY, linewidth=2, zorder=5)
    # Diamond at (0.52, 0.44)
    diamond = Polygon([[0.52, 0.44], [0.51, 0.425], [0.52, 0.41], [0.53, 0.425]],
                      closed=True, facecolor=NAVY, edgecolor=NAVY, zorder=6)
    ax.add_patch(diamond)
    ax.text(0.53, 0.42, "1", fontsize=9, fontweight="bold", color=NAVY)
    ax.text(0.53, 0.37, "1..*", fontsize=9, fontweight="bold", color=NAVY)
    ax.text(0.44, 0.39, "contains >", fontsize=7.5, fontstyle="italic", color=TEXT_MUTED)

    # Prediction depends on MLModelEngine (Dashed arrow)
    arrow_ml = FancyArrowPatch((0.36, 0.48), (0.32, 0.30), arrowstyle="-|>", mutation_scale=12,
                               linestyle="--", linewidth=1.5, color="#6d28d9", zorder=5)
    ax.add_patch(arrow_ml)
    ax.text(0.28, 0.42, "<<invokes>>", fontsize=7.5, fontweight="bold", color="#6d28d9")

    # Prediction depends on ReportGenerator (Dashed arrow)
    arrow_rep = FancyArrowPatch((0.68, 0.48), (0.72, 0.30), arrowstyle="-|>", mutation_scale=12,
                                linestyle="--", linewidth=1.5, color="#be123c", zorder=5)
    ax.add_patch(arrow_rep)
    ax.text(0.66, 0.42, "<<exports>>", fontsize=7.5, fontweight="bold", color="#be123c")

    plt.tight_layout()
    out_path = OUTPUT_DIR / "04_class_diagram.png"
    plt.savefig(out_path, dpi=300, facecolor="#ffffff", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {out_path}")


# =====================================================================
# PROGRAM 5: UML SEQUENCE DIAGRAM
# =====================================================================
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_header(ax, "HEALTHSECURE: SMART HEALTH INSURANCE PREDICTION — UML SEQUENCE DIAGRAM",
                "5", "Dynamic Behavioral Flow for Premium Prediction & Demo Plan Matching")

    # Lifelines
    lifelines = [
        ("Applicant / User", 0.08, "#1e3a8a"),
        ("Frontend View\n(predict.html)", 0.22, "#0369a1"),
        ("Flask Controller\n(app.py)", 0.38, "#0d9488"),
        ("Input Validator\n(parse_form)", 0.52, "#d97706"),
        ("Core ML Engine\n(model.py)", 0.66, "#7c3aed"),
        ("MySQL Database\n(SQLAlchemy)", 0.80, "#b45309"),
        ("XAI & PDF Service\n(ReportGenerator)", 0.93, "#be123c"),
    ]

    for name, x, col in lifelines:
        # Header box
        ax.add_patch(FancyBboxPatch((x - 0.055, 0.82), 0.11, 0.065, boxstyle="round,pad=0.005",
                                   facecolor=col, edgecolor="#0f172a", linewidth=1.4, zorder=3))
        ax.text(x, 0.852, name, fontsize=8.5, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)
        # Vertical Lifeline
        ax.plot([x, x], [0.82, 0.06], color="#94a3b8", linestyle="--", linewidth=1.2, zorder=1)

    # Helper to draw message arrow
    def draw_msg(y, x1, x2, label, msg_type="sync", step_num=""):
        line_color = NAVY
        style = "-|>" if msg_type == "sync" else "->"
        ls = "-" if msg_type in ["sync", "async"] else "--"
        arrow = FancyArrowPatch((x1, y), (x2, y), arrowstyle=style, mutation_scale=10,
                                linestyle=ls, linewidth=1.3, color=line_color, zorder=3)
        ax.add_patch(arrow)
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.012, f"{step_num}. {label}" if step_num else label,
                fontsize=7.8, fontweight="semibold", color=NAVY, ha="center", va="bottom", zorder=4)

    # Sequence Steps
    # 1. Fill Form
    draw_msg(0.77, 0.08, 0.22, "Fill Form: Age, Height, Weight, Smoker, Alcohol, State, Salary", "sync", "1")
    # 2. Submit POST
    draw_msg(0.72, 0.22, 0.38, "HTTP POST /predict (form_data)", "sync", "2")
    # 3. Validate
    draw_msg(0.67, 0.38, 0.52, "parse_form(request.form)", "sync", "3")
    # 4. BMI formula
    draw_msg(0.62, 0.52, 0.52, "Compute BMI: wt / (ht/100)^2", "async", "4")
    # 5. Return validated feature dict
    draw_msg(0.57, 0.52, 0.38, "Return sanitized feature_dict", "return", "5")
    # 6. Predict Premium
    draw_msg(0.52, 0.38, 0.66, "predict_premium(feature_dict)", "sync", "6")
    # 7. Model evaluation
    draw_msg(0.47, 0.66, 0.66, "RandomForest/LinearReg.predict(X)", "async", "7")
    # 8. Return predicted charge
    draw_msg(0.42, 0.66, 0.38, "Return predicted_charge (e.g. INR 14,392.29)", "return", "8")
    # 9. Query Demo Plans
    draw_msg(0.37, 0.38, 0.80, "SELECT * FROM insurance_plans WHERE status='active'", "sync", "9")
    # 10. Return plans & rank L1
    draw_msg(0.32, 0.80, 0.38, "Return active_plans -> Rank by ABS(plan - charge)", "return", "10")
    # 11. DB Transaction: Save Prediction & Recommendation
    draw_msg(0.27, 0.38, 0.80, "INSERT INTO prediction, recommendations; db.session.commit()", "sync", "11")
    # 12. Request XAI Explainability
    draw_msg(0.22, 0.38, 0.93, "explain_prediction(features, charge)", "sync", "12")
    # 13. Return XAI Breakdown
    draw_msg(0.17, 0.93, 0.38, "Return feature_importance & personalized clinical insights", "return", "13")
    # 14. Render Result Template
    draw_msg(0.12, 0.38, 0.22, "render_template('result.html', pred, xai, matched_plans)", "sync", "14")
    # 15. Display UI to User
    draw_msg(0.07, 0.22, 0.08, "HTTP 200 OK: Display Premium, 3 Matched Plans & XAI Dashboard", "return", "15")

    # Activation bars
    def draw_activation(x, y1, y2, color="#93c5fd"):
        ax.add_patch(Rectangle((x - 0.008, y2), 0.016, y1 - y2,
                               facecolor=color, edgecolor=NAVY, linewidth=1, zorder=2))

    draw_activation(0.08, 0.77, 0.07, "#bae6fd")
    draw_activation(0.22, 0.77, 0.07, "#93c5fd")
    draw_activation(0.38, 0.72, 0.12, "#5eead4")
    draw_activation(0.52, 0.67, 0.57, "#fde68a")
    draw_activation(0.66, 0.52, 0.42, "#c4b5fd")
    draw_activation(0.80, 0.37, 0.27, "#fed7aa")
    draw_activation(0.93, 0.22, 0.17, "#fecdd3")

    plt.tight_layout()
    out_path = OUTPUT_DIR / "05_sequence_diagram.png"
    plt.savefig(out_path, dpi=300, facecolor="#ffffff", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {out_path}")


# =====================================================================
# PROGRAM 6: SOFTWARE ARCHITECTURAL DESIGN
# =====================================================================
def generate_architectural_design():
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_header(ax, "HEALTHSECURE: SYSTEM ARCHITECTURAL DESIGN (3-TIER LAYERED & ML INTEGRATED)",
                "6", "Layered, Client-Server, and Machine Learning Micro-Architecture")

    # Helper for Architectural Layers
    def draw_layer_box(x, y, w, h, title, subtitle, bg_color, border_color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.015",
                                   facecolor=bg_color, edgecolor=border_color, linewidth=2, zorder=1))
        ax.text(x + 0.02, y + h - 0.025, title, fontsize=11, fontweight="bold", color=NAVY, va="top", zorder=2)
        ax.text(x + 0.02, y + h - 0.05, subtitle, fontsize=8, fontstyle="italic", color=TEXT_MUTED, va="top", zorder=2)

    def draw_module(x, y, w, h, name, desc, col=CARD_BG, ec=BORDER_COLOR):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                   facecolor=col, edgecolor=ec, linewidth=1.2, zorder=3))
        ax.text(x + w/2, y + h - 0.018, name, fontsize=8.5, fontweight="bold", color=NAVY, ha="center", va="top", zorder=4)
        ax.text(x + w/2, y + 0.015, desc, fontsize=7.2, color=TEXT_MUTED, ha="center", va="bottom", zorder=4)

    # Layer 1: Presentation Layer (Client Tier)
    draw_layer_box(0.04, 0.70, 0.92, 0.19, "1. PRESENTATION LAYER (CLIENT-SIDE USER INTERFACE)",
                   "Responsive Web Browser UI (HTML5, Modern CSS3 System, Vanilla JS, Dynamic Gauge, Chart.js)",
                   "#f0fdfa", "#0d9488")
    draw_module(0.06, 0.72, 0.20, 0.10, "Landing Page View", "index.html\nBrand Hero, CTA, Demo Grid")
    draw_module(0.28, 0.72, 0.20, 0.10, "Prediction Form View", "predict.html\nDynamic BMI, Multi-factor Input")
    draw_module(0.50, 0.72, 0.20, 0.10, "Result & XAI View", "result.html\nMatched Demo Plans, Risk Weights")
    draw_module(0.72, 0.72, 0.22, 0.10, "Scenario & Admin View", "what_if.html / admin_dashboard.html\nSimulations & System Analytics")

    # Layer 2: Application / Controller Layer (Flask Web Server Tier)
    draw_layer_box(0.04, 0.44, 0.92, 0.22, "2. APPLICATION & CONTROLLER LAYER (FLASK MVC CORE)",
                   "RESTful Routing, Session Authentication & RBAC Guard, Input Sanitization, Affordability Math",
                   "#f0f9ff", "#0284c7")
    draw_module(0.06, 0.46, 0.20, 0.13, "Auth & Security Guard", "login_required, admin_required\nWerkzeug scrypt Password Hash\nRole Verification (user/admin)")
    draw_module(0.28, 0.46, 0.20, 0.13, "Input Validation Engine", "parse_form()\nDynamic BMI calculation\nDomain & Range boundary checks")
    draw_module(0.50, 0.46, 0.20, 0.13, "Financial Logic Engine", "build_recommendation()\nAffordability Ratio (charge / income)\nTotal Premium & Benefit Math")
    draw_module(0.72, 0.46, 0.22, 0.13, "Plan Matching Algorithm", "get_matching_plans()\nNearest L1 Premium Distance\nMatch Badges: Very Close / Close")

    # Layer 3: Machine Learning Subsystem Tier
    draw_layer_box(0.04, 0.22, 0.44, 0.18, "3A. MACHINE LEARNING SUBSYSTEM",
                   "Actuarial Cost Regression & XAI Attribution",
                   "#faf5ff", "#7c3aed")
    draw_module(0.06, 0.24, 0.18, 0.10, "Inference Pipeline", "Scikit-Learn Pipeline\nColumnTransformer + OneHot\nRandomForest / LinearReg.")
    draw_module(0.26, 0.24, 0.20, 0.10, "Explainable AI (XAI)", "feature_insights(), explain_prediction()\nRelative Feature Weights %\nPersonalized Clinical Feedback")

    # Layer 4: Data Persistence Layer (Database Tier)
    draw_layer_box(0.52, 0.22, 0.44, 0.18, "3B. DATA PERSISTENCE LAYER (MYSQL 8.0)",
                   "Relational Schema, Transaction Safety & Pooling",
                   "#fffbeb", "#d97706")
    draw_module(0.54, 0.24, 0.18, 0.10, "SQLAlchemy ORM", "Connection Pooling (PyMySQL)\nURL-encoded credentials\nAutomated table migrations")
    draw_module(0.74, 0.24, 0.20, 0.10, "Relational Entities", "users, prediction,\ninsurance_plans, recommendations\nForeign Key Constraints & 3NF")

    # Layer 5: External Services & Reporting Engine
    draw_layer_box(0.04, 0.05, 0.92, 0.13, "4. EXPORT & UTILITY INFRASTRUCTURE",
                   "Document Compilation & Operating Environment",
                   "#fff1f2", "#e11d48")
    draw_module(0.06, 0.065, 0.26, 0.07, "ReportLab PDF Engine", "generate_pdf_report()\nA4 10-section Underwriting PDF")
    draw_module(0.35, 0.065, 0.28, 0.07, "Model Evaluator & Trainer", "train.py -> evaluation_metrics.json\nBenchmarked vs XGBoost, GBR, RF")
    draw_module(0.66, 0.065, 0.28, 0.07, "Runtime Environment", "Python 3.13 / Gunicorn / Windows OS\nStandard UTF-8 Data IO")

    # Connecting Arrows between Layers
    def draw_layer_arrow(x, y1, y2, label=""):
        arrow = FancyArrowPatch((x, y1), (x, y2), arrowstyle="<|-|>", mutation_scale=12,
                                linestyle="-", linewidth=1.8, color=NAVY, zorder=5)
        ax.add_patch(arrow)
        if label:
            ax.text(x + 0.015, (y1 + y2)/2, label, fontsize=8, fontweight="bold", color=NAVY, va="center")

    draw_layer_arrow(0.20, 0.70, 0.66, "HTTP / JSON")
    draw_layer_arrow(0.50, 0.70, 0.66, "Form Data")
    draw_layer_arrow(0.80, 0.70, 0.66, "User Action")

    draw_layer_arrow(0.26, 0.44, 0.40, "Python API")
    draw_layer_arrow(0.74, 0.44, 0.40, "SQL Queries")
    draw_layer_arrow(0.50, 0.22, 0.18, "Report Data")

    plt.tight_layout()
    out_path = OUTPUT_DIR / "06_architectural_design.png"
    plt.savefig(out_path, dpi=300, facecolor="#ffffff", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {out_path}")


# =====================================================================
# PROGRAM 7: UI/UX DESIGN & WIREFRAMES
# =====================================================================
def generate_ui_ux_wireframes():
    fig, ax = plt.subplots(figsize=(16, 11.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_header(ax, "HEALTHSECURE: UI/UX DESIGN & INTERFACE WIREFRAME SPECIFICATIONS",
                "7", "High-Fidelity Wireframes, Visual Hierarchy, and Screen Layouts")

    def draw_browser_frame(x, y, w, h, title):
        # Browser chrome
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.01",
                                   facecolor="#ffffff", edgecolor="#334155", linewidth=1.5, zorder=1))
        # Top titlebar
        bar_h = 0.035
        ax.add_patch(Rectangle((x, y + h - bar_h), w, bar_h,
                               facecolor="#0f172a", edgecolor="#334155", linewidth=1.5, zorder=2))
        # 3 browser dots
        ax.add_patch(Circle((x + 0.015, y + h - bar_h/2), 0.005, facecolor="#ef4444", zorder=3))
        ax.add_patch(Circle((x + 0.030, y + h - bar_h/2), 0.005, facecolor="#f59e0b", zorder=3))
        ax.add_patch(Circle((x + 0.045, y + h - bar_h/2), 0.005, facecolor="#10b981", zorder=3))
        # URL title
        ax.text(x + w/2, y + h - bar_h/2, title, fontsize=8, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=3)

    # 1. Wireframe 1: Landing Page
    draw_browser_frame(0.04, 0.48, 0.43, 0.40, "healthsecure.local/ — Landing Page & Live Demo Plans")
    # Navbar
    ax.add_patch(Rectangle((0.05, 0.81), 0.41, 0.025, facecolor="#0a2540", zorder=2))
    ax.text(0.06, 0.822, "HealthSecure AI", fontsize=8, fontweight="bold", color="#ffffff", va="center", zorder=3)
    ax.text(0.44, 0.822, "[Predict] [Plans] [Login] [Register]", fontsize=7, color="#38bdf8", ha="right", va="center", zorder=3)
    # Hero Box
    ax.add_patch(Rectangle((0.05, 0.69), 0.41, 0.105, facecolor="#f0fdfa", edgecolor="#0d9488", linewidth=1, zorder=2))
    ax.text(0.07, 0.77, "Smart Health Insurance Premium Prediction", fontsize=9, fontweight="bold", color=NAVY, zorder=3)
    ax.text(0.07, 0.74, "Explainable AI-driven underwriting estimates tailored to your health profile.", fontsize=7, color=TEXT_MUTED, zorder=3)
    ax.add_patch(FancyBboxPatch((0.07, 0.70), 0.14, 0.025, boxstyle="square,pad=0", facecolor="#0d9488", zorder=3))
    ax.text(0.14, 0.712, "Calculate Premium Now ->", fontsize=7.5, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)
    # Demo Plans row
    ax.text(0.06, 0.665, "Featured Demo Insurance Coverage Plans", fontsize=8, fontweight="bold", color=NAVY, zorder=3)
    for idx, (pname, pprem) in enumerate([("Starter Shield", "INR 11,999/yr"), ("Standard Care", "INR 27,999/yr"), ("Super Elite", "INR 62,000/yr")]):
        bx = 0.055 + idx * 0.135
        ax.add_patch(Rectangle((bx, 0.50), 0.125, 0.15, facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1, zorder=2))
        ax.text(bx + 0.01, 0.63, pname, fontsize=7.5, fontweight="bold", color=NAVY, zorder=3)
        ax.text(bx + 0.01, 0.60, pprem, fontsize=7.2, fontweight="semibold", color="#0284c7", zorder=3)
        ax.text(bx + 0.01, 0.54, "- Cashless Hospital\n- Zero Copay\n- 24/7 Support", fontsize=6.5, color=TEXT_MUTED, zorder=3)

    # 2. Wireframe 2: Premium Prediction Form
    draw_browser_frame(0.53, 0.48, 0.43, 0.40, "healthsecure.local/predict — Multi-Factor Calculator")
    ax.text(0.55, 0.825, "Personalized Premium Calculator (Dynamic BMI)", fontsize=9, fontweight="bold", color=NAVY, zorder=2)
    # Inputs Grid
    inputs = [
        ("Full Name", "Ganesh Kumar", 0.55, 0.77),
        ("Age (Years)", "28", 0.76, 0.77),
        ("Height (cm)", "175", 0.55, 0.71),
        ("Weight (kg)", "70", 0.76, 0.71),
        ("Auto-Calculated BMI", "22.86 (Healthy)", 0.55, 0.65),
        ("Dependents", "1 child", 0.76, 0.65),
        ("Smoking Status", "[No] / Yes", 0.55, 0.59),
        ("Alcohol Drinker", "[No] / Yes", 0.76, 0.59),
        ("Indian State", "Maharashtra", 0.55, 0.53),
        ("Annual Salary (INR)", "INR 7,50,000", 0.76, 0.53),
    ]
    for label, val, ix, iy in inputs:
        ax.text(ix, iy + 0.018, label, fontsize=6.8, fontweight="bold", color=TEXT_MUTED, zorder=3)
        ax.add_patch(Rectangle((ix, iy - 0.015), 0.18, 0.026, facecolor="#f8fafc", edgecolor="#94a3b8", linewidth=0.8, zorder=2))
        ax.text(ix + 0.01, iy - 0.002, val, fontsize=7, color=TEXT_DARK, zorder=3)

    # 3. Wireframe 3: Results & Matched Plans
    draw_browser_frame(0.04, 0.05, 0.43, 0.40, "healthsecure.local/result/1 — Prediction & XAI Results")
    ax.add_patch(Rectangle((0.05, 0.77 - 0.43), 0.41, 0.075, facecolor="#0a2540", zorder=2))
    ax.text(0.07, 0.40, "Estimated Actuarial Premium: INR 14,392.29 / Year", fontsize=9, fontweight="bold", color="#38bdf8", zorder=3)
    ax.text(0.07, 0.365, "Affordability Ratio: 1.92% of Annual Income (Optimal) | Policy Term: 10 Years", fontsize=7, color="#ffffff", zorder=3)
    # Matched demo plan
    ax.add_patch(Rectangle((0.05, 0.22), 0.41, 0.115, facecolor="#f0fdfa", edgecolor="#0d9488", linewidth=1.2, zorder=2))
    ax.text(0.065, 0.31, "Top Matched Demo Plan: HealthSecure Starter Shield", fontsize=8.5, fontweight="bold", color=NAVY, zorder=3)
    ax.add_patch(FancyBboxPatch((0.34, 0.305), 0.10, 0.022, boxstyle="square,pad=0", facecolor="#0d9488", zorder=3))
    ax.text(0.39, 0.316, "Very Close Match", fontsize=6.8, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)
    ax.text(0.065, 0.27, "Annual Premium: INR 11,999.00 | Difference: INR 2,393.29 (Within 5% bracket)", fontsize=7, color=TEXT_MUTED, zorder=3)
    ax.text(0.065, 0.24, "Coverage: INR 2.0 Lakhs | Inpatient & Outpatient | 24/7 Tele-health Support", fontsize=6.8, color=TEXT_DARK, zorder=3)
    # Action buttons
    ax.add_patch(FancyBboxPatch((0.05, 0.07), 0.19, 0.03, boxstyle="square,pad=0", facecolor="#0284c7", zorder=3))
    ax.text(0.145, 0.085, "Download PDF Report", fontsize=7.5, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)
    ax.add_patch(FancyBboxPatch((0.27, 0.07), 0.19, 0.03, boxstyle="square,pad=0", facecolor="#7c3aed", zorder=3))
    ax.text(0.365, 0.085, "Simulate Scenarios ->", fontsize=7.5, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)

    # 4. Wireframe 4: Scenario Simulator (What-If)
    draw_browser_frame(0.53, 0.05, 0.43, 0.40, "healthsecure.local/what-if — Scenario Simulator")
    ax.text(0.55, 0.40, "Scenario Simulator: Modify Inputs to Test Rate Impacts", fontsize=9, fontweight="bold", color=NAVY, zorder=2)
    # Comparison table box
    ax.add_patch(Rectangle((0.55, 0.17), 0.39, 0.20, facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1, zorder=2))
    ax.text(0.56, 0.34, "Parameter", fontsize=7.5, fontweight="bold", color=NAVY, zorder=3)
    ax.text(0.68, 0.34, "Baseline", fontsize=7.5, fontweight="bold", color=NAVY, zorder=3)
    ax.text(0.79, 0.34, "Simulated", fontsize=7.5, fontweight="bold", color=NAVY, zorder=3)
    ax.plot([0.55, 0.94], [0.325, 0.325], color="#94a3b8", linewidth=0.8, zorder=3)

    sim_rows = [
        ("Smoking Status", "Smoker (Yes)", "Non-Smoker (No)", "#16a34a"),
        ("BMI Metric", "31.2 (Obese)", "24.5 (Normal)", "#16a34a"),
        ("Alcohol Drinker", "Yes", "No", "#16a34a"),
        ("Annual Premium", "INR 32,500.00", "INR 14,850.00", "#16a34a"),
    ]
    for idx, (param, base, sim, col) in enumerate(sim_rows):
        ry = 0.29 - idx * 0.035
        ax.text(0.56, ry, param, fontsize=7, color=TEXT_DARK, zorder=3)
        ax.text(0.68, ry, base, fontsize=7, color=ROSE, zorder=3)
        ax.text(0.79, ry, sim, fontsize=7, fontweight="bold", color=col, zorder=3)

    ax.add_patch(Rectangle((0.55, 0.07), 0.39, 0.075, facecolor="#dcfce7", edgecolor="#16a34a", linewidth=1, zorder=2))
    ax.text(0.57, 0.12, "Projected Annual Savings: INR 17,650.00 (-54.3%)", fontsize=8.2, fontweight="bold", color="#15803d", zorder=3)
    ax.text(0.57, 0.09, "Actionable insight: Lifestyle risk reduction significantly lowers actuarial underwriting costs.", fontsize=6.8, color="#166534", zorder=3)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "07_ui_ux_wireframes.png"
    plt.savefig(out_path, dpi=300, facecolor="#ffffff", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {out_path}")


# =====================================================================
# PROGRAM 8: VERSION CONTROL & IMPLEMENTATION
# =====================================================================
def generate_git_version_control():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_header(ax, "HEALTHSECURE: IMPLEMENTATION USING VERSION CONTROL (GIT & GITHUB)",
                "8", "Modular Development, Git Architecture, Branching Model, and Audit Trail")

    # Section 1: Git 3-Stage Architecture (Top)
    ax.add_patch(FancyBboxPatch((0.04, 0.65), 0.92, 0.23, boxstyle="round,pad=0.01",
                               facecolor="#f8fafc", edgecolor="#0284c7", linewidth=1.8, zorder=1))
    ax.text(0.06, 0.85, "A. Distributed Git Architecture & State Progression", fontsize=11, fontweight="bold", color=NAVY, zorder=2)

    stages = [
        ("1. Working Directory", "D:\\Ganesh\\Health_Insurance_Premium_Prediction\nUntracked & Modified Source Files\n(app.py, model.py, templates)", 0.08, "#fee2e2", "#ef4444"),
        ("2. Staging Index (Cache)", "Index snapshot ready for commit\ngit add app.py model.py\nPrepared metadata tree", 0.39, "#fef3c7", "#f59e0b"),
        ("3. Local Repository (.git)", "Committed objects & commit SHAs\ngit commit -m 'feat: dynamic bmi'\nHEAD -> main branch", 0.70, "#dcfce7", "#10b981"),
    ]
    for title, desc, sx, bg, ec in stages:
        ax.add_patch(FancyBboxPatch((sx, 0.67), 0.22, 0.15, boxstyle="square,pad=0", facecolor=bg, edgecolor=ec, linewidth=1.5, zorder=2))
        ax.text(sx + 0.11, 0.79, title, fontsize=9, fontweight="bold", color=NAVY, ha="center", va="top", zorder=3)
        ax.text(sx + 0.11, 0.75, desc, fontsize=7.2, color=TEXT_DARK, ha="center", va="top", zorder=3)

    # Transition arrows
    arrow1 = FancyArrowPatch((0.30, 0.74), (0.39, 0.74), arrowstyle="-|>", mutation_scale=14, linewidth=2, color=NAVY, zorder=4)
    ax.add_patch(arrow1)
    ax.text(0.345, 0.76, "git add <files>", fontsize=8, fontweight="bold", color=NAVY, ha="center")

    arrow2 = FancyArrowPatch((0.61, 0.74), (0.70, 0.74), arrowstyle="-|>", mutation_scale=14, linewidth=2, color=NAVY, zorder=4)
    ax.add_patch(arrow2)
    ax.text(0.655, 0.76, "git commit -m", fontsize=8, fontweight="bold", color=NAVY, ha="center")

    # Section 2: Actual Repository Commit History (Directly from user's git log)
    ax.add_patch(FancyBboxPatch((0.04, 0.05), 0.92, 0.57, boxstyle="round,pad=0.01",
                               facecolor="#ffffff", edgecolor="#334155", linewidth=1.8, zorder=1))
    ax.text(0.06, 0.59, "B. Actual HealthSecure Git Commit Graph & Feature Lifecycle", fontsize=11, fontweight="bold", color=NAVY, zorder=2)

    commits = [
        ("0dee44c", "Initial commit: Core project architecture & basic dataset setup", "v0.1.0", 0.12, 0.44),
        ("eb20ba7", "Second commit: Scikit-learn regression models & Flask routing", "v0.5.0", 0.30, 0.44),
        ("a8e335d", "feat: complete HealthSecure platform with XAI, simulator & demo plan matching", "v1.0.0", 0.48, 0.44),
        ("058d179", "feat: add height/weight dynamic BMI calculation & liquor drinking feature", "v1.1.0", 0.66, 0.44),
        ("0212d31", "Enhance landing page light theme, single navbar, 12 demo plans, history buttons", "v1.2.0 (HEAD)", 0.84, 0.44),
    ]

    # Draw commit line
    ax.plot([0.12, 0.84], [0.44, 0.44], color="#0284c7", linewidth=3.5, zorder=2)

    for sha, msg, tag, cx, cy in commits:
        ax.add_patch(Circle((cx, cy), 0.022, facecolor="#0284c7", edgecolor=NAVY, linewidth=2, zorder=3))
        ax.text(cx, cy, "C", fontsize=9, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)
        # SHA badge
        ax.add_patch(FancyBboxPatch((cx - 0.038, cy + 0.035), 0.076, 0.028, boxstyle="round,pad=0.002",
                                   facecolor="#0f172a", edgecolor="none", zorder=3))
        ax.text(cx, cy + 0.049, sha, fontsize=8, fontweight="bold", color="#38bdf8", ha="center", va="center", zorder=4)
        # Release tag
        ax.text(cx, cy - 0.035, tag, fontsize=7.5, fontweight="bold", color="#16a34a", ha="center", va="top", zorder=3)
        # Message box
        ax.text(cx, cy - 0.065, msg, fontsize=7, color=TEXT_DARK, ha="center", va="top", wrap=True, zorder=3)

    # Section 3: Module Walkthrough Box (Bottom)
    ax.add_patch(Rectangle((0.06, 0.08), 0.88, 0.16, facecolor="#f1f5f9", edgecolor="#94a3b8", linewidth=1, zorder=2))
    ax.text(0.08, 0.21, "Version Control Workflow Example: Developing the Dynamic BMI Calculation Module",
            fontsize=9.5, fontweight="bold", color=NAVY, zorder=3)
    module_code = (
        "$ git checkout -b feature/dynamic-bmi-liquor              # Create isolated feature branch\n"
        "$ vim app.py model.py templates/predict.html             # Implement BMI = weight / (height/100)^2\n"
        "$ git status                                             # Verify 3 modified files in working directory\n"
        "$ git add app.py model.py templates/predict.html         # Stage modified units to index\n"
        "$ git commit -m 'feat: Add height/weight dynamic BMI'    # Commit SHA: 058d179 (clean atomic commit)\n"
        "$ git checkout main && git merge feature/dynamic-bmi     # Fast-forward merge into main production branch"
    )
    ax.text(0.08, 0.10, module_code, fontsize=7.5, color="#0f172a", fontfamily="monospace", va="bottom", zorder=3)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "08_git_version_control.png"
    plt.savefig(out_path, dpi=300, facecolor="#ffffff", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {out_path}")


# =====================================================================
# PROGRAM 9: SOFTWARE TESTING
# =====================================================================
def generate_software_testing():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_header(ax, "HEALTHSECURE: SOFTWARE TESTING SPECIFICATION & CONTROL FLOW",
                "9", "Black-Box Boundary Value Analysis & White-Box Basis Path Testing")

    # Left Side: White-Box Testing (Control Flow Graph CFG)
    ax.add_patch(FancyBboxPatch((0.04, 0.05), 0.44, 0.83, boxstyle="round,pad=0.01",
                               facecolor="#ffffff", edgecolor="#0284c7", linewidth=1.8, zorder=1))
    ax.text(0.06, 0.85, "A. White-Box Testing: Control Flow Graph (parse_form)", fontsize=10.5, fontweight="bold", color=NAVY, zorder=2)

    # CFG Nodes
    cfg_nodes = [
        (1, "1: Start parse_form()", 0.26, 0.78, "entry"),
        (2, "2: Read form inputs", 0.26, 0.70, "stmt"),
        (3, "3: height & weight provided?", 0.26, 0.61, "decision"),
        (4, "4: Validate 50<=ht<=250 & 20<=wt<=250", 0.14, 0.52, "stmt"),
        (5, "5: Compute bmi = wt/(ht/100)^2", 0.14, 0.43, "stmt"),
        (6, "6: Is explicit bmi in form?", 0.38, 0.52, "decision"),
        (7, "7: Raise ValueError(Missing BMI)", 0.38, 0.43, "error"),
        (8, "8: Validate Age, Salary, Smoker, State", 0.26, 0.33, "decision"),
        (9, "9: Raise ValidationError()", 0.38, 0.24, "error"),
        (10, "10: Return clean values dict", 0.14, 0.24, "exit"),
    ]

    for nid, label, nx, ny, ntype in cfg_nodes:
        if ntype == "decision":
            # Diamond
            ax.add_patch(Polygon([[nx, ny + 0.025], [nx + 0.08, ny], [nx, ny - 0.025], [nx - 0.08, ny]],
                                 closed=True, facecolor="#fef3c7", edgecolor="#d97706", linewidth=1.5, zorder=3))
        elif ntype == "error":
            ax.add_patch(Rectangle((nx - 0.07, ny - 0.02), 0.14, 0.04, facecolor="#fee2e2", edgecolor="#ef4444", linewidth=1.5, zorder=3))
        elif ntype == "exit":
            ax.add_patch(Rectangle((nx - 0.07, ny - 0.02), 0.14, 0.04, facecolor="#dcfce7", edgecolor="#10b981", linewidth=1.5, zorder=3))
        else:
            ax.add_patch(Rectangle((nx - 0.07, ny - 0.02), 0.14, 0.04, facecolor="#e0f2fe", edgecolor="#0284c7", linewidth=1.5, zorder=3))
        ax.text(nx, ny, f"Node {nid}", fontsize=7.5, fontweight="bold", color=NAVY, ha="center", va="center", zorder=4)

    # CFG Edges
    def draw_cfg_edge(p1, p2, label=""):
        arrow = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=10, linewidth=1.3, color=NAVY, zorder=2)
        ax.add_patch(arrow)
        if label:
            mid = ((p1[0] + p2[0])/2 + 0.015, (p1[1] + p2[1])/2)
            ax.text(mid[0], mid[1], label, fontsize=7, fontweight="bold", color="#b45309", zorder=4)

    draw_cfg_edge((0.26, 0.76), (0.26, 0.72))
    draw_cfg_edge((0.26, 0.68), (0.26, 0.635))
    draw_cfg_edge((0.20, 0.61), (0.14, 0.54), "True")
    draw_cfg_edge((0.32, 0.61), (0.38, 0.54), "False")
    draw_cfg_edge((0.14, 0.50), (0.14, 0.45))
    draw_cfg_edge((0.14, 0.41), (0.23, 0.345))
    draw_cfg_edge((0.34, 0.52), (0.26, 0.345), "True")
    draw_cfg_edge((0.38, 0.495), (0.38, 0.45), "False")
    draw_cfg_edge((0.23, 0.31), (0.14, 0.26), "Valid")
    draw_cfg_edge((0.30, 0.31), (0.38, 0.26), "Invalid")

    # Cyclomatic Complexity Box
    ax.add_patch(Rectangle((0.06, 0.07), 0.40, 0.11, facecolor="#f8fafc", edgecolor="#94a3b8", linewidth=1, zorder=2))
    cc_text = (
        "Cyclomatic Complexity Calculation:\n"
        "- Nodes (N) = 10, Edges (E) = 13, Predicates (P) = 3\n"
        "- V(G) = E - N + 2P = 13 - 10 + 2(1) = 5 Independent Paths\n"
        "Path 1: 1->2->3->4->5->8->10 (Valid height/weight)\n"
        "Path 2: 1->2->3->6->8->10 (Direct BMI passed)\n"
        "Path 3: 1->2->3->6->7 (Missing BMI Exception)"
    )
    ax.text(0.07, 0.08, cc_text, fontsize=7, color=TEXT_DARK, va="bottom", zorder=3)

    # Right Side: Black-Box Testing & Test Cases
    ax.add_patch(FancyBboxPatch((0.52, 0.05), 0.44, 0.83, boxstyle="round,pad=0.01",
                               facecolor="#ffffff", edgecolor="#0d9488", linewidth=1.8, zorder=1))
    ax.text(0.54, 0.85, "B. Black-Box Testing: Equivalence & Boundary Analysis", fontsize=10.5, fontweight="bold", color=NAVY, zorder=2)

    # BVA Table
    ax.text(0.54, 0.81, "1. Boundary Value Analysis (BVA) & Partitioning:", fontsize=8.5, fontweight="bold", color=NAVY, zorder=2)
    bva_headers = ["Field", "Valid Class", "Invalid Bounds", "Test Input", "Expected"]
    bva_rows = [
        ("Age", "18 <= age <= 100", "17 (Min-1), 101 (Max+1)", "18 / 101", "Accept / Error"),
        ("Height", "50 <= ht <= 250 cm", "49 cm, 251 cm", "175 / 30", "Accept / Error"),
        ("Weight", "20 <= wt <= 250 kg", "19 kg, 251 kg", "70 / 260", "Accept / Error"),
        ("BMI", "10 <= bmi <= 60", "9.9, 60.1", "22.86 / 8.5", "Accept / Error"),
        ("Salary", "INR 1L to 1 Crore", "< 1L, > 1 Crore", "7.5L / 50K", "Accept / Error"),
    ]

    ty = 0.77
    for col_idx, htext in enumerate(bva_headers):
        ax.text(0.54 + col_idx * 0.085, ty, htext, fontsize=7.2, fontweight="bold", color=NAVY, zorder=3)
    ax.plot([0.54, 0.94], [ty - 0.01, ty - 0.01], color="#0d9488", linewidth=1, zorder=3)

    for row in bva_rows:
        ty -= 0.032
        for col_idx, cell in enumerate(row):
            ax.text(0.54 + col_idx * 0.085, ty, cell, fontsize=6.8, color=TEXT_DARK, zorder=3)

    # Test Suite Results Table
    ax.text(0.54, 0.58, "2. Execution Test Suite (Automated Lab Verification):", fontsize=8.5, fontweight="bold", color=NAVY, zorder=2)
    test_cases = [
        ("TC01", "GET / & /health endpoints", "HTTP 200, status: ok", "PASS"),
        ("TC02", "User registration validation", "Account created in users table", "PASS"),
        ("TC03", "Admin authentication (Admin@123)", "Admin session & role verified", "PASS"),
        ("TC04", "Dynamic BMI calculation", "wt=70, ht=175 -> BMI=22.86", "PASS"),
        ("TC05", "ML Premium Inference", "Return INR 14,392.29", "PASS"),
        ("TC06", "Nearest Demo Plan Matching", "Matches Starter Shield (diff=2393)", "PASS"),
        ("TC07", "XAI Feature Importance", "Smoker weight > 65% identified", "PASS"),
        ("TC08", "What-If Simulator execution", "Calculates savings delta correctly", "PASS"),
        ("TC09", "PDF Report Generation", "A4 PDF buffer compiled (7.2 KB)", "PASS"),
        ("TC10", "SQL Injection / Escaping test", "Haris@128 password escaped", "PASS"),
    ]

    ty = 0.54
    ax.text(0.54, ty, "Test ID", fontsize=7.2, fontweight="bold", color=NAVY, zorder=3)
    ax.text(0.61, ty, "Test Description", fontsize=7.2, fontweight="bold", color=NAVY, zorder=3)
    ax.text(0.81, ty, "Observed Result", fontsize=7.2, fontweight="bold", color=NAVY, zorder=3)
    ax.text(0.91, ty, "Status", fontsize=7.2, fontweight="bold", color=NAVY, zorder=3)
    ax.plot([0.54, 0.94], [ty - 0.01, ty - 0.01], color="#0d9488", linewidth=1, zorder=3)

    for tid, tdesc, tobs, tstat in test_cases:
        ty -= 0.035
        ax.text(0.54, ty, tid, fontsize=6.8, fontweight="bold", color=TEXT_DARK, zorder=3)
        ax.text(0.61, ty, tdesc, fontsize=6.8, color=TEXT_DARK, zorder=3)
        ax.text(0.81, ty, tobs, fontsize=6.8, color=TEXT_MUTED, zorder=3)
        ax.text(0.91, ty, tstat, fontsize=7, fontweight="bold", color="#16a34a", zorder=3)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "09_software_testing.png"
    plt.savefig(out_path, dpi=300, facecolor="#ffffff", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {out_path}")


# =====================================================================
# PROGRAM 10: MINI PROJECT INTEGRATED SDLC LIFECYCLE
# =====================================================================
def generate_mini_project_lifecycle():
    fig, ax = plt.subplots(figsize=(16, 11.5), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_header(ax, "HEALTHSECURE: MINI PROJECT DOCUMENTATION & SDLC INTEGRATION",
                "10", "Integrated Software Engineering Lifecycle: SRS -> Design -> Coding -> Testing -> Report")

    # 5 Sequential Integrated Phases
    phases = [
        ("PHASE 1: REQUIREMENTS (SRS)",
         "IEEE 830 Specification\n"
         "- Problem Statement & Need Analysis\n"
         "- Functional Requirements (FR1-FR8)\n"
         "- Non-Functional: Security, Scalability\n"
         "- Hardware & Software Specifications",
         0.04, "#f0fdfa", "#0d9488"),

        ("PHASE 2: SYSTEM DESIGN",
         "UML Suite & Architecture\n"
         "- Use Case Diagram (Actors & Flows)\n"
         "- Class Diagram (ORM & Entities)\n"
         "- Sequence Diagram (Dynamic Interactions)\n"
         "- 3-Tier Layered MVC Architecture\n"
         "- 3NF MySQL Database Schema",
         0.23, "#f0f9ff", "#0284c7"),

        ("PHASE 3: MODULAR CODING",
         "Implementation & Version Control\n"
         "- Flask 3.1 & SQLAlchemy ORM\n"
         "- Scikit-Learn ML Pipeline\n"
         "- Dynamic BMI Formula Integration\n"
         "- Explainable AI (XAI) Attribution\n"
         "- Git Branching & Commit Audit Trail",
         0.42, "#faf5ff", "#7c3aed"),

        ("PHASE 4: TESTING & QA",
         "Verification & Validation\n"
         "- White-Box Testing (Cyclomatic V(G)=5)\n"
         "- Black-Box BVA & Equivalence Classes\n"
         "- Automated Unit & Integration Suite\n"
         "- 10/10 Test Cases Passed\n"
         "- Security: Credentials Escaping",
         0.61, "#fffbeb", "#d97706"),

        ("PHASE 5: DEPLOYMENT & REPORT",
         "Deliverables & Analytics\n"
         "- Model Benchmarking (MAE=2615 INR)\n"
         "- ReportLab A4 10-Section PDF Engine\n"
         "- Administrator Analytics Dashboard\n"
         "- User Manual & Record Submission\n"
         "- Production Ready on Port 5000",
         0.80, "#fdf2f8", "#db2777"),
    ]

    for title, desc, px, bg, ec in phases:
        # Phase card
        ax.add_patch(FancyBboxPatch((px, 0.44), 0.16, 0.42, boxstyle="round,pad=0.008,rounding_size=0.015",
                                   facecolor=bg, edgecolor=ec, linewidth=2, zorder=2))
        # Top banner of card
        ax.add_patch(Rectangle((px, 0.81), 0.16, 0.05, facecolor=ec, zorder=3))
        ax.text(px + 0.08, 0.835, title, fontsize=7.5, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=4)
        ax.text(px + 0.01, 0.78, desc, fontsize=6.8, color=TEXT_DARK, va="top", zorder=3)

    # Process Arrows connecting phases
    for idx in range(4):
        ax1 = 0.20 + idx * 0.19
        ax2 = 0.23 + idx * 0.19
        arrow = FancyArrowPatch((ax1, 0.65), (ax2, 0.65), arrowstyle="-|>", mutation_scale=14,
                                linewidth=2.5, color=NAVY, zorder=5)
        ax.add_patch(arrow)

    # Bottom Summary Matrix: Artifact Traceability & Outcomes
    ax.add_patch(FancyBboxPatch((0.04, 0.05), 0.92, 0.35, boxstyle="round,pad=0.01",
                               facecolor="#ffffff", edgecolor="#334155", linewidth=1.8, zorder=1))
    ax.text(0.06, 0.36, "Engineering Artifact Traceability Matrix & Project Metrics Summary",
            fontsize=11, fontweight="bold", color=NAVY, zorder=2)

    headers = ["SDLC Phase", "Primary Deliverable Artifact", "Tools / Technologies Used", "Verified Project Outcome"]
    matrix = [
        ("Phase 1: SRS", "SRS Document (IEEE 830 format)", "Markdown, IEEE 830 Standard", "Complete functional definition of 8 core system requirements"),
        ("Phase 2: Design", "UML Diagrams & 3-Tier Layered Architecture", "Matplotlib, PlantUML, MySQL Workbench", "5 validated diagrams: Use Case, Class, Sequence, Architecture, UI"),
        ("Phase 3: Coding", "Modular Flask Backend & ML Engine", "Python 3.13, Flask 3.1, Scikit-Learn, Git", "1,423 LOC app.py, dynamic BMI, 12 demo plans, quote_plus security"),
        ("Phase 4: Testing", "Test Suite Report & CFG Path Analysis", "Pytest, Python unittest, Coverage", "10/10 test cases passed; Cyclomatic complexity V(G)=5 verified"),
        ("Phase 5: Report", "Publication-Grade PDF Underwriting Report", "ReportLab 5.1, Chart.js, Joblib", "Automated A4 PDF generation with XAI explanations & plan matching"),
    ]

    ty = 0.32
    for cidx, h in enumerate(headers):
        x_pos = 0.06 + (0.16 if cidx == 0 else 0.24 if cidx == 1 else 0.26 if cidx == 2 else 0.28) * cidx
        # Let's fix exact x positions:
        x_positions = [0.06, 0.22, 0.48, 0.74]
        ax.text(x_positions[cidx], ty, h, fontsize=8, fontweight="bold", color=NAVY, zorder=3)
    ax.plot([0.06, 0.94], [ty - 0.01, ty - 0.01], color=NAVY, linewidth=1.2, zorder=3)

    for row in matrix:
        ty -= 0.045
        for cidx, val in enumerate(row):
            x_positions = [0.06, 0.22, 0.48, 0.74]
            ax.text(x_positions[cidx], ty, val, fontsize=7.2,
                    fontweight="bold" if cidx == 0 else "normal", color=NAVY if cidx == 0 else TEXT_DARK, zorder=3)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "10_mini_project_lifecycle.png"
    plt.savefig(out_path, dpi=300, facecolor="#ffffff", bbox_inches="tight")
    plt.close(fig)
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    print("Generating 8 publication-grade Software Engineering Lab diagrams...")
    generate_use_case_diagram()
    generate_class_diagram()
    generate_sequence_diagram()
    generate_architectural_design()
    generate_ui_ux_wireframes()
    generate_git_version_control()
    generate_software_testing()
    generate_mini_project_lifecycle()
    print("All 8 diagrams generated successfully in:", OUTPUT_DIR)
