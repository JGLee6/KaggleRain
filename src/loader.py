import csv
import numpy as np

error_lo = -98999.0
error_hi = 998.0

def load(filename, colname=None):

	# We nned to get the total number of entries first
	reader = csv.reader(open(filename), delimiter=',')
	traits = reader.next()

	npoints = 0
	for line in reader:
		npoints += len(line[1].split(' '))

	# Set up the trait dictionary and 
	res = {}
	for trait in traits:
		res[trait] = np.empty(npoints)

	# Reopen the file. We need one more pass to store the data.
	reader = csv.reader(open(filename), delimiter=',')

	# Get the header out of the way.
	traits = reader.next()

	idx = 0
	for line in reader:

		# Figure out how many points are in this entry
		size = np.array(line[1].split(' ')).shape[0]

		for j, trait in enumerate(traits):

			res[trait][idx:idx+size] = np.array(line[j].split(' '))

		idx += size

	# We need to set Kdp ourselves for some stupid reason.
	res['Kdp'] = np.abs(40.6 / res['RR3']) ** 0.866

	# Now reset the values that had errors (and nans to be sure).
	args = (res['RR3'] == np.nan)
	args |= (res['RR3'] < error_lo)
	res['Kdp'][args] = res['RR3'][args]

	return res

def clean(array):

	return array[(array > error_lo) & (array < error_hi) & (array != np.nan)]


def common_indices(array1, array2):

	indices  = array1 != np.nan
	indices &= array1 > error_lo
	indices &= array1 < error_hi
	indices &= array2 != np.nan
	indices &= array2 > error_lo 
	indices &= array2 < error_hi 

	return indices

def accumulator(func, accum, lst):
    if len(lst) == 0:
        return accum
    else:
        return accumulator(func, func(accum, lst[0]), lst[1:])

def indices_clean(array):
    return np.where(np.logical_and(array > error_lo, np.logical_and(array < error_hi, array != np.nan)))[0]

def common_all(arr2d):
    return accumulator(lambda x, y: np.intersect1d(x, indices_clean(y)), np.array(range(len(arr2d[0]))), arr2d)
