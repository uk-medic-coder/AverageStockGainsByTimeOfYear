# Some combined funcs for yfinance

import yfinance as yf
import os
import pandas as pd

# ====================================================
def getyFinanceTickerHistory(sym, doit, p, proxydict, sesh, periodaa, validinterval):
    
    if doit==0:          
        tick = yf.Ticker(sym)
        data = tick.history(period=periodaa, interval=validinterval, prepost=False, auto_adjust=True, back_adjust=False, actions=False)
    else:

        # override requests library in yfinance

        if sesh != None:
            yf.base._requests = sesh
            yf.utils._requests = sesh
            yf.ticker._requests = sesh
                
        tick = yf.Ticker(sym, session=sesh)
        
        # yfinance can accept proxy in dict format or just proxy="https://10.10.1.10:1080" format --- both work fine on my tests
        
        data = tick.history(period=periodaa, interval=validinterval, prepost=False, auto_adjust=True, back_adjust=False, actions=False, proxy=proxydict)    

    return data # as a df

# ====================================================
def getDF_for_Symbol_Via_Yahoo_Or_DataStore(baseDataStore, name, periods, interval, prefix, dropList):

    nn = baseDataStore+name+".csv"
    
    if not os.path.exists(nn):
        df = getyFinanceTickerHistory(name, 0, 0, 0, 0, periods, interval)
        df.to_csv(nn)

    # Now read in and convert
    df = pd.read_csv(nn)
    df['Date']=pd.to_datetime(df['Date'], infer_datetime_format=True)
    df = df.set_index('Date')

    # data cleanse
        # count number of NaNs
    cnt = df.isnull().sum().sum()
    if cnt>0:
        print("\nERROR: "+name+" has NaNs....")
        exit()


    if dropList is not None:
        df = df.drop(dropList, axis=1)

    coldict = {
        "Open": prefix+"O",
        "Close": prefix+"C",
        "High": prefix+"H",
        "Low": prefix+"L",
        "Volume": prefix+"V",
    }


    df = df.rename(columns=coldict)

    return df


# ==============================================================
