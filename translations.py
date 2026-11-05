"""HealthSecure Multi-Language Translation System.

Supports:
- en: English (default)
- ta: Tamil (தமிழ்)
- hi: Hindi (हिन्दी)
"""

from __future__ import annotations
from typing import Any

TRANSLATIONS: dict[str, dict[str, str]] = {
    # -------------------------------------------------------------------------
    # Global & Navigation
    # -------------------------------------------------------------------------
    "nav_brand": {
        "en": "HealthSecure",
        "ta": "ஹெல்த்செக்யூர்",
        "hi": "हेल्थसिक्योर",
    },
    "nav_tagline": {
        "en": "Smart Insurance Prediction",
        "ta": "ஸ்மார்ட் காப்பீட்டுக் கணிப்பு",
        "hi": "स्मार्ट बीमा पूर्वानुमान",
    },
    "nav_home": {
        "en": "Home",
        "ta": "முகப்பு",
        "hi": "होम",
    },
    "nav_dashboard": {
        "en": "Dashboard",
        "ta": "முகப்புப் பலகை",
        "hi": "डैशबोर्ड",
    },
    "nav_predict": {
        "en": "Calculate Premium",
        "ta": "பிரீமியம் கணக்கிடு",
        "hi": "प्रीमियम गणना",
    },
    "nav_history": {
        "en": "History",
        "ta": "வரலாறு",
        "hi": "इतिहास",
    },
    "nav_whatif": {
        "en": "What-If Simulator",
        "ta": "வாட்-இஃப் சிமுலேட்டர்",
        "hi": "व्हॉट-इफ सिम्युलेटर",
    },
    "nav_plans": {
        "en": "Insurance Plans",
        "ta": "காப்பீட்டுத் திட்டங்கள்",
        "hi": "बीमा योजनाएं",
    },
    "nav_favorites": {
        "en": "Favorite Plans",
        "ta": "விருப்பத் திட்டங்கள்",
        "hi": "पसंदीदा योजनाएं",
    },
    "nav_profile": {
        "en": "Profile",
        "ta": "சுயவிவரம்",
        "hi": "प्रोफाइल",
    },
    "nav_notifications": {
        "en": "Notifications",
        "ta": "அறிவிப்புகள்",
        "hi": "सूचनाएं",
    },
    "nav_admin_portal": {
        "en": "Admin Portal",
        "ta": "நிர்வாகி தளம்",
        "hi": "एडमिन पोर्टल",
    },
    "nav_login": {
        "en": "Log in",
        "ta": "உள்நுழைக",
        "hi": "लॉग इन",
    },
    "nav_register": {
        "en": "Create Account",
        "ta": "கணக்கை உருவாக்குக",
        "hi": "खाता बनाएं",
    },
    "nav_logout": {
        "en": "Log out",
        "ta": "வெளியேறுக",
        "hi": "लॉग आउट",
    },
    "nav_back_home": {
        "en": "Back to Home",
        "ta": "முகப்புக்குத் திரும்பு",
        "hi": "होम पर वापस जाएं",
    },

    # -------------------------------------------------------------------------
    # Theme & Language
    # -------------------------------------------------------------------------
    "theme_toggle": {
        "en": "Toggle Dark/Light Mode",
        "ta": "இருண்ட/ஒளி பயன்முறை",
        "hi": "डार्क/लाइट मोड टॉगल करें",
    },
    "theme_light": {
        "en": "Light Mode",
        "ta": "ஒளி பயன்முறை",
        "hi": "लाइट मोड",
    },
    "theme_dark": {
        "en": "Dark Mode",
        "ta": "இருண்ட பயன்முறை",
        "hi": "डार्क मोड",
    },
    "lang_select": {
        "en": "Language",
        "ta": "மொழி",
        "hi": "भाषा",
    },

    # -------------------------------------------------------------------------
    # Common Actions & Buttons
    # -------------------------------------------------------------------------
    "btn_submit": {
        "en": "Submit",
        "ta": "சமர்ப்பிக்கவும்",
        "hi": "जमा करें",
    },
    "btn_calculate": {
        "en": "Calculate Premium Now",
        "ta": "இப்போதே பிரீமியம் கணக்கிடு",
        "hi": "अब प्रीमियम की गणना करें",
    },
    "btn_reset": {
        "en": "Reset",
        "ta": "மீட்டமை",
        "hi": "रीसेट करें",
    },
    "btn_compare": {
        "en": "Compare Plans",
        "ta": "திட்டங்களை ஒப்பிடுக",
        "hi": "योजनाओं की तुलना करें",
    },
    "btn_details": {
        "en": "Inspect Details",
        "ta": "விவரங்களைப் பார்க்க",
        "hi": "विवरण देखें",
    },
    "btn_download_pdf": {
        "en": "Download Official PDF Report",
        "ta": "அதிகாரப்பூர்வ PDF பதிவிறக்கு",
        "hi": "आधिकारिक PDF डाउनलोड करें",
    },
    "btn_email_report": {
        "en": "Send Report to Email",
        "ta": "மின்னஞ்சலுக்கு அறிக்கையை அனுப்புக",
        "hi": "ईमेल पर रिपोर्ट भेजें",
    },
    "btn_email_sending": {
        "en": "Sending Email...",
        "ta": "மின்னஞ்சல் அனுப்பப்படுகிறது...",
        "hi": "ईमेल भेजा जा रहा है...",
    },
    "btn_add_favorite": {
        "en": "Save to Favorites",
        "ta": "விருப்பங்களில் சேமி",
        "hi": "पसंदीदा में सहेजें",
    },
    "btn_remove_favorite": {
        "en": "Remove from Favorites",
        "ta": "விருப்பங்களிலிருந்து நீக்கு",
        "hi": "पसंदीदा से हटाएं",
    },
    "btn_mark_read": {
        "en": "Mark as Read",
        "ta": "படித்ததாகக் குறி",
        "hi": "पढ़ा हुआ चिह्नित करें",
    },
    "btn_mark_all_read": {
        "en": "Mark All as Read",
        "ta": "அனைத்தையும் படித்ததாகக் குறி",
        "hi": "सभी को पढ़ा हुआ चिह्नित करें",
    },
    "btn_delete": {
        "en": "Delete",
        "ta": "நீக்குக",
        "hi": "हटाएं",
    },
    "btn_clear_all": {
        "en": "Clear All",
        "ta": "அனைத்தையும் அழிக்க",
        "hi": "सभी साफ़ करें",
    },
    "btn_explore_plans": {
        "en": "Explore 100+ Plans",
        "ta": "100+ திட்டங்களை ஆராய்க",
        "hi": "100+ योजनाएं देखें",
    },
    "btn_whatif_simulator": {
        "en": "Run What-If Simulator",
        "ta": "வாட்-இஃப் சிமுலேட்டரை இயக்கு",
        "hi": "व्हॉट-इफ सिम्युलेटर चलाएं",
    },

    # -------------------------------------------------------------------------
    # Form Labels (Predict / Input)
    # -------------------------------------------------------------------------
    "form_applicant_profile": {
        "en": "Applicant Profile",
        "ta": "விண்ணப்பதாரர் சுயவிவரம்",
        "hi": "आवेदक प्रोफाइल",
    },
    "form_full_name": {
        "en": "Full Name",
        "ta": "முழுப் பெயர்",
        "hi": "पूरा नाम",
    },
    "form_age": {
        "en": "Age",
        "ta": "வயது",
        "hi": "आयु",
    },
    "form_gender": {
        "en": "Gender",
        "ta": "பாலினம்",
        "hi": "लिंग",
    },
    "gender_male": {
        "en": "Male",
        "ta": "ஆண்",
        "hi": "पुरुष",
    },
    "gender_female": {
        "en": "Female",
        "ta": "பெண்",
        "hi": "महिला",
    },
    "form_height": {
        "en": "Height (cm)",
        "ta": "உயரம் (செ.மீ)",
        "hi": "ऊंचाई (सेमी)",
    },
    "form_weight": {
        "en": "Weight (kg)",
        "ta": "எடை (கிலோ)",
        "hi": "वजन (किग्रा)",
    },
    "form_bmi": {
        "en": "Body Mass Index (BMI)",
        "ta": "உடல் நிறை குறியீடு (BMI)",
        "hi": "बॉडी मास इंडेक्स (BMI)",
    },
    "form_children": {
        "en": "Dependent Children",
        "ta": "சார்ந்திருக்கும் குழந்தைகள்",
        "hi": "आश्रित बच्चे",
    },
    "form_smoker": {
        "en": "Tobacco / Smoking Habit",
        "ta": "புகைபிடிக்கும் பழக்கம்",
        "hi": "धूम्रपान की आदत",
    },
    "form_liquor": {
        "en": "Alcohol Consumption",
        "ta": "மது அருந்தும் பழக்கம்",
        "hi": "शराब का सेवन",
    },
    "form_region": {
        "en": "Residential Region",
        "ta": "குடியிருப்பு மண்டலம்",
        "hi": "आवासीय क्षेत्र",
    },
    "form_salary": {
        "en": "Annual Gross Income (INR)",
        "ta": "ஆண்டு மொத்த வருமானம் (ரூ)",
        "hi": "वार्षिक कुल आय (INR)",
    },
    "form_policy_duration": {
        "en": "Policy Duration",
        "ta": "பாலிசி காலம்",
        "hi": "पॉलिसी अवधि",
    },
    "form_plan_category": {
        "en": "Plan Coverage Tier",
        "ta": "திட்ட அடுக்கு",
        "hi": "योजना श्रेणी",
    },
    "opt_yes": {
        "en": "Yes",
        "ta": "ஆம்",
        "hi": "हाँ",
    },
    "opt_no": {
        "en": "No",
        "ta": "இல்லை",
        "hi": "नहीं",
    },

    # -------------------------------------------------------------------------
    # Results & Metrics
    # -------------------------------------------------------------------------
    "res_predicted_premium": {
        "en": "Estimated Annual Premium",
        "ta": "மதிப்பிடப்பட்ட ஆண்டு பிரீமியம்",
        "hi": "अनुमानित वार्षिक प्रीमियम",
    },
    "res_per_year": {
        "en": "/ year",
        "ta": "/ ஆண்டு",
        "hi": "/ वर्ष",
    },
    "res_affordability": {
        "en": "Premium-to-Income Ratio",
        "ta": "வருமானத்திற்கான பிரீமியம் விகிதம்",
        "hi": "प्रीमियम-से-आय अनुपात",
    },
    "res_sum_insured": {
        "en": "Sum Insured",
        "ta": "காப்பீட்டுத் தொகை",
        "hi": "बीमा राशि",
    },
    "res_duration": {
        "en": "Policy Duration",
        "ta": "பாலிசி காலம்",
        "hi": "पॉलिसी अवधि",
    },
    "res_years": {
        "en": "Years",
        "ta": "ஆண்டுகள்",
        "hi": "वर्ष",
    },
    "res_total_benefit": {
        "en": "Estimated Total Benefit",
        "ta": "மதிப்பிடப்பட்ட மொத்த நன்மை",
        "hi": "अनुमानित कुल लाभ",
    },
    "res_matched_plans": {
        "en": "Recommended Sample Insurance Plans",
        "ta": "பரிந்துரைக்கப்பட்ட மாதிரி காப்பீட்டுத் திட்டங்கள்",
        "hi": "अनुशंसित नमूना बीमा योजनाएं",
    },
    "res_xai_insights": {
        "en": "AI Actuarial Insights & Feature Importance",
        "ta": "AI காப்பீட்டு நுண்ணறிவு & அம்ச முக்கியத்துவம்",
        "hi": "AI अंतर्दृष्टि और फीचर महत्व",
    },

    # -------------------------------------------------------------------------
    # Dashboard Cards & Sections
    # -------------------------------------------------------------------------
    "dash_welcome": {
        "en": "Welcome",
        "ta": "வரவேற்கிறோம்",
        "hi": "स्वागत है",
    },
    "dash_verified_member": {
        "en": "Verified Member",
        "ta": "சரிபார்க்கப்பட்ட உறுப்பினர்",
        "hi": "सत्यापित सदस्य",
    },
    "dash_latest_premium": {
        "en": "Latest Estimated Premium",
        "ta": "சமீபத்திய கணக்கிடப்பட்ட பிரீமியம்",
        "hi": "नवीनतम अनुमानित प्रीमियम",
    },
    "dash_tax_benefit": {
        "en": "Section 80D Tax Benefit",
        "ta": "பிரிவு 80D வரிச் சலுகை",
        "hi": "धारा 80D कर लाभ",
    },
    "dash_cashless_network": {
        "en": "Cashless Network Access",
        "ta": "பணமில்லா மருத்துவமனை வசதி",
        "hi": "कैशलेस नेटवर्क पहुंच",
    },
    "dash_health_status": {
        "en": "Health Profile Status",
        "ta": "சுகாதார விவர நிலை",
        "hi": "स्वास्थ्य प्रोफाइल स्थिति",
    },
    "dash_my_favorites": {
        "en": "My Favorite Insurance Plans",
        "ta": "எனது விருப்பக் காப்பீட்டுத் திட்டங்கள்",
        "hi": "मेरी पसंदीदा बीमा योजनाएं",
    },
    "dash_recent_estimates": {
        "en": "Your Recent Saved Estimates",
        "ta": "உங்கள் சமீபத்திய கணக்கீடுகள்",
        "hi": "आपके हालिया सहेजे गए अनुमान",
    },
    "dash_no_favorites": {
        "en": "No favorite plans saved yet. Explore the catalog and click the heart icon to save policies.",
        "ta": "இதுவரை விருப்பத் திட்டங்கள் எதுவும் சேமிக்கப்படவில்லை. திட்டங்களைச் சேமிக்க இதயக் குறியீட்டைக் கிளிக் செய்க.",
        "hi": "अभी तक कोई पसंदीदा योजना सहेजी नहीं गई है। कैटलॉग देखें और योजनाओं को सहेजने के लिए दिल के आइकन पर क्लिक करें।",
    },

    # -------------------------------------------------------------------------
    # Notifications
    # -------------------------------------------------------------------------
    "notif_title": {
        "en": "Notifications Center",
        "ta": "அறிவிப்பு மையம்",
        "hi": "सूचना केंद्र",
    },
    "notif_unread": {
        "en": "Unread",
        "ta": "படிக்காதவை",
        "hi": "अपठित",
    },
    "notif_all": {
        "en": "All Notifications",
        "ta": "அனைத்து அறிவிப்புகள்",
        "hi": "सभी सूचनाएं",
    },
    "notif_read_tab": {
        "en": "Read",
        "ta": "படித்தவை",
        "hi": "पढ़ी गई",
    },
    "notif_empty": {
        "en": "You have no notifications right now.",
        "ta": "உங்களிடம் தற்போது எந்த அறிவிப்புகளும் இல்லை.",
        "hi": "आपके पास अभी कोई सूचना नहीं है।",
    },
    "notif_view_all": {
        "en": "View all notifications",
        "ta": "அனைத்து அறிவிப்புகளையும் பார்க்க",
        "hi": "सभी सूचनाएं देखें",
    },

    # -------------------------------------------------------------------------
    # Favorites Page
    # -------------------------------------------------------------------------
    "fav_title": {
        "en": "Saved & Favorite Insurance Plans",
        "ta": "சேமிக்கப்பட்ட விருப்பக் காப்பீட்டுத் திட்டங்கள்",
        "hi": "सहेजी गई पसंदीदा बीमा योजनाएं",
    },
    "fav_subtitle": {
        "en": "Review, compare, and organize sample policies bookmarked from your predictions or the multi-insurer catalog.",
        "ta": "உங்கள் கணிப்புகள் அல்லது பல-காப்பீட்டாளர் பட்டியலிலிருந்து புக்மார்க் செய்யப்பட்ட மாதிரி பாலிசிகளை மதிப்பாய்வு செய்து ஒப்பிடுக.",
        "hi": "अपनी भविष्यवाणियों या बहु-बीमाकर्ता कैटलॉग से बुकमार्क की गई नमूना पॉलिसियों की समीक्षा और तुलना करें।",
    },
    "fav_compare_selected": {
        "en": "Compare Selected Plans",
        "ta": "தேர்ந்தெடுத்த திட்டங்களை ஒப்பிடுக",
        "hi": "चयनित योजनाओं की तुलना करें",
    },
    "fav_empty_state": {
        "en": "You haven't bookmarked any insurance plans yet.",
        "ta": "நீங்கள் இன்னும் எந்தக் காப்பீட்டுத் திட்டங்களையும் புக்மார்க் செய்யவில்லை.",
        "hi": "आपने अभी तक किसी भी बीमा योजना को बुकमार्क नहीं किया है।",
    },
    "fav_empty_cta": {
        "en": "Browse Multi-Insurer Catalog",
        "ta": "திட்டங்களின் பட்டியலை உலாவு",
        "hi": "बहु-बीमाकर्ता कैटलॉग ब्राउज़ करें",
    },

    # -------------------------------------------------------------------------
    # Email Status Messages
    # -------------------------------------------------------------------------
    "email_success": {
        "en": "Prediction report successfully dispatched to your email address!",
        "ta": "கணிப்பு அறிக்கை உங்கள் மின்னஞ்சல் முகவரிக்கு வெற்றிகரமாக அனுப்பப்பட்டது!",
        "hi": "भविष्यवाणी रिपोर्ट आपके ईमेल पते पर सफलतापूर्वक भेज दी गई है!",
    },
    "email_error": {
        "en": "Unable to send email report. Please check SMTP configuration or try again.",
        "ta": "மின்னஞ்சல் அறிக்கையை அனுப்ப முடியவில்லை. SMTP அமைப்புகளைச் சரிபார்க்கவும்.",
        "hi": "ईमेल रिपोर्ट भेजने में असमर्थ। कृपया SMTP कॉन्फ़िगरेशन की जांच करें या पुनः प्रयास करें।",
    },
    "email_demo_note": {
        "en": "SMTP credentials are not yet configured in .env. Email feature simulated successfully for evaluation.",
        "ta": "SMTP அமைப்புகள் .env கோப்பில் இன்னும் உள்ளமைக்கப்படவில்லை. மதிப்பீட்டிற்காக மின்னஞ்சல் அம்சம் உருவகப்படுத்தப்பட்டது.",
        "hi": "SMTP क्रेडेंशियल अभी तक .env में कॉन्फ़िगर नहीं हैं। मूल्यांकन के लिए ईमेल सुविधा का अनुकरण किया गया।",
    },

    # -------------------------------------------------------------------------
    # Academic Disclaimer
    # -------------------------------------------------------------------------
    "disclaimer_text": {
        "en": "Disclaimer: HealthSecure is an academic research project applying machine learning for medical cost estimation. All figures and matched insurance plans are illustrative demo models and do not constitute official insurance quotations.",
        "ta": "பொறுப்புத் துறப்பு: ஹெல்த்செக்யூர் என்பது மருத்துவச் செலவு மதிப்பீட்டிற்கான இயந்திரக் கற்றல் கல்வி ஆராய்ச்சித் திட்டமாகும். அனைத்து எண்களும் மாதிரி திட்டங்களும் விளக்கக் குறிப்புகளே தவிர அதிகாரப்பூர்வ காப்பீட்டு விலைப்புள்ளி அல்ல.",
        "hi": "अस्वीकरण: हेल्थसिक्योर चिकित्सा लागत अनुमान के लिए मशीन लर्निंग लागू करने वाली एक शैक्षणिक शोध परियोजना है। सभी आंकड़े और बीमा योजनाएं केवल निर्देशात्मक डेमो मॉडल हैं और आधिकारिक बीमा उद्धरण नहीं हैं।",
    },
    "academic_badge": {
        "en": "Academic Demo Policy",
        "ta": "கல்வி மாதிரி பாலிசி",
        "hi": "शैक्षणिक डेमो पॉलिसी",
    },

    # -------------------------------------------------------------------------
    # Template UI & Action Keys
    # -------------------------------------------------------------------------
    "welcome_prefix": {
        "en": "Welcome,",
        "ta": "வரவேற்கிறோம்,",
        "hi": "स्वागत है,",
    },
    "results_title": {
        "en": "Prediction Results",
        "ta": "கணிப்பு முடிவுகள்",
        "hi": "पूर्वानुमान परिणाम",
    },
    "history_title": {
        "en": "Prediction History",
        "ta": "கணிப்பு வரலாறு",
        "hi": "पूर्वानुमान इतिहास",
    },
    "favorites_title": {
        "en": "Favorite Plans",
        "ta": "விருப்பத் திட்டங்கள்",
        "hi": "पसंदीदा योजनाएं",
    },
    "notifications_title": {
        "en": "Notifications",
        "ta": "அறிவிப்புகள்",
        "hi": "सूचनाएं",
    },
    "recommended_plans_title": {
        "en": "Recommended Insurance Plans",
        "ta": "பரிந்துரைக்கப்பட்ட காப்பீட்டுத் திட்டங்கள்",
        "hi": "अनुशंसित बीमा योजनाएं",
    },
    "nav_simulator": {
        "en": "What-If Simulator",
        "ta": "வாட்-இஃப் சிமுலேட்டர்",
        "hi": "व्हॉट-इफ सिम्युलेटर",
    },
    "nav_compare": {
        "en": "Compare Plans",
        "ta": "திட்டங்களை ஒப்பிடுக",
        "hi": "योजनाओं की तुलना करें",
    },
    "annual_premium": {
        "en": "Annual Premium",
        "ta": "ஆண்டு பிரீமியம்",
        "hi": "वार्षिक प्रीमियम",
    },
    "coverage_amount": {
        "en": "Coverage Amount",
        "ta": "காப்பீட்டு தொகை",
        "hi": "कवरेज राशि",
    },
    "policy_duration": {
        "en": "Policy Duration",
        "ta": "பாலிசி காலம்",
        "hi": "पॉलिसी अवधि",
    },
    "affordability_ratio": {
        "en": "Affordability Ratio",
        "ta": "மலிவுத்தன்மை விகிதம்",
        "hi": "सामर्थ्य अनुपात",
    },
    "download_pdf": {
        "en": "Download PDF Report",
        "ta": "PDF அறிக்கையைப் பதிவிறக்குக",
        "hi": "पीडीएफ रिपोर्ट डाउनलोड करें",
    },
    "send_email_report": {
        "en": "Send Report to Email",
        "ta": "மின்னஞ்சலுக்கு அறிக்கை அனுப்புக",
        "hi": "ईमेल पर रिपोर्ट भेजें",
    },
    "run_what_if": {
        "en": "Run What-If Simulator",
        "ta": "வாட்-இஃப் சிமுலேட்டரை இயக்கு",
        "hi": "व्हॉट-इफ सिम्युलेटर चलाएं",
    },
    "compare_matching_plans": {
        "en": "Compare Matching Plans",
        "ta": "பொருந்தும் திட்டங்களை ஒப்பிடுக",
        "hi": "मिलान योजनाओं की तुलना करें",
    },
    "view_details": {
        "en": "View Details",
        "ta": "விவரங்களைக் காண்க",
        "hi": "विवरण देखें",
    },
    "btn_favorite": {
        "en": "Add to Favorites",
        "ta": "விருப்பங்களில் சேர்",
        "hi": "पसंदीदा में जोड़ें",
    },
    "btn_remove_fav": {
        "en": "Remove from Favorites",
        "ta": "விருப்பங்களிலிருந்து நீக்கு",
        "hi": "पसंदीदा से हटाएं",
    },
    "btn_logout": {
        "en": "Log out",
        "ta": "வெளியேறுக",
        "hi": "लॉग आउट",
    },
    "empty_favorites": {
        "en": "No Favorite Plans Yet",
        "ta": "விருப்பத் திட்டங்கள் எதுவும் இல்லை",
        "hi": "अभी तक कोई पसंदीदा योजना नहीं",
    },
    "disclaimer_academic": {
        "en": "Academic project estimate only. Not an official insurance quotation or binding policy offer.",
        "ta": "கல்வித் திட்ட மதிப்பீடு மட்டுமே. இது அதிகாரப்பூர்வ காப்பீட்டு விலைப்புள்ளி அல்லது ஒப்பந்தக் கொள்கை அல்ல.",
        "hi": "केवल शैक्षणिक परियोजना अनुमान। आधिकारिक बीमा उद्धरण या बाध्यकारी पॉलिसी प्रस्ताव नहीं।",
    },
}


def get_text(key: str, lang: str = "en", default: str | None = None, **kwargs: Any) -> str:
    """Retrieve translation for a key and language with fallback to English."""
    if not lang or lang not in ("en", "ta", "hi"):
        lang = "en"

    entry = TRANSLATIONS.get(key)
    if entry:
        val = entry.get(lang) or entry.get("en")
        if val is not None:
            if kwargs:
                try:
                    return val.format(**kwargs)
                except Exception:
                    return val
            return val

    # Fallback to provided default or key itself
    if default is not None:
        if kwargs:
            try:
                return default.format(**kwargs)
            except Exception:
                return default
        return default
    return key
