'''
The following example was tested with OpenBCI Ganglion board.
'''

#######################
# 0. Define variables.
filepath = '/tmp/pyseeg_test_output.csv'

#######################
# 1. Plot the data.
from pyseeg.visualization import plot_data
plot_data(filepath)
