"""Tests for Blogly app."""

from unittest import TestCase

from app import app
from models import db, User, Post


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost/blogly_test"
app.config["SQLALCHEMY_ECHO"] = False
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


with app.app_context():
    db.drop_all()
    db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for user and post routes."""

    def setUp(self):
        """Add sample user."""

        with app.app_context():
            Post.query.delete()
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
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_users_list(self):
        response = self.client.get("/users")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ava", html)
        self.assertIn("Rose", html)

    def test_new_user_form(self):
        response = self.client.get("/users/new")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Add User", html)

    def test_user_detail(self):
        response = self.client.get(f"/users/{self.user_id}")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Ava", html)
        self.assertIn("Edit", html)

    def test_create_user(self):
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

    def test_new_post_form(self):
        response = self.client.get(f"/users/{self.user_id}/posts/new")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Add Post", html)

    def test_create_post(self):
        response = self.client.post(
            f"/users/{self.user_id}/posts/new",
            data={
                "title": "Test Post",
                "content": "This is a test post."
            },
            follow_redirects=True
        )

        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Post", html)

    def test_post_detail(self):
        with app.app_context():
            post = Post(
                title="Hello",
                content="Post content",
                user_id=self.user_id
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.get(f"/posts/{post_id}")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello", html)
        self.assertIn("Post content", html)

    def test_delete_post(self):
        with app.app_context():
            post = Post(
                title="Delete Me",
                content="Delete content",
                user_id=self.user_id
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.post(
            f"/posts/{post_id}/delete",
            follow_redirects=True
        )

        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Delete Me", html)