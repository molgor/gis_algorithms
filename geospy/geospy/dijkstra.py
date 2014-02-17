#-*- coding: utf-8 -*-

#===============================================================================
# Dijkstra's algorithm for finding the optimal path along a network.
# 
# The algorithm is implented in Python with no other library dependencies 
# than the python core and sys just for passing arguments.
# The class Node has as attributes the ones defined in the state matrix.
# A State Matrix wasn't used in this Dijsktra implementation.
# It is used implicitly in the objects atribute.
# Usage: python dijkstra startNode endNode
# NOTES:
# 
# 
# '''
# Created on 22/11/2013
# a
# @author: Juan Escamilla
# '''
#===============================================================================

class Node:
    '''
    Definition for the network class
    '''
    def __init__(self,xpos=0.0,ypos=0.0,distance=0.0,path=[],visited=False,idx=0,neighbors=[]):
        '''     
        Constructor of the network
        '''
        self.xpos = xpos
        self.ypos = ypos
        self.distance = distance
        self.path = path
        self.visited = visited
        self.idx = idx
        self.neighbors = neighbors
        
    def __repr__(self):
        string = "< Node: %s > : < position: X: %s, Y: %s> : <distance: %s> : < path: %s>: < visited: %s>" %(self.idx,self.xpos,self.ypos,self.distance,self.path,self.visited)
        return string
    
    def getDistanceFrom(self,node):
        """
        Returns the distance from self to node.
        If the edge between self and node does not exist distance will be infinity.
        node should be integer.
        """
        try:
            distance = filter(lambda nodex : nodex[0] == node , self.neighbors).pop()[1]
        except:
            distance = float("inf")
            print "Edge not found assuming infinity distance. \n"
        return distance

    def insertEdge(self,node,_property):
        '''
        This method defines a relation between self node and another one.
        '''
        tupl = (self,node,_property)
        self.neighbors.append(tupl)
        return tupl
    
class Network:
    
    def __init__(self):
        self.adj_mat = [
           [0,20,0,0,0,0,15,0],
           [20,0,8,9,0,0,0,0],
           [0,8,0,6,15,0,0,10],
           [0,9, 6,0,7,0,0,0],
           [0,0,15,7,0,22,18,0],
           [0,0,0,0,22,0,0,0],
           [15,0,0,0,18,0,0,0],
           [0,0,10,0,0,0,0,0]
           ]
        self.state_mat = []
        self.nodes = []
        self.buildNetworkFromMatrix()
        self.startNode_idx = 0
        self.currentdistance = 0

    def buildNetworkFromMatrix(self):
        """
        Converts an adjacency matrix in a listed network definition.
        Build the Network given the adjacency matrix. Needs refactoring.
        """
        for idx,node in enumerate(self.adj_mat):
            # Condensed pythonic syntax for filtering the neighbors and the distance.
            # enumerate function returns a tuple
            # This function selects just the connected nodes.
            edges = filter( lambda edge : edge[1] > 0 ,[ (i,j) for i,j in enumerate(node) ]  )
            n = Node(idx=idx,distance=0.0,neighbors=edges,path=[])
            self.nodes.append(n)
        
    def initializeStateMatrix(self,StartNode_indx):
        """
        Initializes the state matrix prior to perform the Dijisktra method.
        FromNode should be a node index (integer).
        """
        # initialize t(n) <- inf for all n in N. 
        for node in self.nodes:
            node.distance= float("inf")
            node.visited = False
        # visited node set V <- {s}    
        self.nodes[StartNode_indx].visited = True
        self.startNode_idx = StartNode_indx
        self.nodes[StartNode_indx].path.append(StartNode_indx)
        # Set t(n) <- 0
        self.nodes[StartNode_indx].distance = 0
        # For all n in N such that edge sn exists in E do
        for node in self.nodes:
            # Check if the list is empty or not.
            # Make a list of only the important nodes.
            if node.neighbors:
                # Such that edge sn exists in E do:
                SN = filter(lambda edge : edge[0] == StartNode_indx,node.neighbors)
                for neighbor in SN:
                    node.distance = neighbor[1]

    def findShortestPath(self,NodeB):
        """
        Performs calculation of shortest path between first node (declared during initialization of state matrix.
        See: self.initializeStateMatrix(StartNode)
        This method implements the Dijisktra method. The algorithm is explained in the code itself.
        NodeB needs to be a valid index integer.
        """
        # while N != V do
        N_minus_V = filter(lambda node: not node.visited, self.nodes)
        self.state_mat.append(self.startNode_idx)
        while (len(N_minus_V) > 0) and (not self.nodes[NodeB].visited):           
            # Sort by distance
            N_minus_V = filter(lambda node: not node.visited, self.nodes)
            N_minus_V.sort(key=lambda node:node.distance)
            current_node = N_minus_V.pop(0)
            #print  "current node index: %s" %current_node.idx
            # Add n to V
            current_node.visited = True
            # for all m in N/V such that edge nm exists do
            for node in N_minus_V:
                if node.neighbors:
                    NM = filter(lambda edge : edge[0] == current_node.idx,node.neighbors)
                    if NM:
                        for edge in NM:
                            #edge is a tuple of the form (indx,distance).
                            m = node.idx
                            ## Append the node in path
                            if (current_node.distance + edge[1]) < self.nodes[m].distance:
                                self.nodes[m].distance = current_node.distance + edge[1]
                                self.nodes[m].path.append(current_node.idx)
                                self.state_mat.append(current_node.idx)
                         
        return NM
 

    def cleanPathList(self,path):
        """
        This function cleans the path. returning the shortest path that was found with the Dijisktra algoritm.
        """
        newpath = []
        node = path.pop()
        newpath.append(node)
        while path:
            previous_node = path.pop()
            #print "previousn "+str(previous_node)
            for neighbor in self.nodes[node].neighbors:
               # print "neighbor "+str(neighbor[0])
                if neighbor[0] == previous_node:
                    newpath.append(node)
                node = previous_node
        newpath.append(self.startNode_idx)
        newpath.reverse()
        newpath = list(set(newpath))
        return newpath
                     
        
       
def main(startNode,endNode):
    N = Network()
    N.initializeStateMatrix(startNode)
    J=N.findShortestPath(endNode)
    J=[]
    return N,J

from sys import argv as arguments    
if __name__ == "__main__":
    start_node = int(arguments[1])-1
    end_node = int(arguments[2])-1
    N,J = main(start_node,end_node)
    nw_st = start_node + 1
    nw_ed = end_node + 1
    head = "Find shortest route between %s and %s \n" %(nw_st,nw_ed)
    h2 = "Using Dijkstra method. \n"
    #Sorry I didn't figure out a more elegant solution.
    # First filter visited nodes
    visited = filter(lambda node: node.visited, N.nodes)
    # Now, make a union of the paths. All in one hit wonder!
    paths_tmp = reduce(lambda path1,path2 : path1 + path2 , map(lambda node: node.path, visited))
    # Take away node repetition. It is a shortest path tree, no circuits allowed
    paths = list(set(paths_tmp))
    # Add end node
    paths.append(end_node)
    cleaned_path=N.cleanPathList(paths)
    new_path = map(lambda node : node + 1, cleaned_path)
    h3 = "Optimal route: %s \n" %new_path
    h4 = "Total distance covered: %s \n" %N.nodes[end_node].distance
    print head + h2 + h4 + h3
#===========================================================================
