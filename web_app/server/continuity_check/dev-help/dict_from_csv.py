import numpy as np
import os
from mysql.connector import (connection)
host = 'localhost'
user = 'cdms'
pw = 'cdms'
db = 'CDMSTest'

dir_path = os.getcwd()
data = np.genfromtxt(dir_path+'/channel_naming.csv',delimiter=',',dtype=str)
conn = connection.MySQLConnection(
    user=user,
    password=pw,
    host=host,
    database=db)
cursor=conn.cursor()
for i in data:
    ins_form = """
        INSERT INTO
            channel_naming (
                VIB_Name,
                Signal_Name)
        VALUES
            (
            "{vib}",
            "{sig_1}"
            );
        """
    insert_data = ins_form.format(vib=i[0],sig_1=i[1])
    cursor.execute(insert_data)
conn.commit()
conn.close()
        

