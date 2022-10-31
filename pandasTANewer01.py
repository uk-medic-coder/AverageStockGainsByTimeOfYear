
import numpy as np
import matplotlib.pyplot as plt

# =========================================
# =========================================
# This tested out to be fast

def move_column_inplace(df, col, pos):
    
    col = df.pop(col)
    df.insert(pos, col.name, col)
    
    return df
    
# =========================================
def ANCsafeDivide(df, col1, col2, zeroerrorValue):
    
    df = df[col1].div(df[col2]).replace(np.inf, zeroerrorValue)
    return df

# =========================================
# =========================================
def doMAColumnComparisons(df, colname, smaList, aboveSMAflag, keepSMAvalues,keepcolname, MAType):

    # smaList = List of sma values, dont do this routine if None

    # aboveSMAflag: 0 = dont do ; 1 = Greater than or equal to ; 2 = Greater than only ; 3 = Less than equal to ; 4 = Less than

    # keepSMAvalues : 0 = delete original SMA columns if do aboveSMAflag ; 1 = keep them

    # keepcolname: 0 = delete colname after all calcs done ; 1 = keep it
    
    # MAType: 0 = SMA (currently only one done, in for future proofing)
    
    
    droplist = []    
    maOutList = ["SMA"]             # matches MAType
    
    if smaList is not None:
        for x in smaList:
            z = int(x)
            q = colname+"-"+maOutList[MAType]+str(z)
            
            if MAType==0:
                df[q] = df[colname].rolling(z, min_periods=1).mean()

        for x in smaList:
            z = int(x)
            q = colname+"-"+maOutList[MAType]+str(z)

            if aboveSMAflag==1:
                df[colname+">="+q] = df[colname].ge(df[q]).astype(int)
            if aboveSMAflag==2:
                df[colname+">"+q] = df[colname].gt(df[q]).astype(int)
            if aboveSMAflag==3:
                df[colname+"<="+q] = df[colname].le(df[q]).astype(int)
            if aboveSMAflag==4:
                df[colname+"<"+q] = df[colname].lt(df[q]).astype(int)

            if keepSMAvalues==0:
                droplist.append(q)    
    

    if keepcolname==0:
        droplist.append(colname)

    if len(droplist)>0:
        df = df.drop(droplist, axis=1)
        
    return df

