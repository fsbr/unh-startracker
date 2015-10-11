import ST

t = [0,53,13]
ghaZero = [16,18.7]
ghaOne = [31, 21.1]
meanBias = 5.356 # total amount of diff. i need to get out of my system
accounted = 2.7 # stuff i've actually been able to account for so far
dt = -2

alshain = ST.Observation([0,53, 13+dt], 54.6176 - meanBias,[61, 10.299], ghaZero, ghaOne, [6,24.4])
altair2 = ST.Observation([0,53,13+dt], 56.3854 - meanBias, [62, 18.2504], ghaZero, ghaOne, [8,52.0993])
tarazed = ST.Observation([0,53,13+dt],57.4902 - meanBias, [63, 26.1049], ghaZero, ghaOne, [10, 36.7657])
obs = [alshain, altair2, tarazed]

ST.runLocateMeALot(obs) 

