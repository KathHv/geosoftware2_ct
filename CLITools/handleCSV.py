import csv
import helpfunctions as hf
import convex_hull



def getBoundingBox(filePath):
    ''' Function purpose: extracts the spatial extent (bounding box) from a csv-file
    input filepath: type string, file path to csv file
    output SpatialExtent: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
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
            raise Exception('The csv file from ' + filePath + ' has no BoundingBox')
        else:
            SpatialLonExtent.pop(0)
            minlon= (min(SpatialLonExtent))
            maxlon= (max(SpatialLonExtent))
        SpatialExtent= [minlon,minlat,maxlon,maxlat]
        return SpatialExtent




def getTemporalExtent(filePath):
    ''' extracts temporal extent of the csv
    input filepath: type string, file path to csv file
    output time: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
    '''

    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        AllSpatialExtent= []
        AllSpatialExtent.append(hf.searchForParameters(elements, ["time", "timestamp"]))
        if hf.searchForParameters(elements, ["time", "timestamp"] ) is None:
            raise Exception('The csv file from ' + filePath + ' has no TemporalExtent')
        else:
            time=[]
            time.append(min(AllSpatialExtent))
            time.append(max(AllSpatialExtent))
            return time




def getVectorRepresentation(filePath):
    ''' extracts coordinates from csv File (for vector representation)
    input filepath: type string, file path to csv file
    output VectorArray: type list, list of lists with length = 2, contains extracted coordinates of content from csv file
    '''
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
                raise Exception('The csv file from ' + filePath + ' has no VectorRepresentation')
            else:
                SpatialLonExtent.pop(0)
                counter=0
                for x in SpatialLatExtent:
                    SingleArray=[]
                    SingleArray.append(SpatialLonExtent[counter])
                    SingleArray.append(SpatialLatExtent[counter])
                    VectorArray.append(SingleArray)
                    counter=counter+1
                for index, x in enumerate(VectorArray):
                    for i, coor in enumerate(x):
                        VectorArray[index][i] = float(coor)
                VectorArray = convex_hull.graham_scan(VectorArray)
                return VectorArray




def getCRS(filePath):
    ''' extracts coordinatesystem from csv File 
    input filepath: type string, file path to csv file
    output properties: type list, contains extracted coordinate system of content from csv file
    '''
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