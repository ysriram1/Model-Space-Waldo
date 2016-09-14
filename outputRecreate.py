# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 00:38:27 2016

@author: Sriram
"""

####this script recreates the aggregate functions output using our data

def fillDFs(userData):
    startTuple = [(0, list(userData.values()[0]), 'Starting... <br />')]
    remainingTuples = []
    for i, points in enumerate(userData.values()[1:]):
        remainingTuples.append(((i+1)*5,list(points)))
    return startTuple + remainingTuples
    

def fillLines(userData):
    linesLst = []
    for i, points in enumerate(userData.values()):
        if i == 0: 
            x1 = points[0]
            y1 = points[1]
        else:
            x1 = userData.values()[i-1][0]
            y1 = userData.values()[i-1][1]
        x2 = points[0]
        y2 = points[1]
        linesLst.append({'backward': False, 'info':'', 
        'x1':x1,'x2':x2,'y1':y1,'y2':y2, 'count':''})
    return linesLst
    
def DFLinesDict(userData):
    return {'DFs':fillDFs(userData), 'lines':fillLines(userData)}