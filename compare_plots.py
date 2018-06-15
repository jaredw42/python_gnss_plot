#!/usr/bin/python3
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os



def plot_cdf(*args, **metadata):

	plt.figure()
	plt.title('title')
	ax = plt.subplot(1,1,1)
	x = 2 
	#print(kwargs.items())
	fw = metadata['FWversion']
	#fw = []

	#fw[0] = a.strip(".-")
	#fw[1] = 'v1.5.15'
	#print(fw)
	for key, value in metadata.items():
		pass

	for i, value in enumerate(args):
		#print(i," enumerate")

	#	print(value.ndim, "ndims")
		d = np.reshape(value,-1)
		#print(d.ndim, "d-ndim")
		d.sort()
		d = d[~np.isnan(d)]
		yvals = np.arange(len(d)) / float(len(d) - 1)

		plt.plot(d, yvals,label=fw)
		#plt.legend()
		

		#below here sets values for CDF stats printouts on the plots
		a  = []
		y = 0.35
		ydelim = 0.05
		#x = np.max([~np.isnan(dsorted)]) * 0.33

		for q in [50, 68, 95, 99.9]:
			if x == 2:
				a = (("{}% percentile: {:.2f}".format (q, np.percentile(d, q))))
			else:
			#	pass
				a = (("{:.2f}".format (np.percentile(d, q))))
			y =  y - ydelim

			plt.text(x, y, a)
			
		x = 1.5 + x
	plt.grid()
	plt.legend(loc='upper right')
	#plt.legend(['0',])
	#plt.plot([1,2])
	#plt.legend(['data1'], ['data2'])

#plt.xlabel(xlabel)
#plt.ylabel(ylabel)


	#['v140_develop_2018060121_7'], ['v1_5_12']
	#print(ax.get_legend_handle_labels())
	# plt.show()
	# df = pd.DataFrame(value,columns=['oh'])
	# 	print(df.columns)
	# 	#yprint(d.shape)
		
		
	# 	df.sort_values('oh')
	# 	np.squeeze(d).shape
	# 	print(d.shape)
	# 	print(type(d), "data")
