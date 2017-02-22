'''
name:
acquire_and_print_minimal_example.py

type:
script
'''

import pyseeg.modules.board_simple as bs

channel = 0
board = bs.BoardManager()

for i in range(10000):
    sample = board.get_sample(channel=channel)
    id = board.id
    print('%.3d ::: %s' % (id, sample))

board.disconnect()
print('Disconnected')
