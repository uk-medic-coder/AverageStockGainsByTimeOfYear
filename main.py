
# This downloads a stock from yFinance, and shows by day of the year
# what the average X day future gain in price is.
 
import pandas as pd
import numpy as np
import sys
import os
import time
from datetime import datetime, timedelta
from sparklines import sparklines

from matplotlib import pyplot as plt
import matplotlib.dates as mdates

import pandasTANewer01 as pandasTANew01
import yFinanceExtra as yfe
import plotting as ancplot


# ==============================================================

# Where data will be stored
baseDataStore = "/home/YOUR_USERNAME/Documents/"

# This is the number of days percent gain in the future to see
daysGain = 5

yahooSymbol = "^IXIC"

# ==============================================================

pd.set_option('display.max_rows', 300)

os.system('clear')
print ("\n\033[4mAverage Gains By Time Of Year\033[0m\n")


# ==============================================

# This is for Nasdaq100 but can be any stock available on Yahoo Finance

df = yfe.getDF_for_Symbol_Via_Yahoo_Or_DataStore(baseDataStore, yahooSymbol, "max", "1d","", None)

nmm = "FutureGainDays-"+str(daysGain)
df["gaintmp"] = df["C"].pct_change(periods=daysGain).fillna(0).mul(100)
df[nmm] = df["gaintmp"].shift(-daysGain)        # Shift back x days to see what the gain would have been
df["uniqdt"] = df.index.strftime('%b-%d')
df["tmpdate"] = "1972-"+df.index.strftime('%m-%d')          # 1972 is a leap year needed for Feb29!
df["uniqdttm"] = pd.to_datetime(df["tmpdate"], format="%Y-%m-%d")


dropcols = ["H","L","V","O","gaintmp", "tmpdate"]


df = df.drop(columns=dropcols, axis=1)
print(df.head(20))


def sparkline_str(x):
    # xx makes sure no NaN or inf in data to cause an error
    # can use np.isinfinite() to give True or False if these exist also
    xx = np.nan_to_num(x, nan=0, posinf=0, neginf=0)
    bins=np.histogram(xx)[0]
    sl = ''.join(sparklines(bins))
    return sl

def kurtosis(x):
    # coz doesnt exist in .agg groupby
    xx = abs(pd.Series.kurt(x))
    return xx

def AllValues(x):
    nps = np.sort(x)
    return np.array2string(nps, formatter={'float_kind':lambda x: "%.2f" % x}, separator=',')

def PercentNeg(x):
    e = (np.sum(x<0) / x.size)*100
    return e.round(1)

def PercentSumNeg(x):
    return np.where(x<0,x,0).sum(0).round(2)

def Expect(x):
    # This does a % based expectancy, not actual $ value
    pn = (np.sum(x<0) / x.size)*100
    pp = (np.sum(x>=0) / x.size)*100

    meanPos = (np.where(x>=0,x,0).sum(0)) / np.sum(x>=0)
    meanNeg = (np.where(x<0,x,0).sum(0)) / np.sum(x<0)

    r = (pp * meanPos) - (pn * meanNeg)
    return r


sparkline_str.__name__ = "sparkline"

aggs = df.groupby("uniqdttm")[nmm].agg(['mean', 'min', 'median', 'max', 'std', 'skew', Expect, PercentNeg, PercentSumNeg, kurtosis, sparkline_str]).round(3)
print(aggs)

# If the skewness is between -0.5 and 0.5, the data are fairly symmetrical
# If the skewness is between -1 and — 0.5 or between 0.5 and 1, the data are moderately skewed
# If the skewness is less than -1 or greater than 1, the data are highly skewed

# If the absolute value of skew<0.5 then very symmetric.
# If the absolute value of skew is in between 0.5 and 1 then slightly skewed
# If the absolute value of skew is greater than 1 then very skewed.
# And the value of Kurtosis is 0.4 which is greater than 0 means data is slightly pointy to the normal distribution.

grpsa = aggs.reset_index()
print(grpsa)

pclass = ancplot.DFPlotterExplorerFunctions(df=grpsa, setDateIndex="uniqdttm", xticksformat=['%d-%b', 15, 30], dropcols=["sparkline", "min", "max", "uniqdttm"])
pclass.DumpJPGs()
