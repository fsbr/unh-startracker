# using this example code to upload wcs from fits

# load the wcs information from a fits header, and use it
# to convert pixel coordinates to world coordinates.

from __future__ import division

import numpy
from astropy import wcs
from astropy.io import fits
import sys

def loadWcsFromFile(filename):
    # load the fits hdulist using astropy.io.fits
    hduList = fits.open(filename)

    # Parse the WCS keyworkds in the primary HDU
    w = wcs.WCS(hduList[0].header)

    # Print out the "name" of the wCS, as definied in the FITS header
    print w.wcs.name

    # print out all the settings that were parsed from the header
    w.wcs.print_contents()

    # some pixel coordinates
    pixcrd = numpy.array([[0,0], [24, 38], [45, 98]], numpy.float_)
    
    world = w.wcs_pix2world(pixcrd,1)
    print world

    
if __name__ == "__main__":
    loadWcsFromFile(sys.argv[-1])
