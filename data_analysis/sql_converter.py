import numpy as np
import pandas as pd
from mysql.connector import (connection)

conn = connection.MySQLConnection(user='cdms', password='cdms', host='localhost', database='CDMSTest')
cursor = conn.cursor()
expected_file = './expected_result'
expected_result = np.genfromtxt(
        expected_file,
        names=True,
        dtype=[
            ('Signal_1','|U20'),
            ('Signal_2','|U20'),
            ('Expected_Continuity','|U8'),
            ('min',float),
            ('max',float)
            ]
        )

for r in expected_result:
    format_str="""INSERT INTO continuity_prediction (signal_1, signal_2, expected_continuity, min, max)
        VALUES ("{sig1}","{sig2}","{exp_cont}","{min}","{max}");"""
    if r[2].startswith('Dis'):
        r[2]=False
    else: 
        r[2]=True
    
    sql_command = format_str.format(sig1=r[0],sig2=r[1],exp_cont=r[2],min=r[3],max=r[4])
    cursor.execute(sql_command)
conn.commit()
conn.close()
