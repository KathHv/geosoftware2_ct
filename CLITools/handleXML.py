import xml.etree.ElementTree as ET  
import jgraph as ig
import helpfunctions as hf
import ogr2ogr
import pygeoj
import sys, os
from osgeo import gdal, ogr
import convex_hull

'''
 extract bounding box from xml
 input filepath: type string, file path to xml file
 output SpatialExtent: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)]
'''
def getBoundingBox(filePath):
    with open(filePath) as XML_file:
        lat = []
        lon = []
        tree = ET.parse(XML_file)
        root = tree.getroot()
        for x in root:
            if x.find('lat') is not None:  
                latitute = x.find('lat').text
                lat.append(latitute)
            else:
                if x.find('latitude') is not None:
                    latitute = x.find('latitude').text
                    lat.append(latitute)
            if x.find('lon') is not None:  
                longitude = x.find('lon').text
                lon.append(longitude)
            else:
                if x.find('longitude') is not None:
                    longitude = x.find('longitude').text
                    lon.append(longitude)
        SpatialExtent={}
        if lat is not None:
            minlat=min(lat)
            maxlat=max(lat)
            if lon is not None:
                minlon=min(lon)
                maxlon=max(lon)
                SpatialExtent= [minlon,minlat,maxlon,maxlat]
                return SpatialExtent
            else:
                return None
        else:
            return None



'''
 extracts temporal extent of the xml
 input filepath: type string, file path to xml file
 output time: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
'''
def getTemporalExtent(filePath):
    with open(filePath) as XML_File:
        tree = ET.parse(XML_File)
        root = tree.getroot()
        alltime = []
        for x in root:
            if x.find('time') is not None:  
                time = x.find('time').text
                alltime.append(time)
        minTime= None
        maxTime= None
        if alltime is not None:
            minTime=min(alltime)
            maxTime=max(alltime)
            time=[]
            time.append(minTime)
            time.append(maxTime)
            return time
        else:
            return None

'''
 extracts coordinates from xml File (for vector representation)
 input filepath: type string, file path to xml file
 output VectorArray: type list, list of lists with length = 2, contains extracted coordinates of content from xml file
'''
def getVectorRepresentation(filePath):
    with open(filePath) as XML_file:
        lat = []
        lon = []
        tree = ET.parse(XML_file)
        root = tree.getroot()
        for x in root:
            if x.find('lat') is not None:  
                latitute = x.find('lat').text
                lat.append(latitute)
            else:
                if x.find('latitude') is not None:
                    latitute = x.find('latitude').text
                    lat.append(latitute)
            if x.find('lon') is not None:  
                longitude = x.find('lon').text
                lon.append(longitude)
            else:
                if x.find('longitude') is not None:
                    longitude = x.find('longitude').text
                    lon.append(longitude)
        VectorArray=[]
        if lon is None:
            return None
        else:
            if lat is None:
                return None
            else:
                counter=0
                for x in lon:
                    SingleArray=[]
                    SingleArray.append(lon[counter])
                    SingleArray.append(lat[counter])
                    VectorArray.append(SingleArray)
                    counter=counter+1
            return VectorArray

'''
 extracts coordinatesystem from xml File 
 input filepath: type string, file path to xml file
 output properties: type list, contains extracted coordinate system of content from xml file
'''
def getCRS(filePath):
    with open(filePath) as XML_File:
        tree = ET.parse(XML_File)
        root = tree.getroot()
        coordinatesystem = []
        for x in root:
            if x.find('crs') is not None:  
                crs = x.find('crs').text
                coordinatesystem.append(crs)
        if coordinatesystem is not None:
            return coordinatesystem
        else:
            return None
