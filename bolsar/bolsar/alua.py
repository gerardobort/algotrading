import numpy as np, scipy as sp, matplotlib.pyplot as plt
import bolsar
import datetime
from matplotlib import dates

security = 'ALUA'
table = bolsar.getSecurityHistory(security)

x = range(table.shape[0])
y1 = table[:,2] - np.min(table[:,2])
y2 = table[:,8]
y3 = table[:,9] / np.median(table[:,9])
plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)


plt.title(security + ": Price Interdiary Historic")
plt.xlabel("Hora")
plt.ylabel("Price")
plt.xticks([w*7*24 for w in range(30)], 
  ['week %i'%w for w in range(30)])
plt.autoscale(tight=True)
plt.grid()
plt.show()
