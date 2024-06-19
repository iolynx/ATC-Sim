import pygame
import math
from colors import *


font = pygame.font.SysFont("Consolas", 12)

class Airport:
    def __init__(self, numberOfRunways, runwayLength, pos, dir, centerPos):
        self.numberOfRunways = numberOfRunways
        self.runwayLength = []
        for i in range(numberOfRunways):
            self.runwayLength.append(runwayLength[i])
        self.pos = []
        for i in range(numberOfRunways):
            self.pos.append(pos[i])
        self.dir = []
        for i in range(numberOfRunways):
            self.dir.append(dir[i] - math.radians(90))
        self.centerPos = []
        for i in range(numberOfRunways):
            self.centerPos.append(centerPos[i])

        self.ils = []
        for i in range(self.numberOfRunways):
            self.guideLineStart = (self.pos[i][0] - math.cos(self.dir[i]) * self.runwayLength[i] * 13\
            , self.pos[i][1] - math.sin(self.dir[i]) * self.runwayLength[i] * 13)

            self.guideLineEnd = (self.pos[i][0] + math.cos(self.dir[i]) * self.runwayLength[i] * 13\
            , self.pos[i][1] + math.sin(self.dir[i]) * self.runwayLength[i] * 13)

            self.ils.append(self.guideLineStart + self.guideLineEnd)

        print(self.pos)

    def draw(self, surface):
        for i in range(self.numberOfRunways):
            # guideLineStart = [self.pos[i][0] - math.cos(self.dir[i]) * self.runwayLength[i] * 10\
            # , self.pos[i][1] - math.sin(self.dir[i]) * self.runwayLength[i] * 10]

            # guideLineEnd = [self.pos[i][0] + math.cos(self.dir[i]) * self.runwayLength[i] * 10\
            # , self.pos[i][1] + math.sin(self.dir[i]) * self.runwayLength[i] * 10]


            pygame.draw.line(surface, LGREEN, (self.ils[i][0], self.ils[i][1]), (self.ils[i][2], self.ils[i][3]))

            endX = self.pos[i][0] + math.cos(self.dir[i]) * self.runwayLength[i]
            endY = self.pos[i][1] + math.sin(self.dir[i]) * self.runwayLength[i]
            pygame.draw.line(surface, GREEN, (self.pos[i][0], self.pos[i][1]), (endX, endY), 3)



        for i in range(12):
            pygame.draw.circle(surface, LGREEN, self.centerPos, i * 80, 1)

        text = font.render("VOMM", True, GREEN)
        surface.blit(text, (self.centerPos[0] - 3, self.centerPos[1] + 20))