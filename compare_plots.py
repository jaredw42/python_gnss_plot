#!/usr/bin/python3
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


#def plot_cdf(data1, data2,title='title', xlabel='Error', 
#			ylabel='Percent of Epochs', figname='fig'):

def plot_cdf(**kwargs):

	plt.figure()
	plt.title('title')
	print(kwargs.items())
	for key, value in kwargs.items():
		dname = key
		print(key,"key")
		dsorted = np.sort(value)
		print(len(dsorted), key)
		#print(value,"value")#, kwargs[a])

		yvals = np.arange(len(dsorted)) / float(len(dsorted) - 1)
		plt.plot(dsorted, yvals)

		#plt.xlabel(xlabel)
		#plt.ylabel(ylabel)
		plt.grid()

		#below here sets values for CDF stats printouts on the plots
		a  = []
		y = 0.35
		ydelim = 0.05
		#print(np.max(dsorted), "dsorted max")
		print(type(dsorted))
		#x = np.max([~np.isnan(dsorted)]) * 0.33
		x = 1
		#print(x,"x pos")
		# for q in [50, 68, 95, 99.9]:

		# 	a = (("{}% percentile: {}".format (q, np.percentile(dsorted, q))))
		# 	y =  y - ydelim
		# plt.text(x, y, a)

	plt.show()
