import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

# every auth route has the prefix below
bp = Blueprint("chef", __name__, url_prefix="/chef")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: # if no one is logged in, redirect
            return redirect(url_for("chef.login"))

        return view(**kwargs) # otherwise continue showing the view they asked for

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    # put the user in the g namespace to prevent needing to do SELECT all the time
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"] # like request.form.get("username")
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not firstname:
            error = "Firstname is required"
        elif not lastname:
            error = "Lastname is required"
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute("INSERT INTO user (firstname, lastname, username, password) VALUES (? , ? , ?, ?)",
                    (firstname,lastname,username, generate_password_hash(password)))
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("chef.login"))

        flash(error) # shows up on the base.html template to show errors

    return render_template("chef/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("cookbook.index"))

        flash(error)

    return render_template("chef/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("cookbook.index"))
