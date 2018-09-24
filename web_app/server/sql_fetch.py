import sqlite3 as sql
connection = sql.connect("expected_result.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM continuity_prediction")
result = cursor.fetchall()
print(result)
