import pickle

# Getting back the objects:
with open('raw_flted.pickle') as f:
    data, flted_50_stop, flted_1_50_pass_only, flted_1_50_pass = pickle.load(f)

# data - raw data (not filtred)
# flted_50_stop - bandstop fliter 50 Hz (49-51 Hz)
# flted_1_50_pass_only - bandpass filter 1-50 Hz only
# flted_1_50_pass - bandstop filter 50Hz and then bandpass 1-50 Hz
