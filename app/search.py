from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

from app.chef import login_required # the decorator to ensure login
from app.db import get_db

bp = Blueprint("search", __name__)
@bp.route("/search", methods=('GET', 'POST'))
def search():
	filters = ['Title', 'Author', 'Cooktime']
	if request.method == "GET":
		return render_template('search/searchbar.html', filters=filters)

	if request.method == "POST" :
		select_1 = request.form.get('filter')
		select_2 = request.form.get('filter_2')
		input_1 = request.form["form_1"]
		input_2 = request.form.get("form_2")


		error = None

		if error is not None:
			flash(error)
		else:
			db = get_db()
			r = search_request(select_1, select_2, input_1, input_2)
		#return render_template("cookbook/index.html", recipes=r)
		return(str(input_1 + select +  input_2 + select_2))


def search_request():
	db = get_db()
	root_query =  f"""SELECT recipe.id , recipe_name, instructions, create_date, author_id, username FROM recipe"""

	if select_1 != "":
		if select_1 == "Title":
			

	recipe = db.execute(query).fetchall()

	if recipe is None:
		abort(404, f"Recipe name {recipe_name} doesn't exist.") # Not Found

	return recipe