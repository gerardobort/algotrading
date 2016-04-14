import numpy as np, scipy as sp, matplotlib.pyplot as plt
import bolsar

data = bolsar.getSecurityHistory('ALUA')
x = np.sum([data[0].astype(np.float), data[1].astype(np.float)], axis=0)
y = data[2]

plt.scatter(x,y)
plt.title("ALUA Price Interdiary Historic")
plt.xlabel("Hora")
plt.ylabel("Price")
#plt.xticks([w*7*24 for w in range(10)], 
#  ['week %i'%w for w in range(10)])
plt.autoscale(tight=True)
plt.grid()
plt.show()
