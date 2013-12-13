#-*- coding: utf-8 -*-
import networkx as nx
G = nx.Graph()
adj_mat = [
           [0,20,0,0,0,0,15,0],
           [20,0,8,9,0,0,0,0],
           [0,8,0,6,15,0,0,10],
           [0,9, 6,0,7,0,0,0],
           [0,0,15,7,0,22,18,0],
           [0,0,0,0,22,0,0,0],
           [15,0,0,0,18,0,0,0],
           [0,0,10,0,0,0,0,0]
           ]

for i in range(len(adj_mat)):
    G.add_node(i)


    
for id,row in enumerate(adj_mat):
    edges = filter( lambda edge : edge[1] > 0 ,[ (i,j) for i,j in enumerate(row) ]  )    
    for edge in edges:
        G.add_edge(id,edge[0],weight=edge[1])
    
    
pos=nx.spring_layout(G)
nx.draw(G,pos)
nx.draw_networkx_edge_labels(G,pos)
