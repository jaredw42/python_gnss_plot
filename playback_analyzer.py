#!/usr/local/bin/python3
import re
import os, os.path
import matplotlib
matplotlib.use('TkAgg') 
import tkinter as tk
import magicdataanalyzer as mda 
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt 




testpath = '/Users/jwilson/SwiftNav/dev/29-beidou_playback_v164/'

runs = os.listdir(testpath)

navdata = []


for dirName, subdirList, fileList in os.walk(testpath):
    if re.search('DUT\d{2}$', dirName):
    #if re.search('DUT41$', dirName):

        navfile = os.path.join(dirName, 'nav.csv')
        
        nav = pd.read_csv(navfile)

        nav['errN'], nav['errE'], nav['errD'] = mda.calc_LLH2NED(nav)
        nav['errHoriz'] = (nav['errN']**2 + nav['errE']**2)**0.5

        ds = xr.Dataset.from_dataframe(nav)
        ds.attrs = {'playback': dirName}

        navdata.append(ds)


plt.figure(figsize=[12,9])
ax = plt.subplot(1,1,1)
i = 0
for nav in navdata:

    dsorted = np.sort(nav['errHoriz'])
    ds = dsorted[~np.isnan(dsorted)]
    yvals = np.arange(len(ds)) /float(len(ds) - 1) * 100
    ax.plot(ds, yvals)#,label=navdata.attrs['fw'])

    if np.median(ds) > 0.05:
        print(nav.attrs['playback'], 'median horiz error > 0.05')
        i +=1
print(i, 'count')

ax.grid()
ax.set_xlabel('Horizontal Error (m)')
ax.set_ylabel('Percent of Epochs')
ax.set_xscale('log')
plt.title('LabSat File_005 Playback \n All runs \n CDF Horizontal Error')

plt.show()
savepath = testpath + '/plots/'

subplnum = 1
plt.figure(figsize=[12,14])

for n, nav in enumerate(navdata,start=1):

    ax = plt.subplot(8,1,subplnum)
    ax.plot(nav['TOW [s]'], nav['Fix Mode'])
    ax.set_ylabel('Fix Mode')
    subplnum += 1

    if n % 8 == 0 :
        sn = 'plot_{}'.format(n) + '_fix mode'
        sp = savepath + sn 
        plt.savefig(sp)
        plt.close()
        plt.figure(figsize=[12,14])
        subplnum = 1 



subplnum = 1
plt.figure(figsize=[12,12])

for n, nav in enumerate(navdata,start=1):

    ax = plt.subplot(8,1,subplnum)
    ax.plot(nav['TOW [s]'], nav['errHoriz'])
    ax.set_ylabel('2D Error')
    ax.set_xlabel(nav.attrs['playback'])
    subplnum += 1

    if n % 8 == 0 :
        sn = 'plot_{}'.format(n) + '_horiz_error'
        sp = savepath + sn 
        plt.savefig(sp)
        plt.close()
        plt.figure(figsize=[12,12])
        subplnum = 1 

subplnum = 1
plt.figure(figsize=[12,12])

for n, nav in enumerate(navdata,start=1):

    ax = plt.subplot(8,1,subplnum)
    ax.plot(nav['TOW [s]'], nav['errHoriz'])
    ax.set_ylabel('2D Error')
    ax.set_xlabel(nav.attrs['playback'])
    ax.set_yscale('log')
    subplnum += 1

    if n % 8 == 0 :
        sn = 'plot_{}'.format(n) + '_horiz_error_log'
        sp = savepath + sn 
        plt.savefig(sp)
        plt.close()
        plt.figure(figsize=[12,12])
        subplnum = 1 
#plt.show()










