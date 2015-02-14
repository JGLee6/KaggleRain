# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 16:19:14 2015

@author: John
"""

import numpy as np
import warnings
warnings.filterwarnings('error')

def data_integrator(dictData, dataKey):
    """ Returns new variable integratedData as Riemann sum style"""
    lastId = 0.0
    dataLength = len(dictData['TimeToEnd'])
    #initialize timeDifferences and integratedData
    timeDiff = np.zeros(dataLength)
    integratedData = np.zeros(dataLength)
    
    #sum variable for integration over single time series portion
    newSum = 0.0
    
    #Start Marching through to make timeDiff
    for k in range(dataLength):
        if dictData['Id'][k] == lastId:
            deltaT = dictData['TimeToEnd'][k-1] - dictData['TimeToEnd'][k]
            if deltaT > 0:
                timeDiff[k] = deltaT
                newSum += deltaT*dictData[dataKey][k]/60.0
                integratedData[k] = newSum
            else:
                timeDiff[k] = 60.0 - dictData['TimeToEnd'][k]
                newSum = timeDiff[k]*dictData[dataKey][k]/60.0
        else:
            timeDiff[k] = 60.0 - dictData['TimeToEnd'][k]
            newSum = timeDiff[k]*dictData[dataKey][k]/60.0
        lastId = dictData['Id'][k]
        
    return timeDiff, integratedData

def integrate_all(dictData):
    """integrate all rows except TimeToEnd and index, and return modified dict"""
    newKeys = ['Id', 'HybridScan', 'MassWeightedMean', 'Composite', 'RR3', \
    'MassWeightedSD', 'Reflectivity', 'RadarQualityIndex', 'ReflectivityQC', \
    'RR2', 'LogWaterVolume', 'DistanceToRadar', 'RhoHV', 'Expected', 'Velocity', \
    'Zdr', 'Kdp', 'HydrometeorType', 'RR1']
    newDict = {}
    #indices denoting end of sets of rows with the same Id
    pickIndices = np.append(np.where(np.diff(dictData['Id']) != 0)[0], -1)
    #pickIndices = np.append(np.where(np.diff(cumulative) <= 0)[0], -1)
    #pickIndices = np.append(np.where(np.diff(dictData['TimeToEnd']) <= 0)[0], -1)
    for k in newKeys:
        cumulative = data_integrator(dictData, k)[1]
        integrated = cumulative[pickIndices]
        newDict[k] = integrated
    return newDict

    
            

#def integrator2(dictData, key = None):
#    """same as data_integrator (i think)"""
#    boundaries = np.where(np.diff(dictData['TimeToEnd']) > 0)[0] + 1
#    deltaT =  np.diff(-dictData['TimeToEnd'])
#    deltaT[deltaT < 0] = 0
#    splitSum = lambda arr: np.array(map(np.sum, np.split(arr, boundaries, axis = 0)))
#    if key is None:
#        integratedData = {k: splitSum(deltaT * dataDict[k]) for k in dictData.keys()}
#    else:
#        integratedData = splitSum(dictData[key])
#    return timeDiff, integratedData
