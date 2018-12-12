import pytest
import os
import os.path
import sqlite3
import filecmp
import math
import SimScore


dasEntry1 = {"id" : 1,"wkt_geometry" : [45,50, 30,45],"vector" : [[1,1]],"time" : [5, 100],"raster" : False}
dasEntry2 = {"id" : 2,"wkt_geometry" : [50,55,10,12],"vector" : [[1,1],[2,12]],"time" : [2, 10000],"raster" : True}
dasEntry3 = {"id" : 3,"wkt_geometry" : [20,25,4,8],"vector" : [[10,50]],"time" : [150, 500],"raster" : True}
dasEntry4 = {"id" : 4,"wkt_geometry" : [20,22,23,28],"vector" : [[2,1],[3,5],[4,20]],"time" : [0, 3],"raster" : False}
dasDict = [dasEntry1,dasEntry2,dasEntry3,dasEntry4]

#testet, ob die richtigen Resultate beim Vergleichen zweier Datentypen geografischer
#Informationen ausgegeben werden
#Ausgaben:
    #1: gleicher Typ und beide Vektor oder Raster
    #0.8: ungleicher Typ und beide Vektor oder Raster
    #0: ungleicher Typ und nur ein Vektor oder Raster
        #Typ = Punkt || Linie || Polygon
# dict1: Liste aller Einträge
# entry1, eintry2: Zu Vergleichende Einträge aus einem Dictionary

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

#testet, ob die richtigen Resultate beim Vergleichen zweier Datentypen zeitlicher
#Informationen ausgegeben werden getTempDatSim(dict, entry1, entry2):
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

#testet, ob die Dateintypen zweier Eingaben die gleichen sind
#pip install pytest-datafiles
#TODO
#def test_DatatypeSim(dict, entry1, entry2):
    
#testet, die Eingaben in Bezug auf Größenähnlichkeit

def test_getGeoExtSim():
    entry1 = dasEntry2
    entry2 = dasEntry4
    GeoExtentSimilarity = SimScore.getGeoExtSim(entry1, entry2)
    print (GeoExtentSimilarity)
    ans = False
    if (GeoExtentSimilarity >= 0 and GeoExtentSimilarity <= 1):
        ans = True
    assert ans == True

#testet, die Eingaben in Bezug auf Zeitähnlichkeit

def test_getTempExtSim():
    entry1 = dasEntry2
    entry2 = dasEntry4
    TemporalExtentSimilarity = SimScore.getTempExtSim(entry1, entry2)
    print (TemporalExtentSimilarity)
    ans = False
    if (TemporalExtentSimilarity > 0 and TemporalExtentSimilarity <= 1):
        ans = True
    assert ans == True

#testet, calculates ratio between intersection of both bounding boxes and first zwei entries entry,
#0 if disjunct, given two entries as dicts
#Fallunterscheidung:
    #1. Schnitt: Berechnung der Schnittfläche der Bboxes mit getAr, dann Verhältnis Schnittfläche/FlächeA
    #2. A liegt in B: Ähnlichkeit 1
    #3. B liegt in A: Berechnung Verhältnis FlächeB/FlächeA
    #4. Kein Schnitt: Ähnlichkeit 0

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
    #A in B
    # ans = False
    # das andere steht hier nur, damit keine Warnung passiert 
    ans = 0
    ans = ans +1
    if((minLonA > minLonB) and (maxLonA < maxLonB) and (minLatA > minLatB) and (maxLatA < maxLatB)):
        ans = True
    #TODO

#

#def test_getInterTempSim(entry1, entry2):
   # InterTempSimilarity = SimScore.getInterTempSim(entry1, entry2)
   # print (InterTempSimilarity)
  

#testet, ob der Unterschied zwischen den Bounding Boxes von Entry1 und Entry2 der selbe ist wie zwischen Entry2 und Entry1

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


#testet, ob der Unterschied zwischen den Intervallen von Entry1 und Entry2 der selbe ist wie zwischen Entry2 und Entry1

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


#Helpfunction:
    #1. Validity-Check
    #2. Errechnet Länge der Diagonalen
    #3.
    #4.

def intBetween(x, bottom, top):
    if(x>=bottom and x<=top and math.floor(x) == x):
        return True
    else:
        return False 

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
    #entries ein Dict
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
               

def test_getDiagonal():
    entry = dasEntry2
    Diagonale = SimScore.getDiagonal(entry)
    print (Diagonale)
    # ans = False
    # das andere steht hier nur, damit keine Warnung passiert     
    ans = 0
    ans = ans +1 
    if ():
        ans = 9
        #TODO                                                                                                    

def test_getInterv():
    entry = dasEntry2
    Intervall = SimScore.getInterv(entry)
    print (Intervall)
    ans = False
    if(Intervall == entry["time"][1] - entry ["time"][0]):
        ans = True
    assert ans == True
    
def test_getAr():
    points = dasEntry2["wkt_geometry"]
    Ar = SimScore.getAr(points)
    print (Ar)
    ans = 0
    if ((points[0]==points[1]) or (points[2] == points[3])):
        ans = 0.01
    assert ans == 0.01
    #checken lassen     

