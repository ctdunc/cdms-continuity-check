import sys
sys.path.append("../")

import numpy as np
from sql_helper.sql_interface import *
from continuity_check.continuity_calc import *


def perform_check(expected_table='',tests=[],channels=[],institution='',wiring='',device='',temp=''):
    # All of the reading of data that occurs here is from functions found in the sql_interface.py document.
    # reads in dict of check, converts to numpy array
    vib_signal_dtype = np.dtype('U2,U10')
    vib_signal_dict = np.array(get_vib_signal_dict(),vib_signal_dtype)
    
    # added this line to get individual signal names out of the dict, for improved legibility.
    signal_list = np.array([i[1] for i in vib_signal_dict])

    # reads in expected values of check, converts to numpy array
    expected_values = get_validation_request(expected_table,tests)
    expected_datatype = np.dtype([('signal_1','U20'),('signal_2','U20'),('expected_continuity','b'),('min',float),('max',float)])
    expected_values = np.array(expected_values,expected_datatype)
    
    # converts signal names to DMM matrix so that we can just manipulate that from now on. The final write will re-translate from this dict.
    # (we're also lying a little bit here, since it's an array, not a dictionary, but I like the ufunc features of numpy)
    for k in vib_signal_dict:
        expected_values['signal_1'] = np.where(expected_values['signal_1']==k[1],k[0],expected_values['signal_1'])
        expected_values['signal_2'] = np.where(expected_values['signal_2']==k[1],k[0],expected_values['signal_2'])


    # these arrays are created to store the tests we want to perform using our parallel algorithm, and our simple measurement function.
    # this should improve efficiency because it will allow us to split the parallel (connected) tests into multiple, smaller chunks if it fails.

    tests_connected = [k for k in expected_values if k[2]==1] # connected, has to be done for single values
    tests_disconnected = [k for k in expected_values if k[2]==0] # disconnected, can be done in parallel
    
    # instantiate DMM interface with VIB to Signal Dict (this is so that it is constant across all functions working w/ DMM).
    #In the future, we could instantiate multiple DMM objects w/ different signals. Abstraction!
    dmm = dmm_interface(vib_signal_dict)
    final_data = [] 

    # first, perform disconnected tests
    return 0

perform_check()
