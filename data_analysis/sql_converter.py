import sqlite3 as sql
import numpy as np
import pandas as pd
connection = sql.connect("expected_result.db")
cursor = connection.cursor()
expected_file = 'expected_result'

expected_result = np.genfromtxt(
        expected_file,
        names=True,
        dtype=[
            ('Signal_1','|S10'),
            ('Signal_2','|S10'),
            ('Expected_Continuity','|S10'),
            ('min',float),
            ('max',float)
            ]
        )

sql_command = """
CREATE TABLE continuity_prediction (
signal_1 VARCHAR(20),
signal_2 VARCHAR(20),
expected_continuity VARCHAR(20),
min FLOAT,
max FLOAT
);"""

cursor.execute(sql_command)

for r in expected_result:
        format_str="""INSERT INTO continuity_prediction (signal_1, signal_2, expected_continuity, min, max)
        VALUES ("{sig1}","{sig2}","{exp_cont}","{min}","{max}");"""

        sql_command = format_str.format(sig1=r[0],sig2=r[1],exp_cont=r[2],min=r[3],max=r[4])
        cursor.execute(sql_command)
connection.commit()
connection.close()
