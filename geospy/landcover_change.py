#-*- coding: utf-8 -*
#===============================================================================
# This program analyses the table of landcover changes
# 
# '''
# Created on 3/1/2014
# a
# @author: Juan Escamilla
# '''
#===============================================================================

import numpy as np
# files
c_01_05 = 'lc_changes_2001_2005.txt' 
c_05_10 = 'lc_changes_2005_2010.txt'
c_01_10 = 'lc_changes_2001_2010.txt'

changes_f = [c_01_05,c_05_10,c_01_10]
changes = []
for file in changes_f:
    c = open(file,'r')
    tmp = c.readlines()
    tmp.pop(0)
    year = []
    for line in tmp:
        ls = line.split(',')
        class_c = ls[1]
        if len(class_c) == 1:
            s = '00'+'0'+ str(class_c)
        elif len(class_c) == 2:
            s = '00'+ str(class_c)
        elif len(class_c) == 3:
            s = str(class_c)[:2]+'0'+str(class_c)[2]
        else:
            s = str(class_c)
        year.append((s,float(ls[2])))
    changes.append(year)
    c.close()
    
    
#Build the matrix
cname = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']
# c_01_05 = changes[0]
# c_05_10 = changes[1]
# c_01_10 = change[2]
all_years = []
for c in changes:
    rows = []
    for cl in cname:
        row = []
        for lc in cname:        
            name = cl+lc 
    #         print name
            duple = filter(lambda duple : duple[0] == name, c)
    #         print duple
            if len(duple) == 0:
                count = 0
            else:
                count = duple[0][1]
            print count
            row.append(count)
        rows.append(row)
    all_years.append(rows)
    
lc_1=open('lc_changes_2001_2005.csv','w')
lc_2=open('lc_changes_2005_2010.csv','w')
lc_3=open('lc_changes_2001_2010.csv','w')

files = [lc_1,lc_2,lc_3]
for idx,year in enumerate(all_years):
    sname = str(cname).replace("[","").replace("]","")+"\n"
    files[idx].write(sname)
    for row in year:
        srow = str(row).replace("[","").replace("]","")+"\n"
        files[idx].write(srow)
    files[idx].close()
