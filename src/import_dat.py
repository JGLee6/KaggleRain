import numpy as np
import os
import csv
import cPickle


#def getData(path):
#    """
#    return a dict that maps sample number to sample data. Each value is itself a dict;
#    its keys, 'target' and 'features', map to the measured rainfall quantity and a list
#    of arrays (one for each time series in the sample), respectively
#    
#    if a .p (pickle) file with the same name exists it will be loaded instead
#    """
#    if checkCached(path):
#        return getCached(path)
#    else:
#        return loadFromCSV(path)

def loadFromCSV(path):
    dataDict = {}
    def procOneLine(line):
        listForm = map(lambda datarow: map(float, datarow.split()), line.split(','))
        sampleNumber, rainfall = int(listForm[0][0]), float(listForm[-1][0])
        fullArr = np.array(listForm[1:-1])
        times = fullArr[0]
        timeSeriesSplitIndices =  1 + np.where(np.diff(times) > 0)[0]
        timeSeriesList = np.split(fullArr, timeSeriesSplitIndices, axis = 1)
        dataDict[sampleNumber] = {'features': timeSeriesList, 'target': rainfall}
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter = '\n')
        header = reader.next()
        for lineList in reader:
            procOneLine(lineList[0])
    return dataDict

#class Cache:
#def checkCached(path):
#    return True if os.path.isfile(path + '.p') else False
#
#def getCached(path):
    
