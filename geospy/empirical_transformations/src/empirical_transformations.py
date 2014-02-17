#-*- coding: utf-8 -*
#===============================================================================
# Empirical Transformations
# This program transforms a set of coordinates from two different referencing 
# system using an affine transformation.
# Two diferent methods are used to get the correct affine parameters 
# (as decribed in Harrie, 2013. Lecture Notes: Empirical transformations. ) 
# 
# '''
# Created on 18/12/2013
# a
# @author: Juan Escamilla
# '''
#===============================================================================

from numpy import matrix as mat 
from numpy import arctan,cos,sin
from numpy import sqrt
class Point:
    """
    Just for an easier data handle
    """
    def __init__(self,id=0,X=0.0,Y=0.0,x=0.0,y=0.0):
        self.id = id
        self.X = X
        self.Y = Y
        self.x = x
        self.y = y
        self.Tx = 0.0
        self.Ty = 0.0


    def __repr__(self):
        return "< Point %s X: %s Y: %s, Tx: %s, Ty: %s >" %(self.id,self.X,self.Y,self.Tx,self.Ty)


def xyToAffine(x,y,dic_parameters):
    """
    This function transform the coordinates from xy to affine coordinates.
    Using the parameters of angle (alpha), scale on x axis (mx), scale on y axis (my)
    translation vector (X0 and Y0) and shear angle (beta).
    THIS METHOD IS USED WHEN THE NUMBER OF GCP POINTS IS SIX.
    """
    X = dic_parameters['X0']+(x*dic_parameters['mx']*cos(dic_parameters['alpha']))-(y*dic_parameters['my']*sin(dic_parameters['alpha']+dic_parameters['beta']))
    Y = dic_parameters['X0']+(x*dic_parameters['mx']*sin(dic_parameters['alpha']))+(y*dic_parameters['my']*cos(dic_parameters['alpha']+dic_parameters['beta']))
    return X,Y

def xyToAffineRaw(x,y,a,b):
    """
    This function transform the coordinates from xy to affine coordinates.
    Using the parameters obtained from the least square method on a overdetermined
    linear equation system.
    THIS METHOD IS USED WHEN THE NUMBER OF GCP POINTS IS GREATER THAN SIX.
    a and b are a dictionaries of the form a0, a1, a2 and b0,b1,b2 respectively. 
    """
    X = a['a0'] + a['a1']*x + a['a2']*y
    Y = b['b0'] + b['b1']*x + b['b2']*y   
    return X,Y


def calculateAffineParameters(point1,point2,point3):
    """
    Solves the linear system equation.
    Take six ground points and calculates the affine parameters.
    returns dictionary the parameters: X0,Y0,mx,my,alpha,beta
    """
    M = mat([[1,1,1],[point1.x,point2.x,point3.x],[point1.y,point2.y,point3.y]])
    X = mat([[point1.X,point2.X,point3.X]]).transpose()
    Y = mat([[point1.Y,point2.Y,point3.Y]]).transpose()
    # M.I is the inverse of M
    # Compute MI*X = A
    A = M.I*X
    B = M.I*Y
    return A,B
    
def calculateStdParameters(A,B):
    """
    Receives two transposed vectors (matrix)
    returns a dictionary of the parameters X0,Y0,mx,my,alpha,beta
    """
    AL = A.tolist()
    BL = B.tolist()
    a0 = AL[0]#.pop()
    a1 = AL[1]#.pop()
    a2 = AL[2]#.pop()
    b0 = BL[0]#.pop()
    b1 = BL[1]#.pop()
    b2 = BL[2]#.pop()
    
    X0 = a0
    Y0 = b0
    alpha = arctan(b1/a1)
    beta = arctan(-a2/b2) - arctan(b1/a1)
    mx = sqrt((a1*a1) + (b1*b1))
    my = sqrt((a2*a2) + (b2*b2))
    
    return {'X0':X0,'Y0':Y0,'alpha':alpha,'beta':beta,'mx':mx,'my':my}
    
    

def computeAffineParams(triplete_of_points):
    t1 = triplete_of_points[0]
    t2 = triplete_of_points[1]
    t3 = triplete_of_points[2]
    A,B = calculateAffineParameters(t1,t2,t3)
    dicio = calculateStdParameters(A,B)
    return dicio 


def transformAllpoints_fromTriplet(triplet,points):
    """
    Given a set of three gcp (triplet) the program calculates the affine parameters and perform
    change of coordinate from cartesian to affine. 
    Also, this function calculates the RMS of the transformation.
    Returns: list of converted points and dictionary of parameters
    """
    def RMS(points):
        """
        Compute the Root Mean Square error estimator
        """
        # Combo all in one!
        RMS = sqrt(reduce(lambda p,q : p + q , map(lambda p: (p.X - p.Tx)**2 + (p.Y - p.Ty)**2, points))/((2*(len(points))) - 6))
        return RMS
        
    
    XY_List = []
    dic = computeAffineParams(triplet)
    #ny_points = filter(lambda p : p not in triplet,points)
    ny_points = points
    for point in ny_points:
        X,Y = xyToAffine(point.x,point.y,dic)
        point.Tx = X
        point.Ty = Y
        XY_List.append((X,Y))
    
    rms = RMS(ny_points)
    return XY_List,rms


def convertPoints(points, parameters_dic):
    """
    Converts the points from one coordinate system into another one using the affine parameters defined in the parameters_dic data structure.
    """
    for point in points:
        x = point.x
        y = point.y
        X,Y = xyToAffine(x,y,parameters_dic)
        point.Tx = X
        point.Ty = Y
    return True

def applyToAllPoints(points,a,b):
    """
    Converts all coordinates to the new system.
    Used in the lsqr method
    """
    for point in points:
        x = point.x
        y = point.y
        X,Y = xyToAffineRaw(x,y,a,b)
        point.Tx = X
        point.Ty = Y
    return True    

def fitLine(points):
    """
    CAlculates the least square Matrix
    """
    from numpy import array, vstack,linalg, ones
    x = array(map(lambda p : p.x, points))
    y = array(map(lambda p : p.y, points))
    X = array(map(lambda p : p.X, points))
    Y = array(map(lambda p : p.Y, points))
    A = vstack([x,y,ones(len(x))]).T
    #mx = linalg.lstsq(A, X)
    #my = linalg.lstsq(A, Y)
    a1,a2,a0 = linalg.lstsq(A, X)[0]
    b1,b2,b0 = linalg.lstsq(A, Y)[0]
    a = {'a1' : a1,'a2' : a2,'a0' : a0}
    b = {'b1' : b1,'b2' : b2,'b0' : b0}
    return a,b

def calculateRMSof(points):
        """
        Compute the Root Mean Square error estimator
        """
        # Combo all in one!
        RMS = sqrt(reduce(lambda p,q : p + q , map(lambda p: (p.X - p.Tx)**2 + (p.Y - p.Ty)**2, points))/((2*(len(points))) - 6))
        return RMS
    



def main():
    #Read file
    path = 'gcp.txt'
    F = open(path,'r')
    rawD = F.readlines()
    F.close()
    points = []
    for row in rawD:
        l = [ float(i) for i in row.split() ] 
        p = Point(id=l[0],X=l[1],Y=l[2],x=l[3],y=l[4])
        points.append(p)
   
    a,b = fitLine(points) 
    applyToAllPoints(points,a,b)
    rms = calculateRMSof(points)
    print "Coordinates transformations using affine function \n"
    for point in points:
        print str(point) + "\n"
    print "X0 and Y0 are the known (target) coordinates"
    print "Tx and Ty are the coordinates transformed empirically."
    print "Standard Error of the transformation (RMS) : %s " %rms

#===============================================================================
if __name__ == "__main__":
    main()
#===============================================================================
