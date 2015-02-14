import csv
import numpy as np
import numpy.random as rand
import condition_data

error_lo = -98999.0
error_hi = 998.0
TINY = 1e-9


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
        # add TINY to denominator to avoid dividing by 0
	res['Kdp'] = np.abs(40.6 / (TINY + res['RR3'])) ** 0.866

	# Now reset the values that had errors (and nans to be sure).
	args = (res['RR3'] == np.nan)
	args |= (res['RR3'] < error_lo)
	res['Kdp'][args] = res['RR3'][args]

	return res

def clean(arr):
    return condition_data.clean(arr)

def common_indices(array1, array2):

	indices  = array1 != np.nan
	indices &= array1 > error_lo
	indices &= array1 < error_hi
	indices &= array2 != np.nan
	indices &= array2 > error_lo 
	indices &= array2 < error_hi 

	return indices

