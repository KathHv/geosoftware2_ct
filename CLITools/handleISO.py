import xml.etree.ElementTree as ET  
import networkx as nx
import helpfunctions as hf


#gets called when the argument of the command request is a ISOxxx
def extractMetadata(fileFormat, filePath, whatMetadata):
        if fileFormat== "xml":
            if whatMetadata=="s":
                metadata = {}
                metadata["bbox"] = extractSpatialExtentFromXML(filePath)
                return metadata
            if whatMetadata=="t":
                metadata = {}
                metadata["time_end"] = extractEndTimeFromXML(filePath)
                metadata["time_begin"] = extractStartTimeFromXML(filePath)
                return metadata
            if whatMetadata=="e":
                metadata = {}
                metadata["bbox"] = extractSpatialExtentFromXML(filePath)
                metadata["time_end"] = extractEndTimeFromXML(filePath)
                metadata["time_begin"] = extractStartTimeFromXML(filePath)
                metadata["Shapetypes"] = extractShapeTypeFromXML(filePath)
                return metadata
        if fileFormat== "gml":
            if whatMetadata=="s":
                metadata = {}
                metadata["bbox"] = extractSpatialExtentFromGML(filePath)
                return metadata
            if whatMetadata=="t":
                metadata = {}
                metadata["time_end"] = extractEndTimeFromGML(filePath)
                metadata["time_begin"] = extractStartTimeFromGML(filePath)
                return metadata
            if whatMetadata=="e":
                metadata = {}
                metadata["bbox"] = extractSpatialExtentFromGML(filePath)
                metadata["time_end"] = extractEndTimeFromGML(filePath)
                metadata["time_begin"] = extractStartTimeFromGML(filePath)
                metadata["Shapetypes"] = extractShapeTypeFromGML(filePath)
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

def extractStartTimeFromXML(filePath):
    with open(filePath) as XML_File:
        tree = ET.parse(XML_File)
        root = tree.getroot()
        alltime = []
        for x in root:
            if x.find('time') is not None:  
                time = x.find('time').text
                alltime.append(time)
        minTime= None
        if alltime is not None:
            minTime=min(alltime)
        return minTime

def extractEndTimeFromXML(filePath):
    with open(filePath) as XML_File:
        tree = ET.parse(XML_File)
        root = tree.getroot()
        alltime = []
        for x in root:
            if x.find('time') is not None:  
                time = x.find('time').text
                alltime.append(time)
        maxTime= None
        if alltime is not None:
            maxTime=max(alltime)
        return maxTime

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

def extractShapeTypeFromGML(filePath):
    with open(filePath) as GML_File:
        #G = nx.parse_gml(GML_File)
        #print(G.node)
        #return None
        tree = ET.parse(GML_File)
        root = tree.getroot()
        GML=[]
        for x in root:
            gml_single = x.text
            GML.append(gml_single)
            print(GML.index("base:Identifier"))

def extractEndTimeFromGML(filePath):
    with open(filePath) as GML_File:
        return None

def extractStartTimeFromGML(filePath):
    with open(filePath) as GML_File:
        return None

def extractSpatialExtentFromGML(filePath):
    with open(filePath) as GML_File:
        return None