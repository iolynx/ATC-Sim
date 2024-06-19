import pygame
import math

pygame.init()

# font = pygame.font.Font(r"C:\Users\DELL\Downloads\Futura-STD\FuturaStd-Medium.otf", 10)
# font = pygame.font.Font("Futura Std.otf", 15)
font = pygame.font.SysFont("Consolas", 15)
from colors import *

class Aircraft:
    def __init__(self, cs, tp, alt, spd, pos, ang, mode, numOfTrails=5, origin=1):
        self.callsign = cs
        self.type = tp
        self.altitude = alt
        self.airspeed = spd 
        self.speed = spd / 33
        (self.x, self.y) = pos
        self.hdg = ang - math.radians(90)
        self.mode = mode
        self.numOfTrails = numOfTrails
        self.trails = []
        for i in range(self.numOfTrails, -1, -1):
            xvel = math.cos(self.hdg) * self.speed * i
            yvel = math.sin(self.hdg) * self.speed * i
            self.trails.append([self.x - xvel, self.y - yvel])

        self.assignedAlt = self.altitude
        self.assignedSpd = self.airspeed
        self.assignedHdg = self.hdg
        self.delta = math.radians(15)
        self.altDelta = 11
        self.waitingForILS = -1
        self.isLanding = False
        self.color = (255, 210, 104)
        self.drawHdg = False
        self.origin = origin
    
    def Descend(self, distToRwy):
        self.assignedAlt = distToRwy * 0.1
        self.color = WHITE


    def waitForILS(self, rwy):
        if rwy == 7 or rwy == 25:
            self.waitingForILS = 0
        elif rwy == 12 or rwy == 30:
            self.waitingForILS = 1
        else:
            self.waitingForILS = -1

    def setDir(self, newDir):
        self.hdg = newDir
    
    def updatePos(self):
        self.trails = self.trails[1:]
        self.trails.append([self.x, self.y])
        self.x += (math.cos(self.hdg) * self.speed)
        self.y += (math.sin(self.hdg) * self.speed)

        if self.assignedHdg != self.hdg:
            # offset = 360 if (self.assignedHdg - self.hdg) < -180 else 0
            # self.hdg +=  offset + (self.assignedHdg - self.hdg) / 5
            rot = math.atan2(math.cos(self.hdg)*math.sin(self.assignedHdg)-math.cos(self.assignedHdg)*math.sin(self.hdg),  \
            math.cos(self.hdg)*math.cos(self.assignedHdg)+math.sin(self.assignedHdg)*math.sin(self.hdg))

            if rot >= 0: 
                self.hdg = self.hdg + min(self.delta, rot)     
            else:
                self.hdg = self.hdg + max(-self.delta, rot)   

        if self.assignedAlt != self.altitude:
            if (self.altitude - self.assignedAlt) > 20:
                self.altitude -= self.altDelta
            else:
                self.altitude += (self.assignedAlt - self.altitude) / 6

        if self.assignedSpd != self.airspeed:
            self.airspeed += (self.assignedSpd - self.airspeed) / 6
            self.speed = self.airspeed / 33

    def checkStatus(self, boundx, boundy):
        if self.mode == "dep":
            if (self.x > boundx and self.y > boundy) or (self.x < 0 and self.y < 0):
                return "done"

    def setAssignedHdg(self, newHdg):
        self.assignedHdg = math.radians(newHdg)

    def setAssignedAlt(self, newAlt):
        if newAlt > 300 or newAlt < 14:
            print("invalid height!")
            return
        self.assignedAlt = newAlt

    def setAssignedSpd(self, newSpd):
        if newSpd < 120 or newSpd > 250:
            print("invalid speed!")
            return
        self.assignedSpd = newSpd
    
    def draw(self, surface):
        # color = (255, 210, 104) if self.mode == "dep" else (255, 255, 255)
        pygame.draw.circle(surface, self.color, (round(self.x), round(self.y)), 4, 2)

        for i in range(self.numOfTrails):
            # print(self.trails[i])
            pygame.draw.circle(surface, self.color, tuple(self.trails[i]), 1)
            
        pygame.draw.line(surface, self.color, (self.x + 7, self.y), (self.x + 22, self.y))

        text = font.render(self.callsign, True, self.color)
        surface.blit(text, (self.x + 25, self.y - 6))
        text = font.render("FL" + str(int(round(self.altitude, 0))) + " " + str(int(self.airspeed)), True, self.color)
        surface.blit(text, (self.x + 25, self.y + 6))




