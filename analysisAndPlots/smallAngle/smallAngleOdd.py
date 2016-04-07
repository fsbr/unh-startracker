# i'm making my own plots of the small angle approximation to add into thesis.
from __future__ import division
import numpy as np
import pylab as plt

# set up simple vector
x = np.linspace(-0.5*np.pi, 0.5*np.pi, 300, endpoint=True)
tht = x
x2 = 1 - x**2/2
sin_tht = np.sin(tht)
cos_tht = np.cos(tht)
tan_tht = np.sin(tht)/np.cos(tht) 
zp5 = np.ones(len(x))*0.01
#plt.plot(x,tht, label='theta')
#plt.plot(x,sin_tht, label='sin theta') # 2D plotting should have 2 args when possible
#plt.plot(x,tan_tht, label = 'tan theta')
plt.figure(1)
plt.plot(x,x2,label='1-x**2/2')
plt.plot(x,cos_tht,label='cos theta')
#plt.xlim([-0.25*np.pi, 0.25*np.pi])
#plt.ylim([0.6, 1.1])
plt.xlabel('angle (radian)')
plt.ylabel('output')
plt.legend(loc=0)
plt.title('Even Function Small Angle Approximation')

plt.figure(2)
sinerror = abs(tht/sin_tht - 1)
coserror = abs(x2/cos_tht - 1)
tanerror = abs(tht/tan_tht - 1)
print tanerror
plt.plot(x,sinerror, label ='sine error')
plt.plot(x,coserror, label = 'cosine error')
plt.plot(x,tanerror, label = 'tangent error')
plt.plot(x,zp5, label = 'zp01 line')
plt.xlim([0, np.pi/2])
plt.ylim([0,0.05])
plt.legend(loc=0)
plt.xlabel('angle (radian)')
plt.ylabel('output')
plt.title('absolute relative error for trigonometric functions')

plt.show()
