import numpy as np
import pylab as plt
import scipy.signal as sig

execfile('levelTest1.py')
execfile('levelTest2.py')
execfile('levelTest45deg.py')
execfile('levelTest10deg.py')
execfile('levelTest20deg.py')
execfile('levelTest30deg.py')
execfile('levelTest40deg.py')
execfile('levelTest50deg.py')
execfile('levelTest60deg.py')
execfile('levelTest70deg.py')
execfile('levelTest80deg.py')
#execfile('levelTestFullVert.py')

# make a vector of all the data
dataVector = [x1, x2, x3, x10, x20, x30, x40, x50, x60, x70, x80] #add x4 for the "vertical" data

# vector to be populated by the 
sgVector = []

for item in dataVector:
    sgVector.append(sig.savgol_filter(item,51,3))

print sgVector

#calculate the T and A values for the 1st order approx.  T&A LMAO.
nominalAngle = [0, 2, 45, 10, 20, 30, 40, 50, 60, 70, 80]
i = 0
meanVal = []
for x in sgVector:
    print sum(x[10000:12000])/len(x[10000:12000])
    print sum(x[10000:12000])/len(x[10000:12000])-nominalAngle[i]
    meanVal.append( sum(x[10000:12000])/len(x[10000:12000])-nominalAngle[i])
    i+=1 

print sum(meanVal)/len(meanVal)
X = np.linspace(100, 20000, 20000, endpoint=True)

# this is the first order model.
i = 0
qval = []
for x in sgVector:
    Y = (1-np.exp(-X/2253))*1.2105+ nominalAngle[i] #1st order model
    Z =np.exp(-X/2253)*1.2105  #correction factor
    Q = x - (1-Z) 
    qval.append(sum(Q)/len(Q) - nominalAngle[i])
    plt.plot(X,Y)
    #plt.plot(X,Z) # Z was just to learn
    plt.plot(X,Q)
    i+=1

print sum(qval)/len(qval)
plt.plot(x1)
plt.plot(x2)
plt.plot(x3)
# plt.plot(x4)
plt.plot(x10)
#plt.plot(sgVector[4])
plt.plot(x20)
plt.plot(x30)
plt.plot(x40)
plt.plot(x50)
plt.plot(x60)
plt.plot(x70)
plt.plot(x80)
#for thing in sgVector:
#    plt.plot(thing)
#    print len(thing)
plt.xlabel('angle sample number')
plt.ylabel('pitch angle (deg)')
plt.title('first order approximation results 10 degrees')
plt.show()
