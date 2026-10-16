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
    plan_name VARCHAR(100) NOT NULL,
    annual_premium DECIMAL(12,2) NOT NULL,
    coverage_amount DECIMAL(12,2) NOT NULL,
    policy_duration INT NOT NULL DEFAULT 10,
    plan_description TEXT NOT NULL,
    benefits TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
-- Seed 24 Comprehensive Demo Insurance Plans (Configurable from Database)
-- Spanning Micro-Care (₹3,499) to ₹1 Crore Worldwide Shield (₹96,000)
-- ---------------------------------------------------------------------
INSERT INTO insurance_plans (plan_id, plan_name, annual_premium, coverage_amount, policy_duration, plan_description, benefits, status)
VALUES
(1, 'HealthSecure Basic', 19999.00, 450000.00, 5, 'Essential sample coverage plan designed for cost-conscious protection against acute hospitalization.', 'Hospitalization support, basic benefits, standard ambulance cover, daycare procedures', 'active'),
(2, 'HealthSecure Standard', 27999.00, 700000.00, 10, 'Standard balanced protection plan providing comprehensive inpatient and outpatient support.', 'Inpatient treatment, daycare treatments, ambulance support, annual health checkup, pre/post hospitalization', 'active'),
(3, 'HealthSecure Plus', 30500.00, 750000.00, 10, 'Enhanced health protection tier offering higher sum insured and critical illness cover.', 'Extended inpatient care, pre & post hospitalization (60/90 days), critical illness rider, restorative sum insured', 'active'),
(4, 'HealthSecure Family', 31999.00, 1000000.00, 15, 'Family floater health protection offering extended duration and comprehensive pediatric/maternity coverage.', 'Maternity benefits, pediatric care, ICU cover, zero room-rent capping, family floater support', 'active'),
(5, 'HealthSecure Premium', 49999.00, 2000000.00, 20, 'Comprehensive high-tier executive protection with worldwide emergency assistance and zero copays.', 'Zero copay nationwide, worldwide emergency evacuation, unlimited restoration, AYUSH cover, executive wellness suite', 'active'),
(6, 'HealthSecure Starter Shield', 11999.00, 300000.00, 3, 'Pocket-friendly starter health protection plan for young adults and students.', 'Emergency hospitalization, basic OPD consultations, accident cover, 24/7 tele-health helpline', 'active'),
(7, 'HealthSecure SmartCare', 22499.00, 500000.00, 5, 'Balanced health protection tier tailored for young professionals and early-career individuals.', 'Hospitalization, annual preventive wellness checkups, pharmacy vouchers, daycare treatment', 'active'),
(8, 'HealthSecure CriticalCare Rider', 36500.00, 1200000.00, 10, 'Specialized high-severity coverage protecting against 36 major critical illnesses with lump-sum recovery payouts.', '36 critical illnesses covered, lump-sum recovery grant, advanced oncology care, cardiac surgery cover', 'active'),
(9, 'HealthSecure Diabetes Care', 41000.00, 1250000.00, 10, 'Specialized disease management plan covering Type 1 & 2 Diabetes, hypertension, and cardiac care from Day 1.', 'Day-1 pre-existing coverage for diabetes, HbA1c monitoring allowance, dialysis support, cardiovascular cover', 'active'),
(10, 'HealthSecure Senior Protect', 44500.00, 1500000.00, 15, 'Tailored eldercare health protection with reduced waiting periods and comprehensive home hospitalization.', 'Zero pre-policy medical checkup up to age 65, domiciliary hospitalization, AYUSH therapy, companion caregiver allowance', 'active'),
(11, 'HealthSecure Super Elite', 58000.00, 2500000.00, 20, 'High-sum insured elite health shield providing premier private suite accommodations and international second opinions.', 'Private deluxe suite room rent, global medical second opinions, robotic surgery cover, organ donor expenses', 'active'),
(12, 'HealthSecure Imperial Global', 84999.00, 7500000.00, 25, 'Ultra-comprehensive worldwide healthcare protection with unrestricted international hospital access and air ambulance.', 'Global treatment coverage including US/UK/Singapore, international air ambulance, 100% restoration, dedicated medical concierge', 'active'),
(13, 'HealthSecure Student Micro-Shield', 3499.00, 100000.00, 2, 'Ultra-low-cost micro-health protection designed for college students, young gig workers, and first-time policyholders.', 'Accident hospitalization, basic trauma care, 24/7 tele-consultations, emergency ambulance subsidy', 'active'),
(14, 'HealthSecure Arogya Sanjeevani Essential', 5999.00, 200000.00, 3, 'IRDAI-benchmarked standard essential health policy offering clean, capped basic inpatient protection.', 'ICU room cover, basic daycare surgeries, generic pharmacy coverage, zero copay on network hospitals', 'active'),
(15, 'HealthSecure Digital Health OPD Pass', 8499.00, 250000.00, 3, 'Digitally-integrated health policy featuring extensive outpatient (OPD) care, diagnostic allowances, and acute medical cover.', 'Unlimited digital doctor consultations, annual diagnostic tests allowance, dental/vision vouchers, inpatient cover', 'active'),
(16, 'HealthSecure Young Professional Care', 14499.00, 350000.00, 5, 'Dynamic early-career health coverage for young corporate professionals with mental wellness and fitness cashbacks.', 'Stress counseling sessions, preventive annual diagnostics, zero room rent capping on shared rooms, accident cover', 'active'),
(17, 'HealthSecure Bronze Comfort', 16999.00, 400000.00, 5, 'Value-oriented hospitalization plan providing dependable tier-2/3 hospital coverage with low copays.', 'Daycare medical treatments, pre & post hospitalization (30/60 days), road ambulance, restorative sum insured', 'active'),
(18, 'HealthSecure Fit & Active Shield', 24999.00, 600000.00, 7, 'Incentivized wellness coverage rewarding healthy lifestyle habits with premium discounts and gym subscriptions.', 'Fitness tracking rebates, 10% no-claim bonus escalator, complete inpatient care, alternative medicine (AYUSH)', 'active'),
(19, 'HealthSecure Optimum Health Guard', 34200.00, 1000000.00, 10, 'Comprehensive mid-tier shield offering generous room-rent options, modern robot-assisted surgeries, and no copays.', 'Single private AC room, modern robotic treatments, organ donor coverage, emergency road & air assistance', 'active'),
(20, 'HealthSecure Cardio-Pulmonary Care', 38999.00, 1200000.00, 10, 'Tailored health cover designed for individuals with cardiovascular risk, respiratory history, or lifestyle exposures.', 'Heart stent & bypass coverage, pulmonary rehabilitation, specialized angiography vouchers, smoking cessation support', 'active'),
(21, 'HealthSecure Silver Executive', 47000.00, 1500000.00, 15, 'High-grade executive protection plan featuring private suite room entitlements and fast-track cashless claims.', 'Deluxe single room entitlement, priority cashless processing within 30 minutes, executive annual full-body health scan', 'active'),
(22, 'HealthSecure Diamond Global Guard', 67500.00, 3500000.00, 20, 'Ultra-premium international inpatient shield covering major planned surgeries abroad with zero domestic deductible.', 'Planned medical treatments in Europe and Asia-Pacific, international air ambulance, zero copay, personal medical navigator', 'active'),
(23, 'HealthSecure Platinum Pinnacle', 76000.00, 5000000.00, 25, 'High-net-worth comprehensive global medical policy offering top-tier multi-crore sum insured with concierge care.', '₹50 Lakhs sum insured, global second opinion from top US hospitals, air ambulance repatriation, stem cell therapy', 'active'),
(24, 'HealthSecure Ultimate Crore Pati Shield', 96000.00, 10000000.00, 25, 'Flagship ₹1 Crore worldwide health umbrella with zero sub-limits, unlimited sum restoration, and VIP hospital suites.', '₹1 Crore lifetime coverage, unrestricted worldwide hospitals, emergency medical evacuation, zero deductibles globally', 'active')
ON DUPLICATE KEY UPDATE
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
