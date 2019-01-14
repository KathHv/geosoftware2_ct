import xml.etree.ElementTree as ET  
import helpfunctions as hf
import ogr2ogr
import sys, os
from osgeo import gdal, ogr
import convex_hull


def getBoundingBox(filePath):
    '''
    extract bounding box from xml
    input filepath: type string, file path to xml file
    output s: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)]
    '''
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
        spatialExtent={}
        if lat is not None:
            minlat=min(lat)
            maxlat=max(lat)
            if lon is not None:
                minlon=min(lon)
                maxlon=max(lon)
                spatialExtent= [minlon,minlat,maxlon,maxlat]
                return spatialExtent
            else:
                raise Exception('The xml file from ' + filePath + ' has no BoundingBox')
        else:
            raise Exception('The xml file from ' + filePath + ' has no BoundingBox')



'''
 extracts temporal extent of the xml
 input filepath: type string, file path to xml file
 output time: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
'''
def getTemporalExtent(filePath):
    '''
    extracts temporal extent of the xml
    input filepath: type string, file path to xml file
    output time: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
    '''
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
            raise Exception('The xml file from ' + filePath + ' has no TemporalExtent')

'''
 extracts coordinates from xml File (for vector representation)
 input filepath: type string, file path to xml file
 output VectorArray: type list, list of lists with length = 2, contains extracted coordinates of content from xml file
'''
def getVectorRepresentation(filePath):
    '''
    extracts coordinates from xml File (for vector representation)
    input filepath: type string, file path to xml file
    output VectorArray: type list, list of lists with length = 2, contains extracted coordinates of content from xml file
    '''
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
        vectorArray=[]
        if lon is None:
            raise Exception('The xml file from ' + filePath + ' has no VectorRepresentation')
        else:
            if lat is None:
                raise Exception('The xml file from ' + filePath + ' has no VectorRepresentation')
            else:
                counter=0
                for x in lon:
                    singleArray=[]
                    singleArray.append(lon[counter])
                    singleArray.append(lat[counter])
                    vectorArray.append(singleArray)
                    counter=counter+1
            return vectorArray

'''
 extracts coordinatesystem from xml File 
 input filepath: type string, file path to xml file
 output properties: type list, contains extracted coordinate system of content from xml file
'''
def getCRS(filePath):
    '''
    extracts coordinatesystem from xml File 
    input filepath: type string, file path to xml file
    output properties: type list, contains extracted coordinate system of content from xml file
    '''
    with open(filePath) as XML_File:
        tree = ET.parse(XML_File)
        root = tree.getroot()
        coordinatesystem = []
        for x in root:
            if x.find('crs') is not None:  
                crs = x.find('crs').text
                coordinatesystem.append(crs)
        if(len(coordinatesystem) > 0):
            return coordinatesystem
        else:
            raise Exception('The xml file from ' + filePath + ' has no CRS')
