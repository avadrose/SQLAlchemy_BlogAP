"""Models for Blogly."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(
        db.Text,
        nullable=False,
        default="https://www.freeiconspng.com/uploads/profile-icon-9.png"
    )

    posts = db.relationship(
        "Post",
        backref="user",
        cascade="all, delete-orphan"
    )


class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    tags = db.relationship(
        "Tag", 
        secondary="posts_tags",
        backref="posts"
    )

class Tag(db.Model):
    """Tag model."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)


class PostTag(db.Model):
    """PostTag model."""

    __tablename__ = "posts_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True
    )