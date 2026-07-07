"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "secret"

toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route("/")
def root():
    return redirect("/users")

@app.route("/users")
def list_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def new_users_form():
    return render_template("new_user.html")

@app.route("/users/new", methods=["POST"])
def create_user():
    new_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["image_url"] or None,
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"] or user.image_url

    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("new_post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = request.form.getlist("tags")

    post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user_id=user.id
    )

    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("edit_post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tag_ids = request.form.getlist("tags")

    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/tags")
def list_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_detail.html", tag=tag)


@app.route("/tags/new")
def new_tag_form():
    return render_template("new_tag.html")


@app.route("/tags/new", methods=["POST"])
def create_tag():
    tag = Tag(name=request.form["name"])

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form["name"]
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

if __name__ == "__main__":
    app.run(debug=True)


