"""Tests for Blogly app."""

from unittest import TestCase

from app import app
from models import db, User


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost/blogly_test"
app.config["SQLALCHEMY_ECHO"] = False
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


with app.app_context():
    db.drop_all()
    db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for user routes."""

    def setUp(self):
        """Add sample user."""

        with app.app_context():
            User.query.delete()

            user = User(
                first_name="Ava",
                last_name="Rose",
                image_url="https://www.freeiconspng.com/uploads/profile-icon-9.png"
            )

            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

        self.client = app.test_client()

    def tearDown(self):
        """Clean up after each test."""

        with app.app_context():
            db.session.rollback()

    def test_redirect_homepage(self):
        """Test homepage redirects to users list."""

        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/users")

    def test_users_list(self):
        """Test users list page."""

        response = self.client.get("/users")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ava", html)
        self.assertIn("Rose", html)

    def test_new_user_form(self):
        """Test new user form page."""

        response = self.client.get("/users/new")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Add User", html)

    def test_user_detail(self):
        """Test user detail page."""

        response = self.client.get(f"/users/{self.user_id}")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ava", html)
        self.assertIn("Edit", html)

    def test_create_user(self):
        """Test creating a new user."""

        response = self.client.post(
            "/users/new",
            data={
                "first_name": "Cody",
                "last_name": "Rose",
                "image_url": ""
            },
            follow_redirects=True
        )

        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cody", html)