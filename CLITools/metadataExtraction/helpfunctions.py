#!/usr/bin/env python
# coding: utf8
'''
@author: Benjamin Dietz, Niklas Aßelmann, Katharina Hovestadt, Ilka Pleiser
'''

import sys, os, platform, datetime, math, shapefile, fiona 
from datetime import datetime as dtime
from six.moves import configparser
from netCDF4 import Dataset as NCDataset
import netCDF4
import getopt
from os import walk
from osgeo import ogr
from osgeo import osr
from pyproj import Proj, transform
import convex_hull

WGS84_EPSG_ID = 4326

def printObject(object):
    '''
    Function purpose: output of metadata object \n
    Input: object \n
    Output: print("/n")
    '''
    print("\n")
    for a,b in object.items():
        print(str(a) + ": " + str(b))
    print("\n")




def exists(filename):
    '''
    Function purpose: checks whether the filename exists \n
    Input: filename \n
    Output: boolean
    '''
    if os.path.isfile(filename):
        return True
    else:
        return False




def computeBboxOfMultiple(bboxes):
    '''
    Function purpose:  
        compute an overall bbox from an array of bounding boxes
        required format of parameter 'bboxes': [ bbox1, bbox2, ..., bboxn ]
        while each bbox has the format: [ min(longs), min(lats), max(longs), max(lats) ]
    Input: bboxes\n
    Output: array of coordinates
    '''
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




def computeTempExtentOfMultiple(temporal_extents):
    '''
    Function purpose: 
        get multiple temporal extents in the schema [ temp1, temp2, ..., tempn ]
        with the schema of each temporal extent being: [ 'yyyy-mm-dd hh:mm:ss', 'yyyy-mm-dd hh:mm:ss' ]
        returning the overall temporal extent in ISO format
    Input: temporal_extents \n
    Output: array tempExtent (if startingpoint and endpoint follow given rules), None (if they don't)
    '''
    if len(temporal_extents) > 0:
        try:
            startPoint = dtime.strptime(temporal_extents[0][0] ,'%Y-%m-%dT%H:%M:%SZ')
            endPoint = dtime.strptime(temporal_extents[0][1] ,'%Y-%m-%dT%H:%M:%SZ')
            tempExtent = [startPoint, endPoint]
            for x in temporal_extents:
                startPoint = dtime.strptime(x[0] ,'%Y-%m-%dT%H:%M:%SZ')
                endPoint = dtime.strptime(x[1] ,'%Y-%m-%dT%H:%M:%SZ')
                if  startPoint < tempExtent[0]:
                    tempExtent = [ startPoint, tempExtent[1] ]
                if endPoint > tempExtent[1]:
                    tempExtent = [ tempExtent[0], endPoint ]
            return [tempExtent[0].isoformat(), tempExtent[1].isoformat()]
        except ValueError:
            try:
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
            except ValueError:
                startPoint = dtime.strptime(temporal_extents[0][0] ,'%Y-%m-%dT%H:%M:%S')
                endPoint = dtime.strptime(temporal_extents[0][1] ,'%Y-%m-%dT%H:%M:%S')
                tempExtent = [startPoint, endPoint]
                for x in temporal_extents:
                    startPoint = dtime.strptime(x[0] ,'%Y-%m-%dT%H:%M:%S')
                    endPoint = dtime.strptime(x[1] ,'%Y-%m-%dT%H:%M:%S')
                    if  startPoint < tempExtent[0]:
                        tempExtent = [ startPoint, tempExtent[1] ]
                    if endPoint > tempExtent[1]:
                        tempExtent = [ tempExtent[0], endPoint ]
                return [tempExtent[0].isoformat() + "Z", tempExtent[1].isoformat() + "Z"]

    else: return None




def countElements(array):
    '''
    Function purpose: return the occurancies of all values in the array \n
    Input: array \n
    Output: array list
    '''
    list = []
    for x in array:
            if [x, array.count(x)] not in list:
                list.append([x, array.count(x)])
    return list




def getAllRowElements(rowname,elements):
    '''
    Function purpose: help-function to get all row elements for a specific string \n
    Input: rowname, elements \n
    Output: array values
    '''
    for idx, val in enumerate(elements[0]):
        if  rowname in val:
            indexOf = idx
            values = []
            for x in elements:
                if x[indexOf] != rowname:
                    values.append(x[indexOf])
            return values




def searchForParameters(elements, paramArray):
    '''
    Function purpose: return all attributes of a elements in the first row of a file \n
    Input: paramArray, elements \n
    Output: getAllRowElements(x,elements)
    '''
    for x in paramArray:
        for row in elements[0]:
            if x in row:
                return getAllRowElements(x,elements)




def transformingIntoWGS84 (crs, coordinate):
    '''
    Function purpose: transforming SRS into WGS84 (EPSG:4978; used by the GPS satellite navigation system) \n
    Input: crs, point \n
    Output: retPoint constisting of x2, y2 (transformed points)
    '''
    source = osr.SpatialReference()
    source.ImportFromEPSG(int(crs))

    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(source, target)
        
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(coordinate[0]), float(coordinate[1]))
    point = point.ExportToWkt()
    point = ogr.CreateGeometryFromWkt(point)
  
    point.Transform(transform)
    return [point.GetX(), point.GetY()]




def disablePrint():
    ''' Disable Prints '''
    sys.stdout = open(os.devnull, 'w')




def enablePrint():
    ''' Restore Prints'''
    sys.stdout = sys.__stdout__




def transformingArrayIntoWGS84(crs, pointArray):
    '''
    Function purpose: transforming SRS into WGS84 (EPSG:4978; used by the GPS satellite navigation system) from an array \n
    Input: crs, pointArray \n
    Output: array array
    '''
    array = []
    ##vector_rep
    if type(pointArray[0]) == list:
        for x in pointArray:
            array.append(transformingIntoWGS84(crs, x))
        return array
    #bbox
    elif len(pointArray) == 4:
        bbox = [[pointArray[0], pointArray[1]],[pointArray[2], pointArray[3]]]
        transf_bbox = transformingArrayIntoWGS84(crs, bbox)
        return [transf_bbox[0][0],transf_bbox[0][1], transf_bbox[1][0], transf_bbox[1][1]]