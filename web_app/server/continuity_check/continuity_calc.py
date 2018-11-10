import numpy as np
import telnetlib
import sys
sys.path.append("../")

class dmm_interface:
    def __init__(self,host='',disconnected_lower=40.0e6):
       
        if not host:
            host = "192.168.005.120" # this is value of DMM IP from Tim's continuity.py 
        self.tn = telnetlib.Telnet(host)
        self.tn.write("load_functions()\n".encode('ascii'))
        self.disconnected_lower = disconnected_lower

    def individual_continuity(self,expected_value):
        # this should call the #resistance_test lua function, and return either true or false
        signal_1,signal_2 = expected_value['signal_1'],expected_value['signal_2']
        minimum,maximum = expected_value['min'],expected_value['max']
        self.tn.write(("resistance_test(\""+signal_1+"\",\""+signal_2+"\")\n").encode('ascii'))
        measurement = self.tn.read_until(("Ohm").encode("ascii"))
        measurement = measurement.split()
        measurement = float(measurement[0])
        
        success_data_dtype  = np.dtype(expected_value.dtype.descr+[("measured",float),("passing",bool)])
        success_data = np.empty(expected_value.shape, dtype=success_data_dtype)

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
        
        #  TODO  understand lua script and exact parameters to pass (what is this matrix_loc variable?)
        
        for i in init_signal_list:
            # get values corresponding to signal_1 we want to check
            open_tests = expected_values[np.where(expected_values['signal_1']==i)]
            open_tests_vals = open_tests['signal_2']

            # correctly format string to pass to DMM
            open_tests = "\""
            for loc in open_tests_vals:
                open_tests+=loc+"\",\""
            open_tests = open_tests[:-2]
            telnet_cmd = ("open_test(\""+i+"\",{"+open_tests+"})\n").encode("ascii") 

            # perform measurement, read into float dtype
            self.tn.write(telnet_cmd)
            measurement = self.tn.read_until(("Ohm").encode("ascii"))
            measurement = measurement.split()
            measurement = float(measurement[0])
            
            # perform check. Operates as binary search currently
            # TODO: create limits on binary search to improve efficiency

            passed = measurement > self.disconnected_lower
            if passed:
                # appends successful checks to passing data
                success_data_dtype  = np.dtype(open_tests.dtype.descr+[("measured",float),("passing",bool)])
                success_data = np.empty(open_tests.shape, dtype=success_data_dtype)
                for name in open_tests.dtype.names:
                    success_data[name]=open_tests[name]
                success_data['measured'] = measurement
                success_data['passing'] = 1
                yield success_data 
            elif not passed:
                new_checks = np.split(expected_values,2)
                for i in new_checks:
                    if size(i)>1:
                        yield from parallel_disconnect(i)
                    else:
                        yield individual_continuity(i)

         
        
