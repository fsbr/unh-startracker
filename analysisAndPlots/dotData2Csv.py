# this will take an input .data file from the IMU and 
# it will get converted into a csv file which is a little easier to
# work with in the programming environments.
# tckf spring 2016.  SO CLOSE to being done.

#tbh i have no idea how regex works.
import re
from sys import argv

script, dataFile = argv
# open the input file
f = open(dataFile)
output = open('%s.csv'%(dataFile),'w')


for line in f.readlines(): #goes too long
    newData = []
    # the characters to be split will change by dataset
    line = re.split(r'[\[\],: ]', line)
    try:
        # the indices here will change by dataset
        # so will the casts.  think about what you're doing
        newData.append(float(line[2]))
        newData.append(float(line[4]))
        newData.append(float(line[6]))
        newData.append(line[9])
        newData.append(float(line[10]))
        newData.append(float(line[11]))
        newData.append(float(line[12]))

        # write things to the csv file
        for entry in newData:
            output.write(str(entry))
            output.write(",")
        output.write("\n")
    except:
        pass

output.close()
    
