# UNH Star Tracker Calculator
# Uses the Nautical Almanac "Direct Computational" Method
# 2015 Nautical Almanac Commercial Edition pg. 283
# tckf - september - 2015
from __future__ import division
import math as m
import random as rng

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

# doing a bunch of different logs
dLog = open('dLog', 'w')
dLogFinalPoint = open('dLogFinalPoint', 'w')
# for the parameters that aren't supposed to change on each pass
inertialParams = open('inertials0', 'w')

# for the parameters that are changing each iteration
changingParams = open('changes0', 'w')

ip1 = open('inertials1', 'w')
cp1 = open('changes1', 'w')

ip2 = open('inertials2', 'w')
cp2 = open('changes2', 'w')
# to test this we're goign to use "regulus" to calculate the location

class Sextant:

    # the sextant class deals with computing the Observed altitude from the 
    # sextant measurement

    def __init__(self,hSextant, eyeHeight):
        # this is the value you measure from the starCamera or sextant
        self.hSextant = hSextant        # degrees
        self.eyeHeight = eyeHeight      # meteres
        self.dip = self.calcDip()
        self.hApparent = self.calcApparentAlt()
        self.r = self.calcRefraction()
        self.Ho = self.calcAltitude()

    def calcDip(self):
        # calculates an error based on your height of eye
        D = 0.293*m.sqrt(self.eyeHeight)     # degrees
        return D

    def calcApparentAlt(self):
        Hs = self.hSextant - self.dip # + I (eventually)
        return Hs
        
    def calcRefraction(self):
        # refraction is based on 
        H = self.hApparent
        Ro = (0.0167)/(tand((H + 7.32)/(H + 4.32)))
        return Ro
    
    def calcAltitude(self):
        H = self.hApparent
        Ro = self.r
        Ho = H - Ro
        return Ho
 
    def printAns(self):
        print self.hSextant        # degrees
        print self.eyeHeight       # meteres
        print self.dip
        print self.hApparent 
        print self.r 
        print self.Ho

class Observation:
    # LF is LONGITUDE
    # BF is LATITUDE
    # this class defines the observations that we get from the sextant or CNC
    # CNC = CelNavCamera.  PRETTY SWAG
    
    # shared among the rest of the instances of this object
    fixDate = [2015, 10, 7]      # (year, month, date)
    fixTime = [01, 41, 0]        # (hour, minute second)
    v = 0                      # knots
    track = 0                 # track heading in degrees
    lf = -70.934916                  # est. long, @ fixTime E+ W-, degrees
    bf = 43.13376                   # est. lat @ fixTime N+ S-, degrees    
    
    #lf = -75
    #bf = 45                            # note the sign convenction for lha is opposite

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
        print "calcLongLat"
        print "longEst is %s" %longEst
        print "latEst is %s" %latEst
        # calculates the estimate of lat and long based on the running track
        # of the vessel

        lng = longEst + ((self.hourTea*(self.v/60)*sind(self.track))/cosd(latEst))
        lat = (latEst + (self.hourTea*(self.v/60)*cosd(self.track)))# %90 # really just throwing smth in there to see what sticks 
        print "lng = %s lat = %s" %(lng, lat)
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
    
    def writeInertial(self, fileName):
        # this writes the inertial logfile for that observation 
        fileName.write('t == %s\n' %(self.t))
        fileName.write('ho == %s\n' %(self.ho))
        fileName.write('ghAries0 == %s\n' %(self.ghAries0))
        fileName.write('ghAries1 == %s\n' %(self.ghAries1))
        fileName.write('sha == %s\n' %(self.sha))
        fileName.write('increment == %s\n' %(self.increment))
        fileName.write('hourTea == %s\n' %(self.hourTea))
        fileName.write('ghaA == %s\n' %(self.ghaA))
        fileName.write('gha == %s\n' %(self.gha))
        fileName.write('dec == %s\n' %(self.dec))
        fileName.write('\n\n\n')
    
    def writeChanging(self,fileName):
        
        fileName.write('lng == %s\n' %(self.lng))
        fileName.write('lat == %s\n' %(self.lat))
        fileName.write('lha == %s\n' %(self.lha))
        fileName.write('hc == %s\n' %(self.hc))
        fileName.write('z == %s\n' %(self.z))
        fileName.write('p == %s\n' %(self.p))
        fileName.write('\n\n\n')

    def writeAll(self, inertialList, changingList):
        for x in fileList:
            writeInertial(x)
            writeChanging(x)
            

    
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

    # get intercepts from the set of observations
    [intercepts.append(x.p) for x in obs]

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
    newLong = (oldLong + newLongOffset) #i'm trying mod 360
    #print "long off == %s " %str(newLongOffset)
    #print "newlong == %s " %str(newLong)

    # calculate latitude from the averaging method
    newLatOffset = (C*D-B*E)/(G)
    newLat  = (oldLat +newLatOffset)
    #print newLat
    #print "n lat off == %s" %str(newLatOffset)

    d = 60*m.sqrt((newLong-oldLong)**2*cosd(oldLat)**2 + (newLat - oldLat)**2)
    print  "d == %s" %str(d)
    dLog.write("%s\n" %d)
    
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
    mcCount = 0
    while mcCount < 100: # use 1000 for sims, 1 for obs
        # the monte carlo test has to start around this part of the code
        # these are the sample observations from the almanac
                            #t            Ho      sha          gha0
        noiseBound =0 # 0.00625
        randomNumber = 0 #rng.uniform(-noiseBound,noiseBound) # number of degrees offset
        randomNumber1 = 0 #rng.uniform(-noiseBound,noiseBound)
        randomNumber2 = 0 #rng.uniform(-noiseBound,noiseBound)
        bias = 0 
        # Shuai and I gathered the following observations from the Protractor Sextant, these Ho values are off by a lot
        altair1 = Observation([01, 29, 46], 55.219 + randomNumber + bias, [62, 06.6], [13, 36.6], [28, 39.1],
                                [8, 55.0])
       
        altair2 = Observation([01, 37, 53], 54.626 + randomNumber1 + bias , [62, 06.6], [13, 36.6], [28, 39.1],
                                [8, 55.0])
        altair3 = Observation([01, 45, 15], 53.24 +randomNumber2 + bias, [62, 06.6], [13, 36.6], [28, 39.1],
                                [8, 55.0])
               
        # these observations are from the nautical almanac 2015        
                 #t          h0                              sha           gha0 
        regulus = Observation([20, 39, 23], 27.2674 ,[207, 42.3], [222, 30.6], 
                               #gha1        dec
                               [237, 33.1], [11, 53.4]) 

        antares = Observation([20, 45, 47], 25.8742 , [112, 24.2], [222, 30.6],
                              [237, 33.1], [-26, 27.8])

        kochab = Observation([21, 10, 34], 47.5309 , [137, 19.7], [237, 33.1],
                              [252, 35.6], [74, 5.9])

        # make a new "summer triangle" observation data set, as it would be in the images

        deneb = Observation([01,29,46], 77.7754 + randomNumber + bias ,[49, 30.1], [13, 36.6], 
                                [28, 39.1], [45, 20.6])
        vega = Observation([01,29,46], 66.5070 + randomNumber1 + bias , [80, 37.8], [13, 36.6],
                            [28, 39.1], [38, 48.4])
        altair = Observation([01,29,46], 54.1453 +randomNumber2 + bias, [62, 06.6], [13, 36.6],
                            [28, 39.1], [8,55.0])

        vega1 = Observation([01,41,39], 84.4709 , [80, 37.8], [13, 36.6],
                            [28, 39.1], [38, 48.4])
        deneb1 = Observation([01,41,39], 79.1819,[49, 30.1], [13, 36.6], 
                                [28, 39.1], [45, 20.6])
        altair1 = Observation([01,41,39], 75.8566, [62, 06.6], [13, 36.6],
                            [28, 39.1], [8,55.0])

               
        #turns out the stars we were looking at were NOT the summer triangle
        # might be able to use astrometry.net to do all the image processing
        deneb =  Observation([01,51,8 + mcCount],83.7740, [49,38.526], [13,36.6],
                                [28,39.1], [45, 16.8167] ) #1 
        gienah = Observation([01,51,8],80.2062, [54, 26.574], [13,36.6],
                                [28,39.1 + mcCount],  [40, 15.4008]) #2
        sadr = Observation([01,51,8 + mcCount],78.5567, [54, 26.574], [13,36.6],
                                [28,39.1], [33,58.2154]) #3

        sulafat = Observation([01,9,9], 64.6841-5.801, [75, 15.8444], [30,22.0],
                                [45, 24.4], [32, 41.3734])
        sheliak = Observation([01, 9, 9], 63.2888-5.801, [77.0, 28.8012], [30, 22.0],
                                [45, 24.4], [33,21.7601])
        vega2 = Observation([01, 9,9], 64.7062-5.801, [80, 47.02134], [30, 22.0],
                                [45, 24.4], [38, 47.01234])
    
        t = [0,53,13]
        ghaZero = [16,18.7]
        ghaOne = [31, 21.1]
        meanBias = 5.356 # total amount of diff. i need to get out of my system
        accounted = 2.7 # stuff i've actually been able to account for so far
        dt = -2
        alshain = Observation([0,53, 13+dt], 54.6041 - meanBias,[61, 10.299], ghaZero, ghaOne, [6,24.4])
        altair2 = Observation([0,53,13+dt], 56.4606 - meanBias, [62, 18.2504], ghaZero, ghaOne, [8,52.0993])
        tarazed = Observation([0,53,13+dt],57.6411 - meanBias, [63, 26.1049], ghaZero, ghaOne, [10, 36.7657])
        
        alshain = Observation([0,53, 13+dt], 54.6098 - meanBias,[61, 10.299], ghaZero, ghaOne, [6,24.4])
        altair2 = Observation([0,53,13+dt], 56.4312 - meanBias, [62, 18.2504], ghaZero, ghaOne, [8,52.0993])
        tarazed = Observation([0,53,13+dt],57.5817 - meanBias, [63, 26.1049], ghaZero, ghaOne, [10, 36.7657])

        alshain = Observation([0,53, 13+dt], 54.6151 - meanBias,[61, 10.299], ghaZero, ghaOne, [6,24.4])
        altair2 = Observation([0,53,13+dt], 56.4009 - meanBias, [62, 18.2504], ghaZero, ghaOne, [8,52.0993])
        tarazed = Observation([0,53,13+dt],57.5210 - meanBias, [63, 26.1049], ghaZero, ghaOne, [10, 36.7657])

        alshain = Observation([0,53, 13+dt], 54.6176 - meanBias,[61, 10.299], ghaZero, ghaOne, [6,24.4])
        altair2 = Observation([0,53,13+dt], 56.3854 - meanBias, [62, 18.2504], ghaZero, ghaOne, [8,52.0993])
        tarazed = Observation([0,53,13+dt],57.4902 - meanBias, [63, 26.1049], ghaZero, ghaOne, [10, 36.7657])

        #obs = [regulus, antares, kochab]
        # obs = [altair1, altair2, altair3]
        # obs = [deneb, vega, altair] # summer Triangle bitches
        obs = [alshain, altair2, tarazed]
        # obs = [deneb, gienah, sadr]
        inertialList = [inertialParams, ip1, ip2]
        changingList = [changingParams, cp1, cp2]
        # first time
        count =0 

        location = locateMe(obs, count,0,0)
        # print "location is %s" %str(location)
        obs[0].writeInertial(inertialParams) 
        obs[0].writeChanging(changingParams) 

        obs[1].writeInertial(ip1) 
        obs[1].writeChanging(cp1) 

        obs[2].writeInertial(ip2) 
        obs[2].writeChanging(cp2) 

        # iterate the algorithm 10x
        while count < 10:
            for x in obs:
                x.trackStar(location[0], location[1])
        #        print " new long = %s" %str(x.lng)
        #        print "new lat = %s" %str(x.lat)
               # print "new lha = %s" %str(x.lha)
               # print "new hc = %s" %str(x.hc)
               # print "new z = %s" %str(x.z)
               # print "new p = %s" %str(x.p)
            count = count + 1
            location = locateMe(obs, count, location[0], location [1]) 
            obs[0].writeInertial(inertialParams)
            obs[0].writeChanging(changingParams)

            obs[1].writeInertial(ip1) 
            obs[1].writeChanging(cp1) 

            obs[2].writeInertial(ip2) 
            obs[2].writeChanging(cp2) 
            if count == 10:
                dLogFinalPoint.write("%s,%s,%s\n" %(location[0], location[1], location[2]))

        h = Sextant(29, 170)
#        h.printAns()
        #altair1.printAns()
        #altair2.printAns()
        #altair3.printAns()
        mcCount +=1
        
# close the logfile
dLog.close()
inertialParams.close()
changingParams.close()
ip1.close()
cp1.close()
ip2.close()
cp2.close()
dLogFinalPoint.close()
