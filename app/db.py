import sqlite3

import click # command line interface for flask

from flask import current_app
from flask import g
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g: # see if the db is loaded into the g namespace to use
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None) # remove it from the namespace

    if db is not None:
        db.close() # explicitly close it


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

        # read from the schema to reset & create the tables
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    query_insert1 = """INSERT INTO cooktime
                          (cooktime) 
                           VALUES 
                          ('less than five minutes')"""
    db.execute(query_insert1)
    query_insert2 = """INSERT INTO cooktime
                          (cooktime) 
                           VALUES 
                          ('thirty minutes')"""
                          
    db.execute(query_insert2)
    query_insert3 = """INSERT INTO cooktime
                          (cooktime) 
                           VALUES 
                          ('an hour')"""
    db.execute(query_insert3)

    db.commit()





# so we can call "flask init-db" to create the database from command line
@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

# so the app knows what to do with the database
def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)