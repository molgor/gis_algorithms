#-*- coding: utf-8 -*
#===============================================================================
# This program geocodes a landsat image in rst format.
# Change the coordinate system using affine transformations and
# make bilinear and nearest neighbors resampling.
# produce two images of the sampled data. 
#
# '''
# Created on 04/01/2014
# @author: Juan Escamilla
# '''
#===============================================================================
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm 
import empirical_transformations as et

class Pixel:
    """
    Pixel object for the geocoded image
    """
    def __init__(self,x=0,y=0,value=0,GRCS='RT90'):
        self.x = x
        self.y = y
        self.value = value
#         Geodetic Reference Coordinate System
        self.GRCS =  GRCS
    
    def __repr__(self):
        return "< Pixel > x:  %s, y: %s , value: %s </Pixel>" %(self.x,self.y,self.value)
        
class GeoImage:
    """
    Class that defines a georeferenced image.
    """
    def __init__(self,pixel_list,res=1):
        # pixel list is a list of list of pixels
        self.ML = pixel_list
        self.min = (pixel_list[0][0].x,pixel_list[0][0].y)
        self.max = (pixel_list[len(pixel_list)-1][len(pixel_list[0])-1].x,pixel_list[len(pixel_list[0])-1][len(pixel_list[0])-1].y)
#         self.M = self.getMatrixForm()
        self.res = res
#     My first decorator!!
    
    @property
    def M(self):
        """
        return the numpy matrix representation of geoImage.
        """
        mat = []
        for row in self.ML:
            i = []
            for pixel in row:
                i.append(pixel.value)
            mat.append(i)
        m = np.matrix(mat)
        return m 

    @property
    def MCoord(self):
        """
        return the numpy matrix representation of coordinates.
        """
        mat = []
        for row in self.ML:
            i = []
            for pixel in row:
                i.append(complex(pixel.x,pixel.y))
            mat.append(i)
        m = np.matrix(mat)
        return m
    
    
    def display(self,monitor):
        """
        Displays the image.
        Uses the matplotlib library
        """
        f = plt.figure(monitor)
#        plt.imshow(self.M,cmap=cm.gist_yarg,extent=[self.min[0],self.max[0],self.min[1],self.max[1]])
        
        plt.imshow(self.M,cmap=cm.gist_yarg)

        #plt.show() 
        return f
    
    def reflect_Y(self):
        """
        Reflects the matrix using the x axis so that it will be concordant with the standard input.
        """
        tmp = [row for row in self.ML[len(self.ML)-1:0:-1]]
        self.ML = tmp
        
    def nearestNeighborResampleFrom(self,affine_parms,orig_img):
        """
        Performs a nearest neighbor resampling and updates this image.
        """
        a = affine_parms['a']
        b = affine_parms['b']
        for bi,row in enumerate(self.ML):
            perc =float(bi) / len(self.ML)*100
            perc = int(perc)
            sys.stdout.write("\r Calculating nearest neighbor resampling %s " %perc)    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()
            #print ("% s % Nearest Neighbor resampling" %perc),            
            for bj,pixel in enumerate(row):
                j,i = et.affineToxy(pixel.x,pixel.y, a, b)
                i = int(i)
                j = int(j)
                if (i >= 0 and j >= 0) and i < len(orig_img.ML) and j < len(orig_img.ML[i]):
                    pixel.value = orig_img.ML[i][j].value
                    #pixel.value = orig_img.ML[i][(len(orig_img.ML[0])-1)-j].value
                    #blank_img.ML[bi][bj].value = orig_img.ML[i][j].value
                else:
                    pixel.value = 0
                    #print "otro %s, %s" %(i,j)
        print "\n"
        self.reflect_Y()
        return 1        
    def bilinearResampleFrom(self,affine_parms,orig_img):
        """
        Performs a bilinear resampling and updates this image.
        """
        def calculate_bilinear(xp,yp,gs_list):
            p0 = gs_list[0][0],gs_list[0][1]
            dx = 1.0
            dy = 1.0
            u = xp-p0[1] / dx
            w = yp-p0[0] / dy
            if len(gs_list) == 4:
                g1 = gs_list[0][2]
                g2 = gs_list[1][2]
                g3 = gs_list[2][2]
                g4 = gs_list[3][2]
            elif len(gs_list) == 3:
                g1 = gs_list[0][2]
                g2 = gs_list[1][2]
                g3 = gs_list[2][2]
                g4 = gs_list[0][2] 
            elif len(gs_list) == 2:
                g1 = gs_list[0][2]
                g2 = gs_list[1][2]
                g3 = gs_list[0][2]
                g4 = gs_list[1][2]
            elif len(gs_list) == 1:
                g1 = gs_list[0][2]
                g2 = gs_list[0][2]
                g3 = gs_list[0][2]
                g4 = gs_list[0][2]  
            from numpy import matrix as mt
            U = mt([u,1-u])
            W = mt([1-w,w]).transpose()
            G=mt([[g3,g4],[g1,g2]])      
            return float(U*G*W)
            
        a = affine_parms['a']
        b = affine_parms['b']
        l=[]
        for bi,row in enumerate(self.ML):
            perc = float(bi) / len(self.ML)*100
            perc = int(perc)
            sys.stdout.write("\r Calculating bilinear resampling %s " %perc)    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()
            for bj,pixel in enumerate(row):
                y,x = et.affineToxy(pixel.x,pixel.y, a, b)
                i = int(x)
                j = int(y)
                gs = [(i,j),(i+1,j),(i,j+1),(i+1,j+1)]
                if (i >= 0 and j >= 0):
                    if i < len(orig_img.ML) -1 and j < len(orig_img.ML[i]) -1:
                        vals = []
                        for i,j in gs:
                            vals.append((j,i,orig_img.ML[i][j].value))
                        pixel.value = calculate_bilinear(x,y,vals)                  
                    elif i == len(orig_img.ML) -1  and j < len(orig_img.ML[i]) -1:
                        gs = [(i,j),(i,j+1)]
                        vals = []
                        for i,j in gs:
                            vals.append((j,i,orig_img.ML[i][j].value))
                        pixel.value = calculate_bilinear(x,y,vals)
                    elif i < len(orig_img.ML) -1 and j == len(orig_img.ML[i]) -1 :
                        gs = [(i,j),(i+1,j)]
                        vals = []
                        for i,j in gs:
                            vals.append((j,i,orig_img.ML[i][j].value))
                        pixel.value = calculate_bilinear(x,y,vals)
                    elif i == len(orig_img.ML) -1 and j == len(orig_img.ML[i]) -1:
                        vals = []
                        vals.append((j,i,orig_img.ML[i][j].value))
                        pixel.value = calculate_bilinear(x,y,vals)
                    gs = [(i,j),(i+1,j),(i,j+1),(i+1,j+1)]
                    l.append(vals)                     
                #blank_img.ML[bi][bj].value = orig_img.ML[i][j].value
                else:
                    pixel.value = 0
                    #print "otro %s, %s" %(i,j)
                    
        self.reflect_Y()
        return 1

    def __sub__(self,geoimage):
        """
        Returns a geoimage object that is the difference between the two geoimages given as parameters
        """
        print "\n Calculating difference between methods"
        import copy
        diff = copy.deepcopy(self)
        for i,row in enumerate(diff.ML):
                perc = float(i) / len(self.ML)*100
                perc = int(perc)
                sys.stdout.write("\r Calculating difference %s " %perc)    # or print >> sys.stdout, "\r%d%%" %i,
                sys.stdout.flush()
                for j,pixel in enumerate(row):
                    pixel.value = self.ML[i][j].value - geoimage.ML[i][j].value
        print "\n"
        return diff 

    def __add__(self,geoimage):
        """
        Returns a geoimage object that is the difference between the two geoimages given as parameters
        """
        print "\n Calculating difference between methods"
        import copy
        diff = copy.deepcopy(self)
        for i,row in enumerate(diff.ML):
                perc = float(i) / len(self.ML)*100
                perc = int(perc)
                sys.stdout.write("\r Calculating difference %s " %perc)    # or print >> sys.stdout, "\r%d%%" %i,
                sys.stdout.flush()
                for j,pixel in enumerate(row):
                    pixel.value = self.ML[i][j].value + geoimage.ML[i][j].value
        print "\n"
        return diff
    
    
    def __abs__(self):
        """
        Returns a geoimage object that is the difference between the two geoimages given as parameters
       """
        print "\n Calculating difference between methods"
        for i,row in enumerate(self.ML):
                perc = float(i) / len(self.ML)*100
                perc = int(perc)
                sys.stdout.write("\r Making absolute value %s " %perc)    # or print >> sys.stdout, "\r%d%%" %i,
                sys.stdout.flush()
                for j,pixel in enumerate(row):
                    self.ML[i][j].value = abs(self.ML[i][j].value)
        print "\n"
        return 1  


    def equalize(self):
        """
        Returns a geoimage object that is the difference between the two geoimages given as parameters
       """
        print "\n Calculating difference between methods"
        max = 0
        for i,row in enumerate(self.ML):
                perc = float(i) / len(self.ML)*100
                perc = int(perc)
                #sys.stdout.write("\r Making absolute value %s " %perc)    # or print >> sys.stdout, "\r%d%%" %i,
                #sys.stdout.flush()
                for j,pixel in enumerate(row):    
                    if self.ML[i][j].value > max:
                        max = self.ML[i][j].value
        
        for i,row in enumerate(self.ML):
                perc = float(i) / len(self.ML)*100
                perc = int(perc)
                for j,pixel in enumerate(row):    
                    self.ML[i][j].value = (self.ML[i][j].value / float(max))*255
        
        
        print "\n"
        return max
        

def geocodeImage(raw_image,geodetic_parameters):
    """
    Receives a raw binary data(matrix) and geocodes it according to the geodetic parameters,.
    Geodetic parameters is a dictionary with the affine parameters and resolution.
    Returns GeoImage object 
    """
    affine_parms = geodetic_parameters['affine']
    res = geodetic_parameters['resolution']
#     The 0,0 point in the raw image is the left bottom corner.
    a = affine_parms['a']
    b = affine_parms['b']
    limg = []
    n,m = raw_image.shape
    for i in range(n):
        row = []
        for j in range(m):
            y = i
            x = j
            X,Y = et.xyToAffineRaw(x, y, a, b)
            value = raw_image[i][j]
            #Xm = X
            #Ym = Y
            p = Pixel(x=X,y=Y,value=value)
            row.append(p)
        limg.append(row)
    geoimg = GeoImage(limg,res)
    return geoimg





def buildEmptyGeoImage(cell_size, extent):
    """
    Build an empty matrix that corresponds to the extent area and the cell size chosen.
    extent: dictionary X and Y with min and max
    """
    xmin = int(extent['X'][0])
    xmax = int(extent['X'][1])
    ymin = int(extent['Y'][0])
    ymax = int(extent['Y'][1])
    
    ncols = (xmax - xmin) / cell_size
    nrows = (ymax - ymin) / cell_size
    xvals = range(xmin,xmax,cell_size)
    yvals = range(ymin,ymax,cell_size)
    mat = []
    for i in yvals:
        row = []
        for j in xvals:
            row.append(Pixel(x=j,y=i,value=0))
        mat.append(row)
    g = GeoImage(mat,cell_size)
    return g


def get_geoimage_difference(geoimage_a,geoimage_b):
    """
    Returns a geoimage object that is the difference between the two geoimages given as parameters
    """
    print "\n Calculating difference between methods"
    import copy
    diff = copy.deepcopy(geoimage_a)
    for i,row in enumerate(diff.ML):
            perc = float(i) / len(geoimage_a.ML)*100
            perc = int(perc)
            sys.stdout.write("\r Calculating difference %s " %perc)    # or print >> sys.stdout, "\r%d%%" %i,
            sys.stdout.flush()
            for j,pixel in enumerate(row):
                pixel.value = abs(geoimage_a.ML[i][j].value - geoimage_b.ML[i][j].value)
    print "\n"
    return diff    
    



# 1. Read the satellite image in python
PATH = "data/"
LANDSAT = "MSS5.rst"
GCPFILE = "gcp.txt"
with open(PATH+LANDSAT,'rb') as fid:
    data = np.fromfile(fid,np.int8).reshape((512,512))
    #data = data_t[512::-1]



# 2. Transform the image to RT90 by affine transformation
affine_params = et.fitGCPfile(PATH+GCPFILE)
geoparms = {'affine': affine_params , 'resolution' : 80}

gm = geocodeImage(data,geoparms)

# 3. Create the frame in the transformed target image with the following edge coordinates. 
xmin = 1300000
xmax = 1330000
ymin = 6185000
ymax = 6225000

# 4. Choose desired resolution
number = raw_input('Please enter desired resolution in meters (RT90) (e.g. 50 or 100 ):')
try:
    ch_res = int( number )
except:
    sys.exit("Invalid number. Choose an integer number between 10 and 100")
extent = {'X' : (xmin,xmax),'Y':(ymin,ymax)}

# 5. Create two empty target matrixes based on the values of cell size.
nearest = buildEmptyGeoImage(ch_res,extent)
bilinear = buildEmptyGeoImage(ch_res,extent)

# 6. Resampling method for nearest neighbor and bilinear interpolation
nearest.nearestNeighborResampleFrom(geoparms['affine'], gm)
nn = nearest.display(1)
nn.suptitle("Nearest-Neighbor resampling")
nn.set_label("At %s resolution" %ch_res) 
bilinear.bilinearResampleFrom(geoparms['affine'], gm)
bl = bilinear.display(2)
bl.suptitle("Bilinear resampling")

# 7. Make the difference
diff = nearest - bilinear
abs(diff)
d = diff.display(3)
d.suptitle("Difference between NN and Bilinear resampling")

# 8. Displaying of images
gm.reflect_Y()
org = gm.display(0)
org.suptitle("Original image")
print "Displaying images"
plt.show()
