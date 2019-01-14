import csv
import helpfunctions as hf
import convex_hull



def getBoundingBox(filePath):
    '''
    Function purpose: extracts the spatial extent (bounding box) from a csv-file
    input filepath: type string, file path to csv file
    output spatialExtent: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        spatialExtent= {}
        spatialLatExtent=[]
        spatialLonExtent=[]
        spatialLatExtent= hf.searchForParameters(elements, ["lat", "latitude","Latitude"])
        minlat= None
        maxlat= None
        if hf.searchForParameters(elements, ["lat", "latitude","Latitude"]) is None:
            pass
        else:
            spatialLatExtent.pop(0)
            minlat= (min(spatialLatExtent))
            maxlat= (max(spatialLatExtent))
        spatialLonExtent= hf.searchForParameters(elements, ["lon", "longitude","Longitude"])
        minlon= None
        maxlon= None
        if hf.searchForParameters(elements, ["lon", "longitude","Longitude"]) is None:
            raise Exception('The csv file from ' + filePath + ' has no BoundingBox')
        else:
            spatialLonExtent.pop(0)
            minlon= (min(spatialLonExtent))
            maxlon= (max(spatialLonExtent))
        spatialExtent= [minlon,minlat,maxlon,maxlat]
        return spatialExtent




def getTemporalExtent(filePath):
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        allspatialExtent= []
        allspatialExtent.append(hf.searchForParameters(elements, ["time", "timestamp"]))
        if hf.searchForParameters(elements, ["time", "timestamp"] ) is None:
            raise Exception('The csv file from ' + filePath + ' has no TemporalExtent')
        else:
            time=[]
            time.append(min(allspatialExtent))
            time.append(max(allspatialExtent))
            return time




def getVectorRepresentation(filePath):
   with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        vectorArray= []
        spatialLatExtent=[]
        spatialLonExtent=[]
        spatialLatExtent= hf.searchForParameters(elements, ["lat", "latitude","Latitude"])
        spatialLonExtent= hf.searchForParameters(elements, ["lon", "longitude","Longitude"])
        if hf.searchForParameters(elements, ["lat", "latitude","Latitude"]) is None:
            return None
        else:
            spatialLatExtent.pop(0)
            if hf.searchForParameters(elements, ["lon", "longitude","Longitude"]) is None:
                raise Exception('The csv file from ' + filePath + ' has no VectorRepresentation')
            else:
                spatialLonExtent.pop(0)
                counter=0
                for x in spatialLatExtent:
                    singleArray=[]
                    singleArray.append(spatialLonExtent[counter])
                    singleArray.append(spatialLatExtent[counter])
                    vectorArray.append(singleArray)
                    counter=counter+1
                return vectorArray

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
            raise Exception('The csv file from ' + filePath + ' has no CRS')
        else:
            return CoordinateSystem