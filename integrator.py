# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 16:19:14 2015

@author: John
"""

import numpy as np

def data_integrator(dictData, dataKey):
    """ Returns new variable integratedData as Riemann sum style.
    
    This should only get fed data without NANs.
    """
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
            #hopefully first rate point isn't an error but will fix later if is
            lastGoodPt = k
        lastId = dictData['Id'][k]
        
    #update last dataKey contribution from last point
    lastDeltaT = dictData['TimeToEnd'][-1] - 0.0
    integratedData[-1] += lastDeltaT*dictData[dataKey][k-1]/60.0
        
    return timeDiff, integratedData
    
def rev_data_integrator(dictData, dataKey):
    """ Returns new variable integratedData as Riemann sum style.
    
    This should only get fed data without NANs.
    This one does forward rectangle rather than backward.
    """
    lastId = 0
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
                newSum += deltaT*dictData[dataKey][k-1]/60.0
                integratedData[k] = newSum
            else:
                timeDiff[k] = 60.0 - dictData['TimeToEnd'][k]
                newSum = timeDiff[k]*dictData[dataKey][k-1]/60.0
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
            