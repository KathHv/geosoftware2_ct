import xml.etree.ElementTree as ET  
import jgraph as ig
import helpfunctions as hf
import ogr2ogr
import pygeoj
import sys, os
from osgeo import gdal, ogr


#gets called when the argument of the command request is a ISOxxx
def extractMetadata(fileFormat, filePath, whatMetadata):
        metadata = {}
        if fileFormat== "xml":
            if whatMetadata=="s":
                metadata["bbox"] = extractSpatialExtentFromXML(filePath)
                return metadata
            if whatMetadata=="t":
                metadata["temporal_extent"] = extractTemporalExtentFromXML(filePath)
                return metadata
            if whatMetadata=="e":
                metadata["bbox"] = extractSpatialExtentFromXML(filePath)
                metadata["temporal_extent"] = extractTemporalExtentFromXML(filePath)
                metadata["Shapetypes"] = extractShapeTypeFromXML(filePath)
                metadata["Vectors"]=extractVectorRepFromXML(filePath)
                return metadata
        if fileFormat== "gml":
            hf.disablePrint()
            if whatMetadata=="s":
                metadata["bbox"] = extractSpatialExtentFromGML(filePath)
                hf.enablePrint()
                return metadata
            if whatMetadata=="t":
                metadata["temporal_extent"] = extractTemporalExtentFromGML(filePath)
                hf.enablePrint()
                return metadata
            if whatMetadata=="e":
                metadata["bbox"] = extractSpatialExtentFromGML(filePath)
                metadata["temporal_extent"] = extractTemporalExtentFromGML(filePath)
                metadata["vectors"]= extractVectorRepFromGML(filePath)
                hf.enablePrint()
                return metadata
        if fileFormat== "kml":
            hf.disablePrint()
            if whatMetadata=="s":
                metadata["bbox"] = extractSpatialExtentFromKML(filePath)
                hf.enablePrint()
                return metadata
            if whatMetadata=="t":
                metadata["temporal_extent"] = extractTemporalExtentFromKML(filePath)
                hf.enablePrint()
                return metadata
            if whatMetadata=="e":
                metadata["bbox"] = extractSpatialExtentFromKML(filePath)
                metadata["temporal_extent"] = extractTemporalExtentFromKML(filePath)
                metadata["vectors"]= extractVectorRepFromKML(filePath)
                hf.enablePrint()
                return metadata


def extractSpatialExtentFromXML(filePath):
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

def extractTemporalExtentFromXML(filePath):
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

def extractShapeTypeFromXML(filePath):
    with open(filePath) as XML_File:
        tree = ET.parse(XML_File)
        root = tree.getroot()
        allshapes = []
        for x in root:
            if x.find('shape') is not None:
                shapes = x.find('shape').text
                allshapes.append(shapes)
        if allshapes is not None:
            Shapetypes = hf.countElements(allshapes)
            return Shapetypes
        else: 
            return None

def extractVectorRepFromXML(filePath):
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
            

def extractSpatialExtentFromGML(filePath):
        ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        if myGeojson.bbox is not None:    
            return (myGeojson.bbox)
        else:
            return None

def extractTemporalExtentFromGML(filePath):
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

def extractVectorRepFromGML(filePath):
        ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        properties= (myGeojson.get_feature(0).geometry.coordinates[0])
        os.remove("output.json")
        if properties is None:
            return None
        else:
            return(properties)
            
def extractSpatialExtentFromKML(filePath):
        '''srcDS = gdal.OpenEx(filePath)
        ds = gdal.VectorTranslate('output.json', srcDS, format='GeoJSON')
        myGeojson = pygeoj.load(ds)
        print(myGeojson)'''
        return None
        #TODO

def extractTemporalExtentFromKML(filePath):
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

def extractVectorRepFromKML(filePath):
        '''ogr2ogr.main(["","-f", "GeoJSON", "output.json", filePath])
        myGeojson = pygeoj.load(filepath="output.json")
        properties= (myGeojson.get_feature(0).geometry.coordinates[0])
        os.remove("output.json")
        if properties is None:
            return None
        else:
            return(properties)'''
        return None
        #TODO
            