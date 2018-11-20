import helpfunctions as hf

#gets called when the argument of the command request is a GeoTIFF
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}
    # Example how to use object:
    #metadata["bbox"] = [coor0, coor1, coor2, coor3]
    metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]

    # TO DO

    return metadata