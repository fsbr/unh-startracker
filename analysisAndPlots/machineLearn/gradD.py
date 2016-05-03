# trying to write this simple gradient descent because im being so dumb
from __future__ import division
import numpy as np
x_old = 0
x_new = np.pi/8 # the algorithm starts at x=6
gamma = 0.01
precision = 0.0000001

def f_derivative(x):
    #return 4*x**3 - 9*x**2
    return -1*(np.cos(x) +np.sin(x))
while abs(x_new - x_old) > precision:
    x_old = x_new
    x_new = x_old - gamma*f_derivative(x_old)

print "local min occurs at %s"%(x_new)
