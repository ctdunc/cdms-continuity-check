import numpy as np
import sys
sys.path.append("../")
from sql_helper.sql_interface import *


def perform_check(expected_table='',tests=[],channels=[]):
    # All of the reading of data that occurs here is from functions found in the sql_interface.py document.
    # reads in dict of check, converts to numpy array
    vib_signal_dtype = np.dtype('U2,U10')
    vib_signal_dict = np.array(get_vib_signal_dict(),vib_signal_dtype)
    
    # added this line to get individual signal names out of the dict, for improved legibility.
    signal_list = np.array([i[1] for i in vib_signal_dict])

    # reads in expected values of check, converts to numpy array
    expected_values = get_validation_request(expected_table,tests)
    expected_datatype = np.dtype('U20,U20,b,float,float')
    expected_values = np.array(expected_values,expected_datatype)
    return expected_values 

perform_check()
