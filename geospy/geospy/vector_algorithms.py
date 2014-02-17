#-*- coding: utf-8 -*-

#===============================================================================
# Implementation of the point in polygon algorithm using the side function
# Uses the Node class definition inside dijkstra module.
# ''' created on
# 
# @author: Juan Escamilla
# '''
#===============================================================================

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from random import random as rand
from dijkstra import Node

class Polygon:
    """
    This class defines the polygon object.
    """
    
    def __init__(self,ordered_list_of_nodes=[],subplot_object=[],name=0):
        """
        Polygon constructor.
        """
        # Create an order list of Nodes
        self.vertices = ordered_list_of_nodes
        self.subplot = subplot_object
        self.edges =[]
        self.name = name
    
    def pukeVertices(self):
        """
        Returns an order list of coordinates of each vertex in the polygon.
        """
        return map(lambda node : (node.xpos,node.ypos),self.vertices)
        
    def __repr__(self):
        nodes = []
        for n in self.vertices:
            nodes.append(n.idx)
        return str(nodes)
        #return str(self.pukeVertices())
    
    def defineEdges(self):
        """
        links neighboring nodes.
        """
        v_list = self.pukeVertices()
        self.edges = []
        for i in range(len(v_list)-1):
            simplex = (v_list[i],v_list[i+1])
            self.edges.append(simplex)
        
         
    
    def Plot(self,color=[]):
        """
        Add polygon to the canvas.
        """
        if not color:
            poly = patches.Polygon(self.pukeVertices(),fc=(rand(),rand(),rand()))
        else: 
            poly = patches.Polygon(self.pukeVertices(),fc='r')
        self.subplot.add_patch(poly)

    def getArea(self):
        """
        Calculate the area of the polygon.
        """
        ordered_list_of_vertex = self.pukeVertices()
        area = 0.0
        for i in range(len(ordered_list_of_vertex)-1):
            # Harrie area formula
            #area += ordered_list_of_vertex[i][1]*(ordered_list_of_vertex[i+1][0]-ordered_list_of_vertex[i-1][0])
            # Worboys area formula
            area += (ordered_list_of_vertex[i][0]*ordered_list_of_vertex[i+1][1]) - (ordered_list_of_vertex[i+1][0]*ordered_list_of_vertex[i][1])
        area /= 2.0
        return area
    
    def get_externalAreaOf(self,ordered_list_of_vertex):
        """
        Calculate the area of a polygon not involving common nodes.
        ordered_list_of_vertex needs to be a boundary of a polygon.
        """
        area = 0.0
        for i in range(len(ordered_list_of_vertex)-1):
            # Worboys formula
            area += (ordered_list_of_vertex[i][0]*ordered_list_of_vertex[i+1][1]) - (ordered_list_of_vertex[i+1][0]*ordered_list_of_vertex[i][1])
            # Harrie formula
            #area += ordered_list_of_vertex[i][1]*(ordered_list_of_vertex[i+1][0]-ordered_list_of_vertex[i-1][0])
        area /= 2.0
        return area        
        
    def side(self,line,point):
        """
        Side function. 
        line is an order list (x1,y1),(x2,y2) meaning that is an arc that goes from point (x1,y1) to point (x2,y2).
        point should be a tuple (x,y)
        returns:
            -1 if the point is on the left of the line.
            0 if is colinear.
            1 if it is on the right.
        """
        # Build the polygon.
        list_v = [node for node in line]
        list_v.append(point)
        list_v.append(line[0])
        #print list_v 
        area = self.get_externalAreaOf(list_v)
        if area < 0:
            # for debugging purposes 
            #print "point %s is on the left side of %s:" %(point,line)
            return -1
        elif area == 0:
            # for debugging purposes
            #print "point %s colinear to the line: %s" %(point,line)
            return 0
        else:
            # for debugging purposes
            #print "point %s is on the right side %s:" %(point,line)
            return 1        
        
    
    def getLineFromPoint(self,point):
        """
        creates a semi-line parallel to the x axis that passes through point
        """
        x = point[0]
        y = point[1]
        xmin,xmax = self.subplot.get_xlim()
        line = [(x,y),(xmax,y)]
        return line
    
    def edgeIntersectsLine(self,edge,line):
        """
        True if line intersects edge.
        """
        a = edge[0]
        b = edge[1]
        c = line[0]
        d = line[1]
        
        abc = self.side(edge,c)
        abd = self.side(edge,d)
        cda = self.side(line,a)
        cdb = self.side(line,b)
        
        if (abc != abd) and (cda != cdb):
            # for debugging purposes
            #print "Edge %s intersected with line %s" %(edge,line)
            return 1
        else:
            return 0
        
        
    
    def isPointInside(self,point):
        """
        Check if the point (tuple) is inside the polygon.
        """
        self.defineEdges()
        count = 0
        for edge in self.edges:
            lineofp = self.getLineFromPoint(point)
            count += self.edgeIntersectsLine(edge, lineofp)
        # If it is odd then is inside the polygon. Jordan theorem 
        if count %2 == 1:
            return True
        else:
            return False
           

#===============================================================================
# def calculateArea(ordered_list_of_vertex):
#     """
#     Given a closed linear-piecewise polyline.
#     This function returns its area. 
#     """
#     area = 0.0
#     for i in range(len(ordered_list_of_vertex)-1):
#         area += (ordered_list_of_vertex[i][0]*ordered_list_of_vertex[i+1][1]) - (ordered_list_of_vertex[i+1][0]*ordered_list_of_vertex[i][1])
#         #area += ordered_list_of_vertex[i][1]*(ordered_list_of_vertex[i+1][0]-ordered_list_of_vertex[i-1][0])
#     area /= 2
#     return area
# 
# def side(arc_line,point):
#     """
#     Side function. 
#     arc_line is an order list (x1,y1),(x2,y2) meaning that is an arc that goes from point (x1,y1) to point (x2,y2).
#     point should be a tuple (x,y)
#     returns:
#         -1 if the point is on the left of the line.
#         0 if is colinear.
#         1 if it is on the right.
#     """
#     # Build the polygon.
#     list_v = [node for node in arc_line]
#     list_v.append(point)
#     list_v.append(arc_line[0])
#     #print list_v 
#     p = Polygon(ordered_list_of_nodes = list_v)
#     area = calculateArea(list_v)
#     if area < 0:
#         #print "point %s,%s is on the left side:" %point
#         return -1
#     elif area == 0:
#         #print "point %s,%s colinear to the line:" %point
#         return 0
#     else:
#         #print "point %s,%s is on the right side:" %point
#         return 1
#===============================================================================
    

        
def putText(s):
    #print(s)
    plt.title(s,fontsize=16)
    plt.draw()

def makepol(edge,point):
    pol = [node for node in edge]
    pol.append(point)
    pol.append(edge[0])
    return pol


def main():
    """
    This is the main function. PArsing instructions, plotting commands, etc.
    """
    # import text files
    coords_f = open("data/coord.txt","r")
    polys_f = open("data/polygons_oriented.txt","r")
    # Parse file
    coordsl = coords_f.readlines()
    polysl = polys_f.readlines()
    # close text files
    coords_f.close()
    polys_f.close()
    # Matplot lib objects
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_xlim(100,500)
    ax.set_ylim(0,500)


    nodes = []
    polygons = []
    #Instanciate nodes
    for indx,i in enumerate(coordsl):
        xy = i.split(" ")
        n=Node(xpos=int(xy[0]),ypos=int(xy[1]),idx=(indx+1))
        nodes.append(n)
    p = []
    # clear 0 in the list
    for row in polysl:
        p.append(filter(lambda number: int(number) != 0,row.split(" ")))

    idx = 0
    for polygon_def in p:
        node_list = []
        for node_def in polygon_def:
            # filter nodes such that index corresponds to the definition of node_def
            node_list.append(filter(lambda n : n.idx == int(node_def),nodes).pop())
        polygons.append(Polygon(ordered_list_of_nodes=node_list,subplot_object=ax,name=idx+1))
        idx += 1

    for polygon in polygons:
        polygon.Plot()
        
    _exit = False
    while not _exit:
        intersected_polys = []
        xy_l = plt.ginput()
        try:
            point = xy_l.pop()
        except:
            point = []
            _exit = True
        print "Point selected: %s: " %str(point)
        intersected_polys = filter(lambda poly : poly.isPointInside(point),polygons)
        try:
            for p in intersected_polys:
                polyname = p.name
                print "Point inside polygon %s" %polyname
                print "Selected polygon with area: %s" %p.getArea()
                p.Plot()  
                putText("Selected polygon is: %s" %polyname)
        except:
            print "Point outside of every polygon"
        print "Continue clicking polygons or press any key to quit."
        _exit = plt.waitforbuttonpress()
  
if __name__ == "__main__":
    main()  