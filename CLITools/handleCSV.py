import csv
import helpfunctions as hf

#gets called when the argument of the command request is a csv-file
def extractMetadata(filePath, whatMetadata): 
    metadata = {}
    if whatMetadata=="s":
        metadata["spatial_extent"] = extractSpatialExtentFromCSV(filePath)
        return metadata
    if whatMetadata=="t":
<<<<<<< HEAD
        #metadata["temporal_extent"] = extractTemporalExtentFromCSV(filePath)
        #gehört hier Start- oder Endzeit rein? Weil Temporal gibt es ja nicht mehr?
=======
        metadata["temporal_extent"] = extractTemporalExtentFromCSV(filePath)
        return metadata
    if whatMetadata=="e":
        metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
        metadata["keywords"] = extractKeywordsFromCSV(filePath)
        metadata["bbox"] = extractSpatialExtentFromCSV(filePath)
        metadata["temporal_extent"] = extractTemporalExtentFromCSV(filePath)
        metadata["Shapetypes"] = extractShapeTypeFromCSV(filePath)
        return metadata
    else:
        return metadata

def extractKeywordsFromCSV(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        counter=0
        metadata = {}
        elements = []
        firstrow = []
        for x in daten:
            elements.append(x)
        if hf.searchForParameters(elements, ["key","keywords","keys"]) is None:
            for x in elements:
                if counter < 1:
                    firstrow.append(x)
                    counter=counter+1    
            return firstrow
        else:
            metadata= hf.searchForParameters(elements,["key","keywords","keys"] ) 
            return metadata

def extractShapeTypeFromCSV(filePath):
     with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        Shapetypes= {}
        if hf.searchForParameters(elements, ["shape", "shapetype"]) is None:
            return None
        else:
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
        minlat= None
        maxlat= None
        if hf.searchForParameters(elements, ["lat", "latitude"]) is None:
            pass
        else:
            minlat= (min(SpatialLatExtent["lat"]))
            maxlat= (max(SpatialLatExtent["lat"]))
        SpatialLonExtent["lon"] = hf.searchForParameters(elements, ["lon", "longitude"])
        minlon= None
        maxlon= None
        if hf.searchForParameters(elements, ["lon", "longitude"]) is None:
            pass
        else:
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
        AllSpatialExtent= {}
        AllSpatialExtent["Time"] = hf.searchForParameters(elements, ["time", "timestamp"])
        minTime=None
        maxTime=None
        if hf.searchForParameters(elements, ["time", "timestamp"] ) is None:
            pass
        else:
            minTime= (min(AllSpatialExtent["Time"]))
            maxTime= (max(AllSpatialExtent["Time"]))
        time=[]
        time.append(minTime)
        time.append(maxTime)
        return time
