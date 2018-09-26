import numpy as np
from sql_formatter import *
from mysql.connector import (connection)

default_log = "RunHistory"
local_database = "CDMSTest"
local_user = 'cdms'
local_pass = 'cdms'
local_host = 'localhost'


def write_check(data,
        institution,
        vib,
        wiring,
        device,
        temp,
        validation_table):
    # attempt connection to sql database, exit if failure.
    try:
        conn = connection.MySQLConnection(
            user = local_user,
            password=local_pass,
            host=local_host,
            database=local_database)
        cursor = conn.cursor()
    except Exception as e:
        return "Unable to connect to SQL Database! Error: "+str(e)
    while True:
        try:
            # Create New Table
            create_table,table_name = format_check_table()
            cursor.execute(create_table)
            
            #Log creation of table
            log_table = format_log_row(
                    default_log,
                    table_name,
                    institution,
                    vib,
                    wiring,
                    temp,
                    validation_table)
            cursor.execute(log_table)
        except Exception as e:
            print(str(e))
            continue
        
   # Write data to new table
    for d in data:
       enter_d = format_check_row(table_name,
               d[0],d[1],d[2],d[3],d[4],d[5],d[6])
       cursor.execute(enter_d)
    # Commit Changes, exit
    conn.commit()
    conn.close()
    return "Sucess! Data written to: "+table_name
