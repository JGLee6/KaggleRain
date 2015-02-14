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
        timePoints = len(fullArr[0])
        #timeDict[sampleNumber] = (len(fullArr[0]), rainfall)
        #times = fullArr[0]
        #timeSeriesSplitIndices =  1 + np.where(np.diff(times) > 0)[0]
        #timeSeriesList = np.split(fullArr, timeSeriesSplitIndices, axis = 1)
        #dataDict[sampleNumber] = {'features': timeSeriesList, 'target': rainfall}
        sortIndices = np.argsort(fullArr[0])
        fullArr = averageDuplicates(0, fullArr[:, sortIndices])
        summed = riemannSumArray(fullArr[0], fullArr[1:])
        #dataDict[sampleNumber] = {'attributes': summed, 'target': rainfall}
        dataDict[sampleNumber] = np.concatenate((summed, [timePoints, rainfall]))
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter = '\n')
        header = reader.next()[0].split(',')
        for lineList in reader:
            procOneLine(lineList[0])
    labels = header[:-1] + ['number of time points'] + [header[-1]]
    return labels, dataDict


def averageDuplicates(index, arr2d):
    """
    sort array according to values in ith row
    and average columns that are duplicate
    values in that row
    """
    # mask out NaNs
    arr2d = np.ma.masked_array(arr2d,np.isnan(arr2d))
    unique = np.unique(arr2d[index])
    newArr = np.ma.masked_array(np.zeros((len(arr2d), len(unique))))
    for i, val in enumerate(unique):
        toAverage = arr2d[:, np.where(arr2d[index] == val)[0]]
        newArr[:, i] = np.mean(toAverage, axis = 1)
    return newArr.filled(np.nan)

def riemannSum(x, y):
    """
    Compute Riemann sum. x is assumed to be in ascending order
    """
    y = np.ma.masked_array(y, np.isnan(y))
    intervals = np.diff(np.concatenate((np.array([0]), x)))
    return np.sum(intervals * y)

def riemannSumArray(x, arr2d):
    return np.array([riemannSum(x, y) if not np.isnan(y).all() else np.nan for y in arr2d])

#class Cache:
#def checkCached(path):
#    return True if os.path.isfile(path + '.p') else False
#
#def getCached(path):

