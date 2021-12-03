-- Initialize the database.
-- Drop any existing data and create empty tables.
-- This just happens once when the app is first created
-- so data persists between users and sessions.

DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL
);


CREATE TABLE recipes(
  recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_name TEXT UNIQUE NOT NULL,
  author_id tTEXT UNIQUE NOT NUL);
