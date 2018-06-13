#!/usr/local/bin/python3
import numpy as np
import pandas as pd
import pymap3d as pm

#class magicdataanalyzer():

def calcLLH2NED(*args):

	#nav = 
	refLat = 37.77101988
	refLon = -122.40315123
	refAlt = -5.612

	errN, errE, errD = pm.geodetic2ned(nav['Lat [deg]'], nav['Lon [deg]'], nav['Alt Ellips [m]'],
									refLat, refLon, refAlt)
	# nav['errN'] = errN
	# nav['errE'] = errE
	# nav['errD'] = errD