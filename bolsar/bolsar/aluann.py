import numpy as np, scipy as sp, matplotlib.pyplot as plt
import bolsar
import datetime
from matplotlib import dates

security = 'ALUA'
data = bolsar.getSecurityHistory(security)
table = data.transpose()
table = table[table[:,0].argsort()] # sort table by column 0 (timepstamps)

x = range(table.shape[0])
y1 = table[:,2]
y2 = table[:,3]
plt.plot(x, y1)
plt.plot(x, y2)

from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(2, 3, 1)
