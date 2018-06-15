#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import pymap3d as pm
import basic_plots as bp
import matplotlib.pyplot as plt

#class magicdataanalyzer():

def calc_LLH2NED(*args):

	for value in args:

		nav = value
		#print(nav)
		refLat = 37.77101988
		refLon = -122.40315123
		refAlt = -5.612

		errN, errE, errD = pm.geodetic2ned(nav['Lat [deg]'], nav['Lon [deg]'], nav['Alt Ellips [m]'],
											refLat, refLon, refAlt)

		return([errN, errE, errD])

def calc_drift(*args,**kwargs):

	for key, value in kwargs.items():
		tdiff = int(value)

	for data in args:
		#print(type(data))

		#a = 0
		#drift = pd.Series()
		#d=data.rolling(window=900).apply(lambda x: x[-1] - x[0])
		df = pd.DataFrame(data)
		d = df.iloc[900:] - df.iloc[:-900].values
		#x = data[9000:] - data[:-9000]
		#print(d)
		#print(data)
		#print(d)

		return(d)
	

	
