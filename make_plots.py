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

    def make_plots(nav):

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
        fig1.text(figsize[0] * 0.5, figsize[1]*0.5, 'Horizontal error vs time')
        for i, navdata in enumerate(nav):
            print(navdata.attrs['fw'])
            print(type(nav))
            ax = plt.subplot(sbplnum, 1, 1+i)
            ax.plot(navdata['TOW [s]'], navdata['2D Error [m]'],label=navdata.attrs['fw'])

            ax.grid()
            ax.legend()
            ax.set_ylabel('Horiz Error (m)')
            ax.set_xlabel(timelabel)

        
        


        fig2 = plt.figure(figsize=cdfsize)
        """"
        fig 2 - 2D error CDF 
        """
        ax = plt.subplot(1,1,1)
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
        plt.title('CDF Horizontal Error (m)')
        print(dsorted)
        print(len(dsorted))


        fig3 = plt.figure(figsize=figsize)
        """
        figure 3 - sats by time 
        creates subplots for each dataset
        """
        for i, navdata in enumerate(nav):
            ax = plt.subplot(sbplnum, 1, (i+1))

            ax.plot(navdata['TOW [s]'], navdata['SVs Used'], label=navdata.attrs['fw'])
            ax.grid()
            ax.legend()
            ax.set_xlabel(timelabel)
            ax.set_ylabel('Sats in Sol''n')


        plt.text(figsize[0] * 0.5, figsize[1]*0.1, 'Satellites Used in Solution')


        plt.show()







