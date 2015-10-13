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

dataDir = '/home/newmy/research/exp/unh-startracker/dataSets/lyra_oct9/'
dataDir = './'
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
    pixScale = 24.15 # arcsec/pixel
    pixDegrees = pixScale/3600

    imageWidth = 3872 # pix
    imageHeight = 2592 # pix
    xc = imageWidth/2
    yc = imageHeight/2

    #PITCH CALIBRATION SUPER IMPORTANT
    pitch =62.62 #deg 

    # strip 'annotations'
    # starList = starList['annotations']

    shortList = [] # make a short list of the stars we're really interested in
    for star in starList:

        # if the star has an alternate name its probably big or bright or both
        if len(star['names'])>1:
            # pixel offsets
            star['xOff'] = star['pixelx'] - xc
            star['yOff'] = yc - star['pixely']
            # rotation will go here

            # Hc (unrolled)
            star['ho'] = pitch + star['yOff']*pixDegrees # i feel like its plus and the matlab is actually whats wrong
            shortList.append(star)
            print star 
            # print "\n\n\n shortList \n\n\n" %shortList
    return shortList 

def runSTpy(shortList,time):
    # this function runs ST.py with the values from three stars from the "short List"
    # we still need data from the almanac but there's defintiely a way to leverage the astrometry data
    shorterList = []
    for x in range(0, len(shortList)):
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
    print "actually used observations are ===== %s" %shorterList
    observations = []
    for x in shorterList:
        # have to define the gha as constants for now
        gha0 = [17,17.8]
        gha1 = [32, 20.3]
        Ho = x['ho']
        sha = x['sha']
        dec = x['dec']
        observations.append(ST.Observation(time,Ho, sha, gha0, gha1, dec))
    print "OBSERVATIONS ====== %s"%observations
    ST.runLocateMeALot(observations)
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
        time = extractTimeFromImage(image)
        wcsFile = grabWcsFile(image)
        print "wcsFile ========= %s " %wcsFile
        starList = getStarDict(wcsFile)
        shortList = computeHoFromImage(starList)
        runSTpy(shortList, time)  
        # print "fuckkkinnnggggg starrrr rlisttttt ==== %s" %starList
        


if __name__ == "__main__":
    runCenterPixelMethod()  

