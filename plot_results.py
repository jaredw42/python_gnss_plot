#!/usr/local/bin/python3
import matplotlib
matplotlib.use('TkAgg') 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import basic_plots as bp 
import compare_plots as cp
import re
import gc
import pymap3d as pm

class plot_results():


	"""
	plot_results - gets called from start_plots.  needs 4 args to start
	filepath, then args for plotnormalizedboot, plottransistions, plotbydiffmode
	set args to "1" to evaluate
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

			for normalized boot datasets:
				fig ttrtkfix_noboot - 
				fig ttrtkfloat_noboot - 
				fig ttsbas_noboot -
				fig ttsps_noboot - 

	"""


	def plot_individual(self, args):
		print(args)
		filepath = args[0]
		plotnormalizedboot = args[1]
		plottransitions = args[2]
		plotbydiffmode = args[3]
		saveplots = args[4]

		filename = "nav.csv"
		starts = False
		rfonoff = False
		
		

		if re.search('Starts', filepath):
			starts = True
			rfonoff = False
			print('starts dataset detetcted')
		elif re.search('RFOnOff', filepath):
			starts = False
			rfonoff = True
			print('rf-on-off dataset detected')
		else:
			starts= False
			rfonoff=False
			print("no rfonoff or starts data detected")

			

		fullpath = filepath + filename

		print("loading csv: ", fullpath)
		nav = pd.read_csv(fullpath)
		print('nav.csv loaded')

		
		try:
			t = nav['TOW [s]']
		except:
			t = nav['GPS TOW [s]']
		if np.max(t) < 604000:
			timelabel = "GPS TOW(s)"

		else:
			print("near GPS week rollover, swiching to epoch on x axis")
			t = nav.index
			timelabel = "Epoch"

		refLat = 37.77101988
		refLon = -122.40315123
		refAlt = -5.612

		errN, errE, errD = pm.geodetic2ned(nav['Lat [deg]'], nav['Lon [deg]'], nav['Alt Ellips [m]'],
											refLat, refLon, refAlt)
		nav['errN'] = errN
		nav['errE'] = errE
		nav['errD'] = errD

		figsats = bp.plot_linear(t, nav['SVs Used'],figname='figsats', title='Sats used by ' + timelabel, xlabel=timelabel, ylabel='Sats in Solution')
		fighorizerror = bp.plot_linear(t, nav['2D Error [m]'],figname='fighorizerror',  title='Horiz Error by '+ timelabel, xlabel=timelabel, ylabel='2D Error (m)')
		print("horiz err cdf below")
		fighorizcdf = bp.plot_cdf(nav['2D Error [m]'],figname='fighorizcdf', title='CDF Horizontal Error', xlabel='2D Error (m)')
		print("spherical cdf below")
		figspherecdf = bp.plot_cdf(nav['3D Error [m]'], figname='figspherecdf',title='CDF Spherical Error', xlabel='3D Error (m)')
		figoverhead = bp.plot_overhead(errN, errE, title='Overhead Plot\nNorth vs East', xlabel="Error E/W (m)", ylabel='Error N/S (m)')

		if rfonoff == True:
			filename = "rf-on-off.csv"
			fullpath = filepath + filename
			print("loading csv: ", fullpath)
			rf = pd.read_csv(fullpath)
			
		elif starts == True:
			filename = "starts.csv"
			fullpath = filepath + filename
			print("loading csv: ", fullpath)
			rf = pd.read_csv(fullpath)

		if rfonoff == True or starts == True:

			figttrtkfix = bp.plot_cdf_num(rf['TT Fixed [s]'],figname='figttrtkfix' ,title='CDF Time to RTK Fixed', xlabel='Seconds to RTK Fixed')
			figttrtkfloat = bp.plot_cdf_num(rf['TT Float [s]'],figname='figttrtkfloat', title='CDF Time to RTK Float', xlabel='Seconds to RTK Float')
			figttsps = bp.plot_cdf_num(rf['TT SPS [s]'],figname='figttsps', title='CDF Time to SPS Fixed', xlabel='Seconds to SPS Fixed')

			try:
				figttsbas = bp.plot_cdf_num(rf['TT SBAS [s]'], figname='figttsbas', title='CDF Time to SBAS Fixed', xlabel='Seconds to SBAS Fixed')
			except:
				print("No SBAS data in: ", fullpath)


		"""
		plot boot-independent ttfix stats (subtract boot times from ttf values)
		these are sometimes helpful when a FW change noticablly speeds up or slows down boot times

		"""
		if plotnormalizedboot == '1':
			print("plotting fix times with normalized boot stats (TTFix - TTBoot)")
			boot = rf['TT Boot [s]']

			ttrtkfix_noboot = rf['TT Fixed [s]'] - boot
			ttrtkfloat_noboot = rf['TT Float [s]'] - boot
			ttsps_noboot = rf['TT SPS [s]'] - boot

			figttrtkfix_noboot = bp.plot_cdf_num(ttrtkfix_noboot, figname='figttrtkfix_noboot', title='CDF Time to RTK Fixed \nw/Normalized Boot Times', xlabel='Seconds to RTK Fixed')
			figttrtkfloat_noboot = bp.plot_cdf_num(ttrtkfloat_noboot,figname='figttrtkfloat_noboot', title='CDF Time to RTK Float \nw/Normalized Boot Times', xlabel='Seconds to RTK Float')
			figttsps_noboot = bp.plot_cdf_num(ttsps_noboot,figname='figttsps_noboot', title='CDF Time to SPS Fixed \nw/Normalized Boot Times', xlabel='Seconds to SPS Fixed')

			try:
				ttsbas_noboot = rf['TT SBAS [s]'] - boot
				figttsbas_noboot = bp.plot_cdf_num(ttsbas_noboot,figname='figttsbas_noboot', title='CDF Time to SBAS Fixed w/Normalized Boot Times', xlabel='Seconds to SBAS Fixed')
			except:
				print("no SBAS data in ", fullpath)


		"""
		plot transitions between diff modes

		"""

		if plottransitions == '1':
			print("plotting diffmode transition")

			tflotofix = rf['TT Fixed [s]'] - rf ['TT Float [s]']
			figflotofix = bp.plot_cdf_num(tflotofix,figname='figflotofix', title='Transition time by Cycle\n RTK Float to RTK Fixed', xlabel='Seconds to RTK Fixed')

			try:
				tsbastofloat = rf['TT Float [s]'] - rf['TT SBAS [s]']
				figsbastoflo  = bp.plot_cdf_num(tsbastofloat, figname='figsbastoflo', title='Transition time by Cycle\nSBAS to RTK Float', xlabel='Seconds SBAS to RTK Float')
			except Exception as e:
				print("could not do sbas to rtk float transition calc")
				print(e)

			try:
				tspstosbas = rf['TT SBAS [s]'] - rf['TT SPS [s]']
				figspstosbas  = bp.plot_cdf_num(tspstosbas, figname='figspstosbas',title='Transition time by Cycle\nSBAS to RTK Float', xlabel='Seconds SPS to SBAS')
			except Exception as e:
				print("could not do sps to sbas transistion calc")
				print(e)

			try:
				tspstofloat =  rf['TT Float [s]'] - rf['TT SPS [s]']
				figspstofloat = bp.plot_cdf_num(tspstofloat,figname='figspstofloat', title='Transition time by Cycle\nSPS to RTK Float', xlabel='Seconds SPS to RTK Float')
			except Exception as e:
				print("could not do sps to rtk float tranistion calc")
				print(e)

		 
		"""
		plot error by diff mode 

		"""
		if plotbydiffmode == '1':
			fgsbydiffmode = bp.plot_linear_by_diffmode(nav,xlabel=timelabel)
			fgscdfbydiffmode = bp.plot_cdf_by_diffmode(nav,saveplots=saveplots, savepath=filepath)
			fgsovdbydiffmode = bp.plot_overhead_by_diffmode(nav)


		if saveplots == '1':
			d = dir()
			fig = 'fig'

			regex = re.compile(fig)
			selected_vars = filter(regex.search,d)
			for var in selected_vars:
				print(var)
				plt.figure(var)
				savename = filepath + var
				plt.savefig(savename)



		plt.show()

	def plot_comparative(self,args):
		filepath = args[0]
		filepath2 = args[1]
		plotnormalizedboot = args[2]
		plottransitions = args[3]
		plotbydiffmode = args[4]
		saveplots = args[5]

		filename = "nav.csv"
		starts = False
		rfonoff = False
		
		

		if re.search('Starts', filepath):
			starts = True
			rfonoff = False
			print('starts dataset detetcted')
		elif re.search('RFOnOff', filepath):
			starts = False
			rfonoff = True
			print('rf-on-off dataset detected')
		else:
			starts= False
			rfonoff=False
			print("no rfonoff or starts data detected")

		fullpath = filepath + filename
		fullpath2 = filepath2 + filename
		print(filepath2)
		print(fullpath2)
		print("loading csv: ", fullpath)
		nav = pd.read_csv(fullpath)
		nav2 = pd.read_csv(fullpath2)
		print('nav.csvs loaded')

		err1 = nav['2D Error [m]']
		err2 = nav2['2D Error [m]']
		figcdfhoriz = cp.plot_cdf(err1=err1, err2=err2, figname='figcdfhoriz')


