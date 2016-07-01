# unh-startracker
Star tracker location computation and post processing

This program is used with a DSLR camera that gives good images of the stars.
you take pictures and post process them in here, then, tries to guess your location using the USNO conscise method

The concise method is stored in analysisAndPlots/maps/ST.py
The image processing is stored in analysisAndPlots/maps/CPM.py

DO NOT USE the api methods with the terrible wifi card in the unh lab

Currently in the process of porting to python 3, which is just something i
should have done a long time ago tbh

known dependencies: astrometry.net software (built from c source)
                    scipy/numpy stack
                    python-pillow
