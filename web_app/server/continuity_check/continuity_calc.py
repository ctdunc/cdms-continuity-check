import numpy as np
import telnetlib

class dmm_interface:
    def __init__(self,vib_signal_dict,host='',disconnected_lower=40.0e6):
        self.vib_signal_dict = vib_signal_dict
       
        if not host:
            host = "192.168.005.120" # this is value of DMM IP from Tim's continuity.py 
        self.tn = telnetlib.Telnet(host)
        self.tn.write("load_functions()\n".encode('ascii'))

    def individual_continuity(expected_value):
        # this should call the #resistance_test lua function, and return either true or false
        return 0

    def parallel_disconnect(self,expected_values):
        # this should call the #open_test lua function, and return either true or false in 0th index             
        # the expected_values object needs to be a numpy array with the same data types as expected_values, else the function will break
        init_signal_list = np.unique(expected_values['signal_1']) 
        
        # we're also going to make this a generator, so that we immediately know whether a failure occurs
        
        #  TODO  understand lua script and exact parameters to pass (what is this matrix_loc variable?)
        
        for i in init_signal_list:
            # TODO some do_check function here.
            if passed:
                success_data = np.append(expected_values,1*np.ones(expected_values.shape()[0]),axis=0)
                yield success_data 
            elif not passed:
                yield "some failure"
                new_checks = np.split(expected_values,2)
                for i in new_checks:
                    yield from parallel_disconnect(i)
                
            

         
        
