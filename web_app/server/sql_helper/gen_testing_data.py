import itertools
import random
signals = ['TES_1', 'TES_2', 'TES_3', 'TES_4', 'DATA_TEST_1', 'DATA_TEST_2', 'ALPHA', 'BETA']
import random
signal_combinations = list(itertools.combinations(signals,2))
def gen_new_check():
    data = []
    for i in signal_combinations:
        signal_1 = i[0]
        signal_2 = i[1]
        minimum = random.uniform(100,1000)
        maximum = random.uniform(100,1000)
        measured = random.uniform(100,1000)
        Unit = 'ohm'
        passed = minimum < measured < maximum
        data.append([signal_1,signal_2,minimum,maximum,measured,Unit,passed]) 
    return data
