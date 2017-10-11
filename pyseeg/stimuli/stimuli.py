import datetime
import numpy as np
import pygame
import time


class SimpleRectangle(object):

    def __init__(self):
        self.state = None
    
    def display_stimuli(self, size, pos, color, freq):
        self.window.blit(self.rectangle, pos)
        pygame.display.update()
        time.sleep(freq)
        self.window.blit(self.background, pos)
        pygame.display.update()
        time.sleep(freq)
        self.clock.tick(60)

    def display_background(self, pos):
        self.window.blit(self.background, pos)
        pygame.display.update()
    
    def start_display(self, state, streaming, terminate):
        self.state = state

        self.window = pygame.display.set_mode((800, 800), 0, 32)

        position = (0, 0)
        size = (300, 300)
        black = (0, 0, 0)
        grey = (229, 229, 229)

        self.rectangle = pygame.Surface(size)
        self.rectangle.fill(grey)
        self.background = pygame.Surface(size)
        self.background.fill(black)
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
                self.display_stimuli(size, position, black, 1/10.)
            elif seconds < 15:
                state.value = 0
                self.display_background(position)
            elif seconds < 20:
                state.value = 2
                self.display_stimuli(size, position, black, 1/14.)
            elif seconds < 25:
                state.value = 0
                self.display_background(position)
            elif seconds < 30:
                break

        pygame.quit()
        terminate.set()


class TwoRectangles(object):

    def __init__(self, freqs=(10.0, 14.0), timeout=8000):
        self.state = None

        self.freqs = freqs
        self.timeout = timeout
    
    def display_stimuli(self, size, pos, color, freq):
        self.window.blit(self.rectangle, pos)
        pygame.display.update()
        time.sleep(freq)
        self.window.blit(self.background, pos)
        pygame.display.update()
        time.sleep(freq)
        self.clock.tick(60)

    def display_background(self, pos):
        self.window.blit(self.background, pos)
        pygame.display.update()
    
    def start_display(self, state, streaming, terminate):
        self.state = state

        win_size = (1024, 768)

        window = pygame.display.set_mode(win_size, 0, 32)

        grey = (128, 128, 128)

        size = (300, 300)

        red = (255, 0, 0)
        green = (0, 0, 255)

        pos_one = (100, 100)
        pos_two = (500, 100)

        pygame.init()

        # Begin stimuli display when the board is connected and it starts
        # streaming the data.
        print(' & stimuli & Waiting for the board to connect ...')
        streaming.wait()
        print(' & stimuli & Board connected ...')

        start_ticks = pygame.time.get_ticks()
        second= 0
        cnt = 0
        while second < self.timeout:
            second = (pygame.time.get_ticks() - start_ticks) / 1000.

            sin_val_one = 0.5+0.5*np.sin(2 * np.pi * second * float(self.freqs[0]))
            sin_val_two = 0.5+0.5*np.sin(2 * np.pi * second * float(self.freqs[1]))


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
