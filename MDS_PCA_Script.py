# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 00:14:21 2016

@author: SYARLAG1
"""

import arff
import numpy as np
import os
import pandas as pd

os.chdir('C:/Users/SYARLAG1/Desktop/Model-Space-Waldo')



# attributes of the last file have all the columns we need
lastFile = arff.load(open('./data/2000s.arff','rb'))
colNames = lastFile['attributes']
rowCount = len(lastFile['data'])

# initialize a blank dfs
dataAddDf = pd.DataFrame()
dataInfoAddDf = pd.DataFrame()
timeOrdList = []
# iterate through all the files and fille in the DFs (features are cumulative)
for fileName in os.listdir('./data'):

    timeName = fileName[:-5]
    timeOrdList.append(timeName)
    fileLocation = './data/'+fileName
    read = arff.load(open(fileLocation, 'rb'))

    data = read['data']
    features = read['attributes']
    
    posData = np.array(data, dtype='int8')[:,:-8]
    infoData = np.array(data, dtype='int8')[:,-8:]
    infoDataDf = pd.DataFrame(infoData); infoDataDf.columns = features[-8:]
    
    dataInfoAddDf = pd.concat([dataInfoAddDf, infoDataDf])
    
    dataDict = {}
    for index, feature in enumerate(features): #We auto match with attribute and fill in the missing values with NaN
        if index >= posData.shape[1]: break
        dataDict[feature] = posData[:,index]

    dataAddDf = pd.concat([dataAddDf, pd.DataFrame(dataDict)])  
    
dfAllData = dataAddDf.fillna(0)
######Performing PCA or MDS on the entire data
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
redPCAMatrix = pca.fit_transform(dfAllData)
redMat = redPCAMatrix

from sklearn.manifold import MDS
mds = MDS(n_components = 2)
redMDSMatrix = mds.fit_transform(dfAllData)
redMat = redMDSMatrix

# subset this matrix to only include the users we are interested in
# Step 1: look for users that either fast or slow
fastUsrOrdLst = []
slowUsrOrdLst = []

for rowIndex in infoDataDf.index:
    row = infoDataDf.iloc[rowIndex,-2]
    if row == 2:
        if rowIndex not in fastUsrOrdLst: fastUsrOrdLst.append(rowIndex)
    if row == 0:
        if rowIndex not in slowUsrOrdLst: slowUsrOrdLst.append(rowIndex)


# Step 2: extract out only fast and slow users
allFastAndSlowUserLst = fastUsrOrdLst + slowUsrOrdLst
userTimeDict = {}
start = 0; end = 90 # every time file had 90 users
for timeName in timeOrdList:    
    subArray = redMat[start:end]
    for userID, userIndex  in enumerate(allFastAndSlowUserLst):
        if userID not in userTimeDict.keys():
            userTimeDict[userID] = {}
        userTimeDict[userID][int(timeName[:-1])] = subArray[userIndex]
    start = end; end = start + 90

# plot the sequence for each user
# PCA:
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm 
plt.style.use('ggplot')

colors=cm.rainbow(np.linspace(0,1,24))

fig = plt.figure(figsize=(17,17))
ax = fig.add_subplot(111)

for color, userID in zip(colors,userTimeDict.keys()):
    name = 'User' + str(userID+1)
    userDF = pd.DataFrame(userTimeDict[userID]).T
    #pcaVals = [list(x) for x in userTimeDict[userID].values()]
    #ax.scatter(userDF.iloc[:,0], userDF.iloc[:,1], color = 'b', s=40)
    ax.plot(userDF.iloc[:,0], userDF.iloc[:,1], '-', color = color, label = name, linewidth=4)


ax.legend()
plt.xlabel('PCA Proj 1'); plt.ylabel('PCA Proj 2')
plt.title('PCA Projection of different Search Spaces')
#plt.legend(prop={'size':20}, bbox_to_anchor=(1,1))
plt.tight_layout(pad=7)
plt.savefig('./pcaOutput.png')

# MDS
fig = plt.figure(figsize=(17,17))
ax = fig.add_subplot(111)

for color, userID in zip(colors,userTimeDict.keys()):
    name = 'User' + str(userID+1)
    userDF = pd.DataFrame(userTimeDict[userID]).T
    #pcaVals = [list(x) for x in userTimeDict[userID].values()]
    #ax.scatter(userDF.iloc[:,0], userDF.iloc[:,1], color = 'b', s=40)
    ax.plot(userDF.iloc[:,0], userDF.iloc[:,1], '-', color = color, label = name, linewidth=4)


ax.legend()
plt.xlabel('MDS Proj 1'); plt.ylabel('MDS Proj 2')
plt.title('MDS Projection of different Search Spaces')
#plt.legend(prop={'size':20}, bbox_to_anchor=(1,1))
plt.tight_layout(pad=7)
plt.savefig('./mdsOutput.png')


