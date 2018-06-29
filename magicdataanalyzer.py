#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import pymap3d as pm
import basic_plots as bp
import matplotlib.pyplot as plt
import re

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

		df = pd.DataFrame(data)
		d = df.iloc[900:] - df.iloc[:-900].values

		return(d)

def get_metadata(*args):

    filepath = args[0]

    rptpath = filepath + "report.txt"

    #antre = re.compose('Antenna')
    md = {}

    with open(rptpath) as rp:
        for line in rp:
            if re.match('Antenna', line):
                d = line.split(' ')

                md['refAlt'] = d[-2]
                md['refLon'] = d[-4]
                md['refLat'] = d[-6]

            elif re.match('Firmware Version', line):

                d = line.split(':')

                md['FWversion'] = d[-1].strip()

            elif re.match('Name', line):
            	d = line.split(':')

            	md['testname'] = d[-1].strip()

    return(md)

def get_soln_rate(nav):

	"""
	trims [TOW [s]] to finite values then compares the 100th and 101st array values to calculate the navigation rate
	"""
	x = nav['TOW [s]'][np.isfinite(nav['TOW [s]'])]

	#print(x)

	try:
		navrate = 1 / (x[101].data - x[100].data)
	except:
		navrate = 1 / (x.iloc[101] - x.iloc[100])
		#pass
	solnrate = '{:.2f}'.format(navrate)
	
	print(solnrate)
	return(solnrate)




	

	
