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

DATATYPE = "application/kml"


def getBoundingBoxFromKML(filePath):
    ''' extract bounding box from kml \n
    input "filepath": type string, file path to kml file
    '''
    
    raise Exception("Bounding box could not be extracted.")




def getTemporalExtentFromKML(filePath):
    ''' extracts temporal extent of the kml \n
    input "filepath": type string, file path to kml file
    '''
    raise Exception("Temporal Extent could not be extracted.")



def getVectorRepresentationFromKML(filePath):
    ''' extracts coordinates from kml File (for vector representation) \n
    input "filepath": type string, file path to kml file
    '''
    raise Exception("Vector Representation could not be extracted.")


def getCRS(filePath):
    ''' extracts coordinatesystem from kml File \n
    input "filepath": type string, file path to kml file \n
    returns epsg code of the used coordinate reference system
    '''
    return hf.WGS84_EPSG_ID