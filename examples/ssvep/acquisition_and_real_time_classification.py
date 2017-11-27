'''
The following example was tested with OpenBCI Ganglion board.
'''

# from pyseeg.communication import record_data
from pyseeg.communication import simulate_data
from pyseeg.stimuli import TwoRectangles
from pyseeg.classifier import SSVEPRealTime

##################################
# 0. Define variables.
# Output path (default is in your home directory).
output_path = '/tmp/pyseeg_test_output.csv'
# Frequencies (for the two rectangles).
freqs = (10.0, 15.0)

##################################
# 1. Create stimuli object.
sti = TwoRectangles(freqs=freqs, timeout=2)

##################################
# 2. Create classification object.
# SSVEP detection in real-time.
cls = SSVEPRealTime(fs=250, window_len=250, freqs=freqs,
                    harmonics=2, cls_type='CCA', window_kind='nooverlap')

############################################
# 3. Record data and classify in real time.
simulate_data(sti, cls, freqs=freqs, channel=0, output_path=output_path)
# TODO: add aux channels to the output.

############################################
# 4. Optionally: plot the data.
# from pyseeg.visualization import plot_data
# plot_data(output_path)

'''
The acquisition manager will ask the stimuli controller about the `state`
each time it collects the data (255 times per second in the case of OpenBCI).
Then the complete information will be saved to a file (sample id, channels
recordings, auxilliary channels, state).
'''
