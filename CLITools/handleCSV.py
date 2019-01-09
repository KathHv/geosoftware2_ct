import csv
import helpfunctions as hf
import convex_hull


'''
 Function purpose: extracts the spatial extent (bounding box) from a csv-file
 input filepath: type string, file path to csv file
 output SpatialExtent: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
'''
def getBoundingBox(filePath):
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

'''
 extracts coordinatesystem from csv File 
 input filepath: type string, file path to csv file
 output properties: type list, contains extracted coordinate system of content from csv file
'''
def getCRS(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        CoordinateSystem={}
        CoordinateSystem= hf.searchForParameters(elements, ["crs"])
        if hf.searchForParameters(elements, ["crs"]) is None:
            return None
        else:
            return CoordinateSystem