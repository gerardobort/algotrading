import numpy as np, scipy as sp, matplotlib.pyplot as plt
import bolsar
import datetime
from matplotlib import dates

security = 'ALUA'
table = bolsar.getSecurityHistory(security)

x = range(table.shape[0])
y1 = table[:,2]
y2 = table[:,3]
plt.plot(x, y1)
plt.plot(x, y2)

from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(2, 3, 1)
