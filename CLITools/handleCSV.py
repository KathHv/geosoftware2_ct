import csv
import helpfunctions as hf

# Function name: extractMetadata
# Function purpose: Gets called when the argument of the command request is a csv-file
# Input: filePath, whatMetadata (e, s or t)
# Output: object Metadata (corresponding to whatMetadata)
def extractMetadata(filePath, whatMetadata): 
    metadata = {}
    if whatMetadata=="s":
        metadata["Spatial Extent"] = extractSpatialExtentFromCSV(filePath)
        return metadata
    if whatMetadata=="t":
        metadata["temporal_extent"] = extractTemporalExtentFromCSV(filePath)
        # gehört hier Start- oder Endzeit rein? Weil Temporal gibt es ja nicht mehr?
        return metadata
    if whatMetadata=="e":
        metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
        metadata["keywords"] = extractKeywordsFromCSV(filePath)
        metadata["bbox"] = extractSpatialExtentFromCSV(filePath)
        metadata["time_end"] = extractEndTimeFromCSV(filePath)
        metadata["time_begin"] = extractStartTimeFromCSV(filePath)
        metadata["Shapetypes"] = extractShapeTypeFromCSV(filePath)
        return metadata
    else:
        return metadata

# Function name: extractKeywordsFromCSV
# Function purpose: ?
# Input: filePath
# Output: Array firstrow (if no keyword is found), object Metadata (if keyword is found)
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

# Function name: extractShapeTypeFromCSV
# Function purpose: extracts the Shapetype from the csv-file
# Input: filePath
# Output: object Shapetypes (if shapetype is found), None (if Shapetype is not found)
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

# Function name: extractSpatialExtentFromCSV
# Function purpose: extracts the spatial entent from a csv-file
# Input: filePath
# Output: object SpatialExtent consisting of minlon, minlat, maxlon, maxlat
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

# Function name: extractStartTimeFromCSV
# Function purpose: extracts the starting time from a csv-file
# Input: filePath
# Output: minTime
def extractStartTimeFromCSV(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        AllSpatialExtent= {}
        AllSpatialExtent["Time"] = hf.searchForParameters(elements, ["time", "timestamp"])
        minTime= (min(AllSpatialExtent["Time"]))
        return minTime

# Function name: extractEndTimeFromCSV
# Function purpose: extracts the ending time from a csv-file
# Input: filePath
# Output: maxTime
def extractEndTimeFromCSV(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        AllSpatialExtent= {}
        AllSpatialExtent["Time"] = hf.searchForParameters(elements, ["time", "timestamp"])
        maxTime= (max(AllSpatialExtent["Time"]))
        return maxTime
