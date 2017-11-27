'''
The following example was tested with OpenBCI Ganglion board.
name: acquisition_with_stimuli_p300.py
'''

from pyseeg.communication import record_data
from pyseeg.stimuli import P300
from pyseeg.utils import generate_output_path

# 0. Define output path (default is in your home directory),
# e.g. /home/student/p300_00_2017-11-27-13-02.csv).
output_path = generate_output_path(name='p300', user='uampsych',
                                   sub='00', date_and_time=True)

# 1. Create stimuli object.
sti = P300(win_size=(1024, 768), user='uampsych')

# 2. Record data with triggers (20 seconds or delete key press).
record_data(sti, output_path=output_path)

# 3. Optionally: plot the data.
from pyseeg.visualization import plot_data
plot_data(output_path)

'''
The acquisition manager will ask the stimuli controller about the `state`
each time it collects the data (255 times per second in the case of OpenBCI).
Then the complete information will be saved to a file (sample id, channels
recordings, auxilliary channels, state).
'''
