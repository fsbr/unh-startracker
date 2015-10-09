from __future__ import division
import sys
sys.path.append('/home/newmy/research/python/starTracker/.')
import frameworks as fw
import serial
ser = serial.Serial( '/dev/ttyUSB0', baudrate = 57600 )
#ser.write('#osrt')
import time
import numpy as np
import plotting as P
time.sleep(1)


import re
#import expUtils as xU #not sure the diff b/w import and from "" import *

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.gca(projection = '3d')

# i think we have to define all the functions we wanto to use FIRST? idk
# thats how im gonna do it lets hope thats not functional fixedness

def accelCalc(dataVector):
    print "accel"
    #print dataVector

    # do the goofy quaternion thing and plot
    # important, i just wnat to get the numbers in here, then i plot with a general function
    
    # first thing is to read in the accel stuff
    print dataVector

    aX = float(dataVector[1])*np.pi/180
    aY = float(dataVector[2])*np.pi/180
    aZ = float(dataVector[3])*np.pi/180

    print aX
    print aY
    print aZ
    
    # for the yz plane use aY and aZ (zeta)
    zeta = np.arccos(np.dot(aY,aZ))*180/np.pi
    print zeta 

    # for the xz plane use aX and aZ (psi)
    psi = np.arccos(np.dot(aX,aZ))*180/np.pi
    print psi

    
def yprCalc(dataVector):
    print "YPR"
    
    # data vector goes label, y, p, r
    #print dataVector
    
    xAxis = np.matrix([1,0,0]).transpose()
    yAxis = np.matrix([0,1,0]).transpose()
    zAxis = np.matrix([0,0,1]).transpose()

    yawAngle = float(dataVector[1])
    pitchAngle = float(dataVector[2])
    rollAngle = float(dataVector[3])
    
    #rotations (might not be the right order)
    # first yaw then pitch then roll
    
    # let's do the calculation (just get the number)
    # rotation 
    
    # u can't operate on a string
    
    # pretty much here's where the B/L coordinate transformation is happening
    yaw = fw.R3(yawAngle)
    pitch = fw.R2(-pitchAngle)
    roll = fw.R1(rollAngle)
    
    rotationSequence = roll*pitch*yaw

    newX = rotationSequence*xAxis
    newY = rotationSequence*yAxis
    newZ = rotationSequence*zAxis
    #print newX
    #print newY
    #print newZ 
    
    # return a list w/ the new X, Y, Z as matrix objects in the list
    # each element of the list contains 3 values
    yprVector = [newX, newY, newZ]
    return yprVector

def plotYPR(yprVector):
    # does the plotting
    #print "inside the plotting function"
    ypr1x = yprVector[0][0]
    ypr1y = yprVector[1][0]
 

def mainLoop():
    # sets up the   p.plot3dClass(5,1)
    #while True:
    for i in range(0,100):
        # i want to see if resetting the value gets the program to start
        data = 0 
        # this is the main loop for celnav 
        data = ser.readline()
        data =  data.split(',')
        data = [x.rsplit() for x in data]
        if len(data) == 4:
            label = data[0][0]
            x = data[1][0]
            y = data[2][0]
            z = data[3][0]
            newData = [label, x, y, z]
            
            if newData[0] == '#YPR=':
                # really what i want is to do the euler angles
                yprVector = yprCalc(newData)
                #print newData
                #print yprVector
                newX = plotYPR(yprVector)
                
                # change this line to adjust the rest of it
                ax.plot(newX[1], newX[0], newX[2], label = 'fuck')
                plt.ylim([-5,5])
                ax.set_zlim([-5,5])
                plt.xlim([-5,5])
            elif newData[0] == '#A-':
                # do the acceleration thing
                accelCalc(newData)
            else:
                print "neither"


def mainLoop():
    # sets up the   p.plot3dClass(5,1)
    #while True:
    for i in range(0,100):
        # i want to see if resetting the value gets the program to start
        data = 0 
        # this is the main loop for celnav 
        data = ser.readline()
        data =  data.split(',')
        data = [x.rsplit() for x in data]
        if len(data) == 4:
            label = data[0][0]
            x = data[1][0]
            y = data[2][0]
            z = data[3][0]
            newData = [label, x, y, z]
            
            if newData[0] == '#YPR=':
                # really what i want is to do the euler angles
                yprVector = yprCalc(newData)
                #print newData
                #print yprVector
                newX = plotYPR(yprVector)
                
                # change this line to adjust the rest of it
                ax.plot(newX[1], newX[0], newX[2], label = 'fuck')
                plt.ylim([-5,5])
                ax.set_zlim([-5,5])
                plt.xlim([-5,5])
            elif newData[0] == '#A-':
                # do the acceleration thing
                accelCalc(newData)
            else:
                print "neither"
   ypr1z = yprVector[2][0]
    
    # this line for debug purposes
    # ypr_1 = [ypr00, ypr01,

def mainLoop():
    # sets up the   p.plot3dClass(5,1)
    #while True:
    for i in range(0,100):
        # i want to see if resetting the value gets the program to start
        data = 0 
        # this is the main loop for celnav 
        data = ser.readline()
        data =  data.split(',')
        data = [x.rsplit() for x in data]
        if len(data) == 4:
            label = data[0][0]
            x = data[1][0]
            y = data[2][0]
            z = data[3][0]
            newData = [label, x, y, z]
            
            if newData[0] == '#YPR=':
                # really what i want is to do the euler angles
                yprVector = yprCalc(newData)
                #print newData
                #print yprVector
                newX = plotYPR(yprVector)
                
                # change this line to adjust the rest of it
                ax.plot(newX[1], newX[0], newX[2], label = 'fuck')
                plt.ylim([-5,5])
                ax.set_zlim([-5,5])
                plt.xlim([-5,5])
            elif newData[0] == '#A-':
                # do the acceleration thing
                accelCalc(newData)
            else:
                print "neither"
 ypr02]
    ypr1x = float(ypr1x)
    ypr1y = float(ypr1y)
    ypr1z = float(ypr1z)
    
    ypr1x = fw.makeVector(ypr1x)
    ypr1y = fw.makeVector(ypr1y)
    ypr1z = fw.makeVector(ypr1z)

    newX = [ypr1x, ypr1y, ypr1z]
    
    return newX 


def mainLoop():
    # sets up the   p.plot3dClass(5,1)
    mpl.interactive(True)
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    #while True:
    for i in range(0,100):
        # i want to see if resetting the value gets the program to start
        data = 0 
        # this is the main loop for celnav 
        data = ser.readline()
        data =  data.split(',')
        data = [x.rsplit() for x in data]
        if len(data) == 4:
            label = data[0][0]
            x = data[1][0]
            y = data[2][0]
            z = data[3][0]
            newData = [label, x, y, z]
            
            if newData[0] == '#YPR=':
                # really what i want is to do the euler angles
                yprVector = yprCalc(newData)
                #print newData
                #print yprVector
                newX = plotYPR(yprVector)
                
                # change this line to adjust the rest of it
                ax.plot(newX[1], newX[0], newX[2], label = 'fuck')
                plt.ylim([-5,5])
                ax.set_zlim([-5,5])
                plt.xlim([-5,5])
            elif newData[0] == '#A-':
                # do the acceleration thing
                accelCalc(newData)
            else:
                print "neither"
        #time.sleep(1)
# run the main loop
mainLoop()
plt.show(block=True)
