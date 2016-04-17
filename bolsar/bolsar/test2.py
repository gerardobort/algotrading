#----------
# build the dataset
#----------
from pybrain.datasets import SupervisedDataSet
import numpy, math


import numpy as np
import bolsar

data = bolsar.getSecurityHistory('ALUA')
table = data.transpose()
table = table[table[:,0].argsort()] # sort table by column 0 (timepstamps)

x1values = table[:,8][1:] / np.mean(table[:,8][1:]) #VariacionPrecio lshifted
x2values = table[:,9][1:] / np.median(table[:,9][1:]) #Operaciones lshifted
x3values = table[:,10][1:] / np.median(table[:,10][1:]) #TotalOperadoVn lshifted
y0values = table[:,8][:-1] / np.mean(table[:,8][:-1]) #VariacionPrecio rshifted
yvalues = y0values.copy()
yvalues[np.where(y0values > 0)] = 1
yvalues[np.where(y0values <= 0)] = -1
#yvalues = y0values

#xvalues = numpy.linspace(0,2 * math.pi, 1001)
#yvalues = 5 * numpy.sin(xvalues)

ds = SupervisedDataSet(3, 1)
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
import pylab
# neural net approximation
pylab.scatter(x1values,
           [ net.activate([x1, x2, x3]) for x1, x2, x3 in zip(x1values, x2values, x3values) ], linewidth = 2,
           color = 'blue', label = 'NN output')

# target function
pylab.scatter(x1values,
           yvalues, linewidth = 2, color = 'red', label = 'target')

pylab.grid()
pylab.legend()
pylab.show()
