import sys, os, platform, datetime, math, shapefile, fiona 
#nio
from datetime import datetime as dtime
from six.moves import configparser
from netCDF4 import Dataset as NCDataset
import netCDF4
import getopt
from os import walk
from pyproj import Proj, transform
import convex_hull


'''
 Function name: printObject
 Function purpose: output of metadata object
 Input: object
 Output: print("/n")
'''
def printObject(object):
    print("\n")
    for a,b in object.items():
        print(str(a) + ": " + str(b))
    print("\n")



'''
 Does a file with the relative path 'filename' exist locally?
 Function name: extists
 Function purpose: checks whether the filename exists
 Input: filename
 Output: boolean true or false
'''
def exists(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False



'''
 Function name: computeBboxOfMultiple
 Function purpose:  compute an overall bbox from an array of bounding boxes
                    required format of parameter 'bboxes': [ bbox1, bbox2, ..., bboxn ]
                    while earch bbox has the format: [ min(longs), min(lats), max(longs), max(lats) ]
 Input: bboxes
 Output: array of coordinates
'''
def computeBboxOfMultiple(bboxes):
    coordinate0 = 200
    coordinate1 = 200
    coordinate2 = -200
    coordinate3 = -200
    for x in bboxes:
        if x[0] < coordinate0:
            coordinate0 = x[0]
        if x[1] < coordinate1:
            coordinate1 = x[1]
        if x[2] > coordinate2:
            coordinate2 = x[2]
        if x[3] > coordinate3:
            coordinate3 = x[3]
    return [coordinate0, coordinate1, coordinate2, coordinate3]



'''
 Function name: computeTempExtentOfMultiple
 Function purpose:  get multiple temporal extents in the schema [ temp1, temp2, ..., tempn ]
                    with the schema of each temporal extent being: [ 'yyyy-mm-dd hh:mm:ss', 'yyyy-mm-dd hh:mm:ss' ]
                    returning the overall temporal extent in ISO format
 Input: temporal_extents
 Output: array tempExtent (if startingpoint and endpoint follow given rules), None (if they don't)
'''
def computeTempExtentOfMultiple(temporal_extents):
    if len(temporal_extents) > 0:
        startPoint = dtime.strptime(temporal_extents[0][0] ,'%Y-%m-%d %H:%M:%S')
        endPoint = dtime.strptime(temporal_extents[0][1] ,'%Y-%m-%d %H:%M:%S')
        tempExtent = [startPoint, endPoint]
        for x in temporal_extents:
            startPoint = dtime.strptime(x[0] ,'%Y-%m-%d %H:%M:%S')
            endPoint = dtime.strptime(x[1] ,'%Y-%m-%d %H:%M:%S')
            if  startPoint < tempExtent[0]:
                tempExtent = [ startPoint, tempExtent[1] ]
            if endPoint > tempExtent[1]:
                tempExtent = [ tempExtent[0], endPoint ]
        return [tempExtent[0].isoformat() + "Z", tempExtent[1].isoformat() + "Z"]
    else: return None



'''
 Function name: countElements
 Function purpose: return the occurancies of all values in the array
 Input: array
 Output: array list
'''
def countElements(array):
    list = []
    for x in array:
            if [x, array.count(x)] not in list:
                list.append([x, array.count(x)])
    return list



'''
 Function name: getAllRowElements
 Function purpose: help-function to get all row elements for a specific string
 Input: rowname, elements
 Output: array values
'''
def getAllRowElements(rowname,elements):
    for idx, val in enumerate(elements[0]):
        if  rowname in val:
            indexOf = idx
            values = []
            for x in elements:
                if x[indexOf] != rowname:
                    values.append(x[indexOf])
            return values



'''
 Function name: searchForParameters
 Function purpose: ?
 Input: paramArray, elements
 Output: getAllRowElements(x,elements)
'''
def searchForParameters(elements, paramArray):
    for x in paramArray:
        for row in elements[0]:
            if x in row:
                return getAllRowElements(x,elements)



'''
 Function name: transformingIntoWGS84
 Function purpose: transforming SRS into WGS84 (EPSG:4978; used by the GPS satellite navigation system)
 Input: crs, point
 Output: retPoint constisting of x2, y2 (transformed points)
'''
def transformingIntoWGS84 (crs, point):
    inProj = Proj(init = crs)
    outProj = Proj(init ='epsg:4978')
    x1, y1 = point
    x2, y2 = transform(inProj,outProj,x1,y1)
    print (x2,y2)
    retPoint = x2, y2
    return retPoint



'''
 Disable Prints
'''
def disablePrint():
    sys.stdout = open(os.devnull, 'w')



'''
 Restore Prints
'''
def enablePrint():
    sys.stdout = sys.__stdout__



'''
 transforming SRS into WGS84 (EPSG:4978; used by the GPS satellite navigation system) from an array
 Function name: transformingIntoWGS84
 Function purpose: transforming SRS into WGS84 (EPSG:4978; used by the GPS satellite navigation system) from an array
 Input: crs, pointArray
 Output: array array
'''
def transformingArrayIntoWGS84(crs, pointArray):
    array = []
    for x in pointArray:
        array.append(transformingIntoWGS84(crs, x))
    return array