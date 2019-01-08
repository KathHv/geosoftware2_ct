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
def getBoundingFromXML(filePath):
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
def getExtentFromXML(filePath):
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
def getVectorRepresentationFromXML(filePath):
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
 extract bounding box from gml
 input filepath: type string, file path to gml file
 output myGeojson.bbox: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)]
'''
def getBoundingBoxFromGML(filePath):
        ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        if myGeojson.bbox is not None:    
            return (myGeojson.bbox)
        else:
            return None



'''
 extracts temporal extent of the gml
 input filepath: type string, file path to gml file
 output temporal_extent: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
'''
def getTemporalExtentFromGML(filePath):
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
            return None 




'''
 extracts coordinates from gml File (for vector representation)
 input filepath: type string, file path to gml file
 output properties: type list, list of lists with length = 2, contains extracted coordinates of content from gml file
'''
def getVectorRepresentationFromGML(filePath):
        ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        properties= (myGeojson.get_feature(0).geometry.coordinates[0])
        os.remove("output.json")
        if properties is None:
            return None
        else:
            return(properties)



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
            