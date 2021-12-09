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
    """Show all the posts, most recent first."""
    db = get_db()
    query = """SELECT post.id, title, body, created, author_id, username
            FROM post JOIN user ON post.author_id = user.id
            ORDER BY created DESC"""
    posts = db.execute(query).fetchall() # will be a list of all Rows
    return render_template("cookbook/index.html", posts=posts)


def get_my_post(id):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
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