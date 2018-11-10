import datetime
import random
import string
# TODO: make this into a class that can be called

def format_validation_request(expected_table,test_rows=[{}]):
    request_format="""
        SELECT
            Signal_1,
            Signal_2,
            Expected_Continuity,
            Minimum,
            Maximum
        FROM
            {table}
        WHERE
            {conditions}
        """
    if not test_rows:
        row_selector = "1=1"
    else:
        first_up = True
        search = ""
        for test in test_rows:
            if first_up:
                search+="("
                first_up=False
            else:
                search+=" OR ("
            first = True
            for key,condition in test.items():
                if first:
                    search_string = str(key)+"=\""+str(condition)+"\""
                    first = False
                else:
                    search_string = "AND "+str(key)+"=\""+str(condition)+"\""
                search+=search_string
            search+=") "
        row_selector=search
    returned_request = request_format.format(table=expected_table,conditions=row_selector)
    return returned_request
                
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
            Validator,
            Date)
        VALUES (
            "{cname}",
            "{inst}",
            "{vi_b}",
            "{wire}",
            "{dev}",
            "{temperature}",
            "{validator}",
            "{timestamp}"
        );
    """
    log_formatted = log_format.format(
            log=log_table_name,
            cname=check_table_name,
            inst=institution,
            vi_b=vib,
            wire=wiring,
            dev=device,
            temperature=temp,
            validator=validation_table,
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %X'))
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
        Unit VARCHAR(50),
        Pass BIT);
        """
    return [creation_format.format(tname=table_name),table_name]

def format_check_row(table, sig_1, sig_2, minimum, maximum, measured,unit,passed):
    if passed:
        passed = 1
    else:
        passed = 0
    insertion_format =""" 
        INSERT INTO
        {tabl} (
            Signal_1,
            Signal_2,
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
            passing=passed)
def format_get_check(tablename):
    get_format="""
        SELECT
            Signal_1,
            Signal_2,
            Minimum,
            Maximum,
            Measured,
            Unit,
            Pass
        FROM
            {table};
    """
    return get_format.format(table=tablename)

def format_get_expect(tablename):
    get_format="""
        SELECT
            Signal_1,
            Signal_2,
            Expected_Continuity,
            Minimum,
            Maximum
        FROM
            {table};
        """
    return get_format.format(table=tablename)
