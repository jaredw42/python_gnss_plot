#!/usr/local/bin/python3
import os
import re
import tkinter as tk
import plot_results as pr 
import magicdataanalyzer as mda 
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt 
import basic_plots as bp
import make_plots as mkp



class App:

    def __init__(self,master):

        frame = tk.Frame(master)
        frame.pack()
        self.filepath = tk.StringVar()
        self.filepath.set("/Volumes/data/data/PiksiMultiTesting/2018-11/09-RevCRetest85c/DUT61/20181109-152751-dut61-t3-d24h-f3-RTK-Starts-CellModem/")

        self.filepath2 = tk.StringVar()
        self.filepath2.set("/Volumes/data/data/PiksiMultiTesting/2018-11/09-RevCRetest85c/DUT62/20181109-152754-dut62-t3-d24h-f3-RTK-Starts-CellModem/")
        
        self.filepath3 = tk.StringVar()
     #   self.filepath3.set("/Volumes/data/data/PiksiMultiTesting/2018-10/12-v2.1.14-RTK/DUT13/20181012-161050-dut13-t3-d24h-f4-RTK-Starts")
        
        self.filepath4 = tk.StringVar()
        #self.filepath4.set("/Volumes/data/data/PiksiMultiTesting/2018-01/19-GT2_A_starts_B_RFoff_65s/DUT23/20180119-124747-lj23-t3-d24h-f4-RTK-Starts/")

        self.filepath5 = tk.StringVar()
        #self.filepath5.set("/Volumes/data/data/PiksiMultiTesting/2017/2017-11/08-v1.2.14/DUT14/20171108-113337-lj14-t3-d24h-f4-RTK-Starts/")

        self.filepath6 = tk.StringVar()
        #self.filepath6.set("/Volumes/data/data/PiksiMultiTesting/2017/2017-07/26-v1.1.29/LJ4/20170726-152855-lj4-t3-d24h-f4-Starts-cold-rtk/")

        self.fileentry = tk.Entry(frame, textvariable=self.filepath, width=125)
        self.fileentry.pack()

        self.file2 =tk.Entry(frame,textvariable=self.filepath2, width=125)
        self.file2.pack()

        self.file3 =tk.Entry(frame,textvariable=self.filepath3, width=125)
        self.file3.pack()

        self.file4 =tk.Entry(frame,textvariable=self.filepath4, width=125)
        self.file4.pack()

        self.file5 =tk.Entry(frame,textvariable=self.filepath5, width=125)
        self.file5.pack()

        self.file6 =tk.Entry(frame,textvariable=self.filepath6, width=125)
        self.file6.pack()

        self.nb = tk.StringVar()
        self.nb.set("plot normalized boot stats")

        self.tr = tk.StringVar()
        self.tr.set("plot diff mode transition times")

        self.bdm = tk.StringVar()
        self.bdm.set("plots by diff modes")

        self.sp = tk.StringVar()
        self.sp.set("recalc nav")

        opts = [self.nb, self.tr, self.bdm, self.sp]
        opts_len = len(opts)
        for x in range(opts_len):

            varname = opts[x]
            vartext = opts[x].get()
            self.optbox = tk.Checkbutton(frame,text=vartext,variable=varname)
            self.optbox.pack()
        self.runbutton = tk.Button(frame,command=self.execute_test,text="Single dataset Plots")
        self.runbutton.pack()
        self.calcbutton = tk.Button(frame,command=self.execute_calc,text="Plot ALL")
        self.calcbutton.pack()
        self.quitbutton = tk.Button(frame, text="Quit", command=frame.quit)
        self.quitbutton.pack()

    def execute_test(self):
        
        args = [self.filepath.get(), self.nb.get(), self.tr.get(), self.bdm.get(), self.sp.get(),self.filepath2.get()]

        pr.plot_results.plot_individual(args)

    def execute_calc(self):
       
        args = [self.filepath.get(), self.nb.get(), self.tr.get(), self.bdm.get(), self.sp.get(),self.filepath2.get(),
                self.filepath3.get(), self.filepath4.get(), self.filepath5.get(), self.filepath6.get()]

        fplist = []
        for a in args:
            if re.search('dut',a):
                fplist.append(a)
        
        md = {}
        nav = []
        for i, fp in enumerate(fplist):

            md['fp{}'.format(i)] = fp
            readstr = os.path.join(fp, 'nav.csv')
            print(readstr)
            df = pd.read_csv(readstr)
            md = mda.get_metadata(fp)
            solnrate = mda.get_soln_rate(fp)

            refdata = {'refLat': md['refLat'], 
                       'refLon': md['refLon'], 
                       'refAlt': md['refAlt'],
                           'fw': md['FWversion'],
                     'solnrate': solnrate,
                     'filepath': fp,
                     'testname': md['testname'],
                     'device': md['device']}

            ds = xr.Dataset.from_dataframe(df)
            ds.attrs = refdata

            nav.append(ds)
            print(nav)
        mkp.mkp.plot_nav(nav)
        rf = []
        readstr = None
        startstest = False 


        for fp in fplist:
            if re.search('RFOnOff', fp, flags=re.IGNORECASE):
                readstr = os.path.join(fp, 'rf-on-off.csv')
            elif re.search('Starts', fp, flags=re.IGNORECASE):
                readstr = os.path.join(fp , 'starts.csv')
                startstest = True
            elif re.search('CorrOnOff', fp, flags=re.IGNORECASE):
                readstr = os.path.join(fp, 'corr-on-off.csv')
            else:
                pass

            if readstr != None:
                df = pd.read_csv(readstr)
                md = mda.get_metadata(fp)
                solnrate = mda.get_soln_rate(fp)


                refdata = {'refLat': md['refLat'], 
                           'refLon': md['refLon'], 
                           'refAlt': md['refAlt'],
                               'fw': md['FWversion'],
                         'solnrate': solnrate,
                         'filepath': fp,
                         'testname': md['testname'],
                         'device': md['device']}

            
                ds = xr.Dataset.from_dataframe(df)
                ds.attrs = refdata
                rf.append(ds)
        if readstr != None:

            if startstest == True:
                for starts in rf:

                    mda.calc_nobootstats(starts)
                    print(starts)
            mkp.mkp.plot_rf(rf)

        plt.show()

root = tk.Tk()
print(root)
app = App(root)
root.mainloop()
root.destroy()

