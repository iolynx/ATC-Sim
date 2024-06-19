from aircraft import *
from airport import *
from utilities import *

coords7 = [282, 521]
coords30 = [464, 130]

class ATC:
    def __init__(self):
        pass

    def update(self, aircrafts : Aircraft, airport : Airport):
        for a in aircrafts:
            if a.origin == 0:
                if math.dist((a.x, a.y), coords30) > 70:
                    a.setAssignedHdg(angle_between((a.x, a.y), (coords30[0], coords30[1])))
                else:
                    a.setAssignedHdg(angle_between((a.x, a.y), (airport.ils[1][0], airport.ils[1][1])))
                    a.waitingForILS = 1
            else:
                if math.dist((a.x, a.y), coords7) > 90:
                    a.setAssignedHdg(angle_between((a.x, a.y), (coords7[0], coords7[1])))
                else:
                    a.setAssignedHdg(angle_between((a.x, a.y), (airport.ils[0][0], airport.ils[0][1])))
                    a.waitingForILS = 0
            
            a.setAssignedAlt(25)
            if math.dist((a.x, a.y), airport.centerPos) < 200:
                a.setAssignedSpd(150)
            elif math.dist((a.x, a.y), airport.centerPos) < 400:
                a.setAssignedSpd(210)

    def space(self, ac1: Aircraft, ac2 : Aircraft):
        ac1.setAssignedHdg(ac1.hdg - 20)
        ac2.setAssignedHdg(ac2.hdg + 20)


