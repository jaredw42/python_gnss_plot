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
	
	for a in kwargs:
		print (a, kwargs[a])
		plt.figure(kwargs.figname)

		dsorted = np.sort(data1)
		dsorted2 = np.sort(data2)

		yvals = np.arange(len(data1)) / float(len(data1) - 1)
		yvals2 = np.arange(len(data2)) / float(len(data2) - 1)
		
		plt.plot(dsorted, yvals)
		plt.plot(dsorted2, yvals2)
		plt.title(title)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.grid()
		
		#below here sets values for CDF stats printouts on the plots
		a  = []
		y = 0.35
		ydelim = 0.05
		#print(np.max(dsorted), "dsorted max")
		x = np.max([~np.isnan(dsorted)]) * 0.33
		#print(x,"x pos")
		for q in [50, 68, 95, 99.9]:

			a = (("{}% percentile: {}".format (q, np.percentile(dsorted, q))))
			y =  y - ydelim
			plt.text(x, y, a)

		plt.show()
