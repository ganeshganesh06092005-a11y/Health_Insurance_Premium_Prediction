from __future__ import annotations

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_pdf_report(
    prediction,
    user,
    insights: list[dict],
    explanation: dict | None = None,
    matching_plans: list[dict] | None = None,
) -> io.BytesIO:
    """Generate a publication-grade, professional PDF prediction report for HealthSecure.
    
    Contains all 10 required sections plus Automatic Demo Plan Matching:
    1. User Information
    2. Health Information
    3. Financial Information
    4. ML Prediction
    5. Recommended Plan & Automatic Demo Plan Matching
    6. Premium Calculation
    7. Estimated Benefit
    8. AI Prediction Insights
    9. Prediction Date
    10. Disclaimer
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=28,
        bottomMargin=28,
        title=f"HealthSecure Report - #{prediction.id}",
        author="HealthSecure AI System",
    )

    PRIMARY_NAVY = colors.HexColor("#153b59")
    TEAL_MINT = colors.HexColor("#0d9b88")
    TEXT_INK = colors.HexColor("#17324d")
    MUTED_GREY = colors.HexColor("#6d8193")
    BG_LIGHT = colors.HexColor("#f4f8f9")
    BG_CARD = colors.HexColor("#ffffff")
    BORDER_LINE = colors.HexColor("#dce7ec")
    ALERT_BG = colors.HexColor("#fef7e7")
    ALERT_BORDER = colors.HexColor("#e5a63b")

    base_styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=base_styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=PRIMARY_NAVY,
        spaceAfter=2,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=base_styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        textColor=TEAL_MINT,
        textTransform="uppercase",
        letterSpacing=1.2,
        spaceAfter=6,
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=base_styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=PRIMARY_NAVY,
        spaceBefore=6,
        spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=base_styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=TEXT_INK,
    )
    body_bold = ParagraphStyle("BodyBold", parent=body_style, fontName="Helvetica-Bold")
    muted_style = ParagraphStyle(
        "BodyMuted",
        parent=base_styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10.5,
        textColor=MUTED_GREY,
    )
    stat_val_style = ParagraphStyle(
        "StatVal",
        parent=base_styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=PRIMARY_NAVY,
    )
    stat_lbl_style = ParagraphStyle(
        "StatLbl",
        parent=base_styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=8.5,
        textColor=MUTED_GREY,
        textTransform="uppercase",
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=base_styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=11,
        textColor=colors.HexColor("#5c4813"),
    )

    story = []

    # 1. HEADER BANNER
    header_data = [
        [
            Paragraph("HealthSecure", title_style),
            Paragraph(
                f"<b>REPORT ID:</b> HS-{prediction.id:05d}<br/><b>DATE:</b> {prediction.created_at.strftime('%d %B %Y')}",
                ParagraphStyle("MetaR", parent=body_style, alignment=2),
            ),
        ],
        [
            Paragraph("Smart Insurance Prediction &amp; AI Risk Assessment Report", subtitle_style),
            Paragraph("<b>STATUS:</b> Evaluated &amp; Verified", ParagraphStyle("MetaR2", parent=muted_style, alignment=2)),
        ],
    ]
    header_table = Table(header_data, colWidths=[340, 183])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=1.5, color=TEAL_MINT, spaceAfter=6, spaceBefore=2))

    # TOP KPI CARDS
    kpi_data = [
        [
            Paragraph("Estimated Annual Premium", stat_lbl_style),
            Paragraph("Recommended Plan", stat_lbl_style),
            Paragraph("Policy Duration", stat_lbl_style),
            Paragraph("Estimated Total Benefit", stat_lbl_style),
        ],
        [
            Paragraph(f"INR {prediction.estimated_premium:,.2f}", stat_val_style),
            Paragraph(f"{prediction.plan_category.title()}", stat_val_style),
            Paragraph(f"{prediction.policy_duration} Years", stat_val_style),
            Paragraph(f"INR {prediction.estimated_benefit:,.2f}", stat_val_style),
        ],
    ]
    kpi_table = Table(kpi_data, colWidths=[130, 130, 130, 133])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 6))

    # SECTION 1 & 2: USER & HEALTH INFORMATION
    story.append(Paragraph("1. User Information &amp; 2. Health Profile", section_heading))
    user_email = user.email if user else "member@healthsecure.local"
    user_name = prediction.full_name or (user.name if user else "Applicant")

    height_weight_str = (
        f"{prediction.height:.0f} cm / {prediction.weight:.1f} kg"
        if (getattr(prediction, "height", None) and getattr(prediction, "weight", None))
        else "N/A"
    )
    liquor_status_str = (
        "Yes (Drinker)"
        if getattr(prediction, "liquor", "no") == "yes"
        else "No (Non-drinker)"
    )

    profile_data = [
        [
            Paragraph("<b>Full Name:</b>", body_style),
            Paragraph(user_name, body_style),
            Paragraph("<b>Body Mass Index (BMI):</b>", body_style),
            Paragraph(f"{prediction.bmi:.2f}", body_style),
        ],
        [
            Paragraph("<b>Account Email:</b>", body_style),
            Paragraph(user_email, body_style),
            Paragraph("<b>Height / Weight:</b>", body_style),
            Paragraph(height_weight_str, body_style),
        ],
        [
            Paragraph("<b>Age:</b>", body_style),
            Paragraph(f"{prediction.age} years", body_style),
            Paragraph("<b>Smoking Status:</b>", body_style),
            Paragraph(f"{prediction.smoker.title()}", body_style),
        ],
        [
            Paragraph("<b>Gender:</b>", body_style),
            Paragraph(f"{prediction.sex.title()}", body_style),
            Paragraph("<b>Liquor / Alcohol:</b>", body_style),
            Paragraph(liquor_status_str, body_style),
        ],
        [
            Paragraph("<b>Number of Children:</b>", body_style),
            Paragraph(f"{prediction.children} dependent(s)", body_style),
            Paragraph("<b>Geographic Region:</b>", body_style),
            Paragraph(f"{prediction.region.title()}", body_style),
        ],
    ]
    profile_table = Table(profile_data, colWidths=[110, 150, 130, 133])
    profile_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CARD),
        ("BOX", (0, 0), (-1, -1), 0.75, BORDER_LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#edf2f5")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 6))

    # SECTION 3, 4, 5, 6, 7: FINANCIAL, PREDICTION & BENEFIT
    story.append(Paragraph("3. Financial Analysis, 4. ML Prediction &amp; 5–7. Policy Calculation", section_heading))
    calc_data = [
        [
            Paragraph("<b>Financial &amp; Coverage Metric</b>", body_bold),
            Paragraph("<b>Calculated Value</b>", body_bold),
            Paragraph("<b>Actuarial / Financial Explanation</b>", body_bold),
        ],
        [
            Paragraph("Annual Stated Salary", body_style),
            Paragraph(f"INR {prediction.salary:,.2f}", body_style),
            Paragraph("Declared applicant income used for affordability benchmarking.", muted_style),
        ],
        [
            Paragraph("Estimated Annual Premium", body_bold),
            Paragraph(f"<b>INR {prediction.estimated_premium:,.2f}</b>", ParagraphStyle("PriceH", parent=body_bold, textColor=PRIMARY_NAVY)),
            Paragraph("Machine Learning regression model predicted annual medical expenditure.", muted_style),
        ],
        [
            Paragraph("Premium-to-Income Ratio", body_style),
            Paragraph(f"{prediction.premium_income_ratio:.2f}%", body_style),
            Paragraph("Proportion of income allocated toward insurance. Sustainable target < 10%.", muted_style),
        ],
        [
            Paragraph("Selected Coverage Plan", body_style),
            Paragraph(f"{prediction.plan_category.title()} Plan", body_style),
            Paragraph(prediction.recommendation or "Recommended coverage based on profile indicators.", muted_style),
        ],
        [
            Paragraph("Policy Duration", body_style),
            Paragraph(f"{prediction.policy_duration} Years", body_style),
            Paragraph("Multi-year commitment term chosen for health protection.", muted_style),
        ],
        [
            Paragraph("Total Estimated Premium", body_style),
            Paragraph(f"INR {prediction.total_premium:,.2f}", body_style),
            Paragraph("Cumulative annual premium over the chosen policy duration.", muted_style),
        ],
        [
            Paragraph("Benefit Factor Rate", body_style),
            Paragraph(f"{prediction.benefit_factor:.2f}x", body_style),
            Paragraph("Project-defined multiplier representing maturity & protective value.", muted_style),
        ],
        [
            Paragraph("Estimated Benefit Amount", body_bold),
            Paragraph(f"<b>INR {prediction.estimated_benefit:,.2f}</b>", ParagraphStyle("BenH", parent=body_bold, textColor=TEAL_MINT)),
            Paragraph("Total projected benefit (Total Premium × Benefit Factor).", muted_style),
        ],
    ]
    calc_table = Table(calc_data, colWidths=[150, 120, 253])
    calc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.75, BORDER_LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#edf2f5")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(calc_table)
    story.append(Spacer(1, 6))

    # AUTOMATIC DEMO INSURANCE PLANS MATCHING SECTION
    if matching_plans:
        story.append(Paragraph("Recommended Demo Insurance Plans (Automatic Matching)", section_heading))
        story.append(Paragraph(
            "The system automatically searched the available demo plans in the MySQL database and matched "
            "plans whose annual premium is closest to your ML predicted premium (sorted by smallest absolute difference):",
            body_style,
        ))
        story.append(Spacer(1, 3))

        plan_table_data = [
            [
                Paragraph("<b>Demo Plan Name</b>", body_bold),
                Paragraph("<b>Annual Premium</b>", body_bold),
                Paragraph("<b>Coverage Amount</b>", body_bold),
                Paragraph("<b>Difference</b>", body_bold),
                Paragraph("<b>Match Evaluation</b>", body_bold),
            ]
        ]
        for p in matching_plans:
            closest_star = " ★" if p.get("is_closest") else ""
            plan_table_data.append([
                Paragraph(f"<b>{p['plan_name']}{closest_star}</b>", body_style),
                Paragraph(f"INR {p['annual_premium']:,.2f}", body_style),
                Paragraph(p.get("coverage_display", f"INR {p['coverage_amount']:,.0f}"), body_style),
                Paragraph(f"INR {p['difference']:,.2f}", body_style),
                Paragraph(f"<b>{p['match_label']}</b>", ParagraphStyle("MatchTag", parent=body_style, textColor=TEAL_MINT if p.get("is_closest") else PRIMARY_NAVY)),
            ])

        plans_table = Table(plan_table_data, colWidths=[140, 100, 100, 83, 100])
        plans_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BG_LIGHT),
            ("BOX", (0, 0), (-1, -1), 0.75, BORDER_LINE),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#edf2f5")),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(plans_table)
        story.append(Spacer(1, 6))

    # SECTION 8: EXPLAINABLE AI (XAI) INSIGHTS
    story.append(Paragraph("8. AI Prediction Insights (Explainable AI)", section_heading))
    story.append(Paragraph(
        "<b>Model Interpretability:</b> The chart below shows the relative feature importances computed by the "
        "trained tree-based regression model, illustrating each factor's mathematical weight in predicting medical costs.",
        body_style,
    ))
    story.append(Spacer(1, 3))

    bar_rows = [
        [
            Paragraph("<b>Influencing Feature</b>", body_bold),
            Paragraph("<b>Model Importance</b>", body_bold),
            Paragraph("<b>Relative Contribution Bar</b>", body_bold),
        ]
    ]

    max_imp = max((item["importance"] for item in insights), default=100) or 100
    for item in insights:
        pct = item["importance"]
        bar_len = int((pct / max_imp) * 22)
        bar_str = "█" * max(1, bar_len)
        bar_rows.append([
            Paragraph(item["name"], body_style),
            Paragraph(f"{pct:.1f}%", body_bold),
            Paragraph(f"<font color='#0d9b88'>{bar_str}</font>", body_style),
        ])

    bars_table = Table(bar_rows, colWidths=[150, 110, 263])
    bars_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.75, BORDER_LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#edf2f5")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(bars_table)
    story.append(Spacer(1, 3))

    simple_expl = (
        explanation.get("simple_explanation") if explanation else
        "Smoking status had relatively high feature importance in this model. Inputs like smoking status, BMI, and age form the primary drivers of predicted premiums."
    )
    story.append(Paragraph(f"<b>Key Takeaway:</b> {simple_expl}", body_style))
    story.append(Paragraph(
        "<i>Note: Model feature importance reflects mathematical correlation in historical data and does not prove direct medical causation.</i>",
        muted_style,
    ))
    story.append(Spacer(1, 5))

    # SECTION 9 & 10: METADATA & DISCLAIMER
    meta_text = (
        f"<b>9. Prediction Verification &amp; Timestamp:</b> Generated on {prediction.created_at.strftime('%d %B %Y at %H:%M:%S UTC')} "
        f"| Database Record ID: #{prediction.id} | Engine: HealthSecure Production Regressor."
    )
    story.append(Paragraph(meta_text, muted_style))
    story.append(Spacer(1, 4))

    disclaimer_box = [
        [
            Paragraph(
                "<b>10. IMPORTANT DISCLAIMER:</b><br/>"
                "These are project-defined sample insurance plans created for academic demonstration. "
                "They are not real insurance products, official insurer quotes, or financial recommendations. "
                "Premium matching is based only on the project's defined matching logic and should not be interpreted "
                "as an official insurance eligibility or pricing rule.",
                disclaimer_style,
            )
        ]
    ]
    disclaimer_table = Table(disclaimer_box, colWidths=[523])
    disclaimer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ALERT_BG),
        ("BOX", (0, 0), (-1, -1), 1, ALERT_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(disclaimer_table)

    doc.build(story)
    buffer.seek(0)
    return buffer
