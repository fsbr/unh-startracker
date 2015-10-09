# functions for processing the experimental data
from __future__ import division
import sys
sys.path.append('/home/newmy/research/python/starTracker')

from frameworks import *
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from numpy import *
import matplotlib.pyplot as plt

# both the yprProcess and accelProcess functions take a 4 vector in
# they output different stuff though
# ypr outputs a unit vector based on the rotation angle of the imu.

def yprProcess(data):
    # in this function what we need to do is convert the YPR angles into
    # a meaningful unit vector, and then plot it
    print data
    data = [x*(pi/180) for x in data[1:]]
    print data
    print 'fuck'
    
def accelProcess(data):
    print 'you'
