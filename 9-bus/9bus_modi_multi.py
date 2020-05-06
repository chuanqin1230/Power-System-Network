# -*- coding: utf-8 -*-
"""
Created on Thu May 03 04:27:55 2018

@author: Jinglin
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

#algorithm begin
start_time = time.time()
#clusters = louvain.louvain(graph9bus,SVQ)
end_time = time.time()
print "Time: ", end_time - start_time
print "Modularity: "#, new_mod
#print "clusters: ", clusters