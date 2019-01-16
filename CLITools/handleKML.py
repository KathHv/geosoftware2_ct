import xml.etree.ElementTree as ET  
import jgraph as ig
import helpfunctions as hf
import ogr2ogr
import pygeoj
import sys, os
from osgeo import gdal, ogr
import convex_hull




def getBoundingBoxFromKML(filePath):
    ''' extract bounding box from kml
    input filepath: type string, file path to kml file
    '''
    
    raise Exception("Bounding box could not be extracted.")




def getTemporalExtentFromKML(filePath):
    ''' extracts temporal extent of the kml
    input filepath: type string, file path to kml file
    '''
    raise Exception("Temporal Extent could not be extracted.")



def getVectorRepresentationFromKML(filePath):
    ''' extracts coordinates from kml File (for vector representation)
    input filepath: type string, file path to kml file
    '''
    raise Exception("Vector Representation could not be extracted.")


def getCRS(filePath):
    ''' extracts coordinatesystem from kml File 
    input filepath: type string, file path to kml file
    returns epsg code of the used coordinate reference system
    '''
    return 4978