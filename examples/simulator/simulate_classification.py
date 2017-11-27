'''
Simulate acquisition and real-time classification.
'''

# from pyseeg.communication import record_data
from pyseeg.communication import record_data
from pyseeg.classifier import SSVEPRealTime

##################################
# 0. Define variables.
# Input path (previously acquired EEG data).
input_path = '/home/jesmasta/eeg_data/OpenBCI/ssvep_00.csv'
# Output path (default is in your home directory).
output_path = '/tmp/pyseeg_test_output.csv'
# Frequencies (for the two rectangles).
freqs = (10.0, 20.0)

##################################
# 1. Create classification object.
# SSVEP detection in real-time.
cls = SSVEPRealTime(fs=250, window_len=250, freqs=freqs,
                    harmonics=2, cls_type='CCA', window_kind='nooverlap')

############################################
# 2. Record data and classify in real time.
record_data(classifier=cls, freqs=freqs, channel=0, board_type='simulator',
            output_path=output_path,
            sa={'input_path': input_path, 'header': None, 'skiprows': None,
                'usecols': None, 'sep': ',', 'decimal': '.',
                'id': None, 'ch': None, 'aux': None})
# TODO: add aux channels to the output.

############################################
# 3. Plot decisions.
from pyseeg.visualization import plot_data
plot_data(output_path, ptype='decision')

'''
The acquisition manager will ask the stimuli controller about the `state`
each time it collects the data (255 times per second in the case of OpenBCI).
Then the complete information will be saved to a file (sample id, channels
recordings, auxilliary channels, state).
'''
