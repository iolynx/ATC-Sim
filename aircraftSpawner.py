import pygame
import math
from aircraft import *
import random

fixes = {
    "hydok" : [(791, 5), 195],  
    "avgir" : [(1396, 587), 284],
    "tryco" : [(519, 669), 15]   #34
}


def createNewAircraft(ch):
    fixName = list(fixes.keys())[ch]
    fixPos = fixes[fixName][0]
    fixAng = fixes[fixName][1]
    
    ICAOCodes = ["IGO", "SEJ", "VTI", "AIQ", "BDA", "ETH", "AIC", "ETD", "UAE", "QTR", "CPA"]
    codeWeights = [9, 6, 5, 3, 5, 2, 4, 2, 4, 2, 1]
    num = str(random.randint(100, 9999))
    # icaoCode = ICAOCodes[random.randint(0, len(ICAOCodes) - 1)]
    icaoCode = "".join(random.choices(ICAOCodes, codeWeights))


    ac = Aircraft(icaoCode + num, "A322", random.randint(70, 120), random.randint(220, 260), fixPos, math.radians(fixAng), "arr", 6, ch)

    return ac

# def drawFixes(surface):
#     for fixName in fixes.keys():
#         pygame.draw.circle(surface, WHITE, fixes[fixName][0], 10)