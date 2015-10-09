# plot the d value for the star tracker algorithm

import pylab as pl
import numpy as np

# X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

data = [22.701693112,
1.09729551964,
0.000558704106485,
3.15863831379e-07,
1.80041318994e-10,
1.81502836998e-13,
5.84746018958e-13,
1.81502836998e-13,
1.81502836998e-13,
1.81502836998e-13,
5.84746018958e-13]

altair123 = [1365.11315586,
784.083794907,
210.94519493,
13.6251762706,
0.0769786659093,
1.90245313122e-06,
2.19951924341e-11,
2.17661273317e-11,
1.45830080422e-11,
7.00365230975e-12,
1.06229300396e-12,
]

pl.figure()
pl.plot(data)
pl.plot(altair123)
pl.ylabel('estimated position delta')
pl.xlabel('iteration number')
pl.title('Convergence of Nautical Star Tracker Location')
pl.show()
