#----------
# build the dataset
#----------
from pybrain.datasets import SupervisedDataSet
import numpy, math


import numpy as np
import bolsar

def getPredictiveTableSamples(table):
    x1values = table[:,8][1:] / np.mean(table[:,8][1:]) #VariacionPrecio lshifted
    x2values = table[:,9][1:] / np.median(table[:,9][1:]) #Operaciones lshifted
    x3values = table[:,10][1:] / np.median(table[:,10][1:]) #TotalOperadoVn lshifted
    y0values = table[:,8][:-1] / np.mean(table[:,8][:-1]) #VariacionPrecio rshifted
    yvalues = y0values.copy()
    yvalues[np.where(y0values > 0)] = 1
    yvalues[np.where(y0values <= 0)] = -1
    return x1values, x2values, x3values, yvalues

def getRealTableSamples(table):
    x1values = table[:,8] / np.mean(table[:,8]) #VariacionPrecio lshifted
    x2values = table[:,9] / np.median(table[:,9]) #Operaciones lshifted
    x3values = table[:,10] / np.median(table[:,10]) #TotalOperadoVn lshifted
    y0values = table[:,8] / np.mean(table[:,8]) #VariacionPrecio rshifted
    yvalues = y0values.copy()
    yvalues[np.where(y0values > 0)] = 1
    yvalues[np.where(y0values <= 0)] = -1
    return x1values, x2values, x3values, yvalues

table = bolsar.getSecurityHistory('ALUA')
x1values, x2values, x3values, yvalues = getPredictiveTableSamples(table)

ds = SupervisedDataSet(3, 1)

for x1, x2, x3, y in zip(x1values, x2values, x3values, yvalues):
    ds.addSample((x1, x2, x3), (y,))

table = bolsar.getSecurityHistory('YPFD')
x1values, x2values, x3values, yvalues = getPredictiveTableSamples(table[:table.shape[0]/2]) # train with first half of data samples

for x1, x2, x3, y in zip(x1values, x2values, x3values, yvalues):
    ds.addSample((x1, x2, x3), (y,))


#----------
# build the network
#----------
from pybrain.structure import SigmoidLayer, LinearLayer
from pybrain.tools.shortcuts import buildNetwork

net = buildNetwork(3,
                   100, # number of hidden units
                   1,
                   bias = True,
                   hiddenclass = SigmoidLayer,
                   outclass = LinearLayer
                   )
#----------
# train
#----------
from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, ds, verbose = True)
trainer.trainUntilConvergence(maxEpochs = 100)

#----------
# evaluate
#----------
table = bolsar.getSecurityHistory('YPFD')
x1values, x2values, x3values, yvalues = getPredictiveTableSamples(table[-table.shape[0]/2:]) # test with last half of data samples


acertions = 0
tries = 0
for x1, x2, x3, y in zip(x1values, x2values, x3values, yvalues):
    ynn = net.activate([x1, x2, x3])
    if (ynn * y >= 0):
        acertions = acertions + 1
    tries = tries + 1

print('Tries:')
print(tries)
print('Acertions:')
print(acertions)
print('Acertion Ratio:')
print(float(acertions)/tries)




import pylab
# neural net approximation



rx1, rx2, rx3, ry = getPredictiveTableSamples(table) # print the entire real  data samples


x = np.arange(rx1.shape[0])
y = ry
pylab.plot(x, y, linewidth = 1, color = 'red', label = 'real output')

xnn = x[-x.shape[0]/2:]-1
ynn = [ net.activate([x1, x2, x3]) for x1, x2, x3 in zip(x1values, x2values, x3values) ]
pylab.plot(xnn, ynn, linewidth = 2, color = 'blue', label = 'NN output')
#pylab.scatter(xnn, ynn, linewidth = 2, color = 'blue')


pylab.grid()
pylab.legend()
pylab.show()
