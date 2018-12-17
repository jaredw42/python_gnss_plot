#!/usr/local/bin/python3
import os 
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
        #refLat = -35.360799697
        #refLon = 149.207155405
        #refAlt = 638.635

        refLat = -35.36081064
        refLon = 149.20715053
        refAlt = 638.598        

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
    rptpath = os.path.join(filepath, "report.txt")

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

            elif re.match('GNSS', line):
                d = line.split(' ')
                print(d, 'GNSS prot D')
                md['device'] = d[-4]

    return(md)

def get_soln_rate(fp):
    csvpath = os.path.join(str(fp),'nav.csv')
    nav = pd.read_csv(csvpath)

    """
    trims [TOW [s]] to finite values then compares the 100th and 101st array values to calculate the navigation rate
    """
    print(nav)
    print(nav['TOW [s]'])
    x = nav['TOW [s]'][np.isfinite(nav['TOW [s]'])]

    try:
        navrate = 1 / (x[101].data - x[100].data)
    except:
        navrate = 1 / (x.iloc[101] - x.iloc[100])

    solnrate = '{:.2f}'.format(navrate)
    
    print('{} Hz soln rate'.format(solnrate))
    return(solnrate)

def calc_nobootstats(starts):

    for var in starts.data_vars:

        if re.match('^TT', var):
            varname = '{} - noboot'.format(var)
            starts[varname] = starts[var] - starts['TT Boot [s]']

    return(starts)
    

    
