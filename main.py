import pygame
import math
import random
import os
import numpy as np
import pygame_widgets

from colors import *
from aircraft import Aircraft
from airport import Airport
from command import CommandBar
import pygame_textinput as pt
from utilities import *
from aircraftSpawner import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from ATC import ATC

MAXWIDTH = 1400
MAXHEIGHT = 700

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

tick = 60
MOVEEVENT = pygame.USEREVENT+1
SPAWNEVENT = pygame.USEREVENT+2
# moveTimeInterval = 1000
# spawnTimeInterval = 60000
moveTimeInterval = 50
spawnTimeInterval = 1000
pygame.time.set_timer(MOVEEVENT, moveTimeInterval)
pygame.time.set_timer(SPAWNEVENT, spawnTimeInterval)

win = pygame.display.set_mode((MAXWIDTH, MAXHEIGHT))
pygame.display.set_caption("Air Traffic Simulator")
# text_font = pygame.font.SysFont("Helvetica", 30)
# title_text_font = pygame.font.SysFont("Helvetica", 50)
smallfont = pygame.font.SysFont("Consolas", 15)
# number_font = pygame.font.SysFont("Consolas", 32)
font = pygame.font.SysFont("Consolas", 25)

coastline2 = pygame.image.load("coastline.png").convert()
coastline  = pygame.transform.rotozoom(coastline2, 0, 0.79)
headingcircle = pygame.image.load("headingCircleInverted.png").convert_alpha()
headingCircle  = pygame.transform.rotozoom(headingcircle, 1, 0.5)

headingRect = headingCircle.get_rect()


cwd = os.path.realpath(__file__)
cwd = cwd.rstrip("main.py")

#--------- INIT ---------
aircraft = [Aircraft("IGO134", "A322", 80, 200, (200,500), math.radians(90), "dep", 6)]
vomm = Airport(2, [24, 18], [[684, 333], [688, 321]], [math.radians(71), math.radians(119)], (702, 327))
cmb = CommandBar((10, 648, 450, 38))
manager = pt.TextInputManager(validator = lambda input: len(input) <= 31)
text_input = pt.TextInputVisualizer(manager=manager, font_object=font)
text_input.cursor_width = 4
text_input.cursor_blink_interval = 400 # blinking interval in ms
text_input.antialias = True
text_input.font_color = (217, 219, 221)
text_input.cursor_color = (217, 219, 221)
pygame.key.set_repeat(200, 25)
idx = []
inpHistory = []
userInp = ""
spawnSlider = Slider(win, 1300, 15, 40, 20, min = 1, max = 10, step = 1, colour=WHITE, handleColour=LGREY )
spawnOutput = TextBox(win, 1300, 55, 50, 50, fontSize=30, colour=BLACK, textColour=WHITE)
atc = ATC()
atcActivated = True
run = True

while run:
    events = pygame.event.get()
    text_input.update(events)
    for event in events:
        if event.type == pygame.QUIT:
            run = False;
        if event.type == MOVEEVENT:
            for ac in aircraft:
                ac.updatePos()
        if event.type == SPAWNEVENT:
            choices = [0, 1, 2]
            weights = [7, 3, 1]
            ch = random.choices(choices, weights)[0]
            aircraft.append(createNewAircraft(ch))
            # if(random.randint(0, 6) == 2):
            #     aircraft.setDir(aircraft.dir + math.radians(12))
        if event.type == pygame.KEYDOWN:
            inpHisIdx = 1
            if event.key == pygame.K_CAPSLOCK:
                atcActivated = not atcActivated

            if event.key == pygame.K_RETURN:
                userInp = text_input.value
                inpHistory.append(userInp.split()[0])
                print(userInp)
                text_input.value = ""
                inpHisIdx = 1
                for ac in aircraft:
                    ac.drawHdg = False
            if event.key == pygame.K_UP and inpHistory != []:
                text_input.value = "".join(inpHistory[:-inpHisIdx])
                inpHisIdx += 1
            if event.key == pygame.K_BACKSPACE and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                text_input.value = ' '.join(text_input.value.split()[:-1])

            if event.key == pygame.K_t:
                print("tttt")
                # for ac in aircraft:
                    # if ac.callsign == "".join(text_input.value.split()[0]).upper() :
                    #     ac.drawHdg = True
                    #     print("".join(text_input.value.split()[1].upper()))
                    #     print("drawing hdg")
        
    
    win.fill(BLACK)
    win.blit(coastline, (10, -15))
    vomm.draw(win)
    cmb.draw(win)


    if atcActivated:
        atc.update(aircraft, vomm)


    for ac in aircraft:
        ac.draw(win)

        userInpSplit = text_input.value.split()
        if len(userInpSplit) >= 2 and ac.callsign.upper() == userInpSplit[0].upper() and "T" in userInpSplit[1].upper():
            ac.drawHdg = True
            # if(len(userInpSplit) == 3):
        else:
            ac.drawHdg = False


        for ac2 in aircraft:
            if ac == ac2:
                continue 
            if abs(ac.altitude - ac2.altitude) < 4 and math.dist((ac.x, ac.y), (ac2.x, ac2.y)) < 100 and ac.altitude > 15 and ac2.altitude > 15:
                pygame.draw.circle(win, RED, (ac.x, ac.y), 50, 3)
                pygame.draw.circle(win, RED, (ac2.x, ac2.y), 50, 3)
                atc.space(ac, ac2)
            
        
        if ac.drawHdg:
            win.blit(headingCircle, (ac.x - headingRect.width // 2, ac.y - headingRect.height // 2))

        if ac.waitingForILS != -1:
            p3 = np.array([ac.x, ac.y])
            p1 = np.array([vomm.ils[ac.waitingForILS][0], vomm.ils[ac.waitingForILS][1]])
            p2 = np.array([vomm.ils[ac.waitingForILS][2], vomm.ils[ac.waitingForILS][3]])
            d = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
            if d < 24:
                # print("ILS ESTABLISHED")
                ac.isLanding = True
                ac.setAssignedHdg(angle_between((ac.x, ac.y), vomm.centerPos))
                ac.waitingForILS = -1

        if ac.isLanding:
            ac.setAssignedHdg(angle_between((ac.x, ac.y), vomm.centerPos))
            dist = math.dist([ac.x, ac.y], vomm.centerPos)
            ac.Descend(dist)
            if dist < 14:
                idx.append(aircraft.index(ac))
                continue
            # print(math.degrees(ac.assignedHdg))
    
    for i in idx:
        del aircraft[i]
        idx = []

    win.blit(text_input.surface, (20, 654))

    if userInp:
        invalid = False
        userTokens = userInp.split()
        if(len(userTokens)) == 3:
            for i in aircraft:
                if userTokens[0].upper() == i.callsign:
                    if(userTokens[1] == 't'):
                        i.setAssignedHdg(int(userTokens[2]) - 90)
                        ac.drawHdg = True
                    elif(userTokens[1] in "adc"):
                        i.setAssignedAlt(int(userTokens[2]))
                    elif userTokens[1] == "s":
                        i.setAssignedSpd(int(userTokens[2]))
                    elif userTokens[1] == "ils":
                        i.waitForILS(int(userTokens[2]))
                        print("waiting for ils")

        userTokens = []
        userInp = ""


    text = smallfont.render(str(pygame.mouse.get_pos()), True, WHITE)                 
    win.blit(text, (0, 0))
    

    pygame.display.update()
    clock.tick(tick)

pygame.quit()