-- =====================================================================
-- HealthSecure: Advanced Features Migration Script (v2.0)
-- 1. Notifications Table
-- 2. Favorite Plans Table
-- 3. User Language Preference Column
-- =====================================================================

USE health_insurance_db;

-- ---------------------------------------------------------------------
-- 1. Notifications Table (In-App Notification Center)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL DEFAULT 'info',
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notifications_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_notifications_user_read (user_id, is_read),
    INDEX idx_notifications_created (user_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 2. Favorite Plans Table (Saved Insurance Plans for Comparison)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS favorite_plans (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_favorites_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_favorites_plan FOREIGN KEY (plan_id) 
        REFERENCES insurance_plans(plan_id) ON DELETE CASCADE,
    CONSTRAINT uq_user_plan UNIQUE (user_id, plan_id),
    INDEX idx_favorites_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------
-- 3. Add preferred_lang to users table if not exists (MySQL 8.0+)
-- ---------------------------------------------------------------------
-- If preferred_lang does not exist, run:
-- ALTER TABLE users ADD COLUMN preferred_lang VARCHAR(10) NOT NULL DEFAULT 'en';
CALL sys.execute_prepared_stmt('ALTER TABLE users ADD COLUMN preferred_lang VARCHAR(10) NOT NULL DEFAULT \'en\';');
