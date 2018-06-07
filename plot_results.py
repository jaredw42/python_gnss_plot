import matplotlib
matplotlib.use('TkAgg') 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import basic_plots as bp 
import re

#filepath = "/Volumes/data/data/PiksiMultiTesting/2018-06/04-gt1_rf5_v16prelim/DUT11/20180604-145701-lj11-t2-d24h-f4-RTK-RFOnOff-1-5s/"
filepath = "/Volumes/data/data/PiksiMultiTesting/2018-06/04-GT2_ST_v16prelim/DUT22/20180604-145653-lj22-t3-d24h-f4-RTK-Starts/"
filename = "nav.csv"

if re.search('Starts', filepath):
	starts = True
	rfonoff = False
	print 'starts dataset detetcted'
elif re.search('RFOnOff', filepath):
	starts = False
	rfonoff = True
	print 'rf-on-off dataset detected'

	

fullpath = filepath + filename

nav = pd.read_csv(fullpath)


"""
plot_results.py - plots results from gtt nav.csv and rf-on-off.csv or starts.csv file
uses basic_plots for plot functions 
	currently plots for all datasets: 
		figsats - sats in solution by time/epoch
		fighorizerror - 
		fighorizcdf - 
		figspherecdf - 

		for rf on/off and starts datasets:
			 fig ttrtkfix - 
			 fig ttrtkfloat - 
			 fig ttsbas - 
			 fig ttsps -

		for starts datasets:
			fig ttrtkfix_noboot - 
			fig ttrtkfloat_noboot - 
			fig ttsbas_noboot -
			fig ttsps_noboot - 


"""
t = nav['TOW [s]']
if np.max(t) < 604000:
	timelabel = "GPS TOW(s)"

else:
	print "near GPS week rollover, swiching to epoch on x axis"
	t = nav.index
	timelabel = "Epoch"


figsats = bp.plot_linear(t, nav['SVs Used'], title='Sats used by ' + timelabel, xlabel=timelabel, ylabel='Sats in Solution')
fighorizerror = bp.plot_linear(t, nav['2D Error [m]'], title='Horiz Error by '+ timelabel, xlabel=timelabel, ylabel='2D Error (m)')
fighorizcdf = bp.plot_cdf(nav['2D Error [m]'], title='CDF Horizontal Error', xlabel='2D Error (m)')
figspherecdf = bp.plot_cdf(nav['3D Error [m]'], title='CDF Spherical Error', xlabel='3D Error (m)')


if rfonoff == True:
	filename = "rf-on-off.csv"
	fullpath = filepath + filename

	rf = pd.read_csv(fullpath)
	print filename
	print rf.columns

elif starts == True:
	filename = "starts.csv"
	fullpath = filepath + filename

	rf = pd.read_csv(fullpath)
	print filename
	print rf.columns


figttrtkfix = bp.plot_cdf_num(rf['TT Fixed [s]'], title='CDF Time to RTK Fixed', xlabel='Seconds to RTK Fixed')
figttrtkfloat = bp.plot_cdf_num(rf['TT Float [s]'], title='CDF Time to RTK Float', xlabel='Seconds to RTK Float')
figttsps = bp.plot_cdf_num(rf['TT SPS [s]'], title='CDF Time to SPS Fixed', xlabel='Seconds to SPS Fixed')

try:
	figttsbas = bp.plot_cdf_num(rf['TT SBAS [s]'], title='CDF Time to SBAS Fixed', xlabel='Seconds to SBAS Fixed')
except:
	print "No SBAS data in: ", fullpath


"""
plot boot-independent ttfix stats (subtract boot times from ttf values)
these are sometimes helpful when a FW change noticable speeds up or slows down boot times

"""
if starts == True:
	boot = rf['TT Boot [s]']

	ttrtkfix_noboot = rf['TT Fixed [s]'] - boot
	ttrtkfloat_noboot = rf['TT Float [s]'] - boot
	ttsps_noboot = rf['TT SPS [s]'] - boot

	figttrtkfix_noboot = bp.plot_cdf_num(ttrtkfix_noboot, title='CDF Time to RTK Fixed \nw/Normalized Boot Times', xlabel='Seconds to RTK Fixed')
	figttrtkfloat_noboot = bp.plot_cdf_num(ttrtkfloat_noboot, title='CDF Time to RTK Float \nw/Normalized Boot Times', xlabel='Seconds to RTK Float')
	figttsps_noboot = bp.plot_cdf_num(ttsps_noboot, title='CDF Time to SPS Fixed \nw/Normalized Boot Times', xlabel='Seconds to SPS Fixed')

	try:
		ttsbas_noboot = rf['TT SBAS [s]'] - boot
		figttsbas_noboot = bp.plot_cdf_num(ttsbas_noboot, title='CDF Time to SBAS Fixed w/Normalized Boot Times', xlabel='Seconds to SBAS Fixed')
	except:
		print "no SBAS data in ", fullpath


"""
plot transitions between diff modes

"""

if starts == True:# | rfonoff == true:

	tflotofix = rf['TT Fixed [s]'] - rf ['TT Float [s]']
	figflotofix = bp.plot_cdf_num(tflotofix, title='Tranistion time by Cycle\n RTK Float to RTK Fixed', xlabel='Seconds to RTK Fixed')

	try:
		tsbastofloat = rf['TT Float [s]'] - rf['TT SBAS [s]']
		figsbastoflo  = bp.plot_cdf_num(tsbastofloat, title='Tranistion time by Cycle\nSBAS to RTK Float', xlabel='Seconds SBAS to RTK Float')
	except Exception as e:
		print "could not do sbas to rtk float transition calc"
		print e

	try:
		tspstosbas = rf['TT SBAS [s]'] - rf['TT SPS [s]']
		figsbastoflo  = bp.plot_cdf_num(tspstosbas, title='Tranistion time by Cycle\nSBAS to RTK Float', xlabel='Seconds SPS to SBAS')
	except Exception as e:
		print "could not do sps to sbas transistion calc"
		print e

	try:
		tspstofloat =  rf['TT Float [s]'] - rf['TT SPS [s]']
		figspstofloat = bp.plot_cdf_num(tspstosbas, title='Tranistion time by Cycle\nSBAS to RTK Float', xlabel='Seconds SPS to RTK Float')
	except:
		print "could not do sps to rtk float tranistion calc"





#raw_input()
plt.show()


