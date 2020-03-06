#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 11:25:56 2020

@author: jtellier
"""

""" This script was created by Joshua Tellier of Purdue University on 3/5/2020, the purpose of this script
is to serve as a tutroial for working with time & date data with the pandas module. """

import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel
pd.set_option('display.max_rows',15) #this limits maximum number of rows to print in the console, otherwise it would go on and on

# === Data IO and basic analysis === #
!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii #this line still works despite displaying syntax error

ao = np.loadtxt('monthly.ao.index.b50.current.ascii') #loading the data into python
ao[0:2]
ao.shape
dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M')
dates
dates.shape
AO = Series(ao[:,2], index = dates)
AO
AO.plot() #some graphs
AO['1980':'1990'].plot()
AO['1980-05':'1981-03'].plot()
AO[120] #individual value referenced by number
AO['1960-01'] #or by index
AO['1960'] #values for a whole year
AO[AO > 0] #subset of all values

!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii
nao = np.loadtxt('norm.nao.monthly.b5001.current.ascii')
dates_nao = pd.date_range('1950-01', periods=nao.shape[0], freq='M')
NAO = Series(nao[:,2], index=dates_nao)
NAO.index

aonao = DataFrame({'AO' : AO, 'NAO' : NAO}) #creating a data frame to hold both data sets
aonao.plot(subplots=True) #some useful commands
aonao.head()
aonao['NAO']
aonao['Diff'] = aonao['AO'] - aonao['NAO'] #very easy to add new columns to the data frame
aonao.tail() #note NAO has length one less than AO, therefore the final value for NAO and Diff are NaN
del aonao['Diff'] #also easy to delete columns

import datetime
aonao.loc[(aonao.AO >0) & (aonao.NAO <0)
    & (aonao.index > datetime.datetime(1980,1,1))
    & (aonao.index < datetime.datetime(1989,1,1)),
    'NAO'].plot(kind='barh')

aonao.mean()
aonao.max()
aonao.min()
aonao.mean(1) #row-wise means
aonao.describe() #summary stats

# === Resampling === #
AO_mm = AO.resample("A").mean() #resampling with pandas to a different time frequency, the "A" stands for "Annual" time scale
AO_mm.plot(style='g--')
AO_mm = AO.resample("A").median()
AO_mm.plot()
AO_mm = AO.resample("3A").apply(np.max)
AO_mm.plot()

AO_mm = AO.resample("A").apply(['mean', np.min, np.max])
AO_mm['1900':'2020'].plot(subplots=True)
AO_mm['1900':'2020'].plot()

# === Rolling Statistics === #
aonao.rolling(window=12, center=False).mean().plot(style='-g') #rolling mean
aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g') #rolling correlation
aonao.corr() #correlation coefficients for variables
