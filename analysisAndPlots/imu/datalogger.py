# logs the YPR angles from the IMU and the UTC time
# tckf sept - 2015

# this is one of the worst scripts ive ever written. 14-oct-2015

from __future__ import division
import serial
import time
import datetime

f = open('pitch_test', 'w')
e = open('roll_test', 'w')
t = open('timedoc','w')
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
            roll = data[0][3]
            pitch = float(pitch)
            roll = float(roll)
            # f.write(" " + str(data) + "  " + str(datetime.datetime.utcnow()))
            f.write(pitch)
            print pitch
            return [pitch,roll] 
    except:
        pass

def calcBias():
    # the idea of this function is to average some of the early data points
    # and to compute the bias, just do a simple mean

    array = []
    count = 0
    while count<100:
        pitch = readPitchData()
        if pitch == None:
            pass
        elif pitch != None:
            # array.append(pitch)
            f.write(str(pitch[0]) + ",\n")
            e.write(str(pitch[1])+ ",\n")
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
    # bias = calcBias() 
    # print bias
    gcount = 0
    ti = datetime.datetime.now().time()
    while gcount < 1000:
        # print pitch
        pitch = readPitchData()
        f.write(str(pitch) + "\n")
        gcount = gcount +1
    tf = datetime.datetime.now().time()
    t.write(str(ti)+ "\n")
    t.write(str(tf)+ "\n")
    f.close()
