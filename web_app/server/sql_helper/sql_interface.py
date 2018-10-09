from sql_helper.sql_formatter import *
from sql_helper.gen_testing_data import *
from mysql.connector import (connection)

default_log = "RunHistory"
local_database = "CDMSTest"
local_user = 'cdms'
local_pass = 'cdms'
local_host = 'localhost'

def get_check(tablename):
    try:
        conn = connection.MySQLConnection(
            user = local_user,
            password=local_pass,
            host=local_host,
            database=local_database)
        cursor = conn.cursor()
    except Exception as e:
        return "Unable to connect to SQL Database! Error: "+str(e)

    command = format_get_check(tablename)
    
    cursor.execute(command)
    data=cursor.fetchall()
    return data 
def write_check(data,
        institution,
        vib,
        wiring,
        device,
        temp,
        validation_table):
    # IMPORTANT: Remember, data needs to have the format of 
    # [Signal 1, Signal 2, Minimum, Maxmimum, Measured, Unit, Pass?]
    # IF IT IS NOT PASSED to the function in this order, data may be written to the table incorrectly.
    # Eventually, this should only take in pandas.dataframe objects, with an appropriate check for proper field names.
    try:
        conn = connection.MySQLConnection(
            user = local_user,
            password=local_pass,
            host=local_host,
            database=local_database)
        cursor = conn.cursor()
    except Exception as e:
        return "Unable to connect to SQL Database! Error: "+str(e)

    # attempt connection to sql database, exit if failure.
       # Randomly generate 10-character string to serve as relation between individual run and table of runs.
    # This information won't be exposed to the user, it serves purely as an internal method of organizing our database.
    # Should allow at least two million continuity checks before any speed-related problems arise,
    # but making this number larger is a trivial task that we can do later, if need be.
    exist_check = "SHOW TABLES LIKE '{name}'"
        
    # Create New Table
    create_table,table_name = format_check_table()
    print(cursor.execute(exist_check.format(name=table_name)))
    exists = cursor.fetchone()
    cursor.execute(create_table)
    
    #Log creation of table
    log_table = format_log_row(
            default_log,
            table_name,
            institution,
            vib,
            wiring,
            device,
            temp,
            validation_table)
    cursor.execute(log_table)
    # When SQL returns an error (i.e. the table name is already taken), 
    # the program generates a new name, and tries again
        
   # Write data to new table
    for d in data:
       enter_d = format_check_row(table_name,
               d[0],d[1],d[2],d[3],d[4],d[5],d[6])
       cursor.execute(enter_d)
    # Commit Changes, exit
    conn.commit()
    conn.close()
    return "Sucess! Data written to: "+table_name

    
