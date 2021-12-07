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

CREATE TABLE recipe(
  recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_name TEXT UNIQUE NOT NULL,
  author_id TEXT UNIQUE NOT NULL,
  cooktime_id TEXT UNIQUE NOT NULL,
  );

CREATE TABLE ingredients(
  ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
  ingredient_name TEXT UNIQUE NOT NULL,
  ingredient_calories TEXT UNIQUE NOT NUL
  );

CREATE TABLE cooktime(
  cooktime_id INTEGER PRIMARY KEY AUTOINCREMENT,
  cooktime TEXT UNIQUE NOT NULL,
  );

CREATE TABLE tag(
  tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_name TEXT UNIQUE NOT NULL,
  );

CREATE TABLE recipe_ingredients(
  recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
  ingredient_id TEXT UNIQUE NOT NULL,
  ingredient_amount TEXT UNIQUE NOT NULL,
  );

CREATE TABLE recipe_tag(
  recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_id TEXT UNIQUE NOT NULL,
  ingredient_amount TEXT UNIQUE NOT NULL,
  );
