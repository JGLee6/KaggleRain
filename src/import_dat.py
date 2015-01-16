import numpy as np
import csv


def getData(path):
    """
    return a dict that maps sample number to sample data. Each value is itself a dict;
    its keys, 'target' and 'features', map to the measured rainfall quantity and a list
    of arrays (one for each time series in the sample), respectively
    """
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
