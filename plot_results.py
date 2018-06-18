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


    def plot_individual(args):
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

    #    rptpath = filepath + "report.txt"

        print("getting metadata")
        md = plot_results.get_metadata(filepath)


        
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

        # refLat = 37.77101988
        # refLon = -122.40315123
        # refAlt = -5.612

        # errN, errE, errD = pm.geodetic2ned(nav['Lat [deg]'], nav['Lon [deg]'], nav['Alt Ellips [m]'],
        #                                     refLat, refLon, refAlt)
        # nav['errN'] = errN
        # nav['errE'] = errE
        # nav['errD'] = errD

        errN, errE, errD = mda.calc_LLH2NED(nav)

        fw = md['FWversion']
        figsats = bp.plot_linear(t, nav['SVs Used'],figname='figsats', title='Sats used by ' + timelabel, xlabel=timelabel, ylabel='Sats in Solution',fw=fw)
        fighorizerror = bp.plot_linear(t, nav['2D Error [m]'],figname='fighorizerror',  title='Horiz Error by '+ timelabel, xlabel=timelabel, ylabel='2D Error (m)',fw=fw)
        print("horiz err cdf below")
        fighorizcdf = bp.plot_cdf(nav['2D Error [m]'],figname='fighorizcdf', title='CDF Horizontal Error', xlabel='2D Error (m)',fw=fw)
        print("spherical cdf below")
        figspherecdf = bp.plot_cdf(nav['3D Error [m]'], figname='figspherecdf',title='CDF Spherical Error', xlabel='3D Error (m)',fw=fw)
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

            figttrtkfix = bp.plot_cdf_num(rf['TT Fixed [s]'],figname='figttrtkfix' ,title='CDF Time to RTK Fixed', xlabel='Seconds to RTK Fixed',fw=fw)
            figttrtkfloat = bp.plot_cdf_num(rf['TT Float [s]'],figname='figttrtkfloat', title='CDF Time to RTK Float', xlabel='Seconds to RTK Float',fw=fw)
            figttsps = bp.plot_cdf_num(rf['TT SPS [s]'],figname='figttsps', title='CDF Time to SPS Fixed', xlabel='Seconds to SPS Fixed',fw=fw)

            try:
                figttsbas = bp.plot_cdf_num(rf['TT SBAS [s]'], figname='figttsbas', title='CDF Time to SBAS Fixed', xlabel='Seconds to SBAS Fixed',fw=fw)
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

            figttrtkfix_noboot = bp.plot_cdf_num(ttrtkfix_noboot, figname='figttrtkfix_noboot', title='CDF Time to RTK Fixed \nw/Normalized Boot Times', xlabel='Seconds to RTK Fixed',fw=fw)
            figttrtkfloat_noboot = bp.plot_cdf_num(ttrtkfloat_noboot,figname='figttrtkfloat_noboot', title='CDF Time to RTK Float \nw/Normalized Boot Times', xlabel='Seconds to RTK Float',fw=fw)
            figttsps_noboot = bp.plot_cdf_num(ttsps_noboot,figname='figttsps_noboot', title='CDF Time to SPS Fixed \nw/Normalized Boot Times', xlabel='Seconds to SPS Fixed',fw=fw)

            try:
                ttsbas_noboot = rf['TT SBAS [s]'] - boot
                figttsbas_noboot = bp.plot_cdf_num(ttsbas_noboot,figname='figttsbas_noboot', title='CDF Time to SBAS Fixed w/Normalized Boot Times', xlabel='Seconds to SBAS Fixed',fw=fw)
            except:
                print("no SBAS data in ", fullpath)


        """
        plot transitions between diff modes

        """

        if plottransitions == '1':
            print("plotting diffmode transition")

            tflotofix = rf['TT Fixed [s]'] - rf ['TT Float [s]']
            figflotofix = bp.plot_cdf_num(tflotofix,figname='figflotofix', title='Transition time by Cycle\n RTK Float to RTK Fixed', xlabel='Seconds to RTK Fixed',fw=fw)

            try:
                tsbastofloat = rf['TT Float [s]'] - rf['TT SBAS [s]']
                figsbastoflo  = bp.plot_cdf_num(tsbastofloat, figname='figsbastoflo', title='Transition time by Cycle\nSBAS to RTK Float', xlabel='Seconds SBAS to RTK Float',fw=fw)
            except Exception as e:
                print("could not do sbas to rtk float transition calc")
                print(e)

            try:
                tspstosbas = rf['TT SBAS [s]'] - rf['TT SPS [s]']
                figspstosbas  = bp.plot_cdf_num(tspstosbas, figname='figspstosbas',title='Transition time by Cycle\nSBAS to RTK Float', xlabel='Seconds SPS to SBAS',fw=fw)
            except Exception as e:
                print("could not do sps to sbas transistion calc")
                print(e)

            try:
                tspstofloat =  rf['TT Float [s]'] - rf['TT SPS [s]']
                figspstofloat = bp.plot_cdf_num(tspstofloat,figname='figspstofloat', title='Transition time by Cycle\nSPS to RTK Float', xlabel='Seconds SPS to RTK Float',fw=fw)
            except Exception as e:
                print("could not do sps to rtk float tranistion calc")
                print(e)

         
        """
        plot error by diff mode 

        """
        if plotbydiffmode == '1':
            fgsbydiffmode = bp.plot_linear_by_diffmode(nav,xlabel=timelabel,fw=fw)
            fgscdfbydiffmode = bp.plot_cdf_by_diffmode(nav,saveplots=saveplots, savepath=filepath,fw=fw)
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

    def plot_comparative(args):
        filepath = args[0]
        filepath2 = args[1]
        plotnormalizedboot = args[2]
        plottransitions = args[3]
        plotbydiffmode = args[4]
        saveplots = args[5]

        filename = "nav.csv"
        starts = False
        rfonoff = False

        metadata1 = plot_results.get_metadata(filepath)
        metadata2 = plot_results.get_metadata(filepath2)

        print(metadata1)
        
        

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

        #print(nav['2D Error [m]'])
        err1 = nav['2D Error [m]']
        err2 = nav2['2D Error [m]']
        #figcdfhoriz = cp.plot_cdf(err1=err1, err2=err2)

        [errN, errE, errD ] = mda.calc_LLH2NED(nav)
        nav['errN'] = errN
        nav['errE'] = errE 
        nav['errD'] = errD

        [errN, errE, errD ] = mda.calc_LLH2NED(nav2)
        nav2['errN'] = errN
        nav2['errE'] = errE 
        nav2['errD'] = errD

        n1err15N = mda.calc_drift(nav['errN'])
        n1err15E = mda.calc_drift(nav['errE'])

        n2err15N = mda.calc_drift(nav2['errN'])
        n2err15E = mda.calc_drift(nav2['errE'])
 
        n1err15Horiz = (n1err15N.values**2 + n1err15E.values**2)**0.5
        n2err15Horiz = (n2err15N.values**2 + n2err15E.values**2)**0.5
        #print(n1err15Horiz)
        print(n1err15Horiz.shape)
        np.squeeze(n1err15Horiz).shape
        print(n1err15Horiz.shape)
        cp.plot_cdf(n1err15Horiz, n2err15Horiz **metadata1)#, **metadata2)
        #bp.plot_cdf(n1err15Horiz)
        #bp.plot_linear(n1err15Horiz)
        plt.show()

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

                if re.match('Firmware Version', line):

                    d = line.split(':')

                    md['FWversion'] = d[-1].strip()

                #rt = {}
                #rt = 'refLat: {} refLon: {} refAlt: {} FW rev: {}'.format(refLat, refLon, refAlt, FWversion)
        return(md) #{'refLat: {} refLon: {} refAlt: {} FW rev: {}'.format(refLat, refLon, refAlt, FWversion)}





























