# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 16:19:14 2015

@author: John
"""

import numpy as np
import warnings
warnings.filterwarnings('error')

def data_integrator(dictData, dataKey):
    """ Returns new variable integratedData as Riemann sum style.
    
    This still needs to think about cases of only one point, and point to end.
    Basically, backward or forward time step and counterparts contribution."""
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
                integratedData[k] = newSum
        else:
            timeDiff[k] = 60.0 - dictData['TimeToEnd'][k]
            newSum = timeDiff[k]*dictData[dataKey][k]/60.0
            integratedData[k] = newSum
            # add portion up to end of hour from last dataKey contribution
            lastDeltaT = dictData['TimeToEnd'][k-1] - 0.0
            integratedData[k-1] += lastDeltaT*dictData[dataKey][k-1]/60.0
        lastId = dictData['Id'][k]
        
    #update last dataKey contribution from last point
    lastDeltaT = dictData['TimeToEnd'][-1] - 0.0
    integratedData[-1] += lastDeltaT*dictData[dataKey][k-1]/60.0
        
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

    
            

