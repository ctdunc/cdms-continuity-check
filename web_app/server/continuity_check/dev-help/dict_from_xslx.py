import pandas as pd
import os
from MySQLdb import connect
dir_path = os.getcwd()
host = 'localhost'
user = 'cdms'
pw = 'cdms'
db = 'continuity_check'

data = pd.read_excel(dir_path+'/Continuity_PCB.xlsx')
conn = connect(
    user=user,
    password=pw,
    host=host,
    database=db)
cursor=conn.cursor()
print(data)
# DB 78 pin VIB pin  Signal name  Notes

for index,row in data.iterrows():
    str_input = """INSERT INTO channel_naming
    (Matrix_location, DB_78_pin, VIB_pin, Signal_name)
    VALUES
        ("{matr}", "{dpin}", "{vibpin}", "{sign}");
        """
    execute = str_input.format(matr=row["Matrix location"],dpin=row["DB 78 pin"],vibpin=row["VIB pin"],sign=row["Signal name"])
    cursor.execute(execute)
conn.commit()
conn.close()

