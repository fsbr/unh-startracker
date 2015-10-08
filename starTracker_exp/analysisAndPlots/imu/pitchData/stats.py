#O attempting a savitsky golay filter
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

x = np.linspace(0,2*np.pi, 100)
y = np.sin(x) + np.random.random(100)*0.2
yhat = sig.savgol_filter(y, 51,3) 
print yhat
plt.plot(x,y)
plt.plot(x,yhat, color='red')
plt.show()
