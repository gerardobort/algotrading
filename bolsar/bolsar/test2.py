#----------
# bolsar NN future quote prediction
#----------
from pybrain.datasets import SupervisedDataSet
import numpy, math
import numpy as np
import bolsar

LPAD = 4
RPAD = 1

def getTrainingTableSamples(table):
    # ix = [0,1,2,3...7,8]
    x1values = table[:-1,8] / np.mean(table[:-1,8]) #VariacionPrecio
    x2values = table[:-1,9] / np.median(table[:-1,9]) #Operaciones
    x3values = table[:-1,10] / np.median(table[:-1,10]) #TotalOperadoVn
    # iy = [1,2,3,4...8,9]
    y0values = table[1:,8] #VariacionPrecio lshifted
    yvalues = np.sign(y0values).astype(np.float)
    return x1values, x2values, x3values, yvalues

def getTestTableSample(table, operationIndex):
    # ix = [0,1,2,3...7,8]
    if (operationIndex < LPAD):
        return tuple(np.zeros(3*(LPAD+1))), (0,) 
    inp = np.array([])
    for i in range(LPAD+1):
        j = operationIndex - LPAD + i
        if (table[j,8] != 0):
            x1 = table[j,8] / np.mean(table[:j+1,8]) #VariacionPrecio
        else:
            x1 = 0
        x2 = table[j,9] / np.median(table[:j+1,9]) #Operaciones
        x3 = table[j,10] / np.median(table[:j+1,10]) #TotalOperadoVn
        inp = np.append(inp, [x1, x2, x3])
    # iy = [1,2,3,4...8,9]
    y0 = table[operationIndex+RPAD,8] #VariacionPrecio lshifted
    y = float(np.sign(y0))
    return tuple(inp), y




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
    net = buildNetwork(3*(LPAD+1),
                       100, # number of hidden units
                       1,
                       bias = True,
                       hiddenclass = SigmoidLayer,
                       outclass = LinearLayer
                       )
    #----------
    # train
    #----------
    ds = SupervisedDataSet(3*(LPAD+1), 1)

    trainingSecurities = ['YPFD', 'ALUA', 'BMA', 'COME']
    for security in trainingSecurities:
        table = bolsar.getSecurityHistory(security)
        x1values, x2values, x3values, yvalues = getTrainingTableSamples(table)
        for i in range(LPAD+1, yvalues.shape[0]-RPAD):
            inp = np.concatenate((x1values[i-(LPAD+1):i], x2values[i-(LPAD+1):i], x3values[i-(LPAD+1):i]))
            out = yvalues[i]
            ds.addSample(tuple(inp), (out,))

    from pybrain.supervised.trainers import BackpropTrainer
    trainer = BackpropTrainer(net, ds, verbose = True)
    trainer.trainUntilConvergence(maxEpochs = 100)
    NetworkWriter.writeToFile(net, strFilename)



#----------
# evaluate
#----------
table = bolsar.getSecurityHistory('AUSO')
#table = table[0:5000]

# neural net approximation
acertions = 0
tries = 0
zeros = 0

xAxis = np.arange(table.shape[0] - 1) # minus one dimension
yAxisReal = np.sign(np.roll(table[:-1,8],1)).astype(np.float)
yAxisPredicted = np.empty([table.shape[0]-1, 1]) # initialize prodictions list

xyAcertions = ([], [])

results = yAxisPredicted.copy()

for i in xAxis[LPAD+1:]:
    inp, futureY = getTestTableSample(table, i)
    yAxisPredicted[i] = predictedY = net.activate(list(inp))[0]
    if (predictedY * futureY >= 0):
        acertions = acertions + 1
        xyAcertions[0].append(i)
        xyAcertions[1].append(predictedY)
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
pylab.plot(xAxis+1, yAxisPredicted, linewidth = 1, color = 'blue', label = 'NN output')
pylab.plot(xyAcertions[0], xyAcertions[1], linewidth = 2, color = 'green', label = 'NN acertions')

pylab.grid()
pylab.legend()
pylab.show()
