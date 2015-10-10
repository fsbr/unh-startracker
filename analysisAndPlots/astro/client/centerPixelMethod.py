# rewriting the center pixel method for use in python
# eliminates the need to do any kind of "circular hough transform" etc.
# 
from __future__ import division
from PIL import Image
import client
import time
# set up an API object becuase I guess that's how I'm going 

img = Image.open('DSC_0058_NEF_embedded.jpg')
imgTime = img._getexif()
imgTime = imgTime[36868].split()
imgTime = imgTime[1].split(':')

# imgTime is an array of [hr, min, sec] in UTC from the image file
imgTime =  [float(x) for x in imgTime] 
print imgTime

# API calls to astrometry will probably go somewhere around here
# eventually pass these into the function from client.py
imageList = ['DSC_0060_NEF_embedded.jpg']

def getCalibrationAndStarList(imageList):
    apiKey = 'lmrqojqbcjrzxkzx'
    c = client.Client()
    c.login(apiKey) 

    # the reason we set equal c.upload to a variable is because it returns a
    # dictionary with the image id in it
    uploadedImage = c.upload(imageList[0])
    time.sleep(5)
    subId =  uploadedImage['subid']
    print subId
    blah = c.sub_status(subId)
    print blah 

    
    #calibration = c.send_request('jobs/%s/calibration' % jobId)
    #starList = c.send_request('jobs/%s/annotations' % jobId)
#    print c.sub_status('805994')
    return [calibration, starList]

calibration = {'parity': 1.0, 'orientation': -116.11046066495832, 'pixscale': 24.05351131386227, 'radius': 15.566263591365754, 'ra': 282.80884415696005, 'dec': 32.88958327328472}
starList = {'annotations': [{'vmag': 5.1, 'radius': 0.0, 'names': ['90Her'], 'pixelx': 3837.5496154842285, 'pixely': 2232.5704719248015, 'type': 'bright'}, {'vmag': 3.8, 'radius': 0.0, 'names': [u'\u03b8 Her'], 'pixelx': 3429.9026042696914, 'pixely': 2411.185979801152, 'type': 'bright'}, {'vmag': 4.9, 'radius': 0.0, 'names': ['104Her'], 'pixelx': 2394.396318719527, 'pixely': 2502.01286805405, 'type': 'bright'}, {'vmag': 4.3, 'radius': 0.0, 'names': [u'\u03ba Lyr'], 'pixelx': 2851.2273851305717, 'pixely': 1901.1047420426305, 'type': 'bright'}, {'vmag': 5.6, 'radius': 0.0, 'names': ['108Her'], 'pixelx': 2033.8493842608632, 'pixely': 2375.0478838412573, 'type': 'bright'}, {'vmag': 5.1, 'radius': 0.0, 'names': ['107Her'], 'pixelx': 1905.2963702097438, 'pixely': 2453.313705264903, 'type': 'bright'}, {'vmag': 5.1, 'radius': 0.0, 'names': [u'\u03bc Lyr'], 'pixelx': 3226.3368272834896, 'pixely': 1508.941478748954, 'type': 'bright'}, {'vmag': 0.0, 'radius': 0.0, 'names': [u'\u03b1 Lyr', 'Vega'], 'pixelx': 2930.74639256282, 'pixely': 1244.3215773537345, 'type': 'bright'}, {'vmag': 5.0, 'radius': 0.0, 'names': [u'\u03b5 1Lyr'], 'pixelx': 2938.4738043540856, 'pixely': 988.668882187569, 'type': 'bright'}, {'vmag': 5.1, 'radius': 0.0, 'names': [u'\u03b5 2Lyr'], 'pixelx': 2930.247424085273, 'pixely': 991.8468912178366, 'type': 'bright'}, {'vmag': 5.3, 'radius': 0.0, 'names': [u'\u03b5 2Lyr'], 'pixelx': 2930.207247129186, 'pixely': 991.8692233236113, 'type': 'bright'}, {'vmag': 4.3, 'radius': 0.0, 'names': [u'\u03b6 1Lyr'], 'pixelx': 2656.7397149077506, 'pixely': 1130.4250935960356, 'type': 'bright'}, {'vmag': 5.7, 'radius': 0.0, 'names': [u'\u03b6 2Lyr'], 'pixelx': 2654.888192927335, 'pixely': 1130.4222622142017, 'type': 'bright'}, {'vmag': 4.1, 'radius': 0.0, 'names': ['110Her'], 'pixelx': 380.44893864348796, 'pixely': 2356.5185518655107, 'type': 'bright'}, {'vmag': 4.3, 'radius': 0.0, 'names': ['111Her'], 'pixelx': 31.8062730789552, 'pixely': 2491.8845810650937, 'type': 'bright'}, {'vmag': 5.9, 'radius': 0.0, 'names': [u'\u03bd 1Lyr'], 'pixelx': 1948.38696118334, 'pixely': 1342.7911169118156, 'type': 'bright'}, {'vmag': 5.2, 'radius': 0.0, 'names': [u'\u03bd 2Lyr'], 'pixelx': 1912.0400303201975, 'pixely': 1358.2227374968033, 'type': 'bright'}, {'vmag': 3.4, 'radius': 0.0, 'names': [u'\u03b2 Lyr', 'Sheliak'], 'pixelx': 2016.3197726413243, 'pixely': 1294.8874715518486, 'type': 'bright'}, {'vmag': 5.4, 'radius': 0.0, 'names': ['112Her'], 'pixelx': 390.44676257046194, 'pixely': 2082.648764429856, 'type': 'bright'}, {'vmag': 5.5, 'radius': 0.0, 'names': [u'\u03b4 1Lyr'], 'pixelx': 2442.6372318629715, 'pixely': 940.3329177546966, 'type': 'bright'}, {'vmag': 4.5, 'radius': 0.0, 'names': ['113Her'], 'pixelx': 516.3384100153673, 'pixely': 1917.3766542860337, 'type': 'bright'}, {'vmag': 4.3, 'radius': 0.0, 'names': [u'\u03b4 2Lyr'], 'pixelx': 2421.9011927730753, 'pixely': 924.8327701296216, 'type': 'bright'}, {'vmag': 4.0, 'radius': 0.0, 'names': ['13Lyr'], 'pixelx': 3370.0915985072897, 'pixely': 400.13225232658385, 'type': 'bright'}, {'vmag': 3.2, 'radius': 0.0, 'names': [u'\u03b3 Lyr', 'Sulafat'], 'pixelx': 1796.8663140939304, 'pixely': 1095.3272957909144, 'type': 'bright'}, {'vmag': 4.9, 'radius': 0.0, 'names': [u'\u03bb Lyr'], 'pixelx': 1708.907791816758, 'pixely': 1102.2555717403409, 'type': 'bright'}, {'vmag': 5.0, 'radius': 0.0, 'names': ['16Lyr'], 'pixelx': 3716.041867888038, 'pixely': 36.11147271271068, 'type': 'bright'}, {'vmag': 5.2, 'radius': 0.0, 'names': ['17Lyr'], 'pixelx': 1651.820179053967, 'pixely': 868.7349484589197, 'type': 'bright'}, {'vmag': 5.2, 'radius': 0.0, 'names': [u'\u03b9 Lyr'], 'pixelx': 2138.7242443072273, 'pixely': 634.8808048150524, 'type': 'bright'}, {'vmag': 5.9, 'radius': 0.0, 'names': ['19Lyr'], 'pixelx': 1427.6296522502478, 'pixely': 823.8614344674754, 'type': 'bright'}, {'vmag': 4.3, 'radius': 0.0, 'names': [u'\u03b7 Lyr'], 'pixelx': 2471.5621184075, 'pixely': 261.477169625044, 'type': 'bright'}, {'vmag': 5.6, 'radius': 0.0, 'names': ['1Sge'], 'pixelx': 1.055947182188902, 'pixely': 1365.6495085251377, 'type': 'bright'}, {'vmag': 4.7, 'radius': 0.0, 'names': ['1Vul'], 'pixelx': 9.159424489784897, 'pixely': 1325.6358110384924, 'type': 'bright'}, {'vmag': 4.3, 'radius': 0.0, 'names': [u'\u03b8 Lyr'], 'pixelx': 2299.6942547998215, 'pixely': 256.8924101313912, 'type': 'bright'}, {'vmag': 5.4, 'radius': 0.0, 'names': ['2Vul'], 'pixelx': 214.79524055458114, 'pixely': 1172.0973038596137, 'type': 'bright'}, {'vmag': 5.1, 'radius': 0.0, 'names': ['3Vul'], 'pixelx': 589.4953283603128, 'pixely': 809.2092503554888, 'type': 'bright'}, {'vmag': 4.9, 'radius': 0.0, 'names': ['2Cyg'], 'pixelx': 1034.235488709276, 'pixely': 565.0474415325001, 'type': 'bright'}, {'vmag': 5.1, 'radius': 0.0, 'names': ['4Cyg'], 'pixelx': 1929.7460633006324, 'pixely': 101.32092188290596, 'type': 'bright'}, {'vmag': 4.4, 'radius': 0.0, 'names': [u'\u03b1 Vul'], 'pixelx': 285.89716885182065, 'pixely': 723.9605869690919, 'type': 'bright'}, {'vmag': 5.8, 'radius': 0.0, 'names': ['8Vul'], 'pixelx': 296.9811977545892, 'pixely': 709.9992097671748, 'type': 'bright'}, {'vmag': 3.0, 'radius': 0.0, 'names': [u'\u03b2 1Cyg', 'Albireo'], 'pixelx': 717.4930024284138, 'pixely': 465.0541201158885, 'type': 'bright'}, {'vmag': 5.1, 'radius': 0.0, 'names': [u'\u03b2 2Cyg'], 'pixelx': 717.8317374439341, 'pixely': 463.7064918368625, 'type': 'bright'}, {'vmag': 4.7, 'radius': 0.0, 'names': ['8Cyg'], 'pixelx': 1603.8638574074098, 'pixely': 53.030993477674656, 'type': 'bright'}, {'vmag': 5.3, 'radius': 0.0, 'names': ['9Cyg'], 'pixelx': 872.9919612936627, 'pixely': 251.4831971237577, 'type': 'bright'}, {'vmag': 4.6, 'radius': 0.0, 'names': [u'\u03c6 Cyg'], 'pixelx': 912.6497451616098, 'pixely': 74.47020959065821, 'type': 'bright'}, {'vmag': 5.4, 'radius': 0.0, 'names': ['10Vul'], 'pixelx': 239.97787824203056, 'pixely': 183.51131629252814, 'type': 'bright'}]}

# define center pixel constants, pitch calibration and stuff
def computeHcFromImage(calibration, starList):
    rightAscension = calibration['ra']
    declination = calibration['dec']
    pixScale = calibration['pixscale'] # arcsec/pixel
    pixDegrees = pixScale/3600

    imageWidth = 3872 # pix
    imageHeight = 2592 # pix
    xc = imageWidth/2
    yc = imageHeight/2

    #PITCH CALIBRATION SUPER IMPORTANT
    pitch = 62.6 # deg

    # strip 'annotations'
    starList = starList['annotations']

    shortList = [] # make a short list of the stars we're really interested in
    for star in starList:

        # if the star has an alternate name its probably big or bright or both
        if len(star['names'])>1:

            # pixel offsets
            star['xOff'] = star['pixelx'] - xc
            star['yOff'] = yc - star['pixely']
            # rotation will go here

            # Hc (unrolled)
            star['hcu'] = pitch + star['yOff']*pixDegrees
            shortList.append(star)
            print star 

if __name__ == "__main__":

    getCalibrationAndStarList(imageList)
    # computeHcFromImage(calibration,starList) 
