
import generalFuncs as ancgeneral

import os

# ===============================================
# string--> list (dd=separator)

def stringToList(bb, dd):
    
    return bb.split(dd)

# ===============================================
# Converts a list array of strings to a string with delimeter bb

def listarrayToString(aa,bb):
    
    return bb.join(aa)

# ===============================================
# A list of ints or floats to a string with bb delimeter

def numbersListToString(aa, bb):

    a = bb.join(str(e) for e in aa)                       # list of numbers to a string
    return a

# ===============================================

def subtractStringLists(a,b):
    # removes all items of b in list a
    # if b is not found, return "-9999"+fail string item    
    r = a    
    for i in b:
        if i in a:
            r.remove(i)
        else:
            r = "-9999"+i
            break    
        
    return r

# ===============================================

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

# ===============================================

def ReadInAFileToAList(fnuse, LFflag, upperflag):

    symlist = []

    with open(fnuse) as file:
        for line in file:
            
            if upperflag==1:
                line = line.upper()
            
            line = line.strip()
            
            if LFflag==0:
                symlist.append(line)
            else:
                if line !="":
                    symlist.append(line)
    
    # f.close not needed with "with" statements
    return symlist

# ===============================================
def searchAStringForAnyOfThese(searchme, findany, makeAllUpperCaseFlag):
    
    searchme2 = searchme.upper() if makeAllUpperCaseFlag==1 else searchme
    findanythese = findany.upper() if makeAllUpperCaseFlag==1 else findany
    lst = findanythese.split(",")
    
    n = 0
    for it in lst:
        it2 = it.strip()
        if it2 != "":
            it3 = it2.upper() if makeAllUpperCaseFlag==1 else it2
            if searchme2.find(it3) != -1:
                n = 1
    
    return n
    
# ===============================================
def listStringAsMenu(lst, startnumber, inputText, defvalue):
    
    print ("\n")
    i = startnumber
    for x in lst:
        print(str(i)+" = "+x)
        i += 1
    
    d = ancgeneral.prefilledInput("\n"+inputText, defvalue)
    return d

# ===============================================
def listFilesInFolderAsMenu(folder, extensionFilter, defValue, inputText, eraseExtension):

    lst = []

    for x in os.listdir(folder):
        if extensionFilter == "":
            lst.append(x)
        else:
            if x.endswith(extensionFilter):
                lst.append(x)
    
    print ("\n")

    i = 1
    for x in lst:
        print(str(i)+" = "+x)
        i += 1
    
    d = ancgeneral.prefilledInput("\n"+inputText, "" if defValue==0 else str(defValue))

    dd = lst[int(d)-1]

    if eraseExtension==1:
        r = os.path.splitext(dd)[0]
    else:
        r = dd

    return d, r

# ===============================================
def subtractItemsFromAList(mainlist: list(), subtractColsList: list()) -> list():

    # both lists as inputs
    # removes any items found in subtractColsList from mainList

    res = [ ele for ele in mainlist ]
    for a in subtractColsList:
        if a in mainlist:
            res.remove(a)
    
    return res

# ===============================================
def subtractItemsFromListIfContainsANY(mainList: list(), subtractColsList: list()) -> list():

    # both lists as inputs
    # removes any items from mainlist that may contain any strings found in subtractlist

    xxt = mainList.copy()              # else original list modified by remove(m1)
    
    for m in range(0, len(mainList)):
        m1 = str(mainList[m])
        for x in range(0, len(subtractColsList)):
            m2 = str(subtractColsList[x])
            if m2 != "":
                if m1.find(m2) > -1:
                    if m1 in xxt:
                        xxt.remove(m1)

    return xxt
