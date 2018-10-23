import numpy as np
import os

dir_path = os.getcwd()
data = np.genfromtxt(dir_path+'/all_connections.csv',delimiter=',',dtype=str)


