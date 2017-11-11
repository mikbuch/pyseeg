'''
The following example was tested with OpenBCI Ganglion board.
'''

from pyseeg.communication import record_data
from pyseeg.stimuli import TwoRectangles

#######################
# 0. Define variables.
# Output path (default is in your home directory).
output_path = '/tmp/pyseeg_test_output.csv'
# Frequencies (for the two rectangles).
freqs = (10.0, 14.0)

############################
# 1. Create stimuli object.
sti = TwoRectangles(freqs=freqs, timeout=8)

############################################
# 2. Record data and classify in real time.
record_data(sti, freqs=freqs, channel=0, output_path=output_path)
# TODO: add aux channels to the output.

############################################
# 3. Optionally: plot the data.
from pyseeg.visualization import plot_data
plot_data(output_path)

'''
The acquisition manager will ask the stimuli controller about the `state`
each time it collects the data (255 times per second in the case of OpenBCI).
Then the complete information will be saved to a file (sample id, channels
recordings, auxilliary channels, state).
'''
