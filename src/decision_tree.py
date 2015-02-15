import loader
import condition_data
import copy
import numpy as np
import integrator
from sklearn import tree
import pickle
import import_dat
import sys

#sklearn's decision tree learner can't handle NAN values
ERR_NAN = 2 * condition_data.error_hi

dataDir = sys.argv[1]


try:
    labels, dataDict = pickle.load(open(dataDir + '/train_subset.p', 'r'))
except:
    labels, dataDict = import_dat.loadFromCSV(dataDir + '/train_subset.csv')

try:
    testlabels, testDataDict = pickle.load(open(dataDir + '/train_subset_2.p', 'r'))
except:
    testlabels, testDataDict = import_dat.loadFromCSV(dataDir + '/train_subset_2.csv')

def getCleanData(labels, dataDict, mode = 'train'):
    datArray = np.array(dataDict.values())
    datArray = condition_data.substitute_all(datArray, 'nan', ERR_NAN)
    if mode == 'train':
        # create two labels: -1 for rainfall == 0 and 1 for ranfall > 0
        attributes = datArray[:, :-1]
        classes = datArray[:, -1].copy()
        classes[classes > 0] = 1
        classes[classes <= 0] = -1
        return attributes, classes
    elif mode == 'test':
        return datArray

attributes, classes = getCleanData(labels, dataDict)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(attributes, classes)

testAttributes, testClasses = getCleanData(testlabels, testDataDict)

#classify test data and 'booleanize' it
pred = clf.predict(testAttributes)
bpred = np.array(map(lambda x: 0 if x < 0 else int(x), pred))

#the actual labels to compare against
bactual = np.array(map(lambda x: 0 if x < 0 else int(x), testClasses))

accuracyTrue = float(sum(bpred[bactual == 1]))/len(bactual[bactual == 1])
accuracyFalse = 1 - float(sum(bpred[bactual == 0]))/len(bactual[bactual == 0])

print "Rate of correct prediction for no rainfall: " + str(accuracyFalse)
print "Rate of correct prediction for nonzero rainfall: " + str(accuracyTrue)
