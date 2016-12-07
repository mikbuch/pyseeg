#!/usr/bin/env python2

from psychopy import visual


class TablesGenerator(object):
    def_text_table = [
        ['A', 'B', 'C', 'D', 'E'],
        ['F', 'G', 'H', 'I', 'J'],
        ['K', 'L', 'M', 'N', 'O'],
        ['P', 'R', 'S', 'T', 'U'],
        ['W', 'Y', 'Z', '_', '-']
        ]

    def __init__(self, text_table=def_text_table, fullscr=False,
                 pos=(0, 0), bg_color='gray', fg_color='black'):
        self.text_table = text_table

        self.example_no_highlight = [
            '                     \n',
            '  A   B   C   D   E  \n',
            '                     \n',
            '  F   G   H   I   J  \n',
            '                     \n',
            '  K   L   M   N   O  \n',
            '                     \n',
            '  P   R   S   T   U  \n',
            '                     \n',
            '  W   X   Y   Z   -  \n',
            '                     \n'
            ]

        self.no_highlight = []
        self.cols_light = []
        self.rows_light = []

        self.fullscr = fullscr
        self.pos = pos
        self.fg_color = fg_color

        # psychopy Window creation
        self.win_main = visual.Window([1400, 1200], fullscr=self.fullscr,
                                      monitor='testMonitor', pos=self.pos,
                                      winType='pyglet', units='pix', color=bg_color)
        self.win_main.setMouseVisible(False)

        # psychopy TextStim creation
        self.rows_stim = []
        self.cols_stim = []

        for row in range(len(self.text_table)):
            self.no_highlight.append([])
            for i in range(len(self.text_table[0]) +
                           (len(self.text_table[0]) - 1) * 3 + 2 + 2):
                self.no_highlight[-1] += ' '
            self.no_highlight[-1] += '\n'
            self.no_highlight.append([])
            self.no_highlight[-1] += '  '
            for col in range(len(self.text_table[row])):
                self.no_highlight[-1] += self.text_table[row][col]
                if not col == len(self.text_table)-1:
                    self.no_highlight[-1] += '   '
                else:
                    self.no_highlight[-1] += '  \n'
        self.no_highlight.append([])
        for i in range(len(self.text_table[0]) +
                       (len(self.text_table[0]) - 1) * 3 + 2 + 2):
            self.no_highlight[-1] += ' '
        self.no_highlight[-1] += '\n'

    def row_change(self, num):
        real_num = num + num + 1
        new = []
        for row in range(len(self.no_highlight)):
            new.append('')
            for col in range(len(self.no_highlight[row])):
                if (row == real_num - 1 or row == real_num + 1) \
                        and col < len(self.no_highlight[row])-1:
                    if col == 0 or col == len(self.no_highlight[row])-2:
                        new[-1] += '+'
                    else:
                        new[-1] += '-'
                elif row == real_num and \
                        (col == 0 or col == len(self.no_highlight[row])-2):
                        new[-1] += '|'
                else:
                    new[-1] += self.no_highlight[row][col]
        return new

    def col_change(self, num, highlighted):
        real_num = num * 4 + 2
        new = []
        for row in range(len(highlighted)):
            new.append('')
            for col in range(len(highlighted[row])):

                if col == real_num - 2 or col == real_num + 2:
                    if row == 0 or row == len(highlighted) - 1:
                        new[-1] += '+'
                    else:
                        new[-1] += '|'
                elif (col == real_num - 1 or col == real_num or col == real_num + 1)\
                        and (row == 0 or row == len(highlighted)-1):
                    new[-1] += '-'
                else:
                    new[-1] += highlighted[row][col]
        return new

    def rows_generate(self):
        for i in range(len(self.text_table)):
            self.rows_light.append(self.row_change(i))
        return self.rows_light

    def cols_generate(self):
        for i in range(len(self.text_table)):
            self.cols_light.append([])
            for j in range(len(self.text_table[i])):
                self.cols_light[-1].append(self.col_change(j, self.rows_light[i]))
        return self.cols_light

    '''
        PSYCHOPY
        TextStim from tables generator
    '''

    def _create_TextStim(self, win, text, font='Monospace',
                         height=40, wrapWidth=600):

        text_stim = visual.TextStim(win=win, text=''.join(text), font=font,
                                    height=height, wrapWidth=wrapWidth,
                                    color=self.fg_color)

        return text_stim


    def rows_stim_generate(self):
        for row in self.rows_generate():
            row_text = self._create_TextStim(self.win_main, row)
            self.rows_stim.append(row_text)
        return self.rows_stim

    def cols_stim_generate(self):
        for row in self.cols_generate():
            self.cols_stim.append([])
            for col in row:
                col_text = self._create_TextStim(self.win_main, col)
                self.cols_stim[-1].append(col_text)
        return self.cols_stim

    def no_highlight_generate(self):
        for row in self.cols_generate():
            self.cols_stim.append([])
            for col in row:
                col_text = self._create_TextStim(self.win_main, col)
                self.cols_stim[-1].append(col_text)
        return self.cols_stim
