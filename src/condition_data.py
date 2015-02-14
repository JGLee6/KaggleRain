import scipy.interpolate as interp
import numpy as np

error_lo = -98999.0
error_hi = 998.0

# keys for all attributes save Id, Expected, and TimeToEnd
attributeKeys = ['HybridScan', 'MassWeightedMean', 'Composite', 'RR3', \
'MassWeightedSD', 'Reflectivity', 'RadarQualityIndex', 'ReflectivityQC', \
'RR2', 'LogWaterVolume', 'DistanceToRadar', 'RhoHV', 'Velocity', \
'Zdr', 'Kdp', 'HydrometeorType', 'RR1']

def accumulator(func, accum, lst):
    """
    higher-order function to perform accumulation
    """
    if len(lst) == 0:
        return accum
    else:
        return accumulator(func, func(accum, lst[0]), lst[1:])

def indices_clean(array):
    """
    return the indices (NOT the array of values) selected by clean
    """
    return np.where(np.logical_and(~np.isnan(array), np.logical_and(array < error_hi, array > error_lo)))[0]


def clean(array):
	return array[indices_clean(array)]


def common_indices(arr2d, selectionFunc = indices_clean, rows = 'all'):
    """
    return common valid indices (NOT the values) of a subset of the rows of arr2d

    -The selected rows are indicated by the keyword rows (EITHER 'all' OR a 
     list of row indices)
    -The valid column indices are determined by the given index selection function

    use with:
        -selectionFunc = indices_clean, to get indices of valid data
        -selectionFunc = except_outlier_indices, to get rid of outliers
    """
    if rows == 'all':
        selectionArr = arr2d
    else:
        selectionArr = arr2d[rows]
    return accumulator(lambda x, y: np.intersect1d(x, selectionFunc(y)), \
        np.array(range(len(selectionArr[0]))), selectionArr)


def clean_dict(dictData, excluded = None, selectionFunc = indices_clean):
    """
        remove all columns of data containing at least one bad attribute value
        and return a new dict. TimeToEnd and Id are not considered. 

        excluded: a list of additional attributes to exclude from cleaning
    """
    if excluded is not None:
        for key in excluded:
            attributeKeys.remove(key)
    newDict = {}
    valid_indices = common_all([dictData[k] for k in attributeKeys], selectionFunc = selectionFunc)
    for k in dictData.keys():
        newDict[k] = dictData[k][valid_indices]
    return newDict


def except_outlier_indices(arr, dev = 2.5):
    """
    return indices of the array that contain values within dev number of
    standard deviations from the median
    """
    cleaned = clean(arr)
    window = dev * np.std(cleaned)
    avg = np.average(cleaned)
    return np.where(np.logical_and(arr < avg + window, arr > avg - window))[0]

def substitute_all(data, source, target):
    """
    Replace all occurrences of the value source (numeric or nan, denoted by source == 
    'nan') by target. Data may be a dict or array.
    """
    def substitute_1d(arr):
        """
        substitute values in a 1d array
        """
        if source == 'nan':
            arr[np.isnan(arr)] = target
        else:
            arr[np.equal(arr, source)] = target
        return arr
    def substitute_array(arr):
        """
        substitute values in a 1 or 2-d array
        """
        dim = len(np.shape(arr))
        if dim == 1:
            return substitute_1d(arr.copy())
        elif dim == 2:
            newArr = arr.copy()
            for row in newArr:
                substitute_1d(row)
            return newArr
        else:
            raise ValueError("not array of valid shape")
    if type(data) == dict: #data is a dict
        newDict = {}
        for k in data.keys():
            newDict[k] = substitute_1d(data[k].copy())
        return newDict
    else: #data is assumed to be an array
        return substitute_array(data)

def normalize(arr):
    """ subtract mean and divide by standard deviation """
    def normalize1d(arr):
        return (arr - np.average(arr))/np.std(arr)
    dim = len(np.shape(arr))
    if dim == 1:
        return normalize1d(arr)
    elif dim == 2:
        return np.array(map(normalize, arr))
    else:
        raise ValueError("not array of valid shape")

# TODO: UNDER CONSTRUCTION
def attribute_expectations(dictData, samplePoints = 20):
    """
    interpolate the value of each attribute vs. actual
    rainfall amount, this can be used to fill in missing data

    returns two dicts with the same keys as the input:
        -tempDict: same format as input, missing attribute values replaced by 
         interpolated ones
        -interpolationDict: dict values are interpolation functions
    """
    expected = dictData['Expected']
    stride = len(expected)/samplePoints
    tempDict = {}
    interpolationDict = {}
    #filledDict = {'Id': 

    #indices that sort the rainfall amounts
    sortIndices = np.argsort(expected)
    #break sorted indices into bins
    groupedIndices = np.split(sortIndices, stride * np.array(range(samplePoints)))[1:]

    #given an attribute key, compute the mean value for each bin
    attributeGroupMeans = lambda key: np.array(map(np.mean, \
        map(lambda indices: dictData[key][indices], groupedIndices)))

    tempDict['Expected'] = attributeGroupMeans('Expected')
    for key in attributeKeys:
        tempDict[key] = attributeGroupMeans(key)

    makeInterpolation = lambda x, y: interp.interp1d(x, y)
    for key in attributeKeys:
        interpolationDict[key] = makeInterpolation(tempDict['Expected'], tempDict[key])
    

    return tempDict, interpolationDict

def covariance_matrix(arr2d):
    """
    normalize an array and return the covariance matrix of rows
    """
    return np.cov(normalize(arr2d))

class SampleDispenser(object):
    #TODO: current issue is that some of the higher-rainfall amount bins have 0
    #examples (even using the full training data set). Additionally, due to the way
    #grading is done we actually DO want CDFs that are most accurate for low
    #rainfall test examples, which means that this resampling approach may be
    #misguided
    """
    Draw (with replacement) samples with a "flat" distribution of expected
    rainfall values, i.e. examples n training data are grouped into bins according
    to expected rainfall value; probability of drawing from a bin is independent of
    the number of samples in it. This is intended to avert biased result in knn
    originating from the vast overrepresentation of low rainfall values in the
    training data. 
    
    This class can also be used in an implementation of bagging. 

    """

    def __init__(self, dictData, nbins = 80, binRange = (0, 80)):
        expected = dictData['Expected']
        binCenters = np.linspace(binRange[0], binRange[1], nbins)
        binSpacing = binCenters[1] - binCenters[0]
        #binSpacings = np.diff(binCenters)
        #binSpacing = np.append(binSpacings, binSpacings[-1])
        #binSpacingDict = {k: 
        #dict to store indices of examples in each bin
        binDict = {}
        for binVal in binCenters:
            binDict[binVal] = np.where(np.logical_and(expected > binVal - binSpacing/2, \
                expected < binVal + binSpacing/2))[0]

        self.nbins = nbins
        self.dictData = dictData
        self.binDict = binDict

    def drawSamples(self, numSamples):
        """
        draw numSamples - numSamples mod self.nbins number of samples

        returns a new data dictionary composed of the drawn examples
        """
        newDict = {}
        perBin = numSamples/self.nbins
        def drawOneBin(key):
            binIndices = self.binDict[key]
            randIndices = rand.randint(0, len(binIndices), perBin)
            return binIndices[randIndices]
        allIndices = np.concatenate((drawOneBin(key) for key in self.binDict.keys()))
        for key in self.dictData.keys():
            newDict[key] = self.dictData[key][allIndices]
        return newDict


