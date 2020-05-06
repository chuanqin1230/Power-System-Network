# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:21:30 2018

@author: lusha
"""

import csv
import igraph
import numpy
import matplotlib.pyplot as plt
import louvain
import modification
import time


graph9bus=igraph.Graph() 
    
with open('9busnode.csv','rb') as csvfileNode:
    csvreaderNode=csv.reader(csvfileNode)
    mycsvNode=list(csvreaderNode)
    for row in mycsvNode:
        graph9bus.add_vertex(name=row[0])
        
nodeNumber=graph9bus.vcount()

Bmatrix=numpy.zeros((nodeNumber,nodeNumber))
SVQ=numpy.zeros((nodeNumber,nodeNumber))
with open('9busbranch.csv','rb') as csvfileBranch:
    csvreaderBranch=csv.reader(csvfileBranch)
    mycsvBranch=list(csvreaderBranch)
    for row in mycsvBranch:
        B=(1/complex(float(row[2]),float(row[3]))).imag
        graph9bus.add_edge(row[0],row[1])
        Bmatrix[int(row[0])-1,int(row[1])-1]=B
        Bmatrix[int(row[1])-1,int(row[0])-1]=B

#print Bmatrix
for i in range(nodeNumber):
    for j in range(nodeNumber):
        if j!=i:
            Bmatrix[i,i]=Bmatrix[i,i]-Bmatrix[i,j]
        
#print 'Bmtarix',Bmatrix     
SVQ=numpy.linalg.pinv(Bmatrix)
#print SVQ

with open('9busQ.csv','rb') as csvfileQ:
    csvreaderQ=csv.reader(csvfileQ)
    mycsvQ=list(csvreaderQ)
    for row in mycsvQ:
        #print row[1]
        graph9bus.vs.select(int(row[0])-1)["Qsupply"]=float(row[1])
        graph9bus.vs.select(int(row[0])-1)["Qdemand"]=float(row[2])



'''
# using Betweeness
vd=graph9bus.community_edge_betweenness(clusters=None, directed=True, weights=None)
mod=graph9bus.modularity(vd.as_clustering())
print 'Using Betweeness:',vd.as_clustering()
print mod

# using Label propagation
clusters=graph9bus.community_label_propagation(weights=None, initial=None, fixed=None)
mod=graph9bus.modularity(clusters)
print 'Using Label propagation',clusters
print mod
'''
# using Louvain
start_time = time.time()
clusters=graph9bus.community_multilevel()
mod=graph9bus.modularity(clusters)
#print 'Using Lovain:',clusters
#print 'mod:',mod

#louvain.louvain(graph9bus,SVQ)
newmod=modification.modification(mod,graph9bus,SVQ,clusters)
end_time = time.time()
print (end_time - start_time)
print 'new mod',newmod