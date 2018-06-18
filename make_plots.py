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
import magicdataanalyzer as mda

"""
header of nav.csv:
Cycle,UTC,RF On,Corr On,LLA Msg,LLA Msg Time [s],Week,TOW [s],Fix Mode,SVs Used,Lat [deg],Lon [deg],Alt Ellips [m],SOG [m/s],Vert Vel [m/s],COG [deg],Hdg [deg],HDOP,PDOP,EHPE [m],EVPE [m],2D Error [m],Alt Error [m],3D Error [m],Baseline 2D [m],Baseline 3D [m],Baseline 2D Error [m],Baseline 3D Error [m],Hdg Error [deg],Delta LLA Time [s],Error Info

"""

class mkp():

    def plot_nav(nav):

        saveplots = True 

        savepath = "/Users/jwilson/SwiftNav/dev/gnss_plot/"

        sbplnum = (len(nav)) # sets number of subplots by number of datasets analyzed
        
        """
        this section tries two common ways of describing the GPS TOW in the header and also checks
        if it is near the GPS week rollover.  If so, it just uses index of the array for the x axis

        """

        navdata = nav[0]

        try:
            t = navdata['TOW [s]']
        except:
            t = navdata['GPS TOW [s]']
            navdata['GPS TOW [s]'] = navdata['TOW [s]']

        if np.max(t) < 604000:
            timelabel = "GPS TOW(s)"

        else:
            print("near GPS week rollover, swiching to epoch on x axis")
            t = navdata.index
            timelabel = "Epoch"


        figsize = [15, sbplnum * 4]
        cdfsize = [15, 12]
                
        fig1 = plt.figure(figsize=figsize)
        for i, navdata in enumerate(nav):
            print(navdata.attrs['fw'])
            print(type(nav))
            ax = plt.subplot(sbplnum, 1, 1+i)
            ax.plot(navdata['TOW [s]'], navdata['2D Error [m]'],label=navdata.attrs['fw'])

            ax.grid()
            ax.legend()
            ax.set_ylabel('Horiz Error (m)')
            ax.set_xlabel(timelabel)

            if i ==0:
                tl = 'Horizontal error vs time'
                plt.title(tl)



        
        


        fig2 = plt.figure()#figsize=cdfsize
        """"
        fig 2 - 2D error CDF 
        """
        ax = plt.subplot(1,1,1)
       # ax.title('CDF Horizontal Error')
        print(type(nav))

        for i, navdata in enumerate(nav):
            print(type(nav))
            data = navdata['2D Error [m]']

            dsorted = np.sort(data)
            dsorted = dsorted[~np.isnan(dsorted)]

            print(type(dsorted), "type dsorted")

            yvals = np.arange(len(dsorted)) / float(len(dsorted) - 1)
            ax.plot(dsorted, yvals, label=navdata.attrs['fw'])
        ax.legend(loc='right')
        ax.set_xlabel('Horizontal Error (m)')
        ax.set_ylabel('Percent of Epochs')

        plt.grid()
       # ax.title('CDF Horizontal Error (m)')


        print(dsorted)
        print(len(dsorted))


        
        """
        figure 3 - sats by time 
        creates subplots for each datase
        """
        fig3 = plt.figure(figsize=figsize)
        for i, navdata in enumerate(nav):
            ax = plt.subplot(sbplnum, 1, (i+1))

            ax.plot(navdata['TOW [s]'], navdata['SVs Used'], label=navdata.attrs['fw'])
            ax.grid()
            ax.legend()
            ax.set_xlabel(timelabel)
            ax.set_ylabel('Sats in Sol''n')

            if i == 0:
                plt.title('Satellites Used in Solution')


        """
        calc horiz and 3d error stats
        calc 15- minute drift stats 

        # """

       # for i, navdata in enumerate(nav):

            #errN, errE, errD = mda.calc_navLLH2NED(navdata)
            #errHoriz = (errN**2 + errE ** 2 )** 0.5
           # errSphere = (errN**2 + errE ** 2 + errD)** 0.5

        #    err15N, err15E, err15D = mda.calc_drift(errN, errE, errD)

        #    print(err15N)



        """ 
        figure 4 - linear 15-minute drift plot  


        """
     #   fig4 = plt.figure(figsize=figsize)


        fig5 = plt.figure(figsize=cdfsize)


        ax = plt.subplot(1,1,1)

        for i, navdata in enumerate(nav):

            d = navdata.where(navdata['Fix Mode'] == 4)

            ax.plot(d['TOW [s]'], d['2D Error [m]'],label=navdata.attrs['fw'])
        
        ax.grid()
        ax.legend()
        ax.set_ylabel('Horiz Error (m)')
        ax.set_xlabel('GPS TOW (s)')

        plt.title('Horizontal Error by time - RTK Fixed Epochs Only')


        fig6 = plt.figure(figsize=cdfsize)

        ax = plt.subplot(1,1,1)

        for i, navdata in enumerate(nav):
            d = navdata.where(navdata['Fix Mode'] == 4)
            dsorted = np.sort(d['2D Error [m]'])
            yvals = np.arange(len(dsorted)) / float(len(dsorted) - 1)
            ax.plot(dsorted, yvals,label=navdata.attrs['fw'])

        ax.legend()
        ax.grid()
        ax.set_xlabel('RTK Fixed - Horizontal Error (m)')
        ax.set_ylabel('Percent of Epochs')
        plt.title('CDF Horizontal Error by Diff Mode \nDiff Mode: RTK Fixed')


        fig7 = plt.figure(figsize=cdfsize)


        ax = plt.subplot(1,1,1)

        for i, navdata in enumerate(nav):

            d = navdata.where(navdata['Fix Mode'] == 3)

            ax.plot(d['TOW [s]'], d['2D Error [m]'],label=navdata.attrs['fw'])
        
        ax.grid()
        ax.legend()
        ax.set_ylabel('Horiz Error (m)')
        ax.set_xlabel('GPS TOW (s)')

        plt.title('Horizontal Error by time - RTK Float Epochs Only')


        fig8 = plt.figure(figsize=cdfsize)

        ax = plt.subplot(1,1,1)

        for i, navdata in enumerate(nav):
            d = navdata.where(navdata['Fix Mode'] == 3)
            dsorted = np.sort(d['2D Error [m]'])
            yvals = np.arange(len(dsorted)) /float(len(dsorted) - 1)
            ax.plot(dsorted, yvals,label=navdata.attrs['fw'])

        ax.legend()
        ax.grid()
        ax.set_xlabel('RTK Float - Horizontal Error (m)')
        ax.set_ylabel('Percent of Epochs')
        plt.title('CDF Horizontal Error by Diff Mode \nDiff Mode: RTK Float')



    plt.show()






    def plot_rf(rf):

        saveplots = True 

        savepath = "/Users/jwilson/SwiftNav/dev/gnss_plot/"


        cdfsize = [15,12]

        
        fig10 = plt.figure(figsize=cdfsize)

        ax = plt.subplot(1,1,1)

        for i, rfdata in enumerate(rf):

            ttrtkfixsorted = np.sort(rfdata['TT Fixed [s]'])

           # dsorted = dsorted[~np.isnan(dsorted)]
            yvals = np.arange(len(ttrtkfixsorted)) 
            ax.plot(ttrtkfixsorted, yvals,label=rfdata.attrs['fw'])
        ax.grid()
        ax.legend()
        ax.set_xlabel('Time to RTK Fixed (s)')
        ax.set_ylabel('Number of Cycles')

        tl = "CDF Time to RTK Fixed"
        plt.title(tl)
        fig10.savefig(savepath + 'CDF_TTFixed.png',format='png')
       # ax.set_ylimit()

        
        fig11 = plt.figure(figsize=cdfsize)

        ax = plt.subplot(1,1,1)

        for i, rfdata in enumerate(rf):

            rtkfloatsorted = np.sort(rfdata['TT Float [s]'])

           # dsorted = dsorted[~np.isnan(dsorted)]
            yvals = np.arange(len(rtkfloatsorted))
            ax.plot(rtkfloatsorted, yvals, label=rfdata.attrs['fw'])

        #ax.title('Time to RTK Float (s)')
        ax.grid()
        ax.legend()
        ax.set_xlabel('Time to RTK Float (s)')
        ax.set_ylabel('Number of Cycles')
        tl = 'CDF Time to RTK Float '
        plt.title(tl)

        fig11.savefig(savepath + 'CDF_TTFloat.png',format='png')
        






        plt.show()














