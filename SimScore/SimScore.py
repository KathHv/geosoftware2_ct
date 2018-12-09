import math
import heapq
#entries: expects a nested list of the form [[[id],[center],[[bboxMinLon],[bboxMaxLon],[bboxMinLat],[bboxMaxLat]],[coords], [[time1],[time2]] ], .... ]
#cmp: entry to compare to, form: [[id],[center],[[bboxMinX],[bboxMaxX],[bboxMinY],[bboxMaxY]],[coords], [[time1],[time2]] ]
#n: expects a natural number
#e: weight geographic extent (bbox)
#d: weight datatype (type of vector and time)
#l: weight of geographic location
def getSimilarityScore(entries, cmp, n, e, d, l):
    
    #Use of Haversine Formula
    #
    #
    # Checken, ob floats etc richtig
    #
    #
    #

    def getDiagonal(entry):
        r = 6371.0
        dLon = entry[2][1]-entry[2][0]
        dLat = entry[2][3]-entry[2][2]
        a = float((math.sin(float(dLat/2)))**2 + math.cos(entry[2][2]) * math.cos(entry[2][3]) * math.sin(float(dLon/2))**2)
        c = 2*(math.asin(min(1, math.sqrt(a))))
        d = r * c
        return d

    #Get similarity of geographical extent
    def getExtentSim(entryA, entryB):
        diagonalA=float(getDiagonal(entryA))
        diagonalB=float(getDiagonal(entryB))
        min = min(diagonalA, diagonalB)
        max = max(diagonalA, diagonalB)
        sim = float(min/max)
        return sim

    #Get similarity of location of center
    def getLocationSim(entryA, entryB):
        diagonal = float(getDiagonal([[],[],[entryA[1], entryB[1]]]))
        circumf = 20038
        sim = diagonal/circumf
        return sim
    
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
    
    def getSimScoreTotal(entryA, entryB, e, d, l):
        dSim = getDatatypeSim(entryA, entryB)
        lSim = getLocationSim(entryA, entryB)
        eSim = getExtentSim(entryA, entryB)

        simScore = 0.999*(e*eSim+l*lSim+d*dSim)

        return simScore
    
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