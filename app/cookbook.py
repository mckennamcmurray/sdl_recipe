from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

from app.chef import login_required # the decorator to ensure login
from app.db import get_db

# group together related parts of the app
bp = Blueprint("cookbook", __name__)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    recipe = get_my_post(id)
    if request.method == "POST":
        db = get_db()

        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query = "UPDATE recipe SET recipe_name = ?, instructions = ? WHERE id = ?"
            db.execute(query, (title, body, id))
            db.commit()
            return redirect(url_for("cookbook.index"))

    return render_template("cookbook/update.html", post=post)


# main route to show all posts
@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    query = """SELECT recipe.id , recipe_name, instructions, create_date, author_id, username
            FROM recipe JOIN user ON recipe.author_id = user.id
            ORDER BY create_date DESC"""
    recipe = db.execute(query).fetchall() # will be a list of all Rows
    return render_template("cookbook/index.html", recipes=recipe)


@bp.route("/add", methods=("GET", "POST"))
@login_required
def create():

    if request.method == "POST":
        db = get_db()
        cooktime_list = db.execute("SELECT * FROM cooktime order by cooktime")
        print(cooktime_list)
        title = request.form["title"]
        body = request.form["body"]
        #cooktime = request.form[]
        ctime = list(request.form.keys())[2]
        error = None


        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query = "INSERT INTO recipe (recipe_name, instructions, author_id, cooktime_id) VALUES (?, ?, ?, ?)"
            db.execute(query, (title, body, g.user["id"], ctime))
            db.commit()
            return redirect(url_for("cookbook.index"))
    else: # GET REQEUST
        db = get_db()
        cooktime_list = db.execute("SELECT * FROM cooktime order by cooktime_id").fetchall()
        return render_template("cookbook/add.html", cooktime_list = cooktime_list)
