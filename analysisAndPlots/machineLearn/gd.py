# i'm too dumb for matlab.  the only reason i was using it was to be able to get csv data easier but
# the time has come for me to grow into a real man.
# this script

from __future__ import division
import numpy as np
import math as m
tht_old = 0
tht_new = 4
ty_old = 0
ty_new =1 
def sind(theta):
    return m.sin(m.radians(theta))
def cosd(theta):
    return m.cos(m.radians(theta))
def tand(theta):
    return m.tan(m.radians(theta))
    
# i have no idea how these values are selected.
alpha = 0.001
precision = 0.000000001

# theta derivative
def tht_der(tht,thtR, ty, x,y):
    #try it
    # j direction 
    return -x*cosd(tht+thtR) - (y+ty)*sind(tht+thtR)

def ty_der(tht,thtR):
    # try to write the pitch derivative
    return cosd(tht+thtR)  

while abs(tht_new-tht_old+ty_new-ty_old)>precision:
    tht = 0.54
    x = 93.5697
    y = 929.1361
    
    #tht_old = tht_new
    #ty_old = ty_new
    ty_new = ty_old - alpha*ty_der(tht,ty_old)
    tht_new = tht_old - alpha*tht_der(tht,tht_old, ty_old,x,y)
    ty_old = ty_new
    tht_old = tht_new

print "local min occurs at %s,%s"%(tht_new,ty_new)
