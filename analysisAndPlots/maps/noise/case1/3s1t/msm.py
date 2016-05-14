# this script plots points from the monte carlo onto the northeast
from __future__ import division
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import csv as csv
import itertools as itertools
import matplotlib.pyplot as plt
# statistics = open('statistics', 'w')

def findMean(aList):
    return sum(aList)/len(aList)


csvFiles = ['.csv', 'arcTen2.csv']
def makeLatLons(fileName):
    # this function returns the latitude and lognitude from an input file into 
    with open(fileName, 'rb') as f:
        reader = csv.reader(f)
        longLats = list(reader)

    lons = []
    lats = []
    outLIARS = [[],[]]
    realData = [[],[]]
    for row in longLats:
        lons.append(float(row[0]))
        lats.append(float(row[1]))

    longLats = [lons, lats]
    # print longLats[0][:]
    meanLat = findMean(lats)
    meanLon = findMean(lons)
    #print meanLat
    #print meanLon
    return [lats,lons]

dataPoints = makeLatLons('3star1t_1')
lats = dataPoints[0]
lons = dataPoints[1]

data2 = makeLatLons('3star1t_2')
lats2 = data2[0]
lons2 = data2[1]
data3 = makeLatLons('3star1t_5')
lats3 = data3[0]
lons3 = data3[1]

#latQuarts = iqrAndStuff(lats)
#lonQuarts = iqrAndStuff(lons)

#for i in range(0,len(lons)): # the longitudes
#    if longLats[0][i] > lonQuarts[2]:
#        outLIARS[0].append(longLats[0][i])
#        outLIARS[1].append(longLats[1][i])
#        #print "both coordinates, long too big ==%s,%s" %(longLats[0][i],longLats[1][i])
#    elif longLats[0][i] < lonQuarts[1]:
#        outLIARS[0].append(longLats[0][i])
#        outLIARS[1].append(longLats[1][i])
        #print "both coordinate, long to small == %s,%s"%(longLats[0][i],longLats[1][i])
#    elif longLats[1][i] > latQuarts[2]:
#        outLIARS[0].append(longLats[0][i])
#        outLIARS[1].append(longLats[1][i])
        #print "both coordinates, lat too big ==%s,%s" %(longLats[0][i],longLats[1][i])
#    elif longLats[1][i] < latQuarts[1]:
#        outLIARS[0].append(longLats[0][i])
#        outLIARS[1].append(longLats[1][i])
        #print "both coordinate, lat to small == %s,%s"%(longLats[0][i],longLats[1][i])
#    else:
#        realData[0].append(longLats[0][i])
#        realData[1].append(longLats[1][i])
         
#print outLIARS
#oLons = outLIARS[0]
#oLats = outLIARS[1]
#print oLons
#print oLats

#lons = realData[0]
#lats = realData[1]

ab = plt.hist(lons,bins=range(-180,180))
ac = plt.hist(lats,bins=range(-90,90))
plt.xlabel('Degrees of Estimate')
plt.ylabel('Frequency')
plt.title('Histogram of Observations')
plt.show()
print ab
print ac
meanLon = sum(lons)/len(lons)
print meanLon
meanLat = sum(lats)/len(lats)
print meanLat
# print "just long = %s" %longLats[0][i]
# print "just lats = %s" %longLats[1][i]
# print "fuckin both longlats = %s,%s" %(longLats[0][i],longLats[1][i]) 

# find mean of the points

# make sure the value of resolution is a lowercase L,
# for 'low' not number 1

my_map = Basemap(projection='merc', lat_0=43.133947, lon_0=-70.9354,
            resolution='h', area_thresh=1000.0,
            llcrnrlon=-180.0, llcrnrlat=-80.0,
            urcrnrlon=180.0, urcrnrlat=80.0)

# seacoast region ll lon = -75, lat = 40
#                 ur lon = -68, lat = 44

my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color='green')
my_map.drawmapboundary()

my_map.drawstates()
my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))


# put in the points

x,y = my_map(lons, lats)
x1,y1 = my_map(lons2,lats2)
x2,y2 = my_map(lons3,lats3)
#xO,yO = my_map(oLons, oLats)
tvx, tvy = my_map(-70.9349, 43.1337)
my_map.plot(x2,y2,'go',markersize=5)
my_map.plot(x1,y1,'ro',markersize=5)
my_map.plot(x,y, 'bo', markersize =5)
my_map.plot(tvx,tvy, 'co', markersize=10)
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.title('noise for three stars observed at a single time')
plt.legend()

plt.show()
