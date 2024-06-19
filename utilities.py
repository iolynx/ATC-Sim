import numpy as np
import math

# def angle_between(p1, p2):
#     ang1 = np.arctan2(*p1[::-1])
#     ang2 = np.arctan2(*p2[::-1])
#     return (ang1 - ang2) % (2 * np.pi)


def angle_between(p1, p2):
    (x1, y1) = tuple(p1)
    (x2, y2) = tuple(p2)
    return math.degrees(math.atan2(y2-y1, x2-x1))
