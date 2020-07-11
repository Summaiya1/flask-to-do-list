import sqlite3

connection = sqlite3.connect('Database.db',check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
   """ CREATE TABLE users(
       pk INTEGER PRIMARY KEY AUTOINCREMENT,
       username VARCHAR(16),
       password VARCHAR(32),
       email NVARCHAR(320)
   );""")

cursor.execute(
    """ CREATE TABLE list(
        listId INTEGER PRIMARY KEY AUTOINCREMENT,
        listName VARCHAR(16),
        UserId INTEGER FOREIGNKEY REFERENCES users(pk)
        )"""
)

cursor.execute(
    """ CREATE TABLE listTasks(
        taskId INTEGER PRIMARY KEY AUTOINCREMENT,
        taskName VARCHAR(16),
        listId INTEGER FOREIGNKEY REFERENCES list(listId)
        ) """
)
connection.commit()
cursor.close()
connection.close()
