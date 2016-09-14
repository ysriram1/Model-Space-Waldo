# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 00:38:27 2016

@author: Sriram
"""

import pickle
allUsers = pickle.load(open('waldoDataDict10.pickle', 'r'))
userData = allUsers[1]
####this script recreates the aggregate functions output using our data

def fillDFs(userData):
    keyOrder = userData.keys(); keyOrder.sort()
    startTuple = [(0, list(userData[keyOrder[0]]), 'Starting... <br />')]
    remainingTuples = []
    for i, points in enumerate(keyOrder[1:]):
        remainingTuples.append(((i+1)*5,list(userData[points])))
    return startTuple + remainingTuples
    

def fillLines(userData):
    linesLst = [] 
    keyOrder = userData.keys(); keyOrder.sort()
    for i, points in enumerate(keyOrder):
        if i == 0: 
            x1 = userData[points][0]
            y1 = userData[points][1]
        else:
            x1 = userData[keyOrder[i-1]][0]
            y1 = userData[keyOrder[i-1]][1]
        x2 = userData[points][0]
        y2 = userData[points][1]
        linesLst.append({'backward': False, 'info':'', 
        'x1':x1,'x2':x2,'y1':y1,'y2':y2, 'count':''})
    return linesLst
    
def DFLinesDict(userData):
    return {'DFs':fillDFs(userData), 'lines':fillLines(userData)}