#!/usr/local/bin/python3
import tkinter as tk
import plot_results as pr 
import magicdataanalyzer as mda 
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt 
import basic_plots as bp
import make_plots as mkp
import re



class App:

    def __init__(self,master):

        frame = tk.Frame(master)
        frame.pack()
        self.filepath = tk.StringVar()
        self.filepath.set("//Users/jwilson/SwiftNav/Piksi_v16_testing/gtt/18-gt3_5hz_rtkstarts_v160/DUT31/20180618-112325-lj31-t3-d24h-f4-RTK-Starts/")

        self.filepath2 = tk.StringVar()
        self.filepath2.set("/Users/jwilson/SwiftNav/Piksi_v16_testing/gtt/18-gt3_5hz_rtkstarts_v160/DUT32/20180618-112327-lj32-t3-d24h-f4-RTK-Starts/")
        
        self.filepath3 = tk.StringVar()
        #self.filepath3.set("/Volumes/data/data/PiksiMultiTesting/2018-06/18-gt2_5hz_rf5_GPS_GLN_test_v160/DUT23/20180618-083947-lj23-t2-d24h-f4-RTK-RFOnOff-1-5s/")
        
        self.filepath4 = tk.StringVar()
      #  self.filepath4.set("/")

        self.fileentry = tk.Entry(frame, textvariable=self.filepath, width=125)
        self.fileentry.pack()

        self.file2 =tk.Entry(frame,textvariable=self.filepath2, width=125)
        self.file2.pack()

        self.file3 =tk.Entry(frame,textvariable=self.filepath3, width=125)
        self.file3.pack()

        self.file4 =tk.Entry(frame,textvariable=self.filepath4, width=125)
        self.file4.pack()

        self.nb = tk.StringVar()
        self.nb.set("plot normalized boot stats")

        self.tr = tk.StringVar()
        self.tr.set("plot diff mode transition times")

        self.bdm = tk.StringVar()
        self.bdm.set("plots by diff modes")

        self.sp = tk.StringVar()
        self.sp.set("save plots")

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
                self.filepath3.get(), self.filepath4.get()]

        fplist = []
        for a in args:
            if re.search('2018',a):
                fplist.append(a)
        
        md = {}
        nav = []
        

        for i, fp in enumerate(fplist):

            md['fp{}'.format(i)] = fp

            readstr = fp + 'nav.csv'
            df = pd.read_csv(readstr)
            md = mda.get_metadata(fp)
            solnrate = mda.get_soln_rate(df)




            refdata = {'refLat': md['refLat'], 
                       'refLon': md['refLon'], 
                       'refAlt': md['refAlt'],
                           'fw': md['FWversion'],
                     'solnrate': solnrate,
                     'filepath': fp,
                     'testname': md['testname']}

            for k,v in refdata.items():
                ds = xr.Dataset.from_dataframe(df)


                ds.attrs = refdata


            nav.append(ds)
        mkp.mkp.plot_nav(nav)
        rf = []


        for fp in fplist:
            if re.search('RFOnOff', fp):
                readstr = fp + 'rf-on-off.csv'
            elif re.search('Starts', fp):
                readstr = fp + 'starts.csv'
            elif re.search('CorrOnOff', fp):
                readstr = fp + 'corr-on-off.csv'
            else:
                break

            
            df = pd.read_csv(readstr)
            md = mda.get_metadata(fp)



            refdata = {'refLat': md['refLat'], 
                       'refLon': md['refLon'], 
                       'refAlt': md['refAlt'],
                           'fw': md['FWversion'],
                     'solnrate': solnrate,
                     'filepath': fp,
                     'testname': md['testname']}

            if readstr != None:
                ds = xr.Dataset.from_dataframe(df)
                ds.attrs = refdata
                rf.append(ds)

        mkp.mkp.plot_rf(rf)

        plt.show()





root = tk.Tk()
print(root)
app = App(root)
root.mainloop()
root.destroy()

