#!/usr/local/bin/python3
import tkinter as tk
import plot_results as pr  


class App:

    def __init__(self,master):

    	frame = tk.Frame(master)
    	frame.pack()
    	self.filepath = tk.StringVar()
    	self.filepath.set("/Users/jwilson/SwiftNav/dev/gtt/05-GT1_A-RF_B-CN_LBL_v143/DUT11/20180205-080905-lj11-t2-d24h-f4-RTK-RFOnOff-1-5s/")
    	
    	self.fileentry = tk.Entry(frame, textvariable=self.filepath, width=150)
    	self.fileentry.pack()

    	self.nb = tk.StringVar()
    	self.nb.set("plot normalized boot stats")

    	self.tr = tk.StringVar()
    	self.tr.set("plot diff mode transition times")

    	self.bdm = tk.StringVar()
    	self.bdm.set("plots by diff modes")

    	opts = [self.nb, self.tr, self.bdm]
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

    	#for _name in range(self.opts_len):
    	args = [self.filepath.get(), self.nb.get(), self.tr.get(), self.bdm.get()]
    	print(args)
    	pr.plot_results.plot_stuff(self,args)







root = tk.Tk()
print(root)
app = App(root)
root.mainloop()
root.destroy()

