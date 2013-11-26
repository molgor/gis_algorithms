#-*- coding: utf-8 -*-

#===============================================================================
# Dijkstra's algorithm for finding the optimal path along a network.
# 
# The algorithm is implented in Python with no other library dependeces 
# than the python core.
# NOTES:
# Distance -1 means infinity
# 
# '''
# Created on 22/11/2013
# 
# @author: Juan Escamilla
# '''
#===============================================================================

class Node:
    '''
    Definition for the network class
    '''
    def __init__(self,xpos=0.0,ypos=0.0,dist=0.0,path='',visited=False,idx=0,neighbors=[]):
        '''     
        Constructor of the network
        '''
        self.xpos = xpos
        self.ypos = ypos
        self.dist = dist
        self.path = path
        self.visited = visited
        self.idx = idx
        self.neighbors = neighbors
        
    def __repr__(self):
        string = "< Node: %s > : < position: X: %s, Y: %s> : <distance: %s> : < path: %s>: < visited: %s>" %(self.idx,self.xpos,self.ypos,self.dist,self.path,self.visited)
        return string
    

    def insertEdge(self,node,property):
        '''
        This method defines a relation between self node and another one.
        '''
        tupl = (self,node,property)
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

    def buildNetworkFromMatrix(self):
        """
        build the Network given the adjacency matrix. Needs refactoring.
        """
        for idx,node in enumerate(self.adj_mat):
            # Condensed pythonic syntax for filtering the neighbors and the distance.
            # enumerate function returns a tuple
            edges = filter( lambda edge : edge[1] > 0 ,[ (i,j) for i,j in enumerate(node) ]  )
            n = Node(idx=idx,dist=0.0,neighbors=edges)
            self.nodes.append(n)
        
    def initializeStateMatrix(self,StartNode_indx):
        """
        Initializes the state matrix prior to perform the Dijisktra method.
        FromNode should be a node index (integer).
        """
        # initialize t(n) <- inf for all n in N. visited node set V <- {s}
        for node in self.nodes:
            node.dist= float("inf")
            node.visited = False
        self.nodes[StartNode_indx].visited = True
        # Set t(n) <- 0
        self.nodes[StartNode_indx].distance = 0
        # For all n in N such that edge sn exists in E do
        for node in self.nodes:
            # Check if the list is empty or not.
            # Make a list of only the important nodes.
            if node.neighbors:
                SN = filter(lambda edge : edge[0] == StartNode_indx,node.neighbors)
                for neighbor in SN:
                    node.dist = neighbor[1]
#Falta para todo nodo no visitado, cambiar status. me falta ver como es que se puede escoger el nodo del final.
# Until the end node is finished.
                
    
    

        
def getDistance(DISTMAT,nodeA,nodeB):
    '''
    This function calculates the distance between node A and node B using the adjacency matrix DISTMAT
    nodeA and nodeB should be integers and are suppose to be the index in the matrix.
    The matrix is symmetric so dist(NodeA, NodeB) = dist(NodeB,NodeA).
    Satisfies the distance definition of symmetry.
    '''
    try: 
        distance = DISTMAT[nodeA][nodeB]
    except:
        error = "Error: Bad nodes definition or wrong matrix"
        print error
        distance = "NA"
    return distance

 

def initializeStateMatrix(Network,State_M,NodeA):
    """
    Initializes the state matrix prior to perform the Dijisktra method.
    NodeA should be an integer
    Network should be a symmetric matrix.
    State_M should be a state matrix.
    """
    # initialize t(n) <- inf for all n in N. visited node set V <- {s}
    node = Node(idx=NodeA, dist=0.0,visited=True)
    # For all n in N such that edge sn exists in E do
    for node in range(len(Network)):
        if Network[NodeA][node] != 0:
            node.dist = getDistance(Network,NodeA,node.idx)
             
        

def getShortestPath(Adj_Mat,State_M,NodeA,NodeB):
    """
    This gives the shortest path between nodeA and nodeB.
    It uses the Dijikstra'a algorithm.
    Adj_Mat is the adjacency matrix, State_M is the state matrix and NodeA, NodeB should be the indexes in the adjacency matrix for selecting two distinct nodes.
    """
    
    
    
 
 
        
#def main():
Adj_Mat = [
           [0,20,0,0,0,0,15,0],
           [20,0,8,9,0,0,0,0],
           [0,8,0,6,15,0,0,10],
           [0,9, 6,0,7,0,0,0],
           [0,0,15,7,0,22,18,0],
           [0,0,0,0,22,0,0,0],
           [15,0,0,0,18,0,0,0],
           [0,0,10,0,0,0,0,0]
           ]






#Construct the state matrix
#Initialize
state_mat = []
# We will use dist -1 to say that there is no connection.
for i in range(len(Adj_Mat)):
    n = Node(idx=i,dist=-1, path=0, visited = False)
    state_mat.append(n)


   
    
#if __name__ == "__main__":
#    main()

#===============================================================================
# %
# % Create the state matrix
# State_Matrix=[ Inf 0  0 ; ...
#            Inf 0  0 ; ...
#            Inf 0  0 ; ...
#            Inf 0  0 ; ...
#            Inf 0  0 ; ...
#            Inf 0  0 ; ...
#            Inf 0  0 ; ...
#            Inf 0  0 ]; 
#===============================================================================
        
        
        