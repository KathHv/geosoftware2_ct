import csv
import helpfunctions as hf
import convex_hull


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
        SpatialLatExtent=[]
        SpatialLonExtent=[]
        SpatialLatExtent= hf.searchForParameters(elements, ["lat", "latitude","Latitude"])
        minlat= None
        maxlat= None
        if hf.searchForParameters(elements, ["lat", "latitude","Latitude"]) is None:
            pass
        else:
            SpatialLatExtent.pop(0)
            minlat= (min(SpatialLatExtent))
            maxlat= (max(SpatialLatExtent))
        SpatialLonExtent= hf.searchForParameters(elements, ["lon", "longitude","Longitude"])
        minlon= None
        maxlon= None
        if hf.searchForParameters(elements, ["lon", "longitude","Longitude"]) is None:
            pass
        else:
            SpatialLonExtent.pop(0)
            minlon= (min(SpatialLonExtent))
            maxlon= (max(SpatialLonExtent))
        SpatialExtent= [minlon,minlat,maxlon,maxlat]
        return SpatialExtent



'''
 extracts temporal extent of the csv
 input filepath: type string, file path to csv file
 output time: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
'''
def getTemporalExtent(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        AllSpatialExtent= []
        AllSpatialExtent.append(hf.searchForParameters(elements, ["time", "timestamp"]))
        if hf.searchForParameters(elements, ["time", "timestamp"] ) is None:
            return None
        else:
            time=[]
            time.append(min(AllSpatialExtent))
            time.append(max(AllSpatialExtent))
            return time



'''
 extracts coordinates from csv File (for vector representation)
 input filepath: type string, file path to csv file
 output VectorArray: type list, list of lists with length = 2, contains extracted coordinates of content from csv file
'''
def getVectorRepresentation(filePath):
   with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        VectorArray= []
        SpatialLatExtent=[]
        SpatialLonExtent=[]
        SpatialLatExtent= hf.searchForParameters(elements, ["lat", "latitude","Latitude"])
        SpatialLonExtent= hf.searchForParameters(elements, ["lon", "longitude","Longitude"])
        if hf.searchForParameters(elements, ["lat", "latitude","Latitude"]) is None:
            return None
        else:
            SpatialLatExtent.pop(0)
            if hf.searchForParameters(elements, ["lon", "longitude","Longitude"]) is None:
                return None
            else:
                SpatialLonExtent.pop(0)
                counter=0
                for x in SpatialLatExtent:
                    SingleArray=[]
                    SingleArray.append(SpatialLonExtent[counter])
                    SingleArray.append(SpatialLatExtent[counter])
                    VectorArray.append(SingleArray)
                    counter=counter+1
                VectorArray = convex_hull.graham_scan(VectorArray)
                return VectorArray