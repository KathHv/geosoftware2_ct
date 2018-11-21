import shapefile, fiona
import helpfunctions as hf

#gets called when the argument of the command request is a shape-file
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}
    with fiona.open(filePath) as datasetFiona:
        # double security with some attributes
        if whatMetadata == "e":
            metadata["encoding"] = datasetFiona.encoding
            geoTypes = []
            for shapeElement in datasetFiona:
                geoTypes.append(shapeElement["geometry"]["type"])
            metadata["occurancy_shapetypes"] = hf.countElements(geoTypes)
            metadata["shapetype"] = datasetFiona.meta["schema"]["geometry"]
        if whatMetadata != "t":
            metadata["bbox"] = [datasetFiona.bounds[0], datasetFiona.bounds[1], datasetFiona.bounds[2], datasetFiona.bounds[3]]
    if fileFormat == 'shp':
        myshp = open(filePath, "rb")
        dbfPath = filePath[:filePath.rfind(".")] + ".dbf"
        if hf.exists(dbfPath):
            mydbf = open(dbfPath, "rb")
            ourFile = shapefile.Reader(shp=myshp, dbf=mydbf)
        else:
            raise Exception("The searched .dbf file was not found under " + dbfPath + "\n")
    else:
        mydbf = open(filePath, "rb")
        shpPath = filePath[:filePath.rfind(".")] + ".shp"
        if hf.exists(shpPath):
            myshp = open(shpPath, "rb")
            ourFile = shapefile.Reader(shp=myshp, dbf=mydbf)
        else: 
            raise Exception("The searched .shp file was not found under " + shpPath + "\n")
    if whatMetadata != 's':
        metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
        metadata["fileformat"] = fileFormat
    metadata["bbox"] = ourFile.bbox
    if whatMetadata != 's':
        metadata["shapetype"] =  ourFile.shapeTypeName
        metadata["shape_elements"] = len(ourFile)
    return metadata