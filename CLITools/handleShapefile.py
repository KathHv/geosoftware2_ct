import shapefile, fiona
import helpfunctions as hf
import gdal
from osgeo import ogr
import sys

#gets called when the argument of the command request is a shape-file
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}
    
    if whatMetadata == "e":
        addictionalMetadata = getAdditionalMetadata(filePath, fileFormat)
        for x in addictionalMetadata:
            metadata[x] = addictionalMetadata[x]
        try:
            metadata["bbox"] = getBoundingBox(filePath)
        except Exception as e:
            print("Exception: " + str(e))   
        try:
            metadata["temporal_extent"] = getTemporalExtent(filePath)
        except Exception as e:
            print("Exception: " + str(e))
        try:
            metadata["vector_representation"] = getVectorRepresentation(filePath)
        except Exception as e:
            print("Exception: " + str(e))
        
    if whatMetadata == "e" or whatMetadata == "s":
        metadata["bbox"] = getBoundingBox(filePath)
        #metadata["crs"] = getCRS(filePath)
        metadata["vector_representation"] = getVectorRepresentation(filePath)

    if whatMetadata == "t":
        metadata["temporal_extent"] = getTemporalExtent(filePath)

    return metadata

def getTemporalExtent(path):
    raise Exception("The temporal extent cannot (yet) be extracted of a shapefile")

def getAdditionalMetadata(path, format):
    metadata = {}
    with fiona.open(path) as datasetFiona:
        metadata["encoding"] = datasetFiona.encoding
        geoTypes = []
        for shapeElement in datasetFiona:
            geoTypes.append(shapeElement["geometry"]["type"])
        metadata["occurancy_shapetypes"] = hf.countElements(geoTypes)
        metadata["shapetype"] = datasetFiona.meta["schema"]["geometry"]
        if datasetFiona.crs is not None and len(str(datasetFiona.crs)) > 5:
            metadata["crs"] = str(datasetFiona.crs)
        if datasetFiona.crs_wkt is not None:
            if 'crs' in metadata: 
                metadata["crs"] += " " + str(datasetFiona.crs_wkt)
            elif len(str(datasetFiona.crs_wkt)) > 3: metadata["crs"] = str(datasetFiona.crs_wkt)
        metadata["filename"] = path[path.rfind("/")+1:path.rfind(".")]
        metadata["format"] = format
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
                ourFile = shapefile.Reader(shp=myshp, dbf=mydbf)
                metadata["shapetype"] =  ourFile.shapeTypeName
                metadata["shape_elements"] = len(ourFile)
    return metadata


def getVectorRepresentation(path):
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
        return coordinates
    raise Exception("The vector representaton could not be extracted from the file")


def getBoundingBox(path):
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

