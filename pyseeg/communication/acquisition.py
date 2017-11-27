import csv
import datetime
import multiprocessing as mp
import os
import shutil

import pyseeg.modules.filterlib as flt


def record_data(stimuli=None, classifier=None, board_type='ganglion',
                freqs=None, channel=0, simulate=False, output_path=None,
                sa={'input_path': None, 'header': None, 'skiprows': None,
                    'usecols': None, 'sep': ',', 'decimal': '.',
                    'id': None, 'ch': None, 'aux': None}):

    """Function for collecting the data given the specific stimuli.


    Parameters
    ----------
    stimuli : stimulus class object
        Create one and pass to this function. It is started by calling its
        `start_display` method.
    classifier : object handling classification
        Used to classify the data. It detects either SSVEP, P300 or blinks.
        Depending on the stimuli and the classificator used. Default is None,
        if left so signal is only acquired.
    board : string
        ganglion, cyton or simulator -- which board type to use
    sa : dict
        Simulator arguments for OpenBCI simulation.

    Returns
    -------
    bool
        True if successful, False otherwise.


    """

    # Get date and time.
    time_code = datetime.datetime.today().strftime('%Y-%m-%d-%h-%s')

    # Define the process to run in background. It communicates with the parent
    # process via state and terminate variables.
    def mp_acquisition(state):
        print(' * acquisition * Feedback from within process.')
        print(' * acquisition * Current state: %s.' % state.value)
        print(' * acquisition * Acquisition will start soon.')

        # Callback function for OpenBCI class to handle samples.
        def handle_sample(sample):

            # Get data point (value) form n'th channel (by index, def '0').
            smp = sample.channel_data[channel]

            # Filter fist sample (place in list with the index '0').
            smp_flted = frt.filterIIR(smp, 0)

            if classifier is not None:
                # Detect class (SSVEP or P300).
                win_end, cls_decision = classifier.detect(smp_flted)

            # Let the inreface know that the data is streaming.
            if board.streaming:
                streaming.set()

            # Quit program, stop and disconnect board.
            if terminate.is_set():
                print(' * acquisition * Disconnect signal sent...')
                streaming.clear()
                board.disconnect()

            with open(output_path, 'at') as f:

                # Prepare output row.
                output_row = [smp, smp_flted]
                # If state is relevant, append it to the output.
                if state.value >= 0:
                    output_row.append(state.value)
                # Add classifier's decision.
                if classifier is not None:
                    output_row += [int(win_end), cls_decision]

                with open(output_path, 'at') as f:
                    save = csv.writer(f)
                    save.writerow(output_row)

        # Create an object for filtering in real-time.
        frt = flt.FltRealTime()

        print(' * acquisition * Output file preparation...')
        # Prepare output file (backup previous if existed).
        if os.path.isfile(output_path):
            filename, file_extension = os.path.splitext(output_path)
            shutil.copy2(output_path,
                         '%s_%s%s' % (filename, time_code, file_extension))
        with open(output_path, 'w') as f:
            save = csv.writer(f)

        print(' * acquisition * Modules for OpenBCI real time set...')

        if 'cyton' in board_type:
            import pyseeg.openbci.open_bci_v3 as bci
            port = '/dev/ttyUSB0'
            board = bci.OpenBCIBoard(port=port)
        elif 'ganglion' in board_type:
            import pyseeg.openbci.open_bci_ganglion as bci
            # Doesn't need port.
            board = bci.OpenBCIBoard()
        elif 'simulator' in board_type:
            import pyseeg.openbci.open_bci_simulator as bci
            # Need arguments to load datafile.
            board = bci.OpenBCIBoard(sa=sa)
        else:
            print('Please, choose one of the following:')
            print('cyton, ganglion or simulator')


        # For SSVEP state is not important, classifier passes the info
        # whether state.value is None or int.
        print(' * acquisition * Starting streaming...')
        board.start_streaming(handle_sample)
        print(' * acquisition * Disconnect signal sent...')
        board.disconnect()

    if output_path is None:
        # Define default timecode.
        home_dir = os.environ['HOME']
        output_path = os.path.join(home_dir, '%s.csv' % time_code)
    # Multiprocessing variables
    #
    # State tells which stimuli was active.
    state = mp.Value('i', -1)
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
    if stimuli is not None:
        stimuli.start_display(state, streaming, terminate)

    recorder.join()
