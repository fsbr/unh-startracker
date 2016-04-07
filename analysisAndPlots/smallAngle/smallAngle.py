## i'm making my own plots of the small angle approximation to add into thesis.
from __future__ import division
import numpy as np
import pylab as plt

# set up simple vector
x = np.linspace(-0.5*np.pi, 0.5*np.pi, 300, endpoint=True)
tht = x
sin_tht = np.sin(tht)
#cos_tht = np.cos(tht)
tan_tht = np.sin(tht)/np.cos(tht) 
print tan_tht
plt.plot(x,tht, label='theta')
plt.plot(x,sin_tht, label='sin theta') # 2D plotting should have 2 args when possible
plt.plot(x,tan_tht, label = 'tan theta')
#plt.plot(x,cos_tht)
plt.xlim([-0.25*np.pi, 0.25*np.pi])
plt.ylim([-1, 1])
plt.xlabel('angle (radian)')
plt.ylabel('output')
plt.legend(loc=0)
plt.title('Odd Function Small Angle Approximation')
plt.show()
