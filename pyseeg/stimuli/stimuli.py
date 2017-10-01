import datetime
import pygame
import time

class SSVEPStimuli(object):

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
