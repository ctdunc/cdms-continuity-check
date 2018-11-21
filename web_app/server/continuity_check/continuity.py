import sys
sys.path.append("../")
import numpy as np
import time
import json
from sql_helper.sql_interface import *
from continuity_check.continuity_calc import *


def perform_check(expected_table='', tests=[], channels=[],
                  institution='', wiring='', device='', temp='', vib=''):
    # All of the reading of data that occurs here is from functions found in the 
    # sql_interface.py document.
    # reads in dict of check, converts to numpy array

    vib_signal_dtype = np.dtype([('Matrix_location','U5'),('DB_78_pin','U5'),('VIB_pin','U5'),('Signal_name','U20')])
    vib_signal_dict = np.array(get_vib_signal_dict(),vib_signal_dtype) # read in values from SQL
    vib_signal_dict = vib_signal_dict[np.where(vib_signal_dict['Signal_name']!='x')] # sort out elements without mapping
    

    # reads in expected values of check, converts to numpy array
    expected_values = get_validation_request(expected_table,tests)
    expected_datatype = np.dtype([('signal_1','U20'),('signal_2','U20'),('expected_continuity','b'),('min',float),('max',float)])
    expected_values = np.array(expected_values,expected_datatype)

    # these arrays are created to store the tests we want to perform using our parallel algorithm, 
    # and our simple measurement function.
    # this should improve efficiency because it will allow us to split the parallel (connected) 
    # tests into multiple, smaller chunks if it fails.

    # connected, has to be done for single values
    tests_connected = expected_values[np.where(expected_values['expected_continuity']==1)] 
    
    #disconnected, can be done in parallel
    tests_disconnected = expected_values[np.where(expected_values['expected_continuity']==0)]

    # instantiate DMM interface, with option to pass a plot parameter, lower bound for disconnection.
    dmm = dmm_interface(vib_signal_dict=vib_signal_dict) 
    
    # create array in which to store all data, even though we want to yield it to the server.
    final_result_dtype = np.dtype([('signal_1','U20'),('signal_2','U20'),('expected_continuity','b'),('min',float),('max',float),('measured',float),('passing','b')])
    final_result = np.empty(shape=final_result_dtype.shape,dtype=final_result_dtype)

    # perform disconnected tests
        # this line creates a new generator, over which we can iterate, yielding data to the server in real time
        # while preserving the data for later insertion into SQLdb.
        # each yield statement will yield a test with a certain number of passing or failing values.
    disconnect_generator = dmm.parallel_disconnect(tests_disconnected)


    # iterates over generator
    yield {'key': 'MSG', 'value':'Starting parallel disconnected tests...'}
    start_disconnect = time.time()
    for test in disconnect_generator:
        for i in test:
            final_result = np.append(final_result,np.array(i,dtype=final_result.dtype))
            i = measurement_to_json(i)
            yield {'key': 'MEASUREMENT','value':i}
    disc_complete = ("Finished parallell disconnected tests in " + ("--- %s seconds ---" % (time.time() - start_disconnect)))
    # perform connected tests
    # first, create generator over which to iterate
    connect_generator = (dmm.individual_continuity(i)  for i in tests_connected)

    # proceed with iteration
    yield {'key':'MSG', 'value':'Starting individual connected tests...'}
    start_connect = time.time()

    for result in connect_generator:
        final_result = np.append(final_result,np.array(result,dtype=final_result.dtype))
        result = measurement_to_json(result)
        yield {'key':'MEASUREMENT', 'value':result}
    conn_complete = ("Finished individual connected tests in " + ("--- %s seconds ---" % (time.time() - start_connect)))

    # finally, write data to SQLdb
    # TODO: fix the validation table
    write_check(final_result,institution,vib,wiring,device,temp,'') # final element is a placeholder for the appropriate validation table
    yield {'key': 'MSG', 'value': 'Finished.'}

    
def measurement_to_json(m):
    signal_1,signal_2,mini,maxi,passing,measured = m['signal_1'],m['signal_2'],m['min'],m['max'],m['passing'],m['measured']
    result = {
            'signal_1': str(signal_1),
            'signal_2': str(signal_2),
            'min': float(mini),
            'max': float(maxi),
            'measured': float(measured),
            'passing': bool(passing)
            }
    return result

