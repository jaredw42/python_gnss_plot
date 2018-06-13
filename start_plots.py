#!/usr/local/bin/python3
import tkinter as tk
import plot_results as pr  


class App:

    def __init__(self,master):

        frame = tk.Frame(master)
        frame.pack()
        self.filepath = tk.StringVar()
        self.filepath.set("/Users/jwilson/SwiftNav/analysis/08-gt3_sbas_smoothing/DUT33/20180608-103420-lj33-t1-d24h-f6-SBAS-ContNav/")

        self.filepath2 = tk.StringVar()
        self.filepath2.set("/Users/jwilson/SwiftNav/analysis/08-gt3_sbas_smoothing/DUT34/20180608-103421-lj34-t1-d24h-f6-SBAS-ContNav/")
        
        self.fileentry = tk.Entry(frame, textvariable=self.filepath, width=125)
        self.fileentry.pack()

        self.file2 =tk.Entry(frame,textvariable=self.filepath2, width=125)
        self.file2.pack()

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
        self.runbutton = tk.Button(frame,command=self.execute_test,text="Run analysis")
        self.runbutton.pack()
        self.quitbutton = tk.Button(frame, text="Quit", command=frame.quit)
        self.quitbutton.pack()

    def execute_test(self):

        args = [self.filepath.get(), self.nb.get(), self.tr.get(), self.bdm.get(), self.sp.get(),self.file2.get()]
       # pr.plot_results.plot_individual(self,args)

        if self.file2.get() != None:
            args = [self.filepath.get(),self.file2.get(), self.nb.get(), self.tr.get(), self.bdm.get(), self.sp.get()]
            print("ploting comparitively")
            pr.plot_results.plot_comparative(self, args)







root = tk.Tk()
print(root)
app = App(root)
root.mainloop()
root.destroy()

