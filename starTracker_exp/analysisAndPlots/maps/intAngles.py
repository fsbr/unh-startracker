# compute the interior angles and side lengths between these two points

from __future__ import division

# allow me to use the cosd and acosd functions i wrote
import sys as sys
sys.path.append("/home/newmy/research/exp/starTracker_exp")

import math as m
import numpy as np
import ST as ST
def sideLengths(zeroth, first, second):
    # p1 and p2 are 1x2 arrays
    # be extremely careful when you give arguments and globals similar names 
    # returns side 01, 02, and 12 in that order
    s01 = m.sqrt((first[0] - zeroth[0])**2 + (first[1] - zeroth[1])**2 )
    s02 = m.sqrt((second[0] - zeroth[0])**2 + (second[1] - zeroth[1])**2 )
    s12 = m.sqrt((second[0] - first[0])**2 + (second[1] - first[1])**2 )
    return [s01, s02, s12]

def findIntAngles(sides):
    # once we know the sideLengths, we can get the interior angles by using
    # the law of cosines a bunch of times
    print "something something %s" %sides 
    # try the law of Cosines function
    a = sides[0]
    b = sides[1]
    c = sides[2]
    
    gamma = lawOfCosines(a,b,c)
    beta = lawOfCosines(a,c,b)
    alpha = lawOfCosines(b,c,a)
    return [alpha, beta, gamma]

def lawOfCosines(sideA, sideB, sideC):
    # solves for the ANGLE given the three side lengths
    # this corresponds to the pixel lengths that we're already getting
    # from teh star camera
    
    # first compute the thing going into acos
    arg = sideA**2 + sideB**2 - sideC**2
    arg = arg/(2*sideA*sideB)
    angle = ST.acosd(arg)
    return angle
    

def calcSidesAngles(points0, points1, points2):
    # this does everything at once
    
    # break up the points 
    triSides = sideLengths(points0, points1, points2)
    angles = findIntAngles(triSides)
    print "sides are %s" %(triSides)
    print "angles are %s" %(angles)
    print "sum of int. angles is %s" %(sum(angles)) 

if __name__ == '__main__':
    # all i want to be doing is giving the points and running ONE function
 
    p0 = [307.6165, 213.7392]
    p1 = [534.2772, 167.0859]
    p2 = [397.0268, 515.3920]
    
    n0 = [616, 121.6396]
    # n1 = [212.7474, 259.3764]
    n1 = [789, 453] # i manually went and found the star with matlab lol 
    n2 = [502.1208, 321.6461]


    triSides = calcSidesAngles(p0, p1, p2)
    triSides = calcSidesAngles(n0, n1, n2)

