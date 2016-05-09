#plotting the zenith requirement but better

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

# start a new figure
fig = plt.figure()
ax = fig.gca(projection='3d')

#makes a mesh grid of these points
X= np.arange(0, 0.5*np.pi, 0.02)
Y= np.arange(0,0.5*np.pi, 0.02)
X,Y = np.meshgrid(X,Y)
arg = 1-np.sin(X)**2-np.sin(Y)**2
Z = np.sqrt(arg)

surf = ax.plot_surface(X,Y,Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=True)
ax.set_xlabel('pitch (radians)')
ax.set_ylabel('roll (radians)')
ax.set_zlabel('z-component of optical axis')
plt.show()
