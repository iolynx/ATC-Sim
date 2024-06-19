import pygame

from colors import *


pygame.init()
font = pygame.font.SysFont("Consolas", 25)

class CommandBar:
    def __init__(self, size):
        self.size = size

    def draw(self, surface):
        pygame.draw.rect(surface, DGREY, self.size, 0, 12)
        pygame.draw.rect(surface, WHITE, self.size, 2, 12)
        