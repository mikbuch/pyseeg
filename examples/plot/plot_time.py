'''
name: plot_time.py
type: script (example)
'''

from pyseeg.modules.plotlib import plot_time

# specify sampling frequency
fs = 250

# channel
channel = 0

# plot time domain fo the signal
plot_time('../example_data/blink_00.csv', fs, channel)

# # full settings (as it is by default - see doc for the details):
'''
plot_time(
    '../example_data/ssvep_00.csv', fs, channel,
    bandstop=(49, 51), bandpass=(1, 50), order=4,
    sec_remove=1, show=True
    )
'''
