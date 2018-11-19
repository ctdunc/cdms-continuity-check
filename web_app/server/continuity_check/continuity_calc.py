import numpy as np
import telnetlib
import sys
sys.path.append("../")

from continuity_check.continuity_sample_generator import *
class dmm_interface:
    def __init__(self,vib_signal_dict,host='',disconnected_lower=40.0e6):
        self.disconnected_lower=disconnected_lower      
        self.vib_signal_dict=vib_signal_dict

    def __translate_signal(signal):
        signal_result = self.vib_signal_dict[np.where(self.vib_signal_dict['Signal_name']==signal)]
        return signal_result

    def individual_continuity(self,expected_value):
        # this should call the #resistance_test lua function, and return either true or false
        signal_1,signal_2 = expected_value['signal_1'],expected_value['signal_2']
        minimum,maximum = expected_value['min'],expected_value['max']

        measurement = return_random_measurement()

        success_data_dtype  = np.dtype(expected_value.dtype.descr+[("measured",float),("passing",'b')])
        success_data = np.empty(success_data_dtype.shape,dtype=success_data_dtype)
        passed = measurement > minimum and measurement < maximum
        for name in expected_value.dtype.names:
            success_data[name]=expected_value[name]
        success_data['measured'] = measurement
        if passed:
            success_data['passing'] = 1
        else:
            success_data['passing'] = 0
        return success_data

    def parallel_disconnect(self,expected_values):
        # this should call the #open_test lua function, and return either true or false in 0th index             
        # the expected_values object needs to be a numpy array with the same data types as expected_values, 
        # else the function will break
        init_signal_list = np.unique(expected_values['signal_1']) 
        # we're also going to make this a generator, so that we immediately know whether a failure occurs
        
        for i in init_signal_list:
            # get values corresponding to signal_1 we want to check
            open_tests = expected_values[np.where(expected_values['signal_1']==i)]
            open_tests_vals = open_tests['signal_2']


            # perform measurement, read into float dtype
            measurement = return_random_measurement()

            # perform check. Operates as binary search currently
            # TODO: create limits on binary search to improve efficiency
            passed = measurement > self.disconnected_lower

            success_data_dtype  = np.dtype(open_tests.dtype.descr+[("measured",float),("passing",'b')])
            success_data = np.empty(open_tests.shape, dtype=success_data_dtype)
            if passed:
                # appends successful checks to passing data
                for name in open_tests.dtype.names:
                    success_data[name]=open_tests[name]
                success_data['measured'] = measurement
                success_data['passing'] = 1
                yield success_data
            elif not passed:
                new_checks = np.array_split(expected_values,2)

                print(new_checks)
                for k in new_checks:
                    if len(k)>1:
                        yield from self.parallel_disconnect(k)
                    else:
                        yield self.individual_continuity(k)

