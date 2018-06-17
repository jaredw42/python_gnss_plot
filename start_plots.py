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
        self.filepath.set("/Users/jwilson/SwiftNav/analysis/08-gt3_sbas_smoothing/DUT33/20180608-103420-lj33-t1-d24h-f6-SBAS-ContNav/")

        self.filepath2 = tk.StringVar()
        self.filepath2.set("/Users/jwilson/SwiftNav/analysis/08-gt3_sbas_smoothing/DUT34/20180608-103421-lj34-t1-d24h-f6-SBAS-ContNav/")
        
        self.filepath3 = tk.StringVar()
        self.filepath4 = tk.StringVar()

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
        self.runbutton = tk.Button(frame,command=self.execute_test,text="Generate Plots")
        self.runbutton.pack()
        self.calcbutton = tk.Button(frame,command=self.execute_calc,text="qul cHa")
        self.calcbutton.pack()
        self.quitbutton = tk.Button(frame, text="Quit", command=frame.quit)
        self.quitbutton.pack()

    def execute_test(self):
        
        args = [self.filepath.get(), self.nb.get(), self.tr.get(), self.bdm.get(), self.sp.get(),self.filepath2.get()]

        pr.plot_results.plot_individual(args)

        # if self.file2.get() != None:
        #     args = [self.filepath.get(),self.file2.get(), self.nb.get(), self.tr.get(), self.bdm.get(), self.sp.get()]
        #     print("ploting comparitively")
            
          #  pr.plot_results.plot_comparative(args)

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
         #   md['info{}'.format(i)] = pr.plot_results.get_metadata(fp)
            md = pr.plot_results.get_metadata(fp)

            c = df.columns.values.tolist()
          #  nav.append(xr.DataArray(df,dims=c))

            refdata = {'refLat': md['refLat'], 
                       'refLon': md['refLon'], 
                       'refAlt': md['refAlt'],
                           'fw': md['FWversion']}

            for k,v in refdata.items():
                print(k, v, "refdata kv")
            ds = xr.Dataset.from_dataframe(df)
            ds.attrs = refdata

            print(ds.attrs, 'attributes')
            print(ds.attrs.items(), 'items')
           # print(ds.attrs['refLon'])

            for k,v in ds.attrs.items():
                print(k, v, "dataset kv")

            nav.append(ds)
        mkp.mkp.make_plots(nav)





root = tk.Tk()
print(root)
app = App(root)
root.mainloop()
root.destroy()

