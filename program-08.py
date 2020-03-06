#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:36:21 2020

@author: jtellier
"""

""" This script was created by Joshua Tellier of Purdue University on 3/5/2020, the purpose of this script
is to run date/time processing analysis on a Wabash River data file for lab 8 of ABE65100. 
For this program to work, a file named "WabashRiver_DailyDischarge_20150317-20160324.txt" must be in the current working directory."""

import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series
pd.set_option('display.max_rows',15) #this limits maximum number of rows to print in the console, otherwise it would go on and on

# === Data input an parsing === #
#the next line imports the data, defines column names, skips initial text that is not important to the data, and parses datetimes and timezone data
Wabash = pd.read_table('WabashRiver_DailyDischarge_20150317-20160324.txt', header = 13, 
                       skiprows=11, usecols=[2,3,4], names=['DateTime','TZ','Discharge(cfs)'], parse_dates=[[0,1]]) 
Wabash=Wabash.drop(0) #final tidying up of the data, dropping pointless row
Wabash['Discharge(cfs)'] = pd.to_numeric(Wabash['Discharge(cfs)'])
Wabash.dtypes

# === time series analysis & figures === #
dates = pd.date_range('2015-03-17 00:00', periods=Wabash.shape[0], freq='15min') #creating the date range index
WB = Series(Wabash['Discharge(cfs)'].values, index=dates) #must use the .values method here because Series() wants a numpy array as the first argument
WB_rs = WB.resample("D").mean()
plt.figure(figsize=(11,8)) #had to make custom figure size because axes labels were getting cut off on the default
WB_rs.plot(style='-b')
plt.ylabel('Mean Daily Discharge (cfs)')
plt.xlabel('Month')
plt.savefig('Wabash_Daily_Streamflow.pdf')
# delete old figure window before creating next figure

WB2 = WB_rs.nlargest(10) #finding the ten days with highest average streamflow
plt.figure(figsize=(11,8))
WB_rs.plot(color='blue', alpha=0)
plt.scatter(WB2.index,WB2.values,s=20,c='red',marker='x')
plt.ylabel('Mean Daily Discharge (cfs)')
plt.xlabel('Month')
plt.savefig('Wabash_Ten_Highest.pdf')
# delete old figure window before creating next figure

WB_mn = WB.resample("M").mean()
plt.figure(figsize=(11,8)) #had to make custom figure size because axes labels were getting cut off on the default
WB_mn.plot(style='-b')
plt.ylabel('Mean Monthly Discharge (cfs)')
plt.xlabel('Month')
plt.savefig('Wabash_Monthly_Streamflow.pdf')
