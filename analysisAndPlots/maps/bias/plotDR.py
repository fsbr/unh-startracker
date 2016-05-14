# my first foray into the pandas library
# tckf spring 2016
# try to implement line of best fit as well
# okay i can do this

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model

# writing the damn class to do GD

df = pd.read_csv('datapoints.csv')
print df
# grab data rates
#2 grab years

x1 = df[['off']]
y1 = df[['lat']]

#create linear regression object
regr = linear_model.LinearRegression()

#train the model
regr.fit(x1,y1)
print regr.score(x1,y1)
#coeffecients
print 'coefficients %s' %regr.coef_

## PLOTTING STUFF

#describe the color dictionary
# colorDict = {'mars':'red', 'venus':'green', 'mercury':'black', 'saturn':'orange'} 
plt.scatter(x1,y1)
plt.plot(x1,regr.predict(x1), linewidth=2)
#plt.legend(label=df.iloc[:,3].values)
plt.xlabel('offset angle')
plt.ylabel('Latitude Estimate (deg)')
plt.title('Latitude Estimate vs. Bias Angle (w/ linear regr)')
plt.show()
