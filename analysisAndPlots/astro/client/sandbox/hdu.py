# trying to just read in a fits file

from astropy.io import fits

hdulist = fits.open('axy.fits')
print hdulist.info()
print hdulist[0].data
