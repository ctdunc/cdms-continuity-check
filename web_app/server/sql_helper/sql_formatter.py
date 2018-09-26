import datetime
import random
import string

def format_log_row(log_table_name,
        check_table_name,
        institution,
        vib,
        wiring,
        device,
        temp,
        validation_table):
    log_format = """
        INSERT INTO
        {log} (
            Check_name,
            Institution,
            VIB,
            Wiring,
            Device,
            Temperature,
            Validation_table)
        VALUES (
            "{cname}",
            "{inst}",
            "{vi_b}",
            "{wire}",
            "{dev}",
            "{temperature}",
            "{validator}"
        );
    """
    log_formatted = log_format.format(
            log=log_table_name,
            inst=institution,
            vi_b=vib,
            wire=wiring,
            dev=device,
            temperature=temp,
            validator=validation_table)
    return log_formatted

def format_check_table():
    characters = string.ascii_letters
    table_name = "".join(random.choice(characters) for x in range(10))
    creation_format = """
        CREATE TABLE IF NOT EXISTS
        {tname} (
        Signal_1 VARCHAR(50),
        Signal_2 VARCHAR(50),
        Minimum FLOAT,
        Maximum FLOAT,
        Measured FLOAT,
        Unit VARCHAR(20),
        Pass BIT);
        """
    return [creation_format.format(tname=table_name),table_name]

def format_check_row(table, sig_1, sig_2, minimum, maximum, measured,unit,passed):
    insertion_format =""" 
        INSERT INTO
        {tabl} (
            Signal 1,
            Signal 2,
            Minimum,
            Maximum,
            Measured,
            Unit,
            Pass)
        VALUES (
            "{sig1}",
            "{sig2}",
            "{min}",
            "{max}",
            "{measure}",
            "{unitt}",
            "{passing}"
            );
    """
    return insertion_format.format(
            tabl=table,
            sig1=sig_1,
            sig2=sig_2,
            min=minimum,
            max=maximum,
            measure=measured,
            unitt=unit,
            passing=passed
