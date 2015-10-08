# plots the IMU data for nominally horizontal and nominally vertical positions
# the idea is that we're looking for drift etc.

# also apply the savitsky-golay filter 
import matplotlib.pyplot as pl
import numpy as np
import scipy.signal as sig
execfile('pitch1.py')       # p1
execfile('pitch2.py')       # p2
execfile('pitch3.py')       # p3
execfile('pitch4.py')       # p4
execfile('ninety1.py')      #ninety1
execfile('ninety2.py')
execfile('ninety3.py')
execfile('ninety4.py')      # ninety4
execfile('ninety1.py')  
f = open('meanData', 'w')
#apply the filter
# gather my shit
allMyPitchesLoveMe = [p1, p2, p3, p4]
ninetyNineProblems = [ninety1, ninety2, ninety3, ninety4]

def plotSavGolFilter(array):
    count = 0
    for x in array:
        count = count + 1
        pl.figure()
        p4sg = sig.savgol_filter(x,51,1)
        p4cd = np.gradient(p4sg)
        pl.plot(x)
        pl.plot(p4sg)
        pl.plot(p4cd)
        # print p4cd
        for i in range(0, len(x)):
            # iterate thru each array SLOW
            if abs(p4cd[i]) < 1e-4:
                # f.write("%s\n"%count)
                f.write("%s,\n"%i)
    pl.show()


def plotAllTheThings():
    pl.figure()
    test1 = pl.plot(p1, label='Test 1')
    test2 = pl.plot(p2, label='Test 2')
    test3 = pl.plot(p3, label='Test 3')
    test4 = pl.plot(p4, label='Test 4')
    pl.xlim(-5, 200)
    pl.ylim(1,4.5)
    pl.xlabel('Sample Number')
    pl.ylabel('Pitch (deg)')
    pl.title('Pitch Change on IMU Startup, (Horizontal)')
    pl.legend(loc='upper right')



    pl.figure()
    test1 = pl.plot(ninety1, label='Test 1')
    test2 = pl.plot(ninety2, label='Test 2')
    test3 = pl.plot(ninety3, label='Test 3')
    test4 = pl.plot(ninety4, label='Test 4')
    pl.xlim(-5, 200)
    # pl.ylim(-1,4.5)
    pl.xlabel('Sample Number')
    pl.ylabel('Pitch (deg)')
    pl.title('Pitch Change on IMU Startup (Vertical)')
    pl.legend(loc='lower right')
    pl.show()


if __name__ == '__main__':
    # plotAllTheThings()
    plotSavGolFilter(allMyPitchesLoveMe)
    plotSavGolFilter(ninetyNineProblems)
    print "nothing to doing"
