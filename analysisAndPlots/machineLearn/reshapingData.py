# im trying to reshape my data
import pandas as pd
import numpy as np
df = pd.read_csv('analysis.csv',header=None)
df1 = pd.read_csv('plotData.csv',header=None)
hc1 = df.iloc[:,3].values
hc2 = df.iloc[:,4].values
hc3 = df.iloc[:,5].values
hct =[] 
for i in range(0, len(hc1)):
    hct.append(hc1[i])
    hct.append(hc2[i])
    hct.append(hc3[i])
s = pd.Series(hct)
s.to_csv('desiredVals.csv',index=False)
s.plot()
# for now idk how to put these into the same "dataframe"
print s
