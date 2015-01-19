import matplotlib.pyplot as plt
import matplotlib.colors as colors
import loader

data = loader.load('../data/train_subset.csv')

for k1 in data.keys():

	for k2 in data.keys():

		if k1 == k2:
			continue

		args = loader.common_indices(data[k1], data[k2])
		nbins = 100
		explim = 20.0

		# Make a scatter plot.
		plt.figure()
		plt.title(k1 + ' vs ' + k2)
		plt.xlabel(k1)
		plt.ylabel(k2)

		if (k1 == 'Expected'):
			x = data[k1][args][data[k1][args] < explim]
			y = data[k2][args][data[k1][args] < explim]
			plt.scatter(x, y)

		else:
			plt.scatter(data[k1][args], data[k2][args])

		plt.savefig('scatter_' + k1 + '_v_' + k2 + '.png')
		plt.close()

		# Plot a 2d histogram.
		plt.figure()
		plt.title(k1 + ' vs ' + k2)
		plt.xlabel(k1)
		plt.ylabel(k2)

		if (k1 == 'Expected'):
			x = data[k1][args][data[k1][args] < explim]
			y = data[k2][args][data[k1][args] < explim]
			plt.hist2d(x, y, bins=nbins)

		else:
			plt.hist2d(data[k1][args], data[k2][args], bins=nbins)

		plt.savefig('h2_' + k1 + '_v_' + k2 + '.png')
		plt.close()

		# Make a log scale 2d histogram
		plt.figure()
		plt.title(k1 + ' vs ' + k2)
		plt.xlabel(k1)
		plt.ylabel(k2)

		if (k1 == 'Expected'):
			x = data[k1][args][data[k1][args] < explim]
			y = data[k2][args][data[k1][args] < explim]
			plt.hist2d(x, y, bins=nbins, normed=colors.LogNorm)

		else:
			plt.hist2d(data[k1][args], data[k2][args], normed=colors.LogNorm, bins=nbins)

		plt.savefig('h2log_' + k1 + '_v_' + k2 + '.png')
		plt.close()		