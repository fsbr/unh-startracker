# calc d
from __future__ import division
import ST
import math as m
def calcD(Li, Bi, Lf, Bf):
    d = 60*m.sqrt((Li-Lf)**2*ST.cosd(Bf) + (Bi - Bf)**2)
    return d

if __name__ == "__main__":
    print calcD(-78.2927, 44.2405, -70.9349, 43.1337)
    print calcD(-71.239, 44.392, -70.9349, 43.1337)
    print calcD(-70.9404, 43.2087, -70.9349, 43.1337)
    print calcD(-69.6075, 42.3059, -70.9349, 43.1337)
