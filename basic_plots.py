import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
basic_plots.py - function definitions for basic plots from static datasets. 
	linear plots require x and y dataframes 
	cdf plots require 1D dataframe

	all plots take title, xlabel and ylabel as optional arguments

"""

def plot_linear(x,y, title='title', xlabel='nav', ylabel=''):
	plt.figure()
	plt.plot(x,y)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid()

def plot_cdf(data, title='title', xlabel='Error', ylabel='Percent of Epochs'):
	"""
	plot_cdf - sorts values and plots CDF of a 1D dataframe the old fashioned way (percentile as y-axis)
	"""


	
	dsorted = np.sort(data)
	#print np.std(dsorted) 
	yvals = np.arange(len(data)) / float(len(data) - 1)
	plt.figure()
	plt.plot(dsorted, yvals)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid()

def plot_cdf_num(data, title='title', xlabel='Error', ylabel='Number of Cycles'):
	"""
	plot_cdf_num - sorts values and plots CDF of values with y-axis of number of epochs or cycles (as opposed to percentile)
	"""
	dsorted = np.sort(data)
	print np.std(dsorted,ddof=3)
	yvals = np.arange(len(data))

	plt.figure()
	plt.plot(dsorted, yvals)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid()

