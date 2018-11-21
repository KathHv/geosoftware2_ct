import fiona
import helpfunctions as hf


#gets called when the argument of the command request is a geopackage
def extractMetadata(filePath, whatMetadata):
    metadata = {}
    with fiona.open(filePath) as datasetFiona:
        if whatMetadata == "e":
            metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
            metadata["fileformat"] = datasetFiona._driver
            metadata["shape_elements"] = len(datasetFiona)
            metadata["projection"] = datasetFiona.meta["crs"]["proj"]
            metadata["encoding"] = datasetFiona.encoding
            metadata["used_ellipsoid"] = datasetFiona.crs["ellps"]
            geoTypes = []
            for shapeElement in datasetFiona:
                geoTypes.append(shapeElement["geometry"]["type"])
            metadata["occurancy_shapetypes"] = hf.countElements(geoTypes)
            metadata["shapetype"] = datasetFiona.meta["schema"]["geometry"]
        if whatMetadata != "t":
            metadata["bbox"] = [datasetFiona.bounds[0], datasetFiona.bounds[1], datasetFiona.bounds[2], datasetFiona.bounds[3]]
    
    # TO DO: bbox in wgs84 + temporal extent
    
    return metadata

