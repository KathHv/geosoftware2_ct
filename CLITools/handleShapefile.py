import shapefile, fiona
import helpfunctions as hf
import gdal
from osgeo import ogr
import sys
import convex_hull


def getCRS(path):
'''
 gets the coordinate reference systems from the shapefile
 input filepath: type string, file path to shapefile
 output crsCode: type int, EPSG number of taken crs
'''
    raise Exception("The CRS cannot be extracted from shapefiles")




def getTemporalExtent(path):
    '''
 extracts temporal extent of the shapefile
 input path: type string, file path to shapefile file
'''
    raise Exception("The temporal extent cannot (yet) be extracted of a shapefile")




def getVectorRepresentation(path):
'''
 abstract the geometry of the file with a polygon
 first: collects all the points of the file
 then: call the function that computes the polygon of it
 input path: type string, file path to shapefile
 output coordinates: type list, list of lists with length = 2, contains extracted coordinates of content from shapefile
'''
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
    raise Exception("The vector representaton could not be extracted from the file")




def getBoundingBox(path):
'''
 extracts bounding box from shapfile
 input filepath: type string, file path to shapefile
 output bbox: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
'''
    # try to get the bounding box with fiona
    with fiona.open(path) as datasetFiona:
        if hasattr(datasetFiona, "crs"):
            if 'init' in datasetFiona.crs:
                initField = datasetFiona.crs["init"]
                crs = initField[initField.rfind(":") + 1 : ]
                if hasattr(datasetFiona, "bounds"):
                    if len(datasetFiona.bounds) > 3:
                        bboxInOriginalCRS = [datasetFiona.bounds[0], datasetFiona.bounds[1], datasetFiona.bounds[2], datasetFiona.bounds[3]]
                        if crs == "4326":
                            return bboxInOriginalCRS
                        else:
                            # TO DO: first transform into WGS 84
                            return "BBOX liegt in anderem Format vor (" + str(crs) + "): " + str(bboxInOriginalCRS)

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
            return r.bbox

    raise Exception("The bounding box could not be extracted from the file")

