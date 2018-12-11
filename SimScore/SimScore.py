import math
import heapq
from datetime import datetime
import dateutil.parser



'''
Help functions:

    checkValidity:      checks validity for getSimilarityScores inputs

    getDiagonal:        gets diagonal length of bounding box (from entry as dict)

    getInterv:          gets length of temporal interval (from entry as dict)

    getCenter:          calculates center of bounding box

    getAr/getAres:      calculates area of bouunding box on earth surface

'''

def checkValidity(entries, cmp, n, e, d, l, g, t){
    #entries will be checked during iteration in main function
    #cmp
    if cmp is None or cmp["id"] is None or cmp["wkt_geometry"] is None or len(cmp["wkt_geometry"])==0 or cmp["vector"] is None or len(cmp["vector"])==0 or cmp["time"] is None or len(cmp["time"]) == 0:
        return false

    #n will be checked inside main function

    #e,d,g,l,t

    if e<0 or e>5 or d<0 or d>5 or l<0 or l>5 or g<0 or g>5 or t<0 or t>5:
        return false
    
    
    return true
}

#Calculates diagonal of Bounding Box by use of Haversine Formula


# Checken, ob floats etc richtig
def getDiagonal(entry):
    r = 6371.0
    dLon = entry["wkt_geometry"][1]-entry["wkt_geometry"][0]
    dLat = entry["wkt_geometry"][3]-entry["wkt_geometry"][2]

    if dLon == 0 and dLat == 0:
        return 0.01

    a = float((math.sin(float(dLat/2)))**2 + math.cos(entry[2][2]) * math.cos(entry[2][3]) * math.sin(float(dLon/2))**2)
    c = 2*(math.asin(min(1, math.sqrt(a))))
    d = r * c
    return d

#Get length of temporal interval
def getInterv(entry):
    t1 = entry["time"][0]
    t2 = entry["time"][1]
    frmt = "%Y-%m-%dT%H:%M:%S%Z" 
    tdelta = datetime.strptime(t2, frmt) - datetime.strptime(t1, frmt)
    return tdelta

#Calculates center of bbox
def getCenter(entry):
    minLon=entry["wky_geometry"][0]
    maxLon=entry["wkt_geometry"][1]
    minLat=entry["wky_geometry"][2]
    maxLat=entry["wkt_geometry"][3]
    lon = (minLon+maxLon)/2
    lat = (minLat+maxLat)/2
    center = [lon,lat]
    return center

def ConvertToRadian(input):
    return input * Math.PI / 180

def getArea(coordinates):
    area = 0

    if (len(coordinates)>2):
        i=0
        p1Lon = coordinates[i]
        p1Lat = coordinates[i+2]
        p2Lon = coordinates[i+1]
        p2Lat = coordinates[i+3]
        area += ConvertToRadian(p2Lon - p1Lon) * (2 + math.sin(ConvertToRadian(p1Lat)) + math.sin(ConvertToRadian(p2Lat)))

        area = area * 6378137 * 6378137 / 2
    }

    return math.abs(area)
}


def getAr(entry):
    if (entry["bbox"][0]==entry["bbox"][1]) or (entry["bbox"][2]==entry["bbox"][3]):
        return 0
    return getArea(entry["bbox"])



'''
Extent Similarity: 

    getGeoExtSim:       compares geographic extent by comparing diagonal lengths for two entries given as dicts

    getTempExtSim:      compares temporal extent by comparing temporal interval lengths for two entries given as dicts


'''



# Similarity of geographical extent
def getGeoExtSim(entryA, entryB):
    diagonalA=float(getDiagonal(entryA))
    diagonalB=float(getDiagonal(entryB))
    min = min(diagonalA, diagonalB)
    max = max(diagonalA, diagonalB)
    sim = float(min/max)
    return sim



#Similarity of temporal extent
def getTempExtSim(entryA,entryB):
    extA = getInterv(entryA).total_seconds()
    extB = getInterv(entryB).total_seconds()

    if extA=0:
        extA=1
    if extB=0:
        extB=1
    min = min(extA, extB)
    max = max(extA, extB)
    sim = float(min/max)
    return sim


'''
Location Similarity

    Intersection Similarity

        getInterGeoSim:         calculates ratio between intersection of both bounding boxes and first entry, 0 if disjunct, given two entries as dicts

        getInterTempSim:        calculates ratio between intersection of both entries on timeline and first entry, 0 is disjunct, given two entries as dicts

    Center Similarity:

        getCentGeoSim:          calculates difference between centers of bounding boxes of two entries, given as dicts, and calculates ratio to absolute maximum (half the earth's circumference)        

        getCentTempSim:         calculates difference between centers of temporal intervals of two entries, given as dicts, and calculates ratio to absolute max (to be determined)

    Total Location Similarity:

        getLocSim:              combines above similarity calculations, given two entries as dicts, under consideration of weights for geographic and temporal similarity

'''


#Get similarity of location of center
def getCenterGeoSim(entryA, entryB):
    centerA= getCenter(entryA)
    centerB= getCenter(entryB)
    diagonal = float(getDiagonal([[],[],[entryA[1], entryB[1]]]))
    circumf = 20038
    sim = diagonal/circumf
    return sim

def getCenterTempSim(entryA, entryB):
    frmt = "%Y-%m-%dT%H:%M:%S%Z" 
    if entryA["time"][0]==entryA["time"][1]:
        centerA=entryA["time"][0]
    else 
        centerA=datetime.strptime(entryA["time"][0],frmt)+(getInterv(entryA)/2)
    if entryB["time"][0]==entryB["time"][1]:
        centerB=entryB["time"][0]
    else 
        centerB=datetime.strptime(entryB["time"][0],frmt)+(getInterv(entryB)/2)

    tdelta = centerA-centerB
    tdelta = tdelta.total_seconds

    max = timedelta(days=365000).total_seconds

    return tdelta/max


def getInterGeoSim(entryA,entryB):
    
    
def getInterTempSim(entryA,entryB):
    startA= datetime.strptime(entryA["time"][0]



    ####################################################
    ####################################################
    #####################################################

'''
Datatype Similarity 

    getGeoDatSim:       compares datatype of geographic information, given two entries as dicts

    getTempDatSim:      compares datatype of temporal information, given two entries as dicts

    getDatatypeSim:     compares datatype of temporal information, given two entries as dicts

'''


#Get Similarity of Temporal and Vector Datatype
def getDatatypeSim(entryA, entryB):
    #Vector Datatype
    #Equal number of points
    if len(entryA[3])==len(entryB[3]):
        gType = 1
    #Both Polygons
    elif len(entryA[3])>2 and len(entryB[3])>2:
        gType = 1
    #different Types
    else:
        gType = 0
    #EntryA is point and not interval
    if entryA[4][1] is Null:
        #EntryB and EntryA are points
        if entryB[4][1] is Null:
            tType = 1
        #EntryA is point, entryB is interval
        else:
            tType = 0
    #EntryA is interval, entryB is point
    elif entryB[4][1] is Null:
        tType = 0
    #Both are intervals
    else:
        tType = 1
    #1 if both similar, 1/2 if one is similar, 0 if both not similar
    dType = gType*(1.0/2.0)+tType*(1.0/2.0)

    return dType


'''
getIndSim:          combines Geo and Temp Similarites for selected criterium c while taking into consideration weights for geographic and temporal similarity
                    c=0 for Similarity of extent
                    c=1 for Similarity of location
                    c=2 for Similarity of datatype
'''
def getIndSim(entryA, entryB, g, t, c):
    if c=0:
        geoSim = getGeoExtSim(entryA,entryB)
        tempSim = getTempExtSim(entryA,entryB)
    if c=1:
        geoSim = getGeoLocSim(entrya,entryB)
        tempSim = getTempLocSim(entryA,entryB)
    if c=2:
        geoSim = getGeoDatSim(entryA,entryB)
        tempSim = getTempDatSim(entryA,entryB)
    else:
        geoSim = 0
        tempSim = 0
    rel = g/(g+t)
    sim = rel*geoSim + (1-rel)*tempSim

    return sim 




'''
getSimilarityScore: Berechnet den SimilarityScore
        entries: Expects a list of entries (dictionaries), where each dict represents one entry of the repository.

                entry:      {
                                "id" : idOfTheEntry,
                                "wkt_geometry" : [[minLon],[maxLon],[minLat],[maxLat]],
                                "vector" : [[x,y],[x,y]...],
                                "time" : [start, end],
                                "raster"  : bool
                            }   

        cmp is an entry and therefor the same format
        n : number of similar records to be retrieved
        t : weight temporal similarity
        g : weight geographic similarity
        d : weight of datatype similarity 
        e : weight of extent similarity 
        l : weight of location similarity
'''

def getSimScoreTotal(entryA, entryB, e, d, l):
    dSim = getDatatypeSim(entryA, entryB)
    lSim = getLocationSim(entryA, entryB)
    eSim = getExtentSim(entryA, entryB)

    simScore = 0.999*(e*eSim+l*lSim+d*dSim)

    return simScore




def getSimilarityScore(entries, cmp, n, g, t, e, d, l):

    if 

    c=0
    scores=[]
    while c<len(entries):
        if entries[c][0] != cmp[0]:
            score = getSimScoreTotal(entries[c], cmp, e, d, l)
            scores.append([entries[c][0], currscore])
        c=c+1

    return scores




def getSimilarRecords(entries, cmp, n, e, d, l):
    scores = getSimilarityScore(entries, cmp, n, e, d, l)

    records = []

    i=0

    while i < n:
        heappush(records, scores[i])
        i=i+1
    
    while i < len(scores):
        min = heappop(records)
        if min[1]<scores[i][1]:
            heappush(records, scores[i])
        else:
            heappush(records, min)
        i=i+1
    
    output=sorted(records, key= lambda x: x[1])

    return output