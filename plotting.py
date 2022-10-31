import numpy as np
import pandas as pd
import os
import shutil

from matplotlib import pyplot as plt
import matplotlib.dates as mdates

import liststringsGeneral as lst

# ==================================================
def amendFilenameForPlotSave(bf, ff, ex):
    
    r = ff.replace("/", "_");
    r = r.replace(",", "_");
    r = r.replace("!", "_");
    
    return bf+r+ex    

# ==================================================
# A framework for plotting DF columns
# and callable functions within this class
# ==================================================

class DFPlotterExplorerFunctions():

    thisdf = None
    thisdfcolnames = []
    kind = None
    legend = None
    figsize = None
    xticksformat = None
    internalSuppressPlotshowFlag = 0

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, df=None, setDateIndex="", kind="bar", legend="True", figsize=(16,7), xticksformat=[], dropcols=[]):

        self.thisdf = df.copy(deep=True)                # coz drop columns and dont want to alter original

        if setDateIndex != "":
            self.thisdf['Date']=pd.to_datetime(self.thisdf[setDateIndex], infer_datetime_format=True)
            self.thisdf = self.thisdf.set_index('Date')


        if len(dropcols)>0:
            self.thisdf = self.thisdf.drop(columns=dropcols, axis=1)

        self.thisdfcolnames = list(self.thisdf.columns)

        # DF kinds:
            # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html
            # ‘line’ : line plot (default) , bar’ : vertical bar plot.... etc...

        # xticksformat:
            # [0] = format, eg: '%d-%b'
            # [1] = interval, eg 15
            # [2] = rotation, eg 30

        self.kind=kind
        self.legend=legend
        self.figsize=figsize
        self.xticksformat=xticksformat

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # PRIVATE METHOD
    def __DFmenupicker(self, cls=0, addexitvalue=0, menuprefix="Choose Column: "):

        if cls==1:
            os.system('clear')

        cm = self.thisdfcolnames.copy()
        
        if addexitvalue==1:
            cm.append("EXIT LOOP")

        v = int(lst.listStringAsMenu(cm, 1, menuprefix, ""))

        if v==len(cm):
            v = 0

        return v

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def plotDF(self, col=None):

        self.thisdf[col].plot(kind=self.kind, legend=self.legend, figsize=self.figsize)

        if len(self.xticksformat)>0:

            # Format the date into months & days
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(self.xticksformat[0]))

            # Change the tick interval
            plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=self.xticksformat[1]))

            # Puts x-axis labels on an angle
            plt.gca().xaxis.set_tick_params(rotation = self.xticksformat[2])

        if self.internalSuppressPlotshowFlag==0:
            plt.show()
            plt.clf()     # clear plot       
        else:
            return plt

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    def KeyPressPlotLoop(self, maxrows=0):

        exit = 0
        while exit==0:
            os.system('clear')

            if maxrows==0:
                print(self.thisdf)
            else:
                if maxrows==-1:
                    # The scope of these changes made to pandas settings are local to with statement.
                    with pd.option_context('display.max_rows', None):
                        print(self.thisdf)
                else:
                    print(self.thisdf.head(maxrows))

            q = self.__DFmenupicker(addexitvalue=1)

            if q==0:
                exit=1
            else:
                self.plotDF(col=self.thisdfcolnames[q-1])

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    def KeyPressSortLoop(self, maxrows=0, sortdir=False):

        colsorts = []
        for x in self.thisdfcolnames:
            colsorts.append([x, sortdir])

        exit = 0
        while exit==0:
            os.system('clear')
            
            if maxrows==0:
                print(self.thisdf)
            else:
                if maxrows==-1:
                    # The scope of these changes made to pandas settings are local to with statement.
                    with pd.option_context('display.max_rows', None):
                        print(self.thisdf)
                else:
                    print(self.thisdf.head(maxrows))

            q = self.__DFmenupicker(addexitvalue=1)

            if q==0:
                exit=1
            else:
                self.thisdf = self.thisdf.sort_values(self.thisdfcolnames[q-1], ascending=colsorts[q-1][1])
                colsorts[q-1][1] = True if colsorts[q-1][1]==False else False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    def DumpJPGs(self, basefolder="/tmp", drawcols=[], excludecols = []):

        bf = basefolder
        if not bf.endswith("/"):
            bf += "/"
        
        bf+="DumpJPG/"
        
        if os.path.isdir(bf)==True:
            shutil.rmtree(bf)
        os.mkdir(bf)             
        
        if len(drawcols)==0:
            dumpcols = self.thisdfcolnames
        else:
            dumpcols = drawcols

        print("\n\nDrawing JPGs...\n")
        
        for x in dumpcols:
            if x not in excludecols:
                print(x)
                self.internalSuppressPlotshowFlag=1
                
                p = self.plotDF(col=x)
                
                fn = amendFilenameForPlotSave(bf, x, ".jpg")             # coz "/" and "," in some column names will mess up filenames
                
                p.savefig(fn, bbox_inches='tight', dpi=150)
                p.clf()     # clear plot                    
                
                self.internalSuppressPlotshowFlag=0
        
        print("\nDrawing done.\n")

# ==================================================
