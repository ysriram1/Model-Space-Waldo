# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 00:14:21 2016

@author: SYARLAG1
"""

import arff
import numpy as np
import os

os.chdir('C:/Users/SYARLAG1/Desktop/Model-Space-Waldo')

temp_fulldataSet = arff.load(open('./data/70s.arff', 'rb')) #just to test

fullDataDict = {}

dataInfoDict = {}

for fileName in os.listdir('./data'):
    timeName = fileName[:-5]
    fileLocation = './data/'+fileName
    read = arff.load(open(fileLocation, 'rb'))
    data = read['data']
    fullDataDict[timeName] = np.array(data, dtype='int8')[:,:-8]
    dataInfoDict[timeName] = np.array(data, dtype='int8')[:,-8:]



###Performing PCA on data
from sklearn.decomposition import PCA

pca = PCA(n_components=2)

PCADataDict = {}  
for key in fullDataDict.keys():
    PCADataDict[key] = pca.fit_transform(fullDataDict[key])




###Performing MDS on Data
from sklearn.manifold import MDS

mds = MDS(n_components = 2)

MDSDataDict = {}
for key in fullDataDict.keys():
    MDSDataDict[key] = mds.fit_transform(fullDataDict[key])
    
    
###########Plotting Results
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm 
plt.style.use('ggplot')


colors=cm.rainbow(np.linspace(0,1,15))

fig = plt.figure(figsize=(17,17))
ax = fig.add_subplot(111)

for color, time in zip(colors,MDSresultDict.keys()):
    name = 'User' + logID
    MDSVals = MDSresultDict[logID]
    ax.scatter(MDSVals[:,0], MDSVals[:,1], color = 'b', s=40)
    ax.plot(MDSVals[:,0], MDSVals[:,1], '-', color = color, label = name, linewidth=4)


ax.legend()
plt.xlabel('PCA Proj 1'); plt.ylabel('PCA Proj 2')
plt.title('PCA Projection of different Search Spaces')
plt.legend(prop={'size':20}, bbox_to_anchor=(1,1))
plt.tight_layout(pad=7)
plt.savefig('./TSNEOutput.png')

