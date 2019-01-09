import xml.etree.ElementTree as ET  
import jgraph as ig
import helpfunctions as hf
import ogr2ogr
import pygeoj
import sys, os
from osgeo import gdal, ogr
import convex_hull

'''
 extract bounding box from kml
 input filepath: type string, file path to kml file
 output bbox: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)]
'''
def getBoundingBoxFromKML(filePath):
        '''srcDS = gdal.OpenEx(filePath)
        ds = gdal.VectorTranslate('output.json', srcDS, format='GeoJSON')
        myGeojson = pygeoj.load(ds)
        print(myGeojson)'''
        return None
        #TODO



'''
 extracts temporal extent of the kml
 input filepath: type string, file path to kml file
 output timeExtent: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
'''
def getTemporalExtentFromKML(filePath):
        '''dateArray= []
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
            return None '''
        return None
        #TODO



'''
 extracts coordinates from kml File (for vector representation)
 input filepath: type string, file path to kml file
 output coordinates: type list, list of lists with length = 2, contains extracted coordinates of content from kml file
'''
def getVectorRepresentationFromKML(filePath):
        '''ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        properties= (myGeojson.get_feature(0).geometry.coordinates[0])
        os.remove("output.json")
        if properties is None:
            return None
        else:
            return(properties)'''
        #coordinates = convex_hull.graham_scan(coordinates)
        return None
        #TODO

'''
 extracts coordinatesystem from kml File 
 input filepath: type string, file path to kml file
 output properties: type list, contains extracted coordinate system of content from kml file
'''
def getCRS(filePath):
    '''
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
            return None 
            '''
    return None
    #TODO
