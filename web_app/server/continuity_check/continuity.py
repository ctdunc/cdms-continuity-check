import numpy as np
import sys
sys.path.append("../")
from sql_helper.sql_interface import *


def perform_check(expected_table='',tests=[],channels=[]):
    # reads in expected values of check, converts to numpy ndarray
    expected_values = get_validation_request(expected_table,tests)
    expected_datatype = np.dtype('U20,U20,b,float,float')
    expected_values = np.array(expected_values,expected_datatype)
    return expected_values 

