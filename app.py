"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

if __name__ == "__main__":
    app.run(debug=True)