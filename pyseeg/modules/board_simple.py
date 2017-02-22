import pyseeg.openbci.open_bci_v3 as bci
import pyseeg.modules.filterlib as flt


class BoardManager(object):

    def __init__(self, port='/dev/ttyUSB0', baud=115200):

        # filtering in real time object creation
        self.frt = flt.FltRealTime()

        self.board = bci.OpenBCIBoard(port=port, baud=baud)

        print('writing <b> to the board ...')
        self.board.ser.write('b')

    def get_sample(self, filter=True, channel=0):
        smp = self.board._read_serial_binary()
        data = smp.channel_data[channel]
        self.id = smp.id

        if filter:
            # filter a sample (from the channel specified)
            smp.channel_data[channel] = self.frt.filterIIR(data, 0)
        smp_output = smp

        return smp_output

    def write_sample(filename, filter=True, channel=0):
            
        open(filename, 'a').write(','.join([number, data])+'\n')


    def disconnect(self):
        self.board.disconnect()
