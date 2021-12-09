from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

from app.chef import login_required # the decorator to ensure login
from app.db import get_db

# group together related parts of the app
bp = Blueprint("cookbook", __name__)

# main route to show all posts
@bp.route("/")
def index():
    db = get_db()
    query = """SELECT post.id, title, body, created, author_id, username
            FROM post JOIN user ON post.author_id = user.id
            ORDER BY created DESC"""
    posts = db.execute(query).fetchall() # will be a list of all Rows
    return render_template("cookbook/index.html", posts=posts)

def get_my_post(id):
    db = get_db()
    query = """SELECT post.id, title, body, created, author_id, username
            FROM post JOIN user ON post.author_id = user.id
            WHERE post.id = ?"""
    post = db.execute(query, (id,)).fetchone()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.") # Not Found

    if post["author_id"] != g.user["id"]:
        abort(403) # Forbidden

    return post

@bp.route("/add", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query = "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)"
            db.execute(query, (title, body, g.user["id"]))
            db.commit()
            #return redirect(url_for("cookbook.index"))

    return render_template("cookbook/add.html")