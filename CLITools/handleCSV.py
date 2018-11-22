import csv
import helpfunctions as hf

#gets called when the argument of the command request is a csv-file
def extractMetadata(filePath, whatMetadata): 
    if whatMetadata=="s":
        metadata = {}
        metadata["Spatial Extent"] = extractSpatialExtentFromCSV(filePath)
        return metadata
    if whatMetadata=="t":
        metadata = {}
        metadata["Temporal Extent"] = extractTemporalExtentFromCSV(filePath)
        return metadata
    if whatMetadata=="e":
        metadata = {}
        metadata["Metadata"] = extractMetadataFromCSV(filePath)
        metadata["BoundingBox"] = extractSpatialExtentFromCSV(filePath)
        metadata["StartTime-EndTime"] = extractTemporalExtentFromCSV(filePath)
        metadata["Shapetypes"] = extractShapeTypeFromCSV(filePath)
        return metadata
    else:
        metadata = {}
        return metadata

def extractMetadataFromCSV(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        counter=0
        metadata = {}
        elements = []
        for x in daten:
            if counter < 1:
                elements.append(x)
                counter=counter+1    
        metadata["elements"] = elements
        return metadata

def extractShapeTypeFromCSV(filePath):
     with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        Shapetypes= {}
        Shapetypes = hf.countElements(hf.searchForParameters(elements, ["shape", "shapetype"]))
        return Shapetypes

def extractSpatialExtentFromCSV(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        SpatialExtent= {}
        SpatialLatExtent= {}
        SpatialLonExtent= {}
        SpatialLatExtent["lat"] = hf.searchForParameters(elements, ["lat", "latitude"])
        minlat= (min(SpatialLatExtent["lat"]))
        maxlat= (max(SpatialLatExtent["lat"]))
        SpatialLonExtent["lon"] = hf.searchForParameters(elements, ["lon", "longitude"])
        minlon= (min(SpatialLonExtent["lon"]))
        maxlon= (max(SpatialLonExtent["lon"]))
        SpatialExtent= [minlon,minlat,maxlon,maxlat]
        return SpatialExtent

def extractTemporalExtentFromCSV(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        TemporalExtent= {}
        AllSpatialExtent= {}
        AllSpatialExtent["Time"] = hf.searchForParameters(elements, ["time", "timestamp"])
        minTime= (min(AllSpatialExtent["Time"]))
        maxTime= (max(AllSpatialExtent["Time"]))
        TemporalExtent= [minTime, maxTime]
        return TemporalExtent