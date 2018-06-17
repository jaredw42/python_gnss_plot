#!/usr/bin/python3
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

"""
basic_plots.py - function definitions for basic plots from static datasets. 
	linear plots require x and y dataframes 
	cdf plots require 1D dataframe

	all plots take title, xlabel and ylabel as optional arguments

"""

def plot_linear(x,y, figname='fig', title='title', xlabel='nav', ylabel='',fw='fw'):
	plt.figure(figname)
	plt.plot(x,y,label=fw)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid()
	plt.legend(loc='upper right')

def plot_cdf(data,figname='fig', title='title', xlabel='Error', ylabel='Percent of Epochs',fw='fw'):
	"""
	plot_cdf - sorts values and plots CDF of a 1D dataframe the old fashioned way (percentile as y-axis)
	"""


	print(type(data), "input data type")
	#dsorted = np.sort(data[:].values)
	#print np.std(dsorted) 
	dsorted = np.sort(data)
	dsorted = dsorted[~np.isnan(dsorted)]
	print(type(dsorted), "type dsorted")
	yvals = np.arange(len(dsorted)) / float(len(dsorted) - 1)
	plt.figure(figname)
	plt.plot(dsorted, yvals,label=fw)
	plt.legend(loc='upper right')
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid()
	print(dsorted)
	print(len(dsorted))
	#below here sets values for CDF stats printouts on the plots
	a  = []
	y = 0.35
	ydelim = 0.05
	#print(np.max(dsorted), "dsorted max")
	x = np.max(dsorted) * 0.66
	#print(x,"x pos")
	for q in [50, 68, 95, 99.9]:
		a = (("{}% percentile: {:.2f}".format (q, np.percentile(dsorted, q))))
		y =  y - ydelim
		plt.text(x, y, a)
		#print a


def plot_cdf_num(data,figname='fig', title='title', xlabel='Error', ylabel='Number of Cycles',fw='fw'):
	"""
	plot_cdf_num - sorts values and plots CDF of values with y-axis of number of epochs or cycles (as opposed to percentile)
	"""
	dsorted = np.sort(data)
	dsorted = dsorted[~np.isnan(dsorted)]
	yvals = np.arange(len(dsorted))

	plt.figure(figname)
	plt.plot(dsorted, yvals,label=fw)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.grid()
	plt.legend(loc='upper right')
	x = np.max(dsorted) * 0.66

	y = np.max(yvals) * 0.4
	ydelim = 0.2 * y
	for q in [50, 68, 95, 99.9]:
	 	a = (("{}% percentile: {:.1f}".format (q, np.percentile(dsorted, q))))
	 	y =  y - ydelim
	 	plt.text(x, y, a)

def plot_overhead(x, y, title='overhead',xlabel= 'Error X',ylabel ='Error Y'):
	"""
	plot_overhead - seaborn jointplot - can be used for plotting north vs east error
	"""

	#plt.figure()
	s = sns.jointplot(x, y, kind="hex", color="#4CB391")
	s.set_axis_labels('E/W Error (m)' ,'N/S Error (m)')
	plt.title(title)
	#plt.xlabel(xlabel)
	#plt.ylabel(ylabel)

def plot_linear_by_diffmode(nav, title='Horizontal Error By Differential Mode', xlabel='nav', ylabel='Horiz Error (m)',fw='fw'):

	for diffmode in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]:
	#for diffmode in [0:20:1]:

		x = nav['Fix Mode'] == diffmode
		
		if any(np.isfinite(nav['2D Error [m]'] [x])):

			titledmode = "Diffmode: " + str(diffmode) #makes string of diff mode for the title block
			print("Plotting diffmode", diffmode)
			plt.figure()
			plt.plot(nav['TOW [s]'][x],nav['2D Error [m]'][x],label=fw)
			plt.title(str(title) + "\n" + titledmode)
			plt.xlabel(xlabel)
			plt.ylabel(ylabel)
			plt.legend(loc='upper right')
			plt.grid()

def plot_cdf_by_diffmode(nav, saveplots='0',savepath=os.getcwd() + "/", title="CDF Horizontal Error by Differential Mode", xlabel='Horiz Error (m)',ylabel='# Epochs in Diff mode: ',fw='fw'):

	for diffmode in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]:
	#for diffmode in [0:20:1]:


		x = nav['Fix Mode'] == diffmode
		figname = "figcdfhoriz_dMode_" + str(diffmode)
		if any(np.isfinite(nav['2D Error [m]'][x])):
			dsorted = np.sort(nav['2D Error [m]'][x])
			dsorted = dsorted[~np.isnan(dsorted)]
			yvals = np.arange(len(dsorted))

			plt.figure(figname)
			plt.plot(dsorted, yvals,label=fw)
			plt.legend(loc='upper right')

			tl = title + "\n Diffmode: " + str(diffmode)
			plt.title(tl)
			plt.xlabel(xlabel)
			yl = ylabel + str(diffmode)
			plt.ylabel(yl)
			plt.grid()
			x = np.max(dsorted) * 0.66

			y = np.max(yvals) * 0.4
			ydelim = 0.2 * y
			for q in [50, 68, 95, 99.9]:
			 	a = (("{}% percentile: {:.2f}".format (q, np.percentile(dsorted, q))))
			 	y =  y - ydelim
			 	plt.text(x, y, a)

			if saveplots == '1':
				savename = savepath + figname
				plt.savefig(savename)

def plot_overhead_by_diffmode(nav, title='overhead by diffmode: ',xlabel= 'Error X',ylabel ='Error Y'):
	"""
	plot_overhead - seaborn jointplot - can be used for plotting north vs east error
	"""

	for diffmode in [0,1,2,3,4,5,6,7,8,9]:

		x = nav['Fix Mode'] == diffmode

		if any(np.isfinite(nav['2D Error [m]'][x])):
			print("sns diffmode plot", str(diffmode))
			errN = nav['errN'][x]
			errE = nav['errE'][x]

			#plt.figure()
			s = sns.jointplot(errN, errE, kind="hex", color="#4CB391")
			s.set_axis_labels('E/W Error (m)' ,'N/S Error (m)')
			tl = title + str(diffmode)
			plt.title(tl)











