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
import os
import pymap3d as pm
import magicdataanalyzer as mda

"""
header of nav.csv:
Cycle,UTC,RF On,Corr On,LLA Msg,LLA Msg Time [s],Week,TOW [s],Fix Mode,SVs Used,Lat [deg],Lon [deg],Alt Ellips [m],SOG [m/s],Vert Vel [m/s],COG [deg],Hdg [deg],HDOP,PDOP,EHPE [m],EVPE [m],2D Error [m],Alt Error [m],3D Error [m],Baseline 2D [m],Baseline 3D [m],Baseline 2D Error [m],Baseline 3D Error [m],Hdg Error [deg],Delta LLA Time [s],Error Info

"""

class mkp():

    def plot_nav(nav):

        saveplots = True 

        #set save path for plots
        fp = nav[0].attrs['filepath']
        fplist= fp.split('/')

        x = fp.find('DUT')
        savepath = fp[0:x] + "plots/"

        try:
            os.mkdir(savepath)
        except:
            print('could not make plots folder')

        # set number of subplots by number of datasets analyzed
        sbplnum = (len(nav))
        print(sbplnum)
        
        """
        this section tries two common ways of describing the GPS TOW in the header and also checks
        if it is near the GPS week rollover.  If so, it just uses index of the array for the x axis

        """

        rawdate = str(nav[0]['UTC'][0].data)
        tdate = rawdate.split('T')[0]

        print(tdate,'rawdate')

        figsize = [12, sbplnum * 3]
        cdfsize = [12, 9]
      
        fig1 = plt.figure(figsize=figsize)
        maxy = 0.01
        for i, navdata in enumerate(nav):

        #set x-axis smartly (gps time or epoch if near gps rollover)
            try:
                t = navdata['TOW [s]']
            except:
                t = navdata['GPS TOW [s]']
                navdata['GPS TOW [s]'] = navdata['TOW [s]']

            if np.max(t) < 604000:
                timelabel = "GPS TOW(s)"

            else:
                print("near GPS week rollover, swiching to epoch on x axis")

                t = navdata.coords['index']
                timelabel = "Epoch"

            #set subplot ylimits
            if maxy < np.max(navdata['2D Error [m]']):
                maxy = np.max(navdata['2D Error [m]'])


            ax = plt.subplot(sbplnum, 1, 1+i)
            ax.plot(t, navdata['2D Error [m]'],label=navdata.attrs['fw'])

            ax.grid()
            ax.legend()
            ax.set_ylabel('Horiz Error (m)')
            ax.set_ylim(0,maxy)

            if i ==0:

                tlname = 'GTT ' + navdata.attrs['testname']
                tlsoln = '\nSolution rate: ' + navdata.attrs['solnrate'].rstrip() + 'Hz  Date: ' + tdate
                tl = tlname + tlsoln + '\nHorizontal error vs time'
                plt.title(tl)
            elif i == (sbplnum -1 ):

                solnrate = navdata.attrs['solnrate'].split('.')
                solnrate = solnrate[0]
                print(solnrate, 'solnrate')

                ax.set_xlabel(timelabel)
                savename = (tdate.strip('-') + "_" + navdata.attrs['solnrate'].rstrip('.0') + "Hz_" + 
                    navdata.attrs['testname'].strip() + '_err2D_linear')
                savename = savename.replace("-", "")
                sp = savepath + savename
                print(sp)
                plt.savefig(sp)


        diffmodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]

        for dm in diffmodes:

            fig = plt.figure(figsize = cdfsize)
            ax = plt.subplot(1,1,1)
            a = []
            b = np.zeros([2,4])
            cdfwithtxt = []
            cdf = []
            flagcdf = False 

            for i, navdata in enumerate(nav):

                d = navdata.where(navdata['Fix Mode'] == dm)
                plotdata = np.sort(d['2D Error [m]'])
                if any(np.isfinite(plotdata)):
                        
                    plotdata = plotdata[~np.isnan(plotdata)]
                    yvals = np.arange(len(plotdata)) /float(len(plotdata) - 1)
                    ax.plot(plotdata, yvals,label=navdata.attrs['fw'])

                    # find percentile values and add to plot

                    for q in [50, 68, 95, 99]:

                        if flagcdf == False:
                            cdfwithtxt.append(("{}% percentile: {:.2f}".format (q, np.percentile(plotdata, q))))
                            
                        else:
                            cdf.append(("{:.2f}".format (np.percentile(plotdata, q))))

                    flagcdf = True

            ax = plt.gca()
            if len(ax.lines) > 0:


                ax.legend()
                ax.grid()
                x = np.median(plotdata)
                y = np.median(yvals)

                xmin, xmax = ax.get_xlim()
                ymin, ymax = ax.get_ylim()

                ypos = ymax * 0.3
                xpos = xmax * 0.6
                print(a)
                if sbplnum > 2:
                    cdf = np.reshape(cdf,[4,-1])

                try:
                    cdfdata = np.column_stack([cdfwithtxt, cdf])
                except:
                    cdfdata = np.reshape(cdfwithtxt ,[4,-1])

                plt.text(xpos, ypos, cdfdata)
                ax.set_xlabel('Horizontal Error (m) - Diffmode: ' + str(dm))
                ax.set_ylabel('Percent of Epochs')
                tlname = 'GTT ' + navdata.attrs['testname']
                tlsoln = '\nSolution rate: ' + navdata.attrs['solnrate'].rstrip() + 'Hz  Date: ' + tdate
                tl = tlname + tlsoln + '\n CDF Horizontal Error for Diff Mode: ' + str(dm)
                plt.title(tl)

                solnrate = navdata.attrs['solnrate'].split('.')
                solnrate = solnrate[0]

                savename = (tdate + "_" + solnrate + "Hz_" + 
                    navdata.attrs['testname'] + '_CDF_err2D_DM_{}'.format(dm))

                savename = savename.replace("-", "")
                sp = savepath + savename
                print(sp,)
                plt.savefig(sp)
                

            else:
                plt.close(fig)               

        #cycles = [1,2,3,7,89, 63,1274]
        cycles = []
        
        for cyc in cycles:

            fig = plt.figure(figsize = cdfsize)

            for i, navdata in enumerate(nav):

                ax = plt.subplot(sbplnum,1,1+i)

                d = navdata.where(navdata['Cycle'] == cyc)

                ax.scatter(d['TOW [s]'],d['Fix Mode'],label=navdata.attrs['fw'])

                if i ==0:
                    tl = 'GTT Static Dataset\n Diff Mode during cycle\n Cycle: ' + str(cyc)
                    plt.title(tl)
                #elif i == sbplnum:
                ax.set_xlabel('Diffmode - Cycle ' + str(cyc))

                ax.legend()
                ax.grid()
                ax.set_ylabel('Diffmode')




    def plot_rf(rf):

        print(rf)

        sbplnum = len(rf)
        print(sbplnum, 'len rf')

        saveplots = True 
        rawdate = str(rf[0]['Start UTC'][0].data)
        tdate = rawdate.split('T')[0]


        #set save path for plots
        fp = rf[0].attrs['filepath']
        fplist= fp.split('/')

        x = fp.find('DUT')
        savepath = fp[0:x] + "plots/"

        try:
            os.mkdir(savepath)
        except:
            print('could not make plots folder')

        cdfsize = [12,9]
        ttplotmetrics = []

        #create list of TT ___ [s] from the data variables and create
        #plots for these metrics 
        for var in rf[0].data_vars:
            if re.match('^TT', var):
                ttplotmetrics.append(var)

        for plotmetric in ttplotmetrics:
            print(plotmetric)

            plt.figure(figsize=cdfsize)

            ax = plt.subplot(1,1,1)
            flagcdf = False  
            cdfwithtxt = []
            cdf = [] 

            for i, rfdata in enumerate(rf):
                plotdata = np.sort(rfdata[plotmetric])

                if any(np.isfinite(plotdata)):
                    plotdata = plotdata[~np.isnan(plotdata)]
                    yvals = np.arange(len(plotdata))# /float(len(plotmetric) - 1)
                    ax.plot(plotdata, yvals,label=rfdata.attrs['fw'])


                    for q in [50, 68, 95, 99]:

                        if flagcdf == False:
                            cdfwithtxt.append(("{}% percentile: {:.2f}".format (q, np.percentile(plotdata, q))))
                            
                        else:
                            cdf.append(("{:.2f}".format (np.percentile(plotdata, q))))

                    flagcdf = True

                ax = plt.gca()
            if len(ax.lines) > 0:


                ax.legend()
                ax.grid()

                xmin, xmax = ax.get_xlim()
                ymin, ymax = ax.get_ylim()

                ypos = ymax * 0.3
                xpos = xmax * 0.6
                if sbplnum > 2:
                    cdf = np.reshape(cdf,[4,-1])

                try:
                    cdfdata = np.column_stack([cdfwithtxt, cdf])
                except:
                    cdfdata = np.reshape(cdfwithtxt ,[4,-1])

                plt.text(xpos, ypos, cdfdata)
                ax.set_xlabel(str(plotmetric))
                ax.set_ylabel('Number of Cycles')
                tlname = 'GTT ' + rfdata.attrs['testname']
                tlsoln = '\nSolution rate: ' + rfdata.attrs['solnrate'].rstrip() + 'Hz  Date: ' + tdate
                tl = tlname + tlsoln + '\n CDF ' + str(plotmetric) 
                plt.title(tl)

                solnrate = rfdata.attrs['solnrate'].split('.')
                solnrate = solnrate[0]

                sn = str(plotmetric).replace(" ", "")
                savename = (tdate + "_" + solnrate + "Hz_" + 
                    rfdata.attrs['testname'] + '_CDF_' + sn)

                savename = savename.replace("-", "")
                sp = savepath + savename
                print(sp)
                plt.savefig(sp)
                

            else:
                plt.close(fig)               


        
        








