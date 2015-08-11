
# OFFLINE eyes-open-closed classifier

'''
0. Preliminary info. 
(specify the sampling rate)
'''

# sampling frequency, sampling rate
fs = 250


'''
# 1. Specify file containing the data, get data from the file
'''

data = eoc.getDataFromFile('../data/alpha_01.csv')


'''
# 2. Filtering the data:
'''
# if only filter=True is specified then both defaults filters are used
# How to use only one filter? Simply set the other filter values to (1,1)
filtered_data = filterData(data=data, bandstop=(49,51), bandpass=(1,50))


'''
# 3*. Optionally you can generate a spectrogram of the retrieved data
(to check if everyting went as planned)
'''

eoc.generateDataSpect(data)


'''
# 4. Specify classes 
(when did the subject had its eyes opened and when closed)
'''

eoc.alpha_ranges = [[11, 21], [30, 40], [52, 63]]
eoc.control_ranges = [[1, 10], [21, 29], [40, 51]]


'''
# 5*. Optionally you can change time window periods
(default settings are: take one second, every half a second)
'''

eoc.take_x_seconds = 1
eoc.every_x_seconds = 0.5


'''
# 6*. Optionally you can generate a spectrogram of the splitted data
(to check if everyting went as planned)
'''

splitted_data = eoc.generateSplittedDataSpect()


'''
# 7. Transform all the splitted data samples using FFT
'''

transformed_data = eoc.transform()


'''
At this stage you have data samples prepared for further training and
classification

Eventually it it possible to get to this stage with only one line:
'''



