# rewriting the center pixel method for use in python
# eliminates the need to do any kind of "circular hough transform" etc.
# tckf october 2015

 
from __future__ import division
from PIL import Image

try:
    import client
except:
    pass
import time
import sys
import os
import subprocess
import json
# brittle code. need a way to do relative path idk why the relative path
# isn't working 
sys.path.append('/home/newmy/research/exp/unh-startracker/unh-startracker/analysisAndPlots/maps/')
# print sys.path
import re
import glob
import ST

dataDir = '/home/newmy/research/exp/unh-startracker/dataSets/lyra_oct9_second_raw/'
#dataDir = './../'
print "ATTEMPTING TO ACCESS DATA DIR %s" %dataDir
def extractTimeFromImage(img):
    img = Image.open(img)
    imgTime = img._getexif()
    imgTime = imgTime[36868].split()
    imgTime = imgTime[1].split(':')

    # imgTime is an array of [hr, min, sec] in UTC from the image file
    imgTime =  [float(x) for x in imgTime] 
    return imgTime

def populateImageList():
    imageList = glob.glob('%s*.jpg'%dataDir)
    print imageList
    return imageList

def grabWcsFile(image):
    # i think what i really want is to return a string of the wcs file
    filename = os.path.basename(image)
    filename = os.path.splitext(filename)
    filename = "%s.%s"%(filename[0], 'wcs')
    #print "filename === %s" %filename
    return filename 

try:
    def apiGetCalibrationAndStarList(image):
        # UNUSED SINCE WE HAVE THE SOFTWARE LOCALLY NOW
        apiKey = 'lmrqojqbcjrzxkzx'
        c = client.Client()
        c.login(apiKey) 

        # the reason we set equal c.upload to a variable is because it returns a
        # dictionary with the image id in it
        uploadedImage = c.upload(image)
        
        #print "ul image == %s" %uploadedImage
        # time.sleep(30)
        # try to minimize 
        while True: # look forever
            subId =  uploadedImage['subid']
            if subId == None:
                time.sleep(5)
            elif subId != None:
                break
        # print subId
        while True:
            blah = c.sub_status(subId, justdict=True) #NEED TO ACTIVATE THE JUSTDICT = TRUE FLAG 
            try:
                # print "blah =========== %s" %type(blah['jobs'][0])
                if type(blah['jobs'][0]) == int:
                    print "TYEP OF blah =========== %s" %type(blah['jobs'])
                    jobId = blah['jobs'][0]
                    print "jobId =============== %s" % jobId
                    break
            except:
                time.sleep(5) 
                pass

        
        print" fuckkk %s" % blah 
        
        # this time.sleep call will need to be more bulletproof
        time.sleep(60) 
        calibration = c.send_request('jobs/%s/calibration' % jobId)
        starList = c.send_request('jobs/%s/annotations' % jobId)
        #while True:
        #    try:
        #        if calibration[''
        #while True:
         #   calibration = c.send_request('jobs/%s/calibration' % jobId)
         #   starList = c.send_request('jobs/%s/annotations' % jobId)
         #   try:
         #       if exists(calibration['parity']):
         #           return [calibration, starList]
         #   except:
         #       time.sleep(5)
         #       pass


    # define center pixel constants, pitch calibration and stuff
except:
    pass

def makeWcsFiles(image):
    # this function calls astrometry with certain options and puts a .wcs file
    # in the directory specified after '-D'
    subprocess.call(['solve-field', '-p', '--overwrite', '--scale-units',
                    'degwidth', '--scale-low', '25', '--scale-high', '35',
                    '--downsample', '2', '-D', dataDir, image])

def getStarDict(wcsFile):
    # start a star dictionary object (kind of)
    wcsString = '%s%s'%(dataDir,wcsFile)
    command = ['/usr/local/astrometry/bin/plotann.py', '--brightcat','/home/newmy/research/exp/unh-startracker/astrometry.net-0.50/catalogs/brightstars.fits', wcsString]
    print 'command is %s' %command
    sdProc = subprocess.Popen(command, stdout=subprocess.PIPE)
    #sdProc = os.popen(command).read() 
    starDict = sdProc.stdout.read()
    
    # put the dictionary in dictionary (instead of string) form
    starDict = json.loads(starDict)
    print "star dictionary == %s"%type(starDict)
    print starDict
    return starDict

def computeHoFromImage(starList):

    # the leading theory is that this approximation will only work when the stars are closeby
    # that is, the small angle approximation works
    pixScale = 24.1#5 # arcsec/pixel
    pixDegrees = pixScale/3600

    imageWidth = 3872 # pix
    imageHeight = 2592 # pix
    xc = imageWidth/2
    yc = imageHeight/2
    naturalBias =0#-11.0701857994#-5.25 #calc from lyra_oct9

    #PITCH CALIBRATION SUPER IMPORTANT
    pitch =  39.76#62.62 #deg 
    #i'll need to get the correct roll value from the IMU
    roll =1.9 #-0.32-1.9056-3.19+4444#-0.5 # -2.4#-0.54 
    # strip 'annotations'
    # starList = starList['annotations']

    shortList = [] # make a short list of the stars we're really interested in
    for star in starList:
        # if the star has an alternate name its probably big or bright or both
        #if len(star['names'])>1:
            # pixel offsets
        star['newx'] = star['pixelx']*ST.cosd(roll) + star['pixely']*ST.sind(roll)
        star['newy'] = -star['pixelx']*ST.sind(roll) + star['pixely']*ST.cosd(roll)
        star['xOff'] = star['newx'] - xc
        star['yOff'] = yc - star['newy']
        # rotation will go here
        # compute offset from roll angle
        # i think the order we do the roll and pitch operations is kind of important
        star['ho'] = pitch + star['yOff']*pixDegrees + naturalBias # i feel like its plus and the matlab is actually whats wrong
        #shortList.append(star)
        print star 
        # print "\n\n\n shortList \n\n\n" %shortList
    return starList 

def calibrationObservation(shortList, t0):
   # this function runs ST.py with the values from three stars from the "short List"
    # we still need data from the almanac but there's defintiely a way to leverage the astrometry data
    #t0[2] = t0[2] + 4 #lets worry about correcting the 
    shorterList = []
    for x in range(0, len(shortList)):
        for name in shortList[x]['names']:
            #print shortList[x]['names'][name]
            print name

            starName = name 
            if starName  == '14Aql':
                shortList[x]['sha'] = [74, 16.375]
                shortList[x]['dec'] = [-3,41.9393] 
                shorterList.append(shortList[x])
            elif starName == '15Aql':
                shortList[x]['sha'] = [73, 26.2652]
                shortList[x]['dec'] = [-4, 52.95334] 
               
                shorterList.append(shortList[x])
            elif starName == u'\u03bb Aql':
                shortList[x]['sha'] = [73.0, 26.26254]
                shortList[x]['dec'] = [-4,52.95335] 
                shorterList.append(shortList[x])
            else:
                pass
    print "actually used observations are ===== %s" %shorterList
    observations = []
    for x in shorterList:
        # have to define the gha as constants for now
        #gha0 = [17,17.8]
        #gha1 = [32, 20.3]
        gha0 = [32, 20.3]
        gha1 = [47, 33.7]
        Ho = x['ho']
        sha = x['sha']
        dec = x['dec']
        observations.append(ST.Observation(t0,Ho, sha, gha0, gha1, dec))
    print "OBSERVATIONS ====== %s"%observations
    ST.runLocateMeALot(observations)

def lyraObservation(shortList,t0):
    # this function runs ST.py with the values from three stars from the "short List"
    # we still need data from the almanac but there's defintiely a way to leverage the astrometry data

    #t0[2] = t0[2] + 4 #lets worry about correcting the 
    shorterList = []
    for x in range(0, len(shortList)):
        try:
            print shortList[x]['names'][1]
            starName = shortList[x]['names'][1] 
            if starName  == 'Vega':
                shortList[x]['sha'] = [80, 47.02134]
                shortList[x]['dec'] = [38, 47.1234] 
                shorterList.append(shortList[x])
            elif starName == 'Sheliak':
                shortList[x]['sha'] = [77, 28.8012]
                shortList[x]['dec'] = [33, 21.7601] 
               
                shorterList.append(shortList[x])
            elif starName == 'Sulafat':
                shortList[x]['sha'] = [75, 15.8444]
                shortList[x]['dec'] = [32, 41.3734] 
                shorterList.append(shortList[x])
            else:
                pass
        except:
            pass
    print "actually used observations are ===== %s" %shorterList
    observations = []
    for x in shorterList:
        # have to define the gha as constants for now
        #gha0 = [17,17.8]
        #gha1 = [32, 20.3]
        gha0 = [22, 13.5]
        gha1 = [37,15.9]
        Ho = x['ho']
        sha = x['sha']
        dec = x['dec']
        observations.append(ST.Observation(t0,Ho, sha, gha0, gha1, dec))
    print "OBSERVATIONS ====== %s"%observations
    ST.runLocateMeALot(observations)
    return observations
    # i think here we need to put in an observation
     
            
        #    print "vegaaaaaaaaaa =====%s"%shortList[x]

def runCenterPixelMethod():
    # what would go in __name __ == "__main__" so that way it can be easily 
    # exported to another module if one day we need that
    imageList = populateImageList()
    print imageList 
    for image in imageList:
        # produce the initial wcs file
        makeWcsFiles(image)
        t0 = extractTimeFromImage(image)
        wcsFile = grabWcsFile(image)
        print "wcsFile ========= %s " %wcsFile
        starList = getStarDict(wcsFile)
        shortList = computeHoFromImage(starList)
        #lyraObservation(shortList, t0)  
        calibrationObservation(shortList, t0)
        # print "fuckkkinnnggggg starrrr rlisttttt ==== %s" %starList

    subprocess.call(['mv', 'analysis.csv', dataDir])
    subprocess.call(['mv', 'trueInertials.csv', dataDir])
        


if __name__ == "__main__":
    runCenterPixelMethod()  

