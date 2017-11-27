import csv
import datetime
import multiprocessing as mp
# import pyseeg.openbci.open_bci_ganglion as bci
import pyseeg.openbci.open_bci_v3 as bci
import os

import pyseeg.modules.filterlib as flt


def simulate_data(stimuli, classifier, header=None, freqs=None, channel=0,
                output_path=None):

    # Define the process to run in background. It communicates with the parent
    # process via state and terminate variables.
    def mp_acquisition(state):
        print(' * acquisition * Feedback from within process.')
        print(' * acquisition * Current state: %s.' % state.value)
        print(' * acquisition * Acquisition will start soon.')

        # Callback function for OpenBCI class to handle samples.
        def handle_sample(sample):

            if freqs is not None:
                # Get data point (value) form the first channel (index '0').
                smp = sample.channel_data[channel]

                # Filter fist sample (place in list with the index '0').
                smp_flted = frt.filterIIR(smp, 0)

                # Detect ssvep state (stimulus is the subject looking at).
                ssvep_state = classifier.ssvep_detect(smp_flted)

            # Let the inreface know that the data is streaming.
            streaming.set()

            # Quit program, stop and disconnect board.
            if terminate.is_set():
                print(' * acquisition * Disconnect signal sent...')
                streaming.clear()
                board.disconnect()

            with open(output_path, 'at') as f:
                save = csv.writer(f)
                if freqs is not None:
                    save.writerow([sample.id, smp, smp_flted, ssvep_state])
                else:
                    save.writerow([sample.id] + sample.channel_data +
                                                                 [state.value])

            return classifier.corrs, classifier.cls

        if freqs is not None:
            # Create an object for filtering in real-time.
            frt = flt.FltRealTime()

        print(' * acquisition * Output file preparation...')
        if header is not None:
			with open(output_path, 'w') as f:
				save = csv.writer(f)
				save.writerow(header)

        print(' * acquisition * Modules for OpenBCI real time set...')

        import pandas as pd
        from pyseeg.datasets import fetch_ssvep
        import matplotlib.pyplot as plt
        import numpy as np
        print(' * acquisition * File reading modules set...')
        from bieg import ICAManager, get_biosemi_indices
        import os

        '''
        Our BAKA
        '''
        # # Input file location.
        # input_filepath = os.path.join(os.environ['HOME'],
                         # 'eeg_data/SSVEP_Bakardjian/SUBJ1/SSVEP_14Hz_Trial1_SUBJ1.MAT')

        # # Create an object to govern the analysis.
        # bss_ica = ICAManager(input_filepath, dtype='matlab')
        # bss_ica.create_MNE_Raw()

        # picks = get_biosemi_indices(['A15', ])
        # data = bss_ica.data[picks]
        # data = data.flatten()


        '''
        Our SSVEP
        '''
        # filepath = fetch_ssvep()
        # data = pd.read_csv(filepath, names=['e01',], header=None)['e01']


        '''
        Present
        '''
        # data = pd.read_csv('/home/jesmasta/Downloads/OpenBCI-RAW-2017-11-17_12-45-30.txt',
        # data = pd.read_csv('/home/jesmasta/Downloads/OpenBCI-RAW-2017-11-17_12-30-33.txt',
        data = pd.read_csv('/home/jesmasta/Downloads/OpenBCI-RAW-2017-11-17_12-53-32.txt',
                           sep=', ', skiprows=6, usecols=[1,], header=None, decimal=',')
        data = data.values.T[0]
        print(data.shape)
        print(data.mean())
        print(data[:10])

        print(' * acquisition * Data read...')
        rs = {'10': [], '20': []}
        for (i, dt) in enumerate(data):
            sim_sample = bci.OpenBCISample(0, [dt,], [0,])
            correlations, cls = handle_sample(sim_sample)
            if cls:
                rs['10'].append(correlations[0])
                rs['20'].append(correlations[1])
        fig, ax = plt.subplots()
        # print(range(len(rs['10'])), rs['10'])
        # print(range(len(rs['20'])), rs['20'])
        ax.bar(np.arange(len(rs['10'])), rs['10'], width=1.0, color='r')
        ax.bar(np.arange(len(rs['20'])), rs['20'], width=1.0, color='b')
        plt.show()


        # board = bci.OpenBCIBoard()
        # board = bci.OpenBCIBoard(port='/dev/ttyUSB0')
        # print(' * acquisition * Starting streaming...')
        # board.start_streaming(handle_sample)
        # board.disconnect()

    if output_path is None:
        # Define default timecode.
        home_dir = os.environ['HOME']
        time_code = datetime.datetime.today().strftime('%Y-%m-%d-%h-%s')
        output_path = os.path.join(home_dir, '%s.csv' % time_code)
    # Multiprocessing variables
    #
    # State tells which stimuli was active.
    state = mp.Value('i', 0)
    #
    # Flag to communicate the interface when to
    # to start stimuli display.
    streaming = mp.Event()
    #
    # The way to stop the data acquisition.
    terminate = mp.Event()

    # Define process.
    recorder = mp.Process(name='proc_acq', target=mp_acquisition,
                                                                 args=(state,))
    # Start process.
    recorder.start()
    print(' ! main ! Subprocess for recording started')


    ############################################
    # Stimuli reference
    #
    # State is shared between both objects.
    #
    stimuli.start_display(state, streaming, terminate)
