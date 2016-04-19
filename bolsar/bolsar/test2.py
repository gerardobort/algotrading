#----------
# bolsar NN future quote prediction
#----------
from pybrain.datasets import SupervisedDataSet
import numpy, math
import numpy as np
import bolsar

def getTrainingTableSamples(table):
    # ix = [0,1,2,3...7,8]
    x1values = table[:-1,8] / np.mean(table[:-1,8]) #VariacionPrecio
    x2values = table[:-1,9] / np.median(table[:-1,9]) #Operaciones
    x3values = table[:-1,10] / np.median(table[:-1,10]) #TotalOperadoVn
    # iy = [1,2,3,4...8,9]
    y0values = table[1:,8] / np.mean(table[1:,8]) #VariacionPrecio lshifted
    yvalues = np.sign(y0values).astype(np.float)
    return x1values, x2values, x3values, yvalues

def getTestTableSamples(table, todayIndex):
    # ix = [0,1,2,3...7,8]
    if (table[todayIndex,8] == 0):
        return 0, 0, 0, 0 
    x1 = table[todayIndex,8] / np.mean(table[:todayIndex+1,8]) #VariacionPrecio
    x2 = table[todayIndex,9] / np.median(table[:todayIndex+1,9]) #Operaciones
    x3 = table[todayIndex,10] / np.median(table[:todayIndex+1,10]) #TotalOperadoVn
    # iy = [1,2,3,4...8,9]
    y0 = table[todayIndex+1,8] / np.mean(table[1:todayIndex+1,8]) #VariacionPrecio lshifted
    y = float(np.sign(y0))
    return x1, x2, x3, y




#----------
# build the network
#----------
from pybrain.structure import SigmoidLayer, LinearLayer
from pybrain.tools.shortcuts import buildNetwork

from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
import os

strFilename = 'data/nn.xml'

if (os.path.exists(strFilename)):
    net = NetworkReader.readFrom(strFilename)
else:
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
    ds = SupervisedDataSet(3, 1)

    table = bolsar.getSecurityHistory('ALUA')
    x1values, x2values, x3values, yvalues = getTrainingTableSamples(table)
    for x1, x2, x3, y in zip(x1values, x2values, x3values, yvalues):
        ds.addSample((x1, x2, x3), (y,))

    table = bolsar.getSecurityHistory('YPFD')
    x1values, x2values, x3values, yvalues = getTrainingTableSamples(table)
    for x1, x2, x3, y in zip(x1values, x2values, x3values, yvalues):
        ds.addSample((x1, x2, x3), (y,))

    from pybrain.supervised.trainers import BackpropTrainer
    trainer = BackpropTrainer(net, ds, verbose = True)
    trainer.trainUntilConvergence(maxEpochs = 100)
    NetworkWriter.writeToFile(net, strFilename)



#----------
# evaluate
#----------
table = bolsar.getSecurityHistory('PAMP')
table = table[0:400]

# neural net approximation
acertions = 0
tries = 0
zeros = 0

xAxis = np.arange(table.shape[0] - 1) # minus one dimension
yAxisReal = table[:-1,8].astype(np.float)
yAxisPredicted = np.empty([table.shape[0]-1, 1]) # initialize prodictions list
results = yAxisPredicted.copy()

for i in xAxis:
    x1, x2, x3, futureY = getTestTableSamples(table, i)
    yAxisPredicted[i] = predictedY = net.activate([x1, x2, x3])[0]
    print('result:', predictedY, futureY, yAxisReal[i])
    if (predictedY * futureY >= 0):
        acertions = acertions + 1
    if (predictedY * futureY == 0):
        zeros = zeros + 1
    tries = tries + 1

print('Tries:')
print(tries)
print('Acertions:')
print(acertions)
print('Zeros:')
print(zeros)
print('Acertion Ratio:')
print(float(acertions)/tries)


import pylab
pylab.plot(xAxis, yAxisReal, linewidth = 1, color = 'red', label = 'real output')
pylab.plot(xAxis, yAxisPredicted, linewidth = 1, color = 'blue', label = 'NN output')
#pylab.plot(xAxis, results, linewidth = 1, color = 'green', label = 'NN output')

pylab.scatter([0,1], [-2,2], linewidth = 1, color = 'yellow', label = 'edge')

pylab.grid()
pylab.legend()
pylab.show()
#print(xAxis)
#print(yAxisReal)
#print(yAxisPredicted)

