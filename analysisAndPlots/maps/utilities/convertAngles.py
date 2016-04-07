# utils to convert from RA to SHA
from __future__ import division


def raToSha(rA):
    # converts from RA in hr-min-sec to the [deg, arcmin] form 
    # used by ST.py

    hour = rA[0]
    minute = rA[1]
    second = rA[2]
    
    rawSha = 360 - (360/24)*(hour + (minute/60) + (second/3600))
    arcmins,arcsecs = divmod(rawSha*3600,60)
    deg, arcmins = divmod(arcmins, 60)

    
    return [deg,arcmins + arcsecs/60]

def convertDec(dec):
    # converts the declination from [deg, min, sec] to [deg, min]
    deg = dec[0]
    minute = dec[1]
    second = dec[2]
    
    arcmins = minute + second/60
    return [deg, arcmins]
        

if __name__ == "__main__":
    print "sulafat sha %s"  %raToSha([18, 58, 56.62241])
    print "sulafat dec %s"  %convertDec([32, 41, 22.4003])
    print "sheliak sha %s"  %raToSha([18, 50, 04.79525])
    print "sheliak dec %s"  %convertDec([33, 21, 45.6100])
    print "vega sha %s"  %raToSha([18, 36, 56.33635])
    print "vega dec %s" %convertDec([38,47,01.2802])

    print "alshain sha %s"  %raToSha([19,55,18.8])
    print "alshain dec %s"  %convertDec([06,24,24])
    print "altair sha %s"  %raToSha([19,50,46.9985])
    print "altair dec %s"  %convertDec([08.0,52,05.9563])
    print "tarazed sha %s"  %raToSha([19,46,15.58029])
    print "tarazed dec %s" %convertDec([10,36,47.7408])
    print "center ra to sha =%s" %raToSha([18,51,14.123])
    
    print "15aql sha %s"  %raToSha([19, 04, 57.67233])
    print "15aql dec %s"  %convertDec([-04, 1, 53.1059])
    print "L aql sha %s"  %raToSha([19, 06, 14.93898])
    print "L aql dec %s"  %convertDec([-04, 52, 57.2007])
    print "Ayla sha %s"  %raToSha([18, 56, 13.2])
    print "Ayla dec %s" %convertDec([04, 12, 13])
    print "14aql sha %s"  %raToSha([19, 02, 54.499])
    print "14aql dec %s" %convertDec([-03, 41, 56.3561])

