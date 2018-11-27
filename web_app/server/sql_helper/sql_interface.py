from MySQLdb import connect
from sql_helper.sql_formatter import *
from sql_helper.gen_testing_data import *


# TODO: Make this operate as a class, rather than a series of functions to cut down on number of database connections
default_log = "continuity_history"
local_database = "database"
local_user = 'cdms'
local_pass = 'cdms'
local_host = 'localhost'
def get_vib_signal_dict():
    try:
        conn =connect(
            user=local_user,
            password=local_pass,
            host=local_host,
            database = local_database)
        cursor=conn.cursor()
    except Exception  as e:
        print("Failed to connect to database! Error: "+str(e))
        return "Failure"
    command = """
        SELECT
            Matrix_location, DB_78_pin, VIB_pin, Signal_name 
        FROM 
            channel_naming;
    """
    cursor.execute(command)
    data=cursor.fetchall()
    conn.close()
    return data
    
def get_validation_request(expected_table='',test_rows=[{}]):
    try:
        conn = connection.MySQLConnection(
            user=local_user,
            password = local_pass,
            host=local_host,
            database = local_database)
        cursor=conn.cursor()
    except Exception  as e:
        print("Failed to connect to database! Error: "+str(e))
        return "Failure"

    if not expected_table:
        expected_table = 'slac_expected_values'
    if not test_rows:
        0==0
    command = format_validation_request(expected_table,test_rows)
    cursor.execute(command)
    result = cursor.fetchall()
    return result

def get_check(tablename):
    # Try to connect to server, log result in server if failure.
    try:
        conn = connection.MySQLConnection(
            user = local_user,
            password=local_pass,
            host=local_host,
            database=local_database)
        cursor = conn.cursor()
    except Exception as e:
        print("Unable to connect to SQL Database! Error: "+str(e))
        return "failure"

    command = format_get_check(tablename)
    
    cursor.execute(command)
    data=cursor.fetchall()
    conn.close()
    return data 

def get_runs():
    try:
        conn = connection.MySQLConnection(
                user = local_user,
                password = local_pass,
                host = local_host,
                database = local_database)
        cursor=conn.cursor()
    except Exception as e:
        print("Unable to connect to SQL Database! Error:"+str(e))
        return "failure"
    cursor.execute('SELECT Date, Institution, VIB, Wiring, Device, Temperature, Validator, Check_name FROM '+default_log)
    data=cursor.fetchall()
    conn.close()
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


    # Try to connect to server, log result in server if failure.
    try:
        conn = connection.MySQLConnection(
            user = local_user,
            password=local_pass,
            host=local_host,
            database=local_database)
        cursor = conn.cursor()
    except Exception as e:
        print("Unable to connect to SQL Database! Error: "+str(e))
        return "failure"

    # Randomly generate 10-character string to serve as relation between individual run and table of runs
    # This information won't be exposed to the user, it serves purely as an internal method of organizing our database.
    # Should allow at least two million continuity checks before any speed-related problems arise.
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
               d['signal_1'],
               d['signal_2'],
               d['min'],
               d['max'],
               d['measured'],
               "Ohm",
               d['passing']
               )
       cursor.execute(enter_d)
    # Commit Changes, exit
    conn.commit()
    conn.close()
    return "Sucess! Data written to: "+table_name

