# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 00:14:21 2016

@author: SYARLAG1
"""

import arff
import numpy as np
import os
import pandas as pd
import pickle

os.chdir('C:/Users/SYARLAG1/Desktop/Model-Space-Waldo')
#os.chdir('/Users/Sriram/Desktop/DePaul/Model-Space-Waldo')


# attributes of the last file have all the columns we need
lastFile = arff.load(open('./data/2000s.arff','rb'))
colNames = lastFile['attributes']
rowCount = len(lastFile['data'])

# initialize a blank dfs
dataAddDf = pd.DataFrame(np.array([[0]*(len(colNames)-8) for x in range(rowCount)]), columns=colNames[:-8])
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
timeOrdList.insert(0,'0s') #inserting 0 time into the list
######Performing PCA or MDS on the entire data
# PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
redPCAMatrix = pca.fit_transform(dfAllData)
redMat = redPCAMatrix


# MDS
## MDS is not happening on the full data, we perform is instead on the reduced data. 


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
            
allFastAndSlowUserLst = fastUsrOrdLst + slowUsrOrdLst


# Step 2: extract out only fast and slow users # SKIP This if doing MDS

userTimeDict = {}
start = 0; end = 90 # every time file had 90 users
for timeName in timeOrdList:    
    subArray = redMat[start:end]
    for userID, userIndex  in enumerate(allFastAndSlowUserLst):
        if userID not in userTimeDict.keys():
            userTimeDict[userID] = {}
        userTimeDict[userID][int(timeName[:-1])] = subArray[userIndex]
    start = end; end = start + 90


# Optional: Performing MDS (run this code bit only if MDS (AND NOT PCA) is needed)
## Subset Data
dfAllData['order'] = range(dfAllData.shape[0]) 
dfRedData = dfAllData.ix[allFastAndSlowUserLst]
currentUserOrder = dfRedData.index
dfRedData['userOrder'] = currentUserOrder  
dfRedData.index = dfRedData['order']
dfRedData.sort_index(inplace=True) #we need the new red df to be in the same order as the original one
dfRedData.index = range(dfRedData.shape[0]) 


currentUserOrder = dfRedData['userOrder'][:len(allFastAndSlowUserLst)]
currentUserOrder = list(currentUserOrder)
del dfRedData['order']; del dfRedData['userOrder']

## We now remove 3/4 or 124/166  timestamps (this is optional - done to reduce clutter in plots):
dfRedDataSub = pd.DataFrame()
lstIndices = [[x+y for y in range(24)] for x in range(0,dfRedData.shape[0],24)] 
timeIndicesToRm = []
count = 0
for timeIndex, timeChunk in enumerate(lstIndices):
    if count in [1,2,3]:
        print count
        if count == 3: 
            count = 0
            timeIndicesToRm.append(timeIndex)
            continue
        timeIndicesToRm.append(timeIndex)
        count += 1        
        continue
    dfRedDataSub = pd.concat([dfRedDataSub,dfRedData.iloc[timeChunk,:]])
    count += 1

##OPTIONAL! RUN THIS INPLACE OF PREVIOUS LOOP> We now remove 156/166 and keep on 10 timestamps (this is optional - done to reduce clutter in plots):
dfRedDataSub = pd.DataFrame()
lstIndices = [[x+y for y in range(24)] for x in range(0,dfRedData.shape[0],24)]  # we have 24 users
timeIndicesToRm = []
count = 0
for timeIndex, timeChunk in enumerate(lstIndices):
    if count in [1,2,3,4,5,6,7,8,9]: #skip all indices expect for 0
        print count
        if count == 9: 
            count = 0
            timeIndicesToRm.append(timeIndex)
            continue
        timeIndicesToRm.append(timeIndex)
        count += 1        
        continue
    dfRedDataSub = pd.concat([dfRedDataSub,dfRedData.iloc[timeChunk,:]])
    count += 1


#################

from sklearn.manifold import MDS

mds = MDS(n_components = 2, random_state=99, dissimilarity='euclidean')
redMDSMatrix = mds.fit_transform(dfRedDataSub)
redMat = redMDSMatrix

## This is done to equate all the changes
orgRedData = np.array(dfRedDataSub) #we create a numpy array

changes = 0
for i in range(1,len(orgRedData)):
    for j in range(i+1,len(orgRedData)):
        if np.sum(orgRedData[i] == orgRedData[j]) == len(orgRedData[j]):
            if np.sum(redMat[j] == redMat[i]) < len(redMat[i]):
                changes += 1
                redMat[j] = redMat[i]



## Create the data dictionary
userTimeDict = {}
start = 0; end = 24 # every time file had 24 users
for timeIndex, timeName in enumerate(timeOrdList):
    if timeIndex in timeIndicesToRm: continue    
    subArray = redMat[start:end]
    for userID, userIndex  in enumerate(allFastAndSlowUserLst):
        lstIndex = currentUserOrder.index(userIndex)
        if userID not in userTimeDict.keys():
            userTimeDict[userID] = {}
        userTimeDict[userID][int(timeName[:-1])] = subArray[lstIndex]
    start = end; end = start + 24

#########################
# Saving this to pickle
pFile = open('./waldoDataDict.pickle', 'w')
pickle.dump(userTimeDict, pFile)
pFile.close()

#Only 10 points per user
pFile = open('./waldoDataDict10.pickle', 'w')
pickle.dump(userTimeDict, pFile)
pFile.close()


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
plt.savefig('./pcaOutput_0added.png')

# MDS
fig = plt.figure(figsize=(17,17))
ax = fig.add_subplot(111)

for color, userID in zip(colors,userTimeDict.keys()):
    name = 'User' + str(userID+1)
    userDF = pd.DataFrame(userTimeDict[userID]).T
    #pcaVals = [list(x) for x in userTimeDict[userID].values()]
   # ax.scatter(userDF.iloc[:,0], userDF.iloc[:,1], color = 'b', s=40)
    ax.plot(userDF.iloc[:,0], userDF.iloc[:,1], '-', color = color, label = name, linewidth=4)


ax.legend()
plt.xlabel('MDS Proj 1'); plt.ylabel('MDS Proj 2')
plt.title('MDS Projection of different Search Spaces')
#plt.legend(prop={'size':20}, bbox_to_anchor=(1,1))
plt.tight_layout(pad=7)
plt.savefig('./mdsOutput_vectorReplaced_subset.png')


