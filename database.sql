-- Optional MySQL database initialization.
CREATE DATABASE IF NOT EXISTS insurance_premium_db;
USE insurance_premium_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS prediction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    age INT NOT NULL,
    sex VARCHAR(10) NOT NULL,
    bmi DECIMAL(5,2) NOT NULL,
    children INT NOT NULL,
    smoker VARCHAR(5) NOT NULL,
    region VARCHAR(20) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    salary DECIMAL(12,2) NOT NULL,
    policy_duration INT NOT NULL DEFAULT 5,
    plan_category VARCHAR(20) NOT NULL DEFAULT 'silver',
    recommendation VARCHAR(255) NOT NULL,
    estimated_benefit DECIMAL(12,2) NOT NULL,
    estimated_premium DECIMAL(12,2) NOT NULL,
    created_at DATETIME NOT NULL,
    CONSTRAINT fk_prediction_user FOREIGN KEY (user_id) REFERENCES users(id)
);
