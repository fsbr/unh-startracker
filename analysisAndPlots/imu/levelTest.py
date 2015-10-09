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
execfile('levelTestFullVert.py')

# make a vector of all the data
dataVector = [x1, x2, x3, x4, x10, x20, x30, x40, x50, x60, x70, x80]

# vector to be populated by the 
sgVector = []

for item in dataVector:
    sgVector.append(sig.savgol_filter(item,51,3))

print sgVector

plt.plot(x1)
plt.plot(x2)
plt.plot(x3)
plt.plot(x4)
plt.plot(x10)
plt.plot(x20)
plt.plot(x30)
plt.plot(x40)
plt.plot(x50)
plt.plot(x60)
plt.plot(x70)
plt.plot(x80)
plt.show()
