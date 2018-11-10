import sys
sys.path.append("../")

import numpy as np
import time
from sql_helper.sql_interface import *
from continuity_check.continuity_calc import *


def perform_check(expected_table='',tests=[],channels=[],institution='',wiring='',device='',temp='',vib=''):
    # All of the reading of data that occurs here is from functions found in the sql_interface.py document.
    # reads in dict of check, converts to numpy array
    vib_signal_dtype = np.dtype([('Matrix_location','U5'),('DB_78_pin','U5'),('VIB_pin','U5'),('Signal_name','U20')])
    vib_signal_dict = np.array(get_vib_signal_dict(),vib_signal_dtype) # read in values from SQL
    vib_signal_dict = vib_signal_dict[np.where(vib_signal_dict['Signal_name']!='x')] # sort out elements without mapping
    

    # reads in expected values of check, converts to numpy array
    expected_values = get_validation_request(expected_table,tests)
    expected_datatype = np.dtype([('signal_1','U20'),('signal_2','U20'),('expected_continuity','b'),('min',float),('max',float)])
    expected_values = np.array(expected_values,expected_datatype)
    # converts signal names to DMM matrix so that we can just manipulate that from now on. The final write will re-translate from this dict.
    # (we're also lying a little bit here, since it's an array, not a dictionary, but I like the ufunc features of numpy)
    for k in vib_signal_dict:
        expected_values['signal_1'] = np.where(expected_values['signal_1']==k['Signal_name'], # condition
                k['DB_78_pin'], # returns matrix location in correct index if condition
                expected_values['signal_1'] # if not condition, returns initial value
                )
        expected_values['signal_2'] = np.where(expected_values['signal_2']==k['Signal_name'], # condition
                k['DB_78_pin'], # returns matrix location in correct index if condition
                expected_values['signal_2']) # if not condition, returns initial value

    # these arrays are created to store the tests we want to perform using our parallel algorithm, 
    # and our simple measurement function.
    # this should improve efficiency because it will allow us to split the parallel (connected) 
    # tests into multiple, smaller chunks if it fails.

    # connected, has to be done for single values
    tests_connected = expected_values[np.where(expected_values['expected_continuity']==1)] 
    
    #disconnected, can be done in parallel
    tests_disconnected = expected_values[np.where(expected_values['expected_continuity']==0)]

    # instantiate DMM interface, with option to pass a plot parameter, lower bound for disconnection.
    dmm = dmm_interface() 
    
    # create array in which to store all data, even though we want to yield it to the server.
    final_result_dtype = np.dtype([('signal_1','U20'),('signal_2','U20'),('expected_continuity','b'),('min',float),('max',float),('measured',float),('passing','b')])
    final_result = np.empty(shape=final_result_dtype.shape,dtype=final_result_dtype)

    # perform disconnected tests
        # this line creates a new generator, over which we can iterate, yielding data to the server in real time
        # while preserving the data for later insertion into SQLdb.
        # each yield statement will yield a test with a certain number of passing or failing values.
    disconnect_generator = dmm.parallel_disconnect(tests_disconnected)


    # iterates over generator
    yield "Starting parallel disconnected tests..."
    start_disconnect = time.time()
    for test in disconnect_generator:
        for i in test:
            final_result = np.append(final_result,np.array(i,dtype=final_result.dtype))
        yield test
    yield ("Finished parallell disconnected tests in " + ("--- %s seconds ---" % (time.time() - start_disconnect)))
    # perform connected tests
    # first, create generator over which to iterate
    connect_generator = (dmm.individual_continuity(i)  for i in tests_connected)

    # proceed with iteration
    yield "Starting individual connected tests..."
    start_connect = time.time()
    for result in connect_generator:
        final_result = np.append(final_result,np.array(result,dtype=final_result.dtype))
        yield result
    yield ("Finished individual connected tests in " + ("--- %s seconds ---" % (time.time() - start_connect)))

    # re-translate so that we have human-readable signals
    for k in vib_signal_dict:
        final_result['signal_1'] = np.where(final_result['signal_1']==k['DB_78_pin'],
                k['Signal_name'],
                final_result['signal_1']
            )
        final_result['signal_2'] = np.where(final_result['signal_2']==k['DB_78_pin'],
                k['Signal_name'],
                final_result['signal_2']
            )
                
    # finally, write data to SQLdb
    # TODO: fix the validation table
    write_check(final_result,institution,vib,wiring,device,temp,'') # final element is a placeholder for the appropriate validation table
    
    # Let the user know that the data has been written/all tests are completed, re-yield compiled list of all failures
    yield final_result[np.where(final_result['passing']==0)]
    yield "Finished."


    


