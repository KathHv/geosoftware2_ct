'''
@author: Niklas Aßelmann
'''

import xml.etree.ElementTree as ET  
import jgraph as ig
import helpfunctions as hf
import ogr2ogr
import pygeoj
import sys, os
from osgeo import gdal, ogr
import convex_hull

DATATYPE = "application/gml"

def isValid(filePath):
    '''
    Checks whether it is valid gml or not. \n
    input "path": type string, path to file which shall be extracted \n
    output true if file is valid, false if not
    '''
    try:
        ogr2ogr.main(["","-f", "GeoJSON", "outputV.json", filePath])
        myGeojson = pygeoj.load(filepath="outputV.json")
        return True
    except:
        raise Exception('The gml file from ' + filePath + ' has no valid gml Attributes')


def getBoundingBox(filePath):
    '''         
    extract bounding box from gml \n
    input "filepath": type string, file path to gml file \n
    returns bounding box of the file: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)]
    '''
    ogr2ogr.main(["","-f", "GeoJSON", "outputB.json", filePath])
    myGeojson = pygeoj.load(filepath="outputB.json")
    os.remove("outputB.json")
    if myGeojson.bbox is not None:    
        return (myGeojson.bbox)
    else:
        raise Exception('The gml file from ' + filePath + ' has no BoundingBox')




def getTemporalExtent(filePath):
    '''
    extracts temporal extent of the gml \n
    input "filepath": type string, file path to gml file \n
    returns temporal extent of the file: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
    '''
    dateArray= []
    ogr2ogr.main(["","-f", "GeoJSON", "outputT.json", filePath])
    myGeojson = pygeoj.load(filepath="outputT.json")
    properties= (myGeojson.get_feature(0).properties)
    for key, value in properties.items():     
            if key=="beginLifespanVersion" or key=="date" or key=="endLifespanVersion" or key=="Start_Date" or key=="End_Date":
                dateArray.append(value)
            else:
                pass
    temporal_extent= []
    os.remove("outputT.json")
    if(len(dateArray) > 0):
        temporal_extent.append(min(dateArray))
        temporal_extent.append(max(dateArray))
        return temporal_extent
    else: 
        raise Exception('The gml file from ' + filePath + ' has no TemporalExtent') 




def getVectorRepresentation(filePath):
    '''
    extracts coordinates from gml File (for vector representation) \n
    input "filepath": type string, file path to gml file \n
    returns extracted coordinates of content: type list, list of lists with length = 2
    '''
    ogr2ogr.main(["","-f", "GeoJSON", "outputV.json", filePath])
    myGeojson = pygeoj.load(filepath="outputV.json")
    properties= (myGeojson.get_feature(0).geometry.coordinates[0])
    os.remove("outputV.json")
    if properties is None:
        raise Exception('The gml file from ' + filePath + ' has no VectorRepresentation')
    else:
        properties= convex_hull.graham_scan(properties)
        return properties




def getCRS(filePath):
    '''
    extracts coordinatesystem from gml File \n
    input "filepath": type string, file path to gml file \n
    returns epsg code of used coordinate reference system: type list

    coordinatesystem= []
    ogr2ogr.main(["","-f", "GeoJSON", "outputCRS.json", filePath])
    myGeojson = pygeoj.load(filepath="outputCRS.json")
    properties= (myGeojson.get_feature(0).properties)
    for key, value in properties.items():     
        if key=="srsID":
            coordinatesystem.append(value)
        else:
            pass
    os.remove("outputCRS.json")
    if hf.searchForParameters(["crs","srsID"],coordinatesystem) is None:
        raise Exception('The gml file from ' + filePath + ' has no CRS')
    if hf.searchForParameters(["crs","srsID"],coordinatesystem,) == "4326" or "WGS84":
        return "4326"
    else:
        raise Exception('The gml file from ' + filePath + ' has no WGS84 CRS')
    return "4326"
    '''
    return "4326"

