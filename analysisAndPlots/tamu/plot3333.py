#fuck

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

n_angles = 36
n_radii = 8

#an array of radii
radii = np.linspace(0.125, 1.0, n_radii)

#an array of angles
angles = np.linspace(0,2*np.pi, n_angles, endpoint=False)

# repeat all angles for each radius
angles = np.repeat(angles[...,np.newaxis], n_radii, axis=1)

# convert polar (radii, angles) coords to cartesian (x,y) coords
# (0,0) is added here.  There are no duplicate points in the (x,y) plane
x = np.append(0, (radii*np.cos(angles)).flatten())
y = np.append(0, (radii*np.sin(angles)).flatten())

# pringle surface
z = np.sin(-x*y)

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot_trisurf(x,y,z, cmap=cm.jet, linewidth=0.2)
plt.show()
