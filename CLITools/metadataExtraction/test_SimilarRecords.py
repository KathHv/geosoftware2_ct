import pytest
import os
import os.path
import sqlite3
import filecmp  
import math
import SimScore


dasEntry1 = {"id" : 1,"wkt_geometry" : [45,50,30,45],"vector" : [[1,1], [0,9]],"time" : ["2000-07-16T19:20:30+01:00", "2001-07-16T19:20:30+01:00"],"raster" : False}
dasEntry2 = {"id" : 2,"wkt_geometry" : [50,55,10,12],"vector" : [[1,1],[2,12]],"time" : ["1999-07-16T19:20:30+01:00", "2000-07-16T19:20:30+01:00"],"raster" : True}
dasEntry3 = {"id" : 3,"wkt_geometry" : [20,25,4,8],"vector" : [[10,50],[3,54]],"time" : ["1998-07-16T19:20:30+01:00", "1999-07-16T19:20:30+01:00"],"raster" : True}
dasEntry4 = {"id" : 4,"wkt_geometry" : [20,22,23,28],"vector" : [[2,1],[3,5],[4,20]],"time" : ["1997-07-16T19:20:30+01:00", "1998-07-16T19:20:30+01:00"],"raster" : False}
dasDict = [dasEntry1,dasEntry2,dasEntry3,dasEntry4]

'''
 Function purpose: tests whether the correct results are put out
 when comparing two data types of geographic information
 input: -
 output:    1: same type and both vector or raster
            0.8: unequal type and both vector or raster
            0: unequal type and only a vector or raster
'''
def test_getGeoDatSim():
    entry1 = dasEntry1
    entry2 = dasEntry3
    geoSimilarity = SimScore.getGeoDatSim(entry1, entry2)
    print (geoSimilarity)
    # geoSimilarity = 0 || geoSimilarity = 0.8 || geoSimilarity = 1
    ans = 0
    if (entry1["raster"] == entry2["raster"]): #beides true, wenn es Raster ist. beides false, wenn es Vektor ist.
        if ((len(entry1["vector"]) == len(entry2["vector"])) or (len(entry1["vector"]) > 2 and len(entry2["vector"] > 2))): #wegen Punkt = 1, Linie = 2, Polygon > 2
            ans = 1
        else:
            ans = 0.8
    assert ans == geoSimilarity

'''
 Function purpose: Tests whether the correct results are output when comparing two types of temporal information
 input: arrays, entry1, entry2
 output: 
'''

def test_getTempDatSim():
    entry1 = dasEntry2
    entry2 = dasEntry4
    tempSimilarity = SimScore.getTempDatSim(entry1, entry2)
    print (tempSimilarity)
    ans = 0
    if (entry1["time"][0] == entry1["time"][0] and entry2["time"][0] == entry2["time"][0]):
        ans = 1
    elif (entry1["time"][0] != entry1["time"][0] and entry2["time"][0] != entry2["time"][0]):
        ans = 1
    assert ans == tempSimilarity

'''
 Function purpose: Tests whether the file types of two inputs are the same
 input: 
 output: 
'''
#TODO
# def test_DatatypeSim(dict, entry1, entry2):


'''
 Function purpose: Tests the inputs for size-similarity
 input: arrays, entry1, entry2 ?????????????
 output: boolean true/false
'''
def test_getGeoExtSim():
    entry1 = dasEntry2
    entry2 = dasEntry4
    GeoExtentSimilarity = SimScore.getGeoExtSim(entry1, entry2)
    print (GeoExtentSimilarity)
    ans = False
    if (GeoExtentSimilarity >= 0 and GeoExtentSimilarity <= 1):
        ans = True
    assert ans == True

'''
 Function purpose: Tests the inputs for time-similarity
 input: arrays, entry1, entry2 ?????????????
 output: boolean true/false
'''
def test_getTempExtSim():
    entry1 = dasEntry2
    entry2 = dasEntry4
    TemporalExtentSimilarity = SimScore.getTempExtSim(entry1, entry2)
    print (TemporalExtentSimilarity)
    ans = False
    if (TemporalExtentSimilarity > 0 and TemporalExtentSimilarity <= 1):
        ans = True
    assert ans == True


'''
 Function purpose: Calculates ratio between intersection of both bounding boxes and first zwei entries entry,
 0 if disjunct, given two entries as dicts
  Case distinction:
    1. Cut: Calculation of the cut surface of the bboxes with getAr, then ratio cut-surface / areaA
    2. A lies in B: Similarity 1
    3. B lies in A: Calculation Ratio AreaB / AreaA
    4. No cut: Similarity 0
 input: arrays, entry1, entry2 ?????????????
 output: boolean true/false
'''
def test_getInterGeoSim():
    entry1 = dasEntry2
    entry2 = dasEntry4
    InterGeoSimilarity = SimScore.getInterGeoSim(entry1, entry2)
    print (InterGeoSimilarity)
    minLatA=entry1["wkt_geometry"][0]
    maxLatA=entry1["wkt_geometry"][1]
    minLonA=entry1["wkt_geometry"][2]
    maxLonA=entry1["wkt_geometry"][3]
    minLatB=entry2["wkt_geometry"][0]
    maxLatB=entry2["wkt_geometry"][1]
    minLonB=entry2["wkt_geometry"][2]
    maxLonB=entry2["wkt_geometry"][3]

    # A in B
    # ans = False
    # The other one stands here only, so that no warning happens 
    ans = 0
    ans = ans +1
    if((minLonA > minLonB) and (maxLonA < maxLonB) and (minLatA > minLatB) and (maxLatA < maxLatB)):
        ans = True

#TODO


# def test_getInterTempSim(entry1, entry2):
   # InterTempSimilarity = SimScore.getInterTempSim(entry1, entry2)
   # print (InterTempSimilarity)
  

'''
 Function purpose: Tests whether the difference between the bounding boxes of Entry1 and Entry2 is the same
 as between Entry2 and Entry1
 input: arrays, entry1, entry2 ?????????????
 output: boolean true/false
'''
def test_getCenterGeoSim():
    entry1 = dasEntry2
    entry2 = dasEntry4
    geoCentSim1 = SimScore.getCenterGeoSim(entry1, entry2)
    geoCentSim2 = SimScore.getCenterGeoSim(entry2, entry1)
    print (geoCentSim1)
    print (geoCentSim2)    
    ans = False
    if (geoCentSim1 == geoCentSim2 and (geoCentSim1 >= 0 and geoCentSim1 <= 1)):
        ans = True
    assert ans == True   

'''
 Function purpose: Tests whether the difference between the Intervals of Entry1 and Entry2 is the same
 as between Entry2 and Entry1
 input: arrays, entry1, entry2 ?????????????
 output: boolean true/false
'''
def test_getCenterTempSim():
    entry1 = dasEntry2
    entry2 = dasEntry4
    tempCentSim1 = SimScore.getCenterTempSim(entry1, entry2)
    tempCentSim2 = SimScore.getCenterTempSim(entry2, entry1)
    print (tempCentSim1)
    print (tempCentSim2)    
    ans = False
    if (tempCentSim1 == tempCentSim2 and (tempCentSim1 >= 0 and tempCentSim1 <= 1)):
        ans = True
    assert ans == True   


# Helpfunction:

def intBetween(x, bottom, top):
    if(x>=bottom and x<=top and math.floor(x) == x):
        return True
    else:
        return False 

'''
 Function purpose: Tests whether the validity for getSimilarityScores inputs is correct
 input: dict, entries
 output: boolean true/false
'''

def test_checkValidity():
    entries = dasDict
    cmps = 5
    n = 1
    g = 4
    e = 3
    t = 4
    d = 2
    l = 0
    Validity = SimScore.checkValidity(entries, cmps, n, e, d, l, g, t)
    print(Validity)
    ans = False

    #entries a Dict
    if type (entries) is dict:
        #cmps ein int >= 0
        if (cmps >= 0 and math.floor(cmps) == cmps):
            #n ein int >= 1
            if (n >= 1 and math.floor(n) == n):
                #e,d,l,g,t >=0 and <=5
                loop = [e,d,l,g,t]
                temp = True
                for x in loop:
                    if intBetween(x,0,5) == False:
                        temp = False
                        break
                if(temp == True):
                    ans = True
    assert ans == True                    
               
'''
 Function purpose: Tests whether the diagonal length of bounding box (from entry as dict) is correct
 input: dict, entry
 output: boolean true/false
'''
def test_getDiagonal():
    entry = dasEntry2
    Diagonale = SimScore.getDiagonal(entry)
    print (Diagonale)
    # ans = False
    # The other one stands here only, so that no warning happens    
    ans = 0
    ans = ans +1 
    if ():
        ans = 9
        #TODO                                                                                                    

'''
 Function purpose: Tests whether the length of temporal interval (from entry as dict) is correct
 input: dict, entry
 output: boolean true/false
'''
def test_getInterv():
    entry = dasEntry2
    Intervall = SimScore.getInterv(entry)
    print (Intervall)
    ans = False
    if(Intervall == entry["time"][1] - entry ["time"][0]):
        ans = True
    assert ans == True
    
'''
 Function purpose: Tests whether the calculates area of bouunding box on earth surface is correct
 input: dict, entry
 output: boolean true/false
'''
def test_getAr():
    points = dasEntry2["wkt_geometry"]
    Ar = SimScore.getAr(points)
    print (Ar)
    ans = 1
    if ((points[0] == points[2]) and (points[1] == points[3])):
        ans = 0
    if(Ar == 0 and ans == 0):
        ans = True
    elif(Ar != 0 and ans != 0):
        ans = True
    else:
        ans = False
    assert ans == True

