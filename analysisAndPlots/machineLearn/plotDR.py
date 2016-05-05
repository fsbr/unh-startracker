# my first foray into the pandas library
# tckf spring 2016
# try to implement line of best fit as well
# okay i can do this

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model

# writing the damn class to do GD

df = pd.read_csv('datarates.csv')
print df
# grab data rates
y = df.iloc[:, 2].values
planet = np.where(y=='mars',-1,1)
print planet
#2 grab years
x = df.iloc[:,1].values
names = df.iloc[:,0].values

x1 = df[['date']]
y1 = df[['max_datarate']]

#create linear regression object
regr = linear_model.LinearRegression()

#train the model
regr.fit(x1,y1)

#coeffecients
print 'coefficients %s' %regr.coef_

## PLOTTING STUFF

#describe the color dictionary
colorDict = {'mars':'red', 'venus':'green', 'mercury':'black', 'saturn':'orange'} 
plt.scatter(x,y,color=[colorDict[i] for i in df.iloc[:,3]],s=34)
plt.plot(x1,regr.predict(x1), linewidth=2)
#plt.legend(label=df.iloc[:,3].values)
plt.xlabel('Year')
plt.ylabel('Data Tranmission Rate (kbps)')
plt.title('Data Transmission Rates of Various Terrestrial Landers, and Deep Space Probes')
plt.show()
