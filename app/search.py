from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

from app.chef import login_required # the decorator to ensure login
from app.db import get_db

bp = Blueprint("search", __name__)
@bp.route("/search", methods=('GET', 'POST'))
def search():
	if request.method == "GET":
		return render_template('search/searchbar.html')

	if request.method == "POST" :
		recipe_name = request.form["title"]
		error = None

		if error is not None:
			flash(error)
		else:
			db = get_db()
			r = title_request(recipe_name)
		return render_template("cookbook/index.html", recipes=r)



def title_request(recipe_name):
	db = get_db()
	query = """SELECT recipe.id , recipe_name, instructions, create_date, author_id, username FROM recipe JOIN user ON recipe.author_id = user.id WHERE recipe_name = ? ORDER BY create_date DESC"""
	recipe = db.execute(query, (recipe_name,)).fetchall()

	if recipe is None:
		abort(404, f"Recipe name {recipe_name} doesn't exist.") # Not Found

	return recipe