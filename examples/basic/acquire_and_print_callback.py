'''
name:
acquire_and_print.py

type:
script
'''

import pyseeg.openbci.open_bci_v3 as bci
import pyseeg.modules.filterlib as flt
import pyseeg.modules.plotlib as pltmod


###############################################################################
#
#   VARIABLES, PATHS, CONFIGURATION
#
###############################################################################

# MAIN CHANNEL (OpenBCI board)
channel = 0


###############################################################################
#
#   OPENBCI AQUIRING PROCESS
#
###############################################################################

def plotData(sample):

    # get sample form the first channel (index '0')
    smp = sample.channel_data[channel]

    # filter fist sample (place in list with the index '0')
    smp_flted = frt.filterIIR(smp, 0)
    print(smp_flted)

# filtering in real time object creation
frt = flt.FltRealTime()

port = '/dev/ttyUSB0'
baud = 115200
board = bci.OpenBCIBoard(port=port, baud=baud)
print('starting streaming...')
board.start_streaming(plotData)
board.disconnect()
