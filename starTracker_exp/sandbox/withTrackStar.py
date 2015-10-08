# UNH Star Tracker Calculator
# Uses the Nautical Almanac "Direct Computational" Method
# 2015 Nautical Almanac Commercial Edition pg. 283
# tckf - september - 2015
from __future__ import division
import math as m

#simple math utils for working in degrees
def sind(theta):
    return m.sin(m.radians(theta))
def cosd(theta):
    return m.cos(m.radians(theta))
def tand(theta):
    return m.tan(m.radians(theta))

def asind(arg):
    return m.degrees(m.asin(arg))
def acosd(arg):
    return m.degrees(m.acos(arg))
def atand(arg):
    return m.degrees(m.acos(arg))

# open logfile
f = open('logfile', 'w')

# to test this we're goign to use "regulus" to calculate the location
class Observation:

    # this class defines the observations that we get from the sextant or CNC
    # CNC = CelNavCamera.  PRETTY SWAG
    
    # shared among the rest of the instances of this object
    fixDate = [2015, 7, 4]      # (year, month, date)
    fixTime = [21, 0, 0]        # (hour, minute second)
    v = 20                      # knots
    track = 325                 # track heading in degrees
    lf = -15.0                  # est. Lat, @ fixTime W Positive, degrees
    bf = 32.0                   # est. Long @ fixTime N positive, degrees    

    def __init__(self, t,  ho, sha, ghAries0, ghAries1, dec):
        
        # the stuff in here, we just want to exist for THAT INSTANCE

        # everything that is an "input" to the object
        self.t = t
        self.ho = ho
        self.ghAries0 = ghAries0
        self.ghAries1 = ghAries1
        self.sha = self.convertAngle(sha)
        self.dec = self.convertAngle(dec)

        # everything that requires a method to get
        self.increment = self.calcIncrement()
        self.hourTea = self.calcHourTea()
        self.ghaA = self.interpGhaDec(self.ghAries0, self.ghAries1)
        self.gha = self.calcTrueGha()

        # calculate this over again every iteration 
        # self.lng = self.calcLongLat(self.lf, self.bf)[0]
        # self.lat = self.calcLongLat(self.lf, self.bf)[1]
        # self.lng = self.calcLongLat(self.lf, self.bf)

        # self.lha = self.calcLha(self.lf)
        # self.hc = self.calcHcAz(self.lat)[0]
        # self.z = self.calcHcAz(self.lat)[1]
        # self.p = self.calcIntercept()
        self.trackStar(self.lf, self.bf)

    def convertAngle(self, angle):
        # converts an angle from angle + minutes from the almanac to decimal
        if angle[0] < 0:
            ang = -1*(abs(angle[0]) + angle[1]/60)
        else:
            ang = (abs(angle[0]) + angle[1]/60) 
        return ang

    def calcIncrement(self):
        # increment is used to interpolate GHA. Not required until we're
        # automating this mofo

        increment = self.t[1]/60 + self.t[2]/3600
        return increment
    
    def calcHourTea(self):
        # need to convert everything to seconds
        hoursToSeconds = (self.t[0] - self.fixTime[0])*3600 #3600 s per hour
        minsToSeconds = (self.t[1] - self.fixTime[1])*60    # 60 s per min
        secsToSeconds = (self.t[2] -self.fixTime[2])*1      # 1 s per s

        totalDiff = hoursToSeconds + minsToSeconds + secsToSeconds
        return totalDiff/3600       # need the final answer in HOURS

    def interpGhaDec(self, angle0, angle1):
        # attempts the interpolation method for getting GHA.
        # might make the automated look up table part a lot easier
        
        inc = self.increment
        qty0 = angle0
        qty1 = angle1
        
        #convert GHAs to decimal degrees
        a0 = (qty0[0] + (qty0[1]/60))
        a1 = (qty1[0] + (qty1[1]/60))

        # GHA = ghA0 + inc*(ghA1 -ghA0)  
        output = (a0 + inc*(a1 - a0))        
        return output

    def calcLongLat(self, longEst, latEst):
        # calculates the estimate of lat and long based on the running track
        # of the vessel

        lng = longEst + ((self.hourTea*(self.v/60)*sind(self.track))/cosd(latEst))
        lat = latEst + (self.hourTea*(self.v/60)*cosd(self.track)) 
        return [lng, lat]
        

    def calcTrueGha(self):
        # calculates the true GHA of the observation
        # trueGha = (ghaAries + sha)%360. returns the smallest equiv angle
        return (self.ghaA + self.sha)%360


    def calcLha(self, longEst):
        # calculates the local hour angle
        # lha = (gha + long)%360
        
        return (self.gha + longEst)%360 

    def calcHcAz(self,latEst):
        # calculates s, c, and altitude Hc 
        s = sind(self.dec)
        c = cosd(self.dec)*cosd(self.lha)
        hc = asind(s*sind(latEst) + c*cosd(latEst))
        X = (s*cosd(latEst) - c*sind(latEst))/(cosd(hc))
        if X > 1:
            X = 1
        elif X < -1:
            X = -1
        else:
            pass
        A = acosd(X)
        
        # calculate the azimuth Z based on lha
        if self.lha > 180:
            Z = A
        else:
            Z = 360-A
        return [hc, Z]

    def calcIntercept(self):
        # calculates the intercept, which along with Z, and Hc are the most 
        # important attributes
        return self.ho - self.hc

    def trackStar(self, longitude, latitude):
        self.lng = self.calcLongLat(longitude, latitude)[0]
        self.lat = self.calcLongLat(longitude, latitude)[1]
        self.lha = self.calcLha(longitude)
        self.hc = self.calcHcAz(latitude)[0]
        self.z = self.calcHcAz(latitude)[1]
        self.p = self.calcIntercept() 


    def printAns(self):
        # prints the data for the different observations
        print "t == " + str(self.t)
        print "ho == " + str(self.ho)
        print "ghAries0 == " + str(self.ghAries0)
        print "ghAries1 == " + str(self.ghAries1)
        print "sha == " + str(self.sha)
        print "increment == " + str(self.increment)
        print "hourTea == " + str(self.hourTea)
        print "ghaA == " + str(self.ghaA)
        print "gha == " + str(self.gha)
        print "dec == " + str(self.dec)
        # print "count == " + str(self.count)
        print "lng == " + str(self.lng)
        print "lat == " + str(self.lat)
        print "lha == " + str(self.lha)
        print "hc == " + str(self.hc)
        print "z == " + str(self.z)
        print "p == " + str(self.p)

    
def locateMe(obs, count, newLong, newLat):
    # this function will locate me based on the three observations
    # calculates A-G
    # increments count on subsequent iterations 
   
     
    # set up matrices
    azimuth = [] #
    intercepts = []
    A = []
    B = []
    C = []
    D = []
    E = []
    # G = AC - B^2
     
    # single value parameters
    if count == 0:
        print "count == 0"
        oldLat = obs[0].bf
        oldLong = obs[0].lf 
    elif count > 0:
        print "count > 0"
        oldLat = newLat
        oldLong = newLong


    # get azimuths from the set of observations 
    [azimuth.append(x.z) for x in obs]
    print azimuth 
    # get intercepts from the set of observations
    [intercepts.append(x.p) for x in obs]
    print intercepts
    # calculate parameters
    [A.append(cosd(x)**2) for x in azimuth]
    A = sum(A)
    [B.append(cosd(x)*sind(x)) for x in azimuth]
    B = sum(B)

    [C.append(sind(x)**2) for x in azimuth]
    C = sum(C)

    [D.append(intercepts[i]*cosd(azimuth[i])) for i in range(0, len(azimuth))]
    D = sum(D)

    [E.append(intercepts[i]*sind(azimuth[i])) for i in range(0, len(azimuth))]
    E = sum(E)

    G = A*C - B**2


    # print " a = %s" %str(A)
    # print " b = %s" %str(B)
    # print " c = %s" %str(C)
    # print " d = %s" %str(D)
    # print " e = %s" %str(E)
    # print " g = %s" %str(G)

    # FIRST PASS
    # calculate longitude from the averaging method 
    newLongOffset = (A*E - B*D)/(G*cosd(oldLat))
    newLong = oldLong + newLongOffset
    print "long off == %s " %str(newLongOffset)
    print "newlong == %s " %str(newLong)

    # calculate latitude from the averaging method
    newLatOffset = (C*D-B*E)/(G)
    newLat  = oldLat +newLatOffset
    print newLat
    print "n lat off == %s" %str(newLatOffset)

    d = 60*m.sqrt((newLong-oldLong)**2*cosd(oldLat)**2 + (newLat - oldLat)**2)
    print  "d == %s" %str(d)
    f.write("%s\n" %str(d))
    
    return [newLong, newLat, d]

class Image:
    
    x = 25 
    # in here what i'm hoping to do is process the image, find the offset
    def findCenter():
       pass 
        # this function finds the center pixel of the object

    

# sometimes use () sometimes u dont use ()

# verify my observations

# if __name__ lets you run a code when its being run directly. 
# this way is OP when you want to test a part of the code separately
# and you don't want to use FUCKING matlab
if __name__ == "__main__":
                        #t            Ho      sha          gha0
    regulus = Observation([20, 39, 23], 27.2674,[207, 42.3], [222, 30.6], 
                           #gha1        dec
                           [237, 33.1], [11, 53.4]) 

    antares = Observation([20, 45, 47], 25.8742, [112, 24.2], [222, 30.6],
                          [237, 33.1], [-26, 27.8])

    kochab = Observation([21, 10, 34], 47.5309, [137, 19.7], [237, 33.1],
                          [252, 35.6], [74, 5.9])
   
    # regulus.printAns()
    # antares.printAns()
    # kochab.printAns()

    obs = [regulus, antares, kochab]

    # first time
    count =0 
    location = locateMe(obs, count,0,0)
    print "location is %s" %str(location)
    
    while count < 10:
        for x in obs:
            x.trackStar(location[0], location[1])
         
            # calculate this over again every iteration 
            # x.lng = x.calcLongLat(location[0], location[1])[0]
            # x.lat = x.calcLongLat(location[0], location[1])[1]
            # x.lha = x.calcLha(location[0])
            # x.hc = x.calcHcAz(location[1])[0]
            # x.z = x.calcHcAz(location[1])[1]
            # x.p = x.calcIntercept() 
            
            # print " new long = %s" %str(x.lng)
            # print "new lat = %s" %str(x.lat)
            # print "new lha = %s" %str(x.lha)
            # print "new hc = %s" %str(x.hc)
            # print "new z = %s" %str(x.z)
            # print "new p = %s" %str(x.p)
        count = count + 1
        location = locateMe(obs, count, location[0], location [1]) 

# close the logfile
f.close()
