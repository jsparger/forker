-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS version;

CREATE TABLE version (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  parent INTEGER NOT NULL,
  content TEXT NOT NULL
);

INSERT INTO version (id, parent, content) VALUES (0, 0, '{}');
