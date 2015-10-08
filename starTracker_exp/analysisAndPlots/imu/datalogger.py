# logs the YPR angles from the IMU and the UTC time
# tckf sept - 2015

from __future__ import division
import serial
import time
import datetime

f = open('pitch_test', 'w')
ser = serial.Serial('/dev/ttyUSB0', baudrate = 57600)
# ser.write('#ot')
time.sleep(1)

def readPitchData():
    data = ser.readline()
    data = data.split(',')
    data = [x.rsplit() for x in data]
    print data
    # f.write(str(data) + ",\n")

    # save this trycatch to view the data in different ways
    #try:
    #    pass
     #   print data[2][0]
    #except:
    #    pass

    # we need to get only the ypr data
    try:
        if data[0][0] == '#YPR=':
            # print type(float(data[2][0]))
            # f.write(str(data))
            pitch = data[0][2]
            pitch = float(pitch)
            # f.write(" " + str(data) + "  " + str(datetime.datetime.utcnow()))
            print pitch
            return pitch 
    except:
        pass

def calcBias():
    # the idea of this function is to average some of the early data points
    # and to compute the bias, just do a simple mean

    array = []
    count = 0
    while count<10000:
        pitch = readPitchData()
        if pitch == None:
            pass
        elif pitch != None:
            # array.append(pitch)
            f.write(str(pitch) + ",\n")
            count = count + 1
        else:
            # nothing happens
            pass
    # print array
    
    # get the average
    total = sum(array)
    n = len(array)
    # bias = total/n
    return bias
    
if __name__ == "__main__":
    # calculate the offset for the neutral position
    bias = calcBias() 
    # print bias
    count = 0
    while count < 100:
        # print pitch
        pitch = readPitchData()
        # f.write(str(pitch) + "\n")
        count = count +1
