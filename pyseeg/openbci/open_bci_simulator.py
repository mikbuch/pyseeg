"""
name: open_bci_simulator.py

This class simulates OpenBCI behaviour. It may be used for testing
real-time utilities.

Core OpenBCI object for handling connections and samples from the board.

EXAMPLE USE:

def handle_sample(sample):
  print(sample.channels)


"""

import pandas as pd


class OpenBCIBoard(object):

    def __init__(self, sa):
        """OpenBCI class for simulation.


        Parameters
        ----------
        sa : dict
            Simulator arguments. This is passed from control file, via
            acquisition module.

        """

        print("Connecting to the device")
        print("Serial established...")

        print('In Waiting')

        print('Check if we have connection...')
        print('Start streaming...')
        self.streaming = True

        self.data = pd.read_csv(sa['input_path'], sep=sa['sep'],
                                skiprows=sa['skiprows'],
                                header=sa['header'], decimal=sa['decimal'])
        self.sa = sa

    def start_streaming(self, callback):

        # Row by row
        for _, row in self.data.iterrows():

            sample_id = None
            aux_data = None

            # Sample id (if present).
            if self.sa['id'] is not None:
                sample_id = row[self.sa['id']]

            # Channel data (if set).
                if self.sa['id'] is not None:
                    channel_data = row[self.sa['ch']]

            # Aux data (if present).
            if self.sa['aux'] is not None:
                aux_data = [self.sa['aux']]

            if self.sa['id'] is None and self.sa['ch'] is None and \
                    self.sa['aux'] is None:
                channel_data = row.values

            sample = OpenBCISample(sample_id, channel_data, aux_data)
            # print(row)
            # print(sample.channel_data)
            # print(type(sample.channel_data))

            callback(sample)

    def disconnect(self):
        print('DISCONNECTED simulator')


class OpenBCISample(object):
    """Object encapulsating a single sample from the OpenBCI board."""
    def __init__(self, packet_id, channel_data, aux_data):
        self.id = packet_id
        self.channel_data = channel_data
        self.aux_data = aux_data
