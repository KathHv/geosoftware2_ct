import xml.etree.ElementTree as ET  
import jgraph as ig
import helpfunctions as hf
import ogr2ogr
import pygeoj
import sys, os
from osgeo import gdal, ogr
import convex_hull

'''         
 extract bounding box from gml
 input filepath: type string, file path to gml file
 output myGeojson.bbox: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)]
'''
def getBoundingBox(filePath):
        ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        if myGeojson.bbox is not None:    
            return (myGeojson.bbox)
        else:
            raise Exception('The gml file from ' + filePath + ' has no BoundingBox')



'''
 extracts temporal extent of the gml
 input filepath: type string, file path to gml file
 output temporal_extent: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
'''
def getTemporalExtent(filePath):
        dateArray= []
        ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        properties= (myGeojson.get_feature(0).properties)
        for key, value in properties.items():     
                if key=="beginLifespanVersion" or key=="date" or key=="endLifespanVersion" or key=="Start_Date" or key=="End_Date":
                    dateArray.append(value)
                else:
                    pass
        temporal_extent= []
        os.remove("output.json")
        if(len(dateArray) > 0):
            temporal_extent.append(min(dateArray))
            temporal_extent.append(max(dateArray))
            return temporal_extent
        else: 
            raise Exception('The gml file from ' + filePath + ' has no TemporalExtent') 

'''
 extracts coordinates from gml File (for vector representation)
 input filepath: type string, file path to gml file
 output properties: type list, list of lists with length = 2, contains extracted coordinates of content from gml file
'''
def getVectorRepresentation(filePath):
        ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        properties= (myGeojson.get_feature(0).geometry.coordinates[0])
        os.remove("output.json")
        if properties is None:
            raise Exception('The gml file from ' + filePath + ' has no VectorRepresentation')
        else:
            return(properties)

'''
 extracts coordinatesystem from gml File 
 input filepath: type string, file path to gml file
 output properties: type list, contains extracted coordinate system of content from gml file
'''
def getCRS(filePath):
        coordinatesystem= []
        ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        properties= (myGeojson.get_feature(0).properties)
        for key, value in properties.items():     
                if key=="crs":
                    coordinatesystem.append(value)
                else:
                    pass
        os.remove("output.json")
        if(len(coordinatesystem) > 0):
            return coordinatesystem
        else: 
            raise Exception('The gml file from ' + filePath + ' has no CRS')

