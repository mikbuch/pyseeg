import numpy as np
import os
import pygame
import time
from random import shuffle
from pyseeg.utils import fetch_stimuli


class WaitKeyPress(object):

    def __init__(self):
        self.state = None

    def start_display(self, state, streaming, terminate):
        self.state = state

        self.window = pygame.display.set_mode((800, 800),
                                              pygame.FULLSCREEN, 32)
        self.clock = pygame.time.Clock()

        pygame.init()
        pygame.mouse.set_visible(False)

        # Begin stimuli display when the board is connected and it starts
        # streaming the data.
        print(' & stimuli & Waiting for the board to connect ...')
        streaming.wait()
        print(' & stimuli & Board connected ...')

        self.window.fill((35, 85, 35))
        pygame.display.update()

        start_ticks = pygame.time.get_ticks()
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        while seconds < 10:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > 0.3 :
                self.window.fill((0, 0, 0))
                pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('space')
                        state.value = 1
                    elif event.key == pygame.K_DELETE:
                        print('delete')
                        state.value = 0
                        break
                else:
                    state.value = 0

        pygame.quit()
        terminate.set()


class SimpleRectangle(object):

    def __init__(self, freqs, win_size=(1000, 1000), position=(300, 300),
                 stim_size=(400, 400), colors=((255, 255, 255), (0, 0, 0))):
        self.freqs = freqs
        self.win_size = win_size
        self.position = position
        self.stim_size = stim_size
        self.colors = colors

        self.state = None

    def display_stimuli(self, colors, size, pos, freq):

        pygame.draw.rect(self.window, colors[0], pos+size)
        pygame.display.flip()
        self.clock.tick(int(freq*2.))

        pygame.draw.rect(self.window, colors[1], pos+size)
        pygame.display.flip()
        self.clock.tick(int(freq*2.))

    def start_display(self, state, streaming, terminate):
        self.state = state

        self.window = pygame.display.set_mode(self.win_size, 0, 32)
        self.clock = pygame.time.Clock()

        pygame.init()

        # Begin stimuli display when the board is connected and it starts
        # streaming the data.
        print(' & stimuli & Waiting for the board to connect ...')
        streaming.wait()
        print(' & stimuli & Board connected ...')

        start_ticks = pygame.time.get_ticks()
        while True:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds < 5:
                state.value = 0
            elif seconds < 10:
                state.value = 1
                self.display_stimuli(self.colors, self.stim_size,
                                     self.position, self.freqs[0])
            elif seconds < 15:
                state.value = 0
            elif seconds < 20:
                state.value = 2
                self.display_stimuli(self.colors, self.stim_size,
                                     self.position, self.freqs[1])
            elif seconds < 25:
                state.value = 0
            elif seconds > 30:
                break

        pygame.quit()
        terminate.set()


class TwoRectangles(object):

    def __init__(self, freqs=(10.0, 14.0), timeout=8000):
        self.state = None

        self.freqs = freqs
        self.timeout = timeout

    def start_display(self, state, streaming, terminate):
        self.state = state

        win_size = (2024, 768)

        window = pygame.display.set_mode(win_size, 0, 32)

        grey = (128, 128, 128)

        size = (300, 300)

        red = (255, 0, 0)
        green = (0, 0, 255)

        pos_one = (100, 100)
        pos_two = (700, 100)

        pygame.init()

        # Begin stimuli display when the board is connected and it starts
        # streaming the data.
        print(' & stimuli & Waiting for the board to connect ...')
        streaming.wait()
        print(' & stimuli & Board connected ...')

        start_ticks = pygame.time.get_ticks()
        second = 0
        cnt = 0
        while second < self.timeout:
            second = (pygame.time.get_ticks() - start_ticks) / 1000.

            sin_val_one = 0.5+0.5*np.sin(2 * np.pi * second *
                                         float(self.freqs[0]))
            sin_val_two = 0.5+0.5*np.sin(2 * np.pi * second *
                                         float(self.freqs[1]))

            stim_one = pygame.Surface(size)
            stim_one.fill(red)
            stim_one.set_alpha(255 * sin_val_one)

            stim_two = pygame.Surface(size)
            stim_two.fill(green)
            stim_two.set_alpha(255 * sin_val_two)

            window.fill(grey)
            window.blit(stim_one, pos_one)
            window.blit(stim_two, pos_two)
            pygame.display.update()

            cnt += 1

        pygame.quit()
        terminate.set()


class P300(object):
    def __init__(self, win_size=(1024, 768), user='root'):

        self.win_size = win_size
        self.user = user
        self.state = None

    def start_display(self, state, streaming, terminate):
        self.state = state
        self.state.value = 0

        window = pygame.display.set_mode(self.win_size, 0, 32)

        stim = ['1', '2', '3', '4']

        stim_order = []
        for i in range(30):
            shuffle(stim)
            stim_order.extend(stim)

        # Base directory for stimuli.
        base_stim_dir = '/home/%s/eeg_data/stimuli/p300_img' % self.user
        unzip_dir = '/home/%s/eeg_data/stimuli' % self.user

        fetch_stimuli(stim_type='p300', target_dir=unzip_dir)
        time.sleep(2.0)

        one = pygame.image.load(os.path.join(base_stim_dir, 'one.png'))
        two = pygame.image.load(os.path.join(base_stim_dir, 'two.png'))
        three = pygame.image.load(os.path.join(base_stim_dir, 'three.png'))
        four = pygame.image.load(os.path.join(base_stim_dir, 'four.png'))
        one_neg = pygame.image.load(os.path.join(base_stim_dir, 'one_neg.png'))
        two_neg = pygame.image.load(os.path.join(base_stim_dir, 'two_neg.png'))
        three_neg = pygame.image.load(os.path.join(base_stim_dir,
                                                   'three_neg.png'))
        four_neg = pygame.image.load(os.path.join(base_stim_dir,
                                                  'four_neg.png'))

        pygame.init()

        # Begin stimuli display when the board is connected and it starts
        # streaming the data.
        print(' & stimuli & Waiting for the board to connect ...')
        streaming.wait()
        print(' & stimuli & Board connected ...')

        window.blit(one, (200, 150))
        window.blit(two, (400, 150))
        window.blit(three, (600, 150))
        window.blit(four, (800, 150))
        pygame.display.update()

        print(' & stimuli & Acquiring 2 first seconds ...')
        time.sleep(2.)
        print(' & stimuli & Interface displayed ...')
        for i in stim_order:
            if i == '1':
                window.blit(one_neg, (200, 150))
                self.state.value = 1
            elif i == '2':
                window.blit(two_neg, (400, 150))
                self.state.value = 2
            elif i == '3':
                window.blit(three_neg,  (600,  150))
                self.state.value = 3
            elif i == '4':
                window.blit(four_neg, (800, 150))
                self.state.value = 4

            pygame.display.update()
            time.sleep(1/10.)
            self.state.value = 0
            window.blit(one, (200, 150))
            window.blit(two, (400, 150))
            window.blit(three, (600, 150))
            window.blit(four, (800, 150))
            pygame.display.update()
            time.sleep(1/10.)

        print(' & stimuli & Interface closed ...')
        print(' & stimuli & Acquiring 2 last seconds ...')
        time.sleep(2.)

        pygame.quit()
        terminate.set()
