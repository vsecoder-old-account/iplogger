import sqlite3

db = sqlite3.connect('database.db')
sql = db.cursor()

logs = """
CREATE TABLE "logs" (
	"id"	INTEGER NOT NULL UNIQUE,
	"url"	TEXT,
	"data"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id")
);
"""

sql.execute(logs)

db.commit()