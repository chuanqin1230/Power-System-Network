# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 13:50:33 2018

@author: Jinglin
"""

import os
from pygrid import *
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn import cluster, datasets, mixture
import modification

def louvain(graph_silm,SQV):

    #set default weight value
    graph_silm.es['weight'] = 1.0
    edge_weight = graph_silm.es['weight']
    #print graph_silm.es['weight']
    
    
    #get adjacency matrix of weighted graph
    adjacency_matrix = graph_silm.get_adjacency(attribute='weight')
    #print adjacency_matrix
    
    
    #node value/weight: the edges connected to the node
    node_value = []
    for node in graph_silm.vs:
        node_value.append(sum(adjacency_matrix[node.index]))
    graph_silm.vs["node_value"] = node_value
    #print node_value
    
    
    #calculate total edge weight
    #resolution = 1/total_edge_weight
    total_edge_weight = 0.0
    for i in range(graph_silm.vcount()):
        total_edge_weight += sum(adjacency_matrix[i])
    print total_edge_weight
    
    ''' 
       IGraph library.
       Copyright (C) 2006-2012  Gabor Csardi <csardi.gabor@gmail.com>
       334 Harvard street, Cambridge, MA 02139 USA
    '''
    
    #the level of alg
    multi_level = 1 #3
    resolution1 = 1.0
    resolution2 = resolution1/total_edge_weight #use standard modularity function
    random_starts_number = 1 #10
     
    
    #New graph with all nodes from graph_silm
    #Initial network each node as a cluster
    copy_graph_silm = graph_silm.as_undirected()
    copy_graph_silm.delete_edges(None)
    #print copy_graph_silm.vcount()
    
    
    #get the initial clusters, 1 node as 1 clusters
    initial_clusters = copy_graph_silm.clusters()
    #print initial_clusters
    
    
    #node_list has the node order, node neighbors has its neighbors' list
    node_list = graph_silm.vs['name']
    node_neighbors = []
    for i in node_list:
        node_neighbors.append(graph_silm.neighbors(i))
    #print node_neighbors
    
    
    #Louvain begin
    for level in range(multi_level):
        clusters_weight = np.zeros(len(initial_clusters))
        for one_cluster in initial_clusters:
            #print one_cluster        
            for vertex_index in one_cluster:
                clusters_weight[one_cluster] += node_value[vertex_index]
                #print copy_graph_silm.vs.select(vertex_index)['name']
                #print node_value[vertex_index]
				#print clusters_weight'''
    
    #max modularity
    max_modularity = -10000
    #random seed 0, each time random the same value
    random.seed(10)
    random_value = random.random()
    
    for i in range(random_starts_number):
        if (random_starts_number > 1):
            print 'No.' + (i+1) + ' Random Start'
        
        #New graph with all nodes from graph_silm
        #Initial network each node as a cluster
        new_copy_graph_silm = graph_silm.as_undirected()
        new_copy_graph_silm.delete_edges(None)
        #print copy_graph_silm.vcount()
        
        #get the initial clusters, 1 node as 1 clusters
        new_initial_clusters = copy_graph_silm.clusters()
        #print initial_clusters
        
        j = 0
        update_flag = 1 #True
        
        #into the the multi-level loop
        while ((j < multi_level) and update_flag):
            if (multi_level > 1):
                print 'No.' + (multi_level+1) + 'multilevel'
            #update the update_flag
            update_flag = update_flag_with_random(graph_silm, new_initial_clusters, random_value)
            #print update_flag

def update_flag_with_random(graph_silm, new_initial_clusters, random_value):
    if (graph_silm.vcount() == 1):
        return 0
    update_flag = local_moving_alg(graph_silm, new_initial_clusters, random_value)

    if (clustering_n_clusters < n_nodes):
        update_flag2 = local_moving_alg(graph_silm, new_initial_clusters, random_value)

        if (update_flag2 == 1):
            update_flag = 1
            clustering.merge_clusters(clustering)

    return update
	
    
    
def local_moving_alg(graph_silm, new_initial_clusters, random_value):
    if (graph_silm.vcount() == 1):
        return 0
    update_flag = 0
    clusters_weight = np.zeros(len(new_initial_clusters))
    for one_cluster in new_initial_clusters:
        #print one_cluster        
        for vertex_index in one_cluster:
            clusters_weight[one_cluster] += graph_silm.vs.select(vertex_index)['node_value']
    print list(clusters_weight)
    
    #absent for unused clusters 
    
    #get an index of random list of node
    random_node_T = []
    for i in graph_silm.vs:
        random_node_T.append(i.index)
    #print list(random_node_T)
    random.shuffle(random_node_T)
    #print random_node_T
    
    #first neighbor index
    first_neighbor_index = []
    temp_edges = 0
    for i in graph_silm.vs:
        first_neighbor_index[i] = temp_edges
    
    stable_nodes_number = 0
    index = 0
    while(stable_nodes_number < graph_silm.vcount()):
        j = random_node_T[index]
        neighbor_clusters_number = 0
		
		for k in range(first_neighbor_index[j]):
			if (k < first_neighbor_index[j + 1]):
                l = clustering_cluster[network_neighbor[k]]
                if (edgeWeightPerCluster[l] == 0):
                    neighboring_cluster[n_neighboring_clusters] = l
                    n_neighboring_clusters++
                edge_weightPer_cluster[l] += edge_weight[k]

            cluster_weight[clustering_cluster[j]] -= node_weight[j]
            n_nodes_per_cluster[clustering_cluster[j]]= n_nodes_per_cluster[clustering_cluster[j]] - 1
            if (n_nodes_per_cluster[clustering-cluster[j]] == 0):
                unusedCluster[n_unused_clusters] = clustering_cluster[j]
                n_unused_clusters = n_unused_clusters + 1

            best_cluster = -1
            max_quality_function = 0
            for k in range(n_neighboring_clusters[j]):
                l = neighboring_cluster[k]
                quality_function = edge_weight_per_cluster[l] - node_weight[j] * cluster_weight[l]
                if ((quality_function > max_quality_function) or ((quality_function == max_quality_function) and (l < best_cluster))):
                    best_cluster = l
                    max_quality_function = quality_function
                edge_weight_per_cluster[l] = 0
            
            if (max_quality_function == 0):
                best_cluster = unused_cluster[n_unused_clusters - 1]
                n_unused_clusters--

            cluster_weight[best_cluster] += node_weight[j]
            n_nodes_per_cluster[best_cluster]++
            if (best_cluster == clustering_cluster[j]):
                stable_nodes_number++
            else:
                clustering_cluster[j] = best_cluster
                stable_nodes_number = 1
                update_flag = 1
				
		new_cluster = new int[n_nodes]
        clustering_n_clusters = 0
        for i in range(n_nodes):
            if (n_nodes_per_cluster[i] > 0):
                new_cluster[i] = clustering_n_clusters
                n_clusters++
        for i in range(n_nodes):
            clustering_cluster[i] = new_cluster[clustering_cluster[i]]
			
	return update_flag