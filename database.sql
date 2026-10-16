-- =====================================================================
-- HealthSecure: Smart Insurance Prediction System
-- MySQL Database Schema and Initialization Script
-- =====================================================================

CREATE DATABASE IF NOT EXISTS health_insurance_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE health_insurance_db;

-- ---------------------------------------------------------------------
-- 1. Users Table (Authentication & Role-Based Access Control)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(30) NULL,
    dob DATE NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- 2. Demo Insurance Plans Table (Configurable Sample Plans for Matching)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS insurance_plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL DEFAULT 'HealthSecure',
    plan_name VARCHAR(150) NOT NULL,
    annual_premium DECIMAL(12,2) NOT NULL,
    coverage_amount DECIMAL(12,2) NOT NULL,
    policy_duration INT NOT NULL DEFAULT 10,
    plan_description TEXT NOT NULL,
    benefits TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_plan_company (company_name),
    INDEX idx_plan_status (status),
    INDEX idx_plan_premium (annual_premium)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- 3. Prediction Records Table (ML Predictions, Inputs & Financials)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS prediction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    age INT NOT NULL,
    sex VARCHAR(10) NOT NULL,
    height DECIMAL(5,2) NULL,
    weight DECIMAL(5,2) NULL,
    bmi DECIMAL(5,2) NOT NULL,
    children INT NOT NULL,
    smoker VARCHAR(5) NOT NULL,
    liquor VARCHAR(5) NOT NULL DEFAULT 'no',
    region VARCHAR(20) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    salary DECIMAL(12,2) NOT NULL,
    policy_duration INT NOT NULL DEFAULT 5,
    plan_category VARCHAR(20) NOT NULL DEFAULT 'silver',
    recommendation VARCHAR(255) NOT NULL,
    estimated_benefit DECIMAL(12,2) NOT NULL,
    premium_income_ratio DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    total_premium DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    benefit_factor DECIMAL(5,2) NOT NULL DEFAULT 1.20,
    estimated_premium DECIMAL(12,2) NOT NULL,
    recommended_plan_id INT NULL,
    created_at DATETIME NOT NULL,
    CONSTRAINT fk_prediction_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT fk_prediction_demo_plan FOREIGN KEY (recommended_plan_id) REFERENCES insurance_plans(plan_id) ON DELETE SET NULL,
    INDEX idx_prediction_user (user_id),
    INDEX idx_prediction_created_at (created_at),
    INDEX idx_prediction_plan (plan_category),
    INDEX idx_prediction_smoker (smoker),
    INDEX idx_prediction_liquor (liquor),
    INDEX idx_prediction_region (region),
    INDEX idx_prediction_rec_plan (recommended_plan_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------
-- 4. Recommendations Table (Plan & Benefit Details)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prediction_id INT NOT NULL,
    plan_name VARCHAR(50) NOT NULL,
    policy_years INT NOT NULL,
    annual_premium DECIMAL(12,2) NOT NULL,
    total_premium DECIMAL(12,2) NOT NULL,
    estimated_benefit DECIMAL(12,2) NOT NULL,
    benefit_factor DECIMAL(5,2) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recommendation_prediction FOREIGN KEY (prediction_id) REFERENCES prediction(id) ON DELETE CASCADE,
    INDEX idx_recommendation_prediction (prediction_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------

-- ---------------------------------------------------------------------
-- Seed 118 Comprehensive Demo Insurance Plans Across 8 Leading Insurers:
-- Star Health, Care Health, HDFC ERGO, ICICI Lombard, Bajaj Allianz, New India Assurance, United India, HealthSecure
-- ---------------------------------------------------------------------
INSERT INTO insurance_plans (plan_id, company_name, plan_name, annual_premium, coverage_amount, policy_duration, plan_description, benefits, status)
VALUES
(1, 'Star Health and Allied Insurance', 'Star Comprehensive Health Insurance', 29999.00, 1000000.00, 10, 'Star Health''s premier all-round health shield with zero room rent capping, bariatric surgeries, and maternity coverage.', 'Zero room rent capping, maternity & newborn care, bariatric surgery, air ambulance, 100% restoration', 'active'),
(2, 'Star Health and Allied Insurance', 'Star Senior Citizens Red Carpet', 42500.00, 1500000.00, 15, 'Specialized eldercare health policy for individuals aged 60-75 with no prior medical screening and day-1 consultations.', 'No pre-policy medical checkup, day-1 medical consultations, domiciliary hospitalization, sub-limit waived for ICU', 'active'),
(3, 'Star Health and Allied Insurance', 'Star Family Health Optima', 31500.00, 1000000.00, 15, 'Super-popular family floater plan with automatic sum insured recharge and assisted reproduction coverage.', 'Automatic 3X recharge, assisted reproduction treatment, organ donor expenses, compassionate travel cover', 'active'),
(4, 'Star Health and Allied Insurance', 'Star Young Star Insurance', 13999.00, 500000.00, 5, 'Dynamic health policy tailored for young professionals up to age 40 with wellness discounts and cumulative bonus.', '100% cumulative bonus escalator, wellness activity rebates, automatic restoration, zero copayment', 'active'),
(5, 'Star Health and Allied Insurance', 'Star Cardiac Care Platinum', 39500.00, 1200000.00, 10, 'Industry-first dedicated cardiac health insurance for individuals who have undergone PTCA stent surgery or CABG.', 'Day-1 cardiac cover, stent & bypass surgeries covered, cardiovascular disease consultations, angiogram subsidy', 'active'),
(6, 'Star Health and Allied Insurance', 'Star Diabetes Safe Insurance', 38200.00, 1000000.00, 10, 'Designed explicitly for Type 1 and Type 2 Diabetes patients, covering renal dialysis and diabetic retinopathy.', 'Covers complications of Type 1 & 2 Diabetes from Day 1, dialysis support, kidney care, annual HbA1c tests', 'active'),
(7, 'Star Health and Allied Insurance', 'Star Health Premier Insurance', 54000.00, 2500000.00, 20, 'High-sum insured elite healthcare cover for adults aged 50+, offering single private AC suites and rehabilitation.', 'Single private AC room, home healthcare, hospice care allowance, zero copay, unlimited cumulative bonus', 'active'),
(8, 'Star Health and Allied Insurance', 'Star Critical Illness Multipay', 36000.00, 1500000.00, 10, 'Lump-sum critical illness policy paying multiple claims across 37 major illnesses divided into 4 medical groups.', 'Multiple payouts for distinct illnesses, 37 critical ailments covered, oncology care, neurosurgery support', 'active'),
(9, 'Star Health and Allied Insurance', 'Star Special Care (Autism & Disabilities)', 21000.00, 500000.00, 5, 'Groundbreaking policy created for children and individuals diagnosed with Autism Spectrum Disorder.', 'Inpatient therapy, behavioral counseling, neurodevelopmental support, specialized daycare procedures', 'active'),
(10, 'Star Health and Allied Insurance', 'Star Women Care Insurance', 26500.00, 750000.00, 10, 'Dedicated women-centric health policy with zero waiting period for in-utero fetal surgery and pregnancy care.', 'Maternity delivery cover, in-utero fetal surgery, newborn congenital defects cover, assisted reproduction', 'active'),
(11, 'Star Health and Allied Insurance', 'Star Super Surplus Top-Up', 8999.00, 2000000.00, 5, 'High sum insured top-up policy with flexible deductibles to safeguard against catastrophic medical bills.', '₹20 Lakhs excess buffer over base threshold, zero medical checkup up to 55, pre/post hospitalization', 'active'),
(12, 'Star Health and Allied Insurance', 'Star Out Patient Care (OPD)', 11500.00, 300000.00, 3, 'Standalone outpatient plan covering routine doctor consultations, pharmacy vouchers, dental, and optical tests.', 'OPD consultations, pharmacy reimbursement, dental and ophthalmic procedures, diagnostic checkups', 'active'),
(13, 'Star Health and Allied Insurance', 'Star Micro Rural Health Shield', 3899.00, 150000.00, 2, 'Grassroots micro-insurance providing essential hospitalization support for semi-urban and rural tier-3 families.', 'Emergency trauma care, ambulance subsidy, generic hospital medicine coverage, basic ICU protection', 'active'),
(14, 'Star Health and Allied Insurance', 'Star Arogya Sanjeevani', 6499.00, 300000.00, 3, 'IRDAI-benchmarked standard essential policy offering dependable, standardized cashless coverage.', 'Standard inpatient treatment, ICU room protection, AYUSH therapy, zero co-pay on network hospitals', 'active'),
(15, 'Star Health and Allied Insurance', 'Star Health Assure Plan', 48500.00, 2000000.00, 15, 'Comprehensive individual and family protection with automatic restoration up to 200% and companion allowance.', '200% automatic restoration, non-medical items (consumables) covered, home care nursing, companion benefits', 'active'),
(16, 'Star Health and Allied Insurance', 'Star Cancer Care Platinum', 34500.00, 1250000.00, 10, 'Pioneering cancer insurance providing indemnity cover for oncology therapies, chemotherapy, and surgical excision.', 'Chemotherapy & radiotherapy cover, advanced immunotherapy, surgical oncologist fees, reconstructive surgery', 'active'),
(17, 'Care Health Insurance', 'Care Classic Essential', 18500.00, 500000.00, 5, 'Dependable base health protection offering clean, un-capped inpatient care and daycare treatments.', 'Inpatient hospitalization, 540+ daycare procedures, pre/post hospital expenses (30/60 days), ambulance cover', 'active'),
(18, 'Care Health Insurance', 'Care Supreme Flagship', 28800.00, 1000000.00, 10, 'Care''s bestselling comprehensive policy with unlimited recharge, cumulative bonus super up to 500%, and zero copay.', 'Unlimited automatic recharge, 500% cumulative bonus super, zero room rent restrictions, AYUSH cover', 'active'),
(19, 'Care Health Insurance', 'Care Advantage High-Sum', 46000.00, 2500000.00, 15, 'High sum insured medical umbrella designed to cushion against steep corporate tertiary hospital treatment bills.', '₹25 Lakhs sum insured, single private room, no disease-wise sub-limits, annual preventive health scan', 'active'),
(20, 'Care Health Insurance', 'Care Freedom Diabetes & BP', 37800.00, 1000000.00, 10, 'Tailored for individuals with pre-existing diabetes, hypertension, or elevated BMI without mandatory pre-policy tests.', 'Day-1 pre-existing coverage, home care hospitalization, dialysis support, cardiovascular health checkup', 'active'),
(21, 'Care Health Insurance', 'Care Senior Eldercare', 43900.00, 1500000.00, 15, 'Comprehensive eldercare insurance for parents with domiciliary care, AYUSH therapy, and dedicated claims concierge.', 'Domiciliary care, AYUSH coverage, zero medical tests up to age 65, dedicated personal claim manager', 'active'),
(22, 'Care Health Insurance', 'Care Heart Cardiac Protection', 39200.00, 1200000.00, 10, 'Engineered for heart patients, covering pre-existing cardiac conditions, heart surgery, and pacemaker implants.', 'Angioplasty & bypass cover, cardiac monitoring allowance, zero room rent capping, cardiac rehabilitation', 'active'),
(23, 'Care Health Insurance', 'Care 1 Crore Super Cover', 72000.00, 10000000.00, 25, 'Flagship ₹1 Crore medical protection shield with worldwide emergency cover and zero domestic deductibles.', '₹1 Crore lifetime coverage, unrestricted hospital choice, air ambulance, 100% restoration, zero copays', 'active'),
(24, 'Care Health Insurance', 'Care Global Worldwide Care', 88000.00, 10000000.00, 25, 'Ultra-elite global medical treatment policy providing cashless planned hospitalization in US, UK, Europe, & Singapore.', 'Global planned treatment (US/UK included), international air ambulance, second medical opinion, VIP medical liaison', 'active'),
(25, 'Care Health Insurance', 'Care Shield Inflation Rider', 22999.00, 750000.00, 7, 'Inflation-protected health cover with 100% reimbursement for non-medical consumables (gloves, PPE, masks).', 'Consumables coverage (zero deductions), inflation-indexed sum insured escalator, no-claim bonus shield', 'active'),
(26, 'Care Health Insurance', 'Care Explore Travel-Health', 15500.00, 500000.00, 5, 'Dual domestic and overseas emergency healthcare shield designed for frequent corporate travelers.', 'Emergency medical treatment across India and abroad, loss of baggage cover, medical evacuation pass', 'active'),
(27, 'Care Health Insurance', 'Care Joy Maternity & Child', 33500.00, 1000000.00, 10, 'Comprehensive maternity plan with short 9-month waiting period, newborn baby cover, and pediatric vaccination.', '9-month maternity waiting period, normal & C-section delivery cover, newborn health shield, vaccination costs', 'active'),
(28, 'Care Health Insurance', 'Care OPD 360 Health Pass', 9999.00, 250000.00, 3, 'Day-to-day outpatient coverage featuring unlimited digital doctor consultations, diagnostics, and dental care.', 'Unlimited digital tele-consults, diagnostic testing allowance, pharmacy discounts, dental & vision cover', 'active'),
(29, 'Care Health Insurance', 'Care Micro Arogya Bima', 4200.00, 150000.00, 2, 'Micro-insurance offering affordable basic hospitalization safety net for self-employed individuals and blue-collar workers.', 'Accidental injury inpatient cover, daily hospital allowance, ambulance subsidy, basic surgery cover', 'active'),
(30, 'Care Health Insurance', 'Care Critical Mediclaim', 35000.00, 1500000.00, 10, 'Comprehensive 32 critical illness cover offering lump-sum financial support upon clinical diagnosis.', '32 critical illnesses covered, lump-sum recovery payment, global second opinion, chemotherapy reimbursement', 'active'),
(31, 'Care Health Insurance', 'Care Economy Saver', 12800.00, 400000.00, 5, 'Cost-conscious hospitalization cover designed for tier-2/tier-3 cities with a modest 10% co-payment.', 'Tier-2/3 network hospital cashless care, daycare surgeries, pre & post hospitalization (30/60 days)', 'active'),
(32, 'Care Health Insurance', 'Care NCB Super Booster', 26000.00, 800000.00, 10, 'Rewarding policy that ramps sum insured by 50% each claim-free year up to a massive 150% booster.', '150% cumulative bonus escalation, unlimited restoration, zero room rent capping, annual health scan', 'active'),
(33, 'HDFC ERGO General Insurance', 'HDFC ERGO Optima Secure', 31200.00, 1000000.00, 10, 'Revolutionary health plan offering 4X cover (Secure, Plus, Restore, & Protect) with 2X coverage on Day 1.', 'Instant 2X coverage on Day 1, 100% restoration, zero deductions on non-medical consumables, cumulative bonus', 'active'),
(34, 'HDFC ERGO General Insurance', 'HDFC ERGO Optima Restore', 27500.00, 800000.00, 10, 'Iconic health protection with automatic 100% restoration of sum insured immediately after partial or complete claim.', '100% restore benefit, stay active fitness discount (up to 8%), zero room rent capping, AYUSH coverage', 'active'),
(35, 'HDFC ERGO General Insurance', 'HDFC ERGO My:Health Suraksha', 24500.00, 750000.00, 7, 'Customizable healthcare protection with air ambulance, recovery grant, home treatment, and maternity riders.', 'Air ambulance cover, recovery benefit, home healthcare, alternative treatments, preventive wellness checkup', 'active'),
(36, 'HDFC ERGO General Insurance', 'HDFC ERGO My:Health Medisure Classic', 19200.00, 500000.00, 5, 'Clean, predictable base medical policy with maternity additions, newborn coverage, and day care procedures.', 'Day-care procedures covered, pre-post hospitalization (30/60 days), road ambulance cover, maternity add-on', 'active'),
(37, 'HDFC ERGO General Insurance', 'HDFC ERGO My:Health Women Suraksha', 25800.00, 1000000.00, 10, 'Specialized female health policy protecting against 41 women-specific critical illnesses, oncology, and pregnancy complications.', '41 female-specific illnesses covered, loss of job benefit, child education fund rider, post-surgery nursing', 'active'),
(38, 'HDFC ERGO General Insurance', 'HDFC ERGO Optima Super Secure', 52000.00, 2500000.00, 20, 'Executive high-tier plan featuring 3X cumulative bonus escalation and worldwide emergency air ambulance.', '3X cumulative bonus, private deluxe suite room, robotic surgery cover, worldwide emergency assistance', 'active'),
(39, 'HDFC ERGO General Insurance', 'HDFC ERGO Critical Illness Platinum', 36800.00, 1500000.00, 10, 'Comprehensive lump-sum payout cover protecting against 38 critical medical conditions including cancer and paralysis.', '38 critical illnesses covered, lump-sum payout on diagnosis, zero survival period for select riders, second opinion', 'active'),
(40, 'HDFC ERGO General Insurance', 'HDFC ERGO Senior Citizen Security', 45200.00, 1500000.00, 15, 'Elderly healthcare protection with pre-existing disease coverage after reduced 2-year waiting and home nursing.', 'Reduced waiting period (24 months), domiciliary hospitalization, companion daily allowance, AYUSH therapy', 'active'),
(41, 'HDFC ERGO General Insurance', 'HDFC ERGO Energy Diabetes Care', 40500.00, 1200000.00, 10, 'Disease management plan specifically crafted for individuals with Type 2 Diabetes and hypertension.', 'Day-1 coverage for diabetic complications, personalized health coach, annual diagnostic tests package', 'active'),
(42, 'HDFC ERGO General Insurance', 'HDFC ERGO Easy Health Standard', 16500.00, 450000.00, 5, 'Cost-effective, dependable coverage with hospital daily cash allowance and zero copay nationwide.', 'Hospital daily cash (up to ₹2,500/day), emergency road ambulance, inpatient treatment, daycare surgeries', 'active'),
(43, 'HDFC ERGO General Insurance', 'HDFC ERGO Global Health Supreme', 89500.00, 10000000.00, 25, 'Flagship ₹1 Crore worldwide healthcare umbrella covering planned treatments in leading US, European, and Swiss clinics.', 'Worldwide planned treatment including US/UK, global second medical opinion, travel & accommodation subsidy', 'active'),
(44, 'HDFC ERGO General Insurance', 'HDFC ERGO Health Wallet Family', 33900.00, 1200000.00, 10, 'Innovative health wallet plan allowing accumulated reserve funds to roll over for OPD consults, dental, and pharmacy.', 'Health wallet reserve rollover, outpatient consults, dental & vision cover, vaccination expenses, ICU care', 'active'),
(45, 'HDFC ERGO General Insurance', 'HDFC ERGO Arogya Sanjeevani', 6100.00, 300000.00, 3, 'Clean, IRDAI-benchmarked standard essential health policy supported by HDFC ERGO''s top-rated claim ratio.', 'Inpatient treatment, ICU coverage, generic pharmacy reimbursement, zero copay on network hospitals', 'active'),
(46, 'HDFC ERGO General Insurance', 'HDFC ERGO Micro Rural Kavach', 3600.00, 100000.00, 2, 'Budget micro-insurance safety shield for farmers, village artisans, and agricultural workers.', 'Accidental injury cover, hospitalization reimbursement, basic surgical operations, ambulance grant', 'active'),
(47, 'HDFC ERGO General Insurance', 'HDFC ERGO Day Care Specialist', 14200.00, 400000.00, 5, 'Advanced outpatient surgical policy covering minimally invasive, robotic, laparoscopic, and laser surgeries.', 'Robotic & laparoscopic day care procedures, dialysis, radiation therapy, eye cataract surgeries covered', 'active'),
(48, 'HDFC ERGO General Insurance', 'HDFC ERGO Active Life Shield', 23400.00, 650000.00, 7, 'Incentivized wellness coverage rewarding physical fitness milestones with up to 25% renewal premium discounts.', 'Fitness tracking discounts, 10% annual bonus escalator, single private room, annual full-body scan', 'active'),
(49, 'ICICI Lombard General Insurance', 'ICICI Lombard Complete Health Insurance', 29500.00, 1000000.00, 10, 'Flagship comprehensive protection plan featuring reset benefits, super no-claim bonus, and wellness points.', 'Reset benefit for unrelated illnesses, super no-claim bonus up to 100%, zero room rent cap, wellness rewards', 'active'),
(50, 'ICICI Lombard General Insurance', 'ICICI Lombard Health AdvantEdge', 34800.00, 1250000.00, 10, 'Modern health shield offering domestic & global emergency assistance, organ donor cover, and convalescence grant.', 'Worldwide emergency assistance, organ donor treatment, convalescence allowance, critical illness booster', 'active'),
(51, 'ICICI Lombard General Insurance', 'ICICI Lombard Elevate Health Plan', 42000.00, 1500000.00, 15, 'Future-proof medical plan with infinite claim restoration, personalized wellness plans, and comprehensive riders.', 'Infinite claim restoration, zero copayment, private AC room, annual executive full body health check', 'active'),
(52, 'ICICI Lombard General Insurance', 'ICICI Lombard MaxProtect 1 Crore', 74500.00, 10000000.00, 25, 'Massive ₹1 Crore coverage designed for high-net-worth protection with worldwide emergency evacuation.', '₹1 Crore sum insured, international emergency evacuation, zero sub-limits, luxury single suite', 'active'),
(53, 'ICICI Lombard General Insurance', 'ICICI Lombard Golden Shield Senior', 46500.00, 1500000.00, 15, 'Tailored for senior citizens aged 60+, featuring reduced pre-existing waiting period, physiotherapy, and AYUSH.', 'Senior citizen tailored, reduced waiting period, home physiotherapy, AYUSH hospital cover, zero room cap', 'active'),
(54, 'ICICI Lombard General Insurance', 'ICICI Lombard Health Booster Top-Up', 7800.00, 1500000.00, 5, 'Economical super top-up plan providing high medical buffer with deductible options from ₹3 Lakhs to ₹10 Lakhs.', '₹15 Lakhs super top-up protection, cashless network claims, zero pre-policy medical checkup', 'active'),
(55, 'ICICI Lombard General Insurance', 'ICICI Lombard Health Care Plus', 21500.00, 600000.00, 5, 'Solid, dependable coverage featuring extended 60/180-day pre & post hospitalization and road ambulance.', 'Pre/post hospitalization (60/180 days), road ambulance cover, daycare surgeries, restorative cover', 'active'),
(56, 'ICICI Lombard General Insurance', 'ICICI Lombard Comprehensive Shield', 38000.00, 1200000.00, 10, 'Unified family floater package with maternity, newborn baby vaccinations, and preventive healthcare diagnostics.', 'Maternity care, newborn vaccination subsidy, pediatric ICU cover, annual diagnostic scan', 'active'),
(57, 'ICICI Lombard General Insurance', 'ICICI Lombard Critical Illness Guard', 35500.00, 1500000.00, 10, 'Dedicated financial safety net paying a lump sum on diagnosis of 34 acute and catastrophic illnesses.', '34 critical illnesses covered, 100% lump sum grant, second medical opinion, advanced oncology reimbursement', 'active'),
(58, 'ICICI Lombard General Insurance', 'ICICI Lombard Outpatient OPD Elite', 10500.00, 200000.00, 3, 'Complete outpatient care policy covering clinical visits, diagnostic testing, dental checkups, and optical vouchers.', 'Doctor consultations, pharmacy bills, diagnostic imaging tests, dental care, zero deductible', 'active'),
(59, 'ICICI Lombard General Insurance', 'ICICI Lombard Family Shield Floater', 32400.00, 1000000.00, 12, 'Extended family health policy with single-premium coverage for couple and up to 3 dependent children.', 'Family floater umbrella, zero room rent capping, child hospitalization cover, restorative sum insured', 'active'),
(60, 'ICICI Lombard General Insurance', 'ICICI Lombard Arogya Sanjeevani', 6200.00, 300000.00, 3, 'Clean, IRDAI-benchmarked standard essential health policy with ICICI Lombard''s quick cashless settlement.', 'Inpatient treatments, ICU room support, cataract and joint surgery cover, zero network copay', 'active'),
(61, 'ICICI Lombard General Insurance', 'ICICI Lombard Smart Health Executive', 51000.00, 2000000.00, 18, 'Premium tier executive cover offering single private AC suite accommodations and instant claim clearance.', 'Executive suite room entitlement, 30-min cashless claims processing, full-body health scan, personal concierge', 'active'),
(62, 'ICICI Lombard General Insurance', 'ICICI Lombard Micro Rural Suraksha', 3500.00, 100000.00, 2, 'Low-cost grassroots healthcare policy providing essential hospitalization protection for agricultural families.', 'Hospitalization expense reimbursement, trauma care, ambulance support, generic pharmacy voucher', 'active'),
(63, 'ICICI Lombard General Insurance', 'ICICI Lombard FitLife Health Shield', 23900.00, 700000.00, 7, 'Dynamic wellness coverage rewarding healthy lifestyle milestones with premium cashback and gym perks.', 'Wearable fitness tracker discounts, 10% no-claim escalator, alternative medicine, complete inpatient care', 'active'),
(64, 'ICICI Lombard General Insurance', 'ICICI Lombard Cardiac & Vital Organ', 39800.00, 1200000.00, 10, 'Specialized cover for vital organ and heart conditions including coronary bypass, angioplasty, and transplants.', 'Heart stent & bypass coverage, pulmonary rehabilitation, organ donor expenses, specialized angiography vouchers', 'active'),
(65, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Health Guard Individual', 26800.00, 750000.00, 10, 'Trusted individual healthcare policy with comprehensive inpatient, pre/post hospital, and daycare surgeries.', 'Inpatient care, 100% restoration, daycare surgeries, ambulance support, cumulative bonus up to 50%', 'active'),
(66, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Health Guard Family Floater', 32000.00, 1000000.00, 12, 'Unified family health umbrella providing pooled coverage for parents and children with zero hospital co-pay.', 'Family floater coverage, maternity rider, child vaccination cover, zero room rent sub-limits', 'active'),
(67, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Health Care Supreme', 44000.00, 1500000.00, 15, 'High-end comprehensive medical policy with recovery grants, organ donor cover, and physiotherapy sessions.', 'Recovery benefit grant, organ donor expenses, physiotherapy allowance, AYUSH therapy, private deluxe room', 'active'),
(68, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Silver Health Senior', 45800.00, 1500000.00, 15, 'Specialized senior policy for individuals aged 46-70 with 50% waiver on pre-existing condition waiting period.', '50% waiver on pre-existing waiting period, domiciliary hospitalization, companion allowance, ICU coverage', 'active'),
(69, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Critical Illness Insurance', 36200.00, 1500000.00, 10, 'Financial safety policy providing lump-sum capital grant upon diagnosis of 36 critical medical conditions.', '36 critical illnesses covered, lump-sum payout, global second opinion, oncology & stroke recovery support', 'active'),
(70, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Extra Care Plus Top-Up', 8200.00, 2000000.00, 5, 'Affordable super top-up policy with flexible deductibles and zero medical screening for applicants up to age 55.', '₹20 Lakhs high-sum top-up, zero pre-policy medical checkup up to 55, emergency ambulance cover', 'active'),
(71, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Global Health Care', 82500.00, 10000000.00, 25, 'Premier international health insurance covering planned and emergency medical procedures in leading overseas hospitals.', '₹1 Crore worldwide coverage, overseas planned surgeries, international air ambulance, VIP medical concierge', 'active'),
(72, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Tax Gain Mediclaim', 18900.00, 500000.00, 5, 'Dual benefit policy designed for maximum Section 80D tax deductions combined with outpatient and hospitalization care.', 'Maximum 80D tax savings, OPD consultation vouchers, hospitalization cover, diagnostic tests reimbursement', 'active'),
(73, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Health Infinity', 56500.00, 2500000.00, 20, 'High-tier shield with unlimited sum insured restoration and zero capping on room rent, ICU, or road ambulance.', 'Unlimited sum insured restoration, zero room rent capping, robotic treatment, international second opinion', 'active'),
(74, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Arogya Sanjeevani', 6300.00, 300000.00, 3, 'IRDAI standard essential policy with Bajaj Allianz''s swift claim settlement and nationwide cashless hospitals.', 'Inpatient care, standard daycare procedures, generic medicine allowance, road ambulance cover', 'active'),
(75, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Women Cancer Shield', 24800.00, 800000.00, 8, 'Targeted oncology health policy covering breast, ovarian, and cervical cancer with specialized recovery grants.', 'Female cancer protection, chemotherapy & radiation cover, surgery excision grant, post-treatment therapy', 'active'),
(76, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Hospital Daily Cash', 9200.00, 200000.00, 3, 'Daily allowance benefit plan paying up to ₹5,000 every 24 hours of hospitalization to offset non-medical outlays.', 'Daily cash payout up to ₹5,000/day, double cash for ICU hospitalization, zero deductions, no bills needed', 'active'),
(77, 'Bajaj Allianz General Insurance', 'Bajaj Allianz M-Care Micro Insurance', 3750.00, 120000.00, 2, 'Micro-insurance safety net crafted for informal workers, gig drivers, and agricultural labor.', 'Inpatient hospitalization, fracture & trauma treatment, emergency ambulance grant, basic surgical cover', 'active'),
(78, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Prime Health Shield', 49500.00, 2000000.00, 15, 'Deluxe corporate executive health shield with private single room entitlement and fast-track 60-minute claim clearance.', 'Single private suite room, priority cashless approval in 60 mins, executive annual health scan, zero copay', 'active'),
(79, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Diabetes & Cardiac Protect', 41200.00, 1250000.00, 10, 'Specialized health protection covering diabetes complications, hypertension, and heart disease from Day 1.', 'Day-1 pre-existing diabetes coverage, HbA1c test monitoring allowance, dialysis support, cardiovascular cover', 'active'),
(80, 'Bajaj Allianz General Insurance', 'Bajaj Allianz Young Care Professional', 14800.00, 450000.00, 5, 'Digital-first policy for early-career professionals featuring gym vouchers, mental wellness sessions, and accident cover.', 'Stress counseling sessions, preventive annual diagnostics, zero room rent capping on shared rooms, accident cover', 'active'),
(81, 'The New India Assurance Co. Ltd.', 'New India Mediclaim Policy', 25500.00, 700000.00, 10, 'India''s benchmark public sector mediclaim policy offering rock-solid coverage backed by sovereign trust.', 'Inpatient hospitalization, pre-post hospital expenses, ICU coverage, ambulance subsidy, AYUSH treatment', 'active'),
(82, 'The New India Assurance Co. Ltd.', 'New India Floater Mediclaim', 31000.00, 1000000.00, 12, 'Public sector family floater covering self, spouse, and dependent children under a unified sum insured.', 'Family floater coverage, maternity & child cover, zero co-pay on network hospitals, cumulative bonus', 'active'),
(83, 'The New India Assurance Co. Ltd.', 'New India Premier Mediclaim', 48900.00, 2000000.00, 18, 'Top-tier PSU healthcare plan featuring critical illness riders, air ambulance, and single private AC room.', 'Critical illness rider, emergency air ambulance, single private AC room, organ donor expenses, zero copay', 'active'),
(84, 'The New India Assurance Co. Ltd.', 'New India Sixty Plus Senior Mediclaim', 43500.00, 1200000.00, 15, 'Tailored eldercare health protection with reduced waiting periods and comprehensive home hospitalization.', 'Zero pre-policy medical checkup up to age 65, domiciliary hospitalization, AYUSH therapy, companion caregiver allowance', 'active'),
(85, 'The New India Assurance Co. Ltd.', 'New India Asha Kiran', 17500.00, 500000.00, 5, 'Specially designed family protection plan providing special discounts for families with only girl children.', 'Discount for girl-child families, hospitalization support, road ambulance, daycare procedures', 'active'),
(86, 'The New India Assurance Co. Ltd.', 'New India Cancer Medical Expense', 32500.00, 1000000.00, 10, 'Dedicated oncology policy reimbursing medical expenses for diagnosis, surgery, radiotherapy, and chemo.', 'Cancer therapy reimbursement, chemotherapy, targeted immunotherapy, surgical excision, post-op care', 'active'),
(87, 'The New India Assurance Co. Ltd.', 'New India Top Up Mediclaim', 7500.00, 1500000.00, 5, 'Affordable public sector deductible top-up policy protecting against major surgical emergencies.', 'High sum insured buffer, low annual premium, seamless cashless settlement across PSU network hospitals', 'active'),
(88, 'The New India Assurance Co. Ltd.', 'New India Global Mediclaim', 79000.00, 10000000.00, 25, 'Public sector worldwide healthcare protection with unrestricted international hospital access and air ambulance.', 'Global treatment coverage including US/UK/Singapore, international air ambulance, 100% restoration', 'active'),
(89, 'The New India Assurance Co. Ltd.', 'New India Arogya Sanjeevani', 5800.00, 300000.00, 3, 'IRDAI standard essential policy backed by the sovereign reliability of India''s largest general insurer.', 'ICU room cover, basic daycare surgeries, generic pharmacy coverage, zero copay on network hospitals', 'active'),
(90, 'The New India Assurance Co. Ltd.', 'New India Bima Care Essential', 11900.00, 350000.00, 5, 'Economical hospitalization plan for budget-conscious families seeking reliable PSU cashless claims.', 'Inpatient treatment, pre & post hospitalization (30/60 days), road ambulance, restorative sum insured', 'active'),
(91, 'The New India Assurance Co. Ltd.', 'New India Rural Micro Shield', 2999.00, 100000.00, 2, 'Ultra-low-cost government-backed micro health policy designed for farmers and village self-help groups.', 'Accidental hospitalization, basic trauma care, emergency ambulance subsidy, zero paperwork hassle', 'active'),
(92, 'The New India Assurance Co. Ltd.', 'New India Executive Health Guard', 37500.00, 1200000.00, 10, 'Corporate PSU executive shield offering single private room entitlement and comprehensive critical care.', 'Single private AC room, modern robotic treatments, organ donor coverage, emergency road & air assistance', 'active'),
(93, 'The New India Assurance Co. Ltd.', 'New India Universal Health Insurance', 4800.00, 150000.00, 3, 'Affordable mass healthcare policy subsidized for informal wage earners, providing essential hospitalization protection.', 'Hospitalization expense reimbursement, loss of earning compensation, funeral expenses grant, daycare cover', 'active'),
(94, 'The New India Assurance Co. Ltd.', 'New India Standard Hospitalization', 21800.00, 600000.00, 7, 'Standard balanced protection plan providing comprehensive inpatient and outpatient support.', 'Inpatient treatment, daycare treatments, ambulance support, annual health checkup, pre/post hospitalization', 'active'),
(95, 'The New India Assurance Co. Ltd.', 'New India Cardio Care Shield', 39000.00, 1200000.00, 10, 'Tailored health cover designed for individuals with cardiovascular risk, respiratory history, or lifestyle exposures.', 'Heart stent & bypass coverage, pulmonary rehabilitation, specialized angiography vouchers, smoking cessation support', 'active'),
(96, 'The New India Assurance Co. Ltd.', 'New India Youth Smart Health', 13500.00, 400000.00, 5, 'Clean, affordable health policy for young college graduates, first-jobbers, and young married couples.', 'Hospitalization support, basic benefits, standard ambulance cover, daycare procedures, wellness vouchers', 'active'),
(97, 'United India Insurance Co. Ltd.', 'United India Individual Mediclaim', 24900.00, 650000.00, 10, 'Heritage PSU policy providing reliable cashless treatment at 7,000+ accredited hospitals nationwide.', 'Inpatient treatment, ICU support, daycare treatments, ambulance support, pre/post hospitalization', 'active'),
(98, 'United India Insurance Co. Ltd.', 'United India Family Medicare', 29800.00, 1000000.00, 12, 'Comprehensive public sector family floater covering acute illnesses, accidents, and maternity care.', 'Family floater coverage, maternity benefits, pediatric care, ICU cover, zero room-rent capping', 'active'),
(99, 'United India Insurance Co. Ltd.', 'United India Senior Citizen Health', 42800.00, 1200000.00, 15, 'Tailored for senior citizens aged 60+, featuring domiciliary treatments, AYUSH therapy, and caregiver allowance.', 'Domiciliary care, AYUSH therapy, companion caregiver allowance, zero pre-policy checkup up to 65', 'active'),
(100, 'United India Insurance Co. Ltd.', 'United India Super Top Up Medicare', 7200.00, 1500000.00, 5, 'Cost-effective PSU top-up policy providing financial cushion against large unexpected hospital bills.', '₹15 Lakhs catastrophic cover buffer, affordable annual premium, cashless processing across PSU network', 'active'),
(101, 'United India Insurance Co. Ltd.', 'United India Critical Illness Benefit', 34000.00, 1200000.00, 10, 'Lump-sum benefit policy paying full sum insured upon confirmed diagnosis of major vital organ conditions.', 'Lump-sum recovery payout, 30+ critical illnesses covered, oncology care, cardiac surgery cover', 'active'),
(102, 'United India Insurance Co. Ltd.', 'United India Uni-Mediclaim', 19800.00, 500000.00, 5, 'Straightforward hospitalization policy providing reliable medical coverage with minimal exclusions.', 'Inpatient treatment, pre & post hospitalization (30/60 days), road ambulance, restorative sum insured', 'active'),
(103, 'United India Insurance Co. Ltd.', 'United India Arogya Sanjeevani', 5750.00, 300000.00, 3, 'Standardized IRDAI product with zero room-rent capping on shared ICU accommodations.', 'ICU room cover, basic daycare surgeries, generic pharmacy coverage, zero copay on network hospitals', 'active'),
(104, 'United India Insurance Co. Ltd.', 'United India Micro Insurance Arogya', 2850.00, 100000.00, 2, 'Economical micro-insurance health security for village artisans, agricultural workers, and self-employed women.', 'Accident hospitalization, basic trauma care, emergency ambulance subsidy, minimal documentation', 'active'),
(105, 'United India Insurance Co. Ltd.', 'United India Workman & Executive Guard', 36500.00, 1200000.00, 10, 'Industrial and executive health protection covering workplace injuries, occupational ailments, and critical illnesses.', 'Workplace trauma coverage, critical illness rider, ICU room care, 60/90 days pre/post hospitalization', 'active'),
(106, 'United India Insurance Co. Ltd.', 'United India Shrestha Health Guard', 46000.00, 1800000.00, 15, 'High sum insured PSU tier offering single private AC room and modern robotic/laser treatments.', 'Single private room, modern robotic treatments, organ donor coverage, emergency road & air assistance', 'active'),
(107, 'United India Insurance Co. Ltd.', 'United India Health Plus', 16200.00, 450000.00, 5, 'Affordable family package covering generic medicines, diagnostics, and routine acute inpatient treatments.', 'Hospitalization support, basic benefits, standard ambulance cover, daycare procedures, diagnostic subsidy', 'active'),
(108, 'United India Insurance Co. Ltd.', 'United India Mahila Suraksha Mediclaim', 23500.00, 700000.00, 8, 'Women-centric health protection plan covering maternity, neonatal care, and female-specific oncology.', 'Maternity delivery care, newborn protection, female oncology cover, pre/post natal diagnostic tests', 'active'),
(109, 'United India Insurance Co. Ltd.', 'United India Gramin Swasthya Bima', 3200.00, 100000.00, 2, 'Grassroots village healthcare cover offering emergency hospitalization relief with simple claim processing.', 'Emergency trauma care, ambulance reimbursement, generic pharmacy voucher, minimal KYC', 'active'),
(110, 'United India Insurance Co. Ltd.', 'United India Comprehensive Hospitalization', 33800.00, 1000000.00, 10, 'Full-spectrum inpatient coverage with ICU, daycare surgeries, and road ambulance subsidy across India.', 'Extended inpatient care, pre & post hospitalization (60/90 days), restorative sum insured, AYUSH care', 'active'),
(111, 'United India Insurance Co. Ltd.', 'United India Platinum Shield', 53000.00, 2500000.00, 20, 'Premier PSU shield with restorative sum insured, organ donor coverage, and private suite entitlements.', 'Private deluxe suite room rent, organ donor expenses, unlimited restoration, zero copay nationwide', 'active'),
(112, 'United India Insurance Co. Ltd.', 'United India Diabetes & Cardiac Shield', 38500.00, 1000000.00, 10, 'Tailored protection for chronic cardiovascular and diabetic management with reduced waiting periods.', 'Day-1 pre-existing coverage for diabetes, HbA1c monitoring allowance, cardiovascular surgery cover', 'active'),
(113, 'HealthSecure', 'HealthSecure Starter Shield', 11999.00, 300000.00, 3, 'Pocket-friendly starter health protection plan for young adults, students, and early-career individuals.', 'Emergency hospitalization, basic OPD consultations, accident cover, 24/7 tele-health helpline', 'active'),
(114, 'HealthSecure', 'HealthSecure SmartCare', 22499.00, 500000.00, 5, 'Balanced health protection tier tailored for young professionals with preventive diagnostic allowances.', 'Hospitalization, annual preventive wellness checkups, pharmacy vouchers, daycare treatment', 'active'),
(115, 'HealthSecure', 'HealthSecure CriticalCare Rider', 36500.00, 1200000.00, 10, 'Specialized high-severity coverage protecting against 36 major critical illnesses with lump-sum recovery payouts.', '36 critical illnesses covered, lump-sum recovery grant, advanced oncology care, cardiac surgery cover', 'active'),
(116, 'HealthSecure', 'HealthSecure Fit & Active Shield', 24999.00, 600000.00, 7, 'Incentivized wellness coverage rewarding healthy lifestyle habits with premium discounts and gym subscriptions.', 'Fitness tracking rebates, 10% no-claim bonus escalator, complete inpatient care, alternative medicine (AYUSH)', 'active'),
(117, 'HealthSecure', 'HealthSecure Silver Executive', 47000.00, 1500000.00, 15, 'High-grade executive protection plan featuring private suite room entitlements and fast-track cashless claims.', 'Deluxe single room entitlement, priority cashless processing within 30 minutes, executive annual full-body health scan', 'active'),
(118, 'HealthSecure', 'HealthSecure Ultimate Crore Pati Shield', 96000.00, 10000000.00, 25, 'Flagship ₹1 Crore worldwide health umbrella with zero sub-limits, unlimited sum restoration, and VIP hospital suites.', '₹1 Crore lifetime coverage, unrestricted worldwide hospitals, emergency medical evacuation, zero deductibles globally', 'active')
ON DUPLICATE KEY UPDATE
    company_name = VALUES(company_name),
    plan_name = VALUES(plan_name),
    annual_premium = VALUES(annual_premium),
    coverage_amount = VALUES(coverage_amount),
    policy_duration = VALUES(policy_duration),
    plan_description = VALUES(plan_description),
    benefits = VALUES(benefits),
    status = VALUES(status);

-- ---------------------------------------------------------------------
-- Seed Default Administrator (Password: Admin@123)
-- Uses Werkzeug scrypt/pbkdf2 hash format compatible with Flask
-- ---------------------------------------------------------------------
INSERT INTO users (name, email, password_hash, role, created_at)
SELECT 'System Administrator', 'admin@healthsecure.com',
       'scrypt:32768:8:1$u7F5G1E0bM1N6GqF$237f3747683d7890febe6f76c5b96791e84ca3b5c4ad2fbc9671db8858a74ec76495be2489679cb046dfc792198be08764041b31a89c3132bf6e1e695fa9fe9e',
       'admin', NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin@healthsecure.com'
);
