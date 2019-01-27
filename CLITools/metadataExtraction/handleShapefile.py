'''
@author: Benjamin Dietz
'''

import shapefile, fiona
import helpfunctions as hf
import gdal
from osgeo import ogr
import sys
import convex_hull

DATATYPE = "application/shp"

def isValid(path):
    '''Checks whether it is valid shapefile or not. \n
    input "path": type string, path to file which shall be extracted \n
    output true if file is valid, false if not
    '''
    pathWithoutEnding = path[:len(path)-4]
    if not (hf.exists(pathWithoutEnding + ".dbf") and hf.exists(pathWithoutEnding + ".shp") and \
        hf.exists(pathWithoutEnding + ".shx")):
        return False
    try:
        mydbf = open(pathWithoutEnding + ".dbf", "rb")
        myshp = open(pathWithoutEnding + ".shp", "rb")
        myshx = open(pathWithoutEnding + ".shx", "rb")
        r = shapefile.Reader(shp=myshp, dbf=mydbf, shx=myshx)
    except:
        return False
    return True

def getCRS(path):
    ''' gets the coordinate reference systems from the shapefile \n
    input "path": type string, file path to shapefile \n
    returns epsg code of the used coordinate reference system
    '''
    try:
        with fiona.open(path) as datasetFiona:
            if hasattr(datasetFiona, "crs"):
                if 'init' in datasetFiona.crs:
                    initField = datasetFiona.crs["init"]
                    crs = initField[initField.rfind(":") + 1 : ]
                    return int(crs)                
    except Exception as e:
        pathWithoutEnding = path[:len(path)-4]
        if not (hf.exists(pathWithoutEnding + ".dbf") and hf.exists(pathWithoutEnding + ".shp") and \
            hf.exists(pathWithoutEnding + ".shx")):
            raise Exception("One of the required files with the following ending are missing: .dbf, .shp or .shx")
        else:
            raise e
    raise Exception("The CRS cannot be extracted from shapefiles")


def getTemporalExtent(path):
    ''' extracts temporal extent of the shapefile \n
    input "path": type string, file path to shapefile file
    '''

    raise Exception("The temporal extent cannot be extracted of a shapefile")




def getVectorRepresentation(path):
    ''' abstract the geometry of the file with a polygon
    first: collects all the points of the file
    then: call the function that computes the polygon of it \n
    input "path": type string, file path to shapefile \n
    returns extracted coordinates of content from shapefiletype list, list of lists with length = 2, 
    '''
    try:
        if not '.shp' in path:
            shpPath = path[:path.rfind(".")+1]
            shpPath += "shp"
            if not hf.exists(shpPath):
                raise FileNotFoundError("Related shp-file could not be found!")
            else:
                path = shpPath
        with fiona.open(path) as datasetFiona:
            if datasetFiona is not None:
                coordinates = ""
                for x in datasetFiona:
                    if 'geometry' in x:
                        if 'coordinates' in x["geometry"]:
                            if len(x["geometry"]["coordinates"]) > 0:
                                coors = str(x["geometry"]["coordinates"][0])
                                coordinatesASString = coors[coors.find("(") : coors.rfind(")") + 1]
                                if len(coordinatesASString) < 3 and len(x["geometry"]["coordinates"]) == 2:
                                    coordinates += "(" + str(x["geometry"]["coordinates"][0]) + ", " + str(x["geometry"]["coordinates"][1]) + ")"
                                coordinates += coordinatesASString + ", "
                coordinates = coordinates[: len(coordinates) - 4]
                coordinates = coordinates.split("), (")
                for index, value in enumerate(coordinates):
                    coordinates[index] = str(value).split(", ")
            for index, value in enumerate(coordinates):
                if len(value) != 2:
                    print("Error: Coordinate does not have two values")
                try:
                    coordinates[index][0] = float(value[0].replace("(", "").replace(")", ""))
                    coordinates[index][1] = float(value[1].replace("(", "").replace(")", ""))
                except:
                    print("Error: Value cannot be converted into float" + value[0])
            coordinates = convex_hull.graham_scan(coordinates)
            return coordinates
    except Exception as e:
        pathWithoutEnding = path[:len(path)-4]
        if not (hf.exists(pathWithoutEnding + ".dbf") and hf.exists(pathWithoutEnding + ".shp") and \
            hf.exists(pathWithoutEnding + ".shx")):
            raise Exception("One of the required files with the following ending are missing: .dbf, .shp or .shx")
        else:
            raise e
    raise Exception("The vector representaton could not be extracted from the file")




def getBoundingBox(path):
    ''' extracts bounding box from shapfile \n
    input "path": type string, file path to shapefile \n
    returns bounding box of the file: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
    # try to get the bounding box with fiona
    try:
        with fiona.open(path) as datasetFiona:
            if hasattr(datasetFiona, "bounds"):
                if len(datasetFiona.bounds) > 3:
                    bboxInOriginalCRS = [datasetFiona.bounds[0], datasetFiona.bounds[1], datasetFiona.bounds[2], datasetFiona.bounds[3]]
                    return bboxInOriginalCRS

        # if fiona is not working (on this file), try to get the bbox with the module 'shapefile'
        pathWithoutEnding = path[:len(path)-4]
        if '.shp' in path:
            if hf.exists(pathWithoutEnding + ".dbf"):
                mydbf = open(pathWithoutEnding + ".dbf", "rb")
                myshp = open(path, "rb")
        elif '.dbf' in path:
            if hf.exists(pathWithoutEnding + ".shp"):
                myshp = open(pathWithoutEnding + ".shp", "rb")
                mydbf = open(path, "rb")
        if 'myshp' in locals():
            if 'mydbf' in locals():
                r = shapefile.Reader(shp=myshp, dbf=mydbf)
                boundingbox = r.bbox
                if type(boundingbox) == list:
                    if len(boundingbox) == 6:
                        boundingbox.pop(2)
                        boundingbox.pop(len(boundingbox)-1)
                return boundingbox
    except Exception as e:
        pathWithoutEnding = path[:len(path)-4]
        if not (hf.exists(pathWithoutEnding + ".dbf") and hf.exists(pathWithoutEnding + ".shp") and \
            hf.exists(pathWithoutEnding + ".shx")):
            raise Exception("One of the required files with the following ending are missing: .dbf, .shp or .shx")
        else:
            raise e

    raise Exception("The bounding box could not be extracted from the file")
