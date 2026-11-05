import os
import sys
import unittest
import io

os.environ["FLASK_ENV"] = "testing"
from werkzeug.security import generate_password_hash
from app import app, db, User, Prediction, InsurancePlan, Notification, FavoritePlan, build_prediction_pdf_buffer
from email_service import send_prediction_report_email, is_valid_email
from translations import get_text, TRANSLATIONS

class TestFiveAdvancedFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

        with app.app_context():
            test_user = User.query.filter_by(email="user@healthsecure.com").first()
            if not test_user:
                test_user = User(
                    name="Demo Member",
                    email="user@healthsecure.com",
                    password_hash=generate_password_hash("User@123"),
                    preferred_lang="en"
                )
                db.session.add(test_user)
                db.session.commit()
            cls.user_id = test_user.id
            cls.user_email = test_user.email
            cls.user_name = test_user.name

            pred = Prediction.query.filter_by(user_id=cls.user_id).first()
            if not pred:
                pred = Prediction(
                    user_id=cls.user_id,
                    full_name="Demo Member",
                    age=30,
                    sex="male",
                    bmi=24.5,
                    height=175.0,
                    weight=75.0,
                    children=1,
                    smoker="no",
                    liquor="no",
                    region="southwest",
                    salary=600000.0,
                    policy_duration=5,
                    plan_category="silver",
                    estimated_premium=15500.0,
                    estimated_benefit=93000.0,
                    premium_income_ratio=2.58,
                    benefit_factor=1.2,
                    recommendation="Recommended Silver Plan"
                )
                db.session.add(pred)
                db.session.commit()
            cls.prediction_id = pred.id

            plan = InsurancePlan.query.first()
            cls.test_plan_id = plan.plan_id if plan else 1

    def login(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.user_id
            sess["user_name"] = self.user_name
            sess["user_role"] = "consumer"
            sess["lang"] = "en"

    # =========================================================================
    # FEATURE 1: Email Prediction Reports Tests
    # =========================================================================
    def test_01_email_validation(self):
        self.assertTrue(is_valid_email("user@example.com"))
        self.assertTrue(is_valid_email("test.name+tag@sub.domain.co.in"))
        self.assertFalse(is_valid_email("invalid-email"))
        self.assertFalse(is_valid_email("user@.com"))
        self.assertFalse(is_valid_email(""))

    def test_02_pdf_generation_buffer(self):
        with app.app_context():
            pred = db.session.get(Prediction, self.prediction_id)
            user = db.session.get(User, self.user_id)
            pdf_buf = build_prediction_pdf_buffer(pred, user)
            self.assertIsNotNone(pdf_buf)
            pdf_bytes = pdf_buf.getvalue()
            self.assertGreater(len(pdf_bytes), 1000)
            self.assertTrue(pdf_bytes.startswith(b"%PDF"))

    def test_03_email_service_dispatch(self):
        dummy_pdf = b"%PDF-1.4 mock pdf data for testing"
        success, msg = send_prediction_report_email(
            recipient_email=self.user_email,
            recipient_name=self.user_name,
            pdf_bytes=dummy_pdf,
            prediction_id=self.prediction_id,
            filename="Test_Report.pdf"
        )
        self.assertTrue(success, f"Email sending failed: {msg}")
        self.assertTrue(any(word in msg.lower() for word in ["dispatched", "simulated", "generated", "email"]))

    def test_04_email_prediction_route(self):
        self.login()
        res = self.client.post(
            f"/prediction/{self.prediction_id}/email",
            json={"email": self.user_email},
            headers={"X-Requested-With": "XMLHttpRequest"}
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("message", data)

        with app.app_context():
            notif = Notification.query.filter_by(user_id=self.user_id, notification_type="report_email").order_by(Notification.created_at.desc()).first()
            self.assertIsNotNone(notif)
            self.assertIn("Report Emailed", notif.title)

    # =========================================================================
    # FEATURE 2: Notifications System Tests
    # =========================================================================
    def test_05_notifications_view_page(self):
        self.login()
        res = self.client.get("/notifications")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Notifications", res.data)

    def test_06_notifications_unread_api(self):
        self.login()
        res = self.client.get("/api/notifications/unread-count")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["unread_count"], int)

    def test_07_mark_notification_read_and_delete(self):
        self.login()
        with app.app_context():
            n = Notification(
                user_id=self.user_id,
                title="Test Alert",
                message="Testing notification mark read and delete",
                notification_type="general",
                is_read=False
            )
            db.session.add(n)
            db.session.commit()
            n_id = n.notification_id

        # Mark read via AJAX
        res = self.client.post(f"/notifications/{n_id}/read", headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

        with app.app_context():
            n = db.session.get(Notification, n_id)
            self.assertTrue(n.is_read)

        # Delete via AJAX
        res = self.client.post(f"/notifications/{n_id}/delete", headers={"X-Requested-With": "XMLHttpRequest"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

        with app.app_context():
            n = db.session.get(Notification, n_id)
            self.assertIsNone(n)

    # =========================================================================
    # FEATURE 3: Multi-Language User Interface Tests
    # =========================================================================
    def test_08_translations_dictionary_and_fallbacks(self):
        self.assertEqual(get_text("nav_dashboard", "en"), "Dashboard")
        self.assertEqual(get_text("nav_dashboard", "ta"), TRANSLATIONS["nav_dashboard"]["ta"])
        self.assertEqual(get_text("nav_dashboard", "hi"), TRANSLATIONS["nav_dashboard"]["hi"])

        # Fallback to English when key missing
        self.assertEqual(get_text("non_existent_key_xyz", "ta", default="Fallback Val"), "Fallback Val")
        # Ensure notif_title exists
        self.assertEqual(get_text("notif_title", "en"), "Notifications Center")

    def test_09_set_language_routes(self):
        self.login()
        # Set Tamil
        res = self.client.get("/set-language/ta", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("lang"), "ta")

        # Set Hindi
        res = self.client.get("/set-language/hi", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("lang"), "hi")

        # Set English
        res = self.client.get("/set-language/en", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get("lang"), "en")

    # =========================================================================
    # FEATURE 4: Saved / Favorite Insurance Plans Tests
    # =========================================================================
    def test_10_toggle_favorite_plan(self):
        self.login()
        plan_id = self.test_plan_id

        # Clean existing favorite if any
        with app.app_context():
            existing = FavoritePlan.query.filter_by(user_id=self.user_id, plan_id=plan_id).first()
            if existing:
                db.session.delete(existing)
                db.session.commit()

        # First toggle -> Add to favorites
        res = self.client.post(f"/favorites/toggle/{plan_id}")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertTrue(data["is_favorite"])

        # Second toggle -> Remove from favorites
        res = self.client.post(f"/favorites/toggle/{plan_id}")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertFalse(data["is_favorite"])

        # Toggle back to true for favorites page test
        res = self.client.post(f"/favorites/toggle/{plan_id}")
        self.assertTrue(res.get_json()["is_favorite"])

    def test_11_favorites_page_and_remove(self):
        self.login()
        res = self.client.get("/favorites")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Favorite", res.data)

        # Remove favorite via POST /favorites/remove/<id>
        res = self.client.post(f"/favorites/remove/{self.test_plan_id}", follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        with app.app_context():
            fav = FavoritePlan.query.filter_by(user_id=self.user_id, plan_id=self.test_plan_id).first()
            self.assertIsNone(fav)

    # =========================================================================
    # FEATURE 5: Dark Mode / Light Mode Assets & Pages Tests
    # =========================================================================
    def test_12_theme_assets_exist(self):
        theme_js_path = os.path.join(app.root_path, "static", "js", "theme.js")
        self.assertTrue(os.path.exists(theme_js_path))
        with open(theme_js_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("toggleTheme", content)
        self.assertIn("data-theme", content)
        self.assertIn("localStorage", content)

    def test_13_all_key_views_render_200(self):
        self.login()
        routes = [
            "/",
            "/dashboard",
            "/predict",
            "/history",
            "/what-if",
            "/plans",
            "/compare-plans",
            "/favorites",
            "/notifications",
            "/profile",
            f"/result/{self.prediction_id}",
            f"/prediction/{self.prediction_id}",
            f"/plan/{self.test_plan_id}"
        ]
        for r in routes:
            res = self.client.get(r)
            self.assertEqual(res.status_code, 200, f"Route {r} failed with status {res.status_code}")

if __name__ == "__main__":
    unittest.main()
