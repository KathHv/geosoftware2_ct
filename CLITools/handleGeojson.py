import helpfunctions as hf


#gets called when the argument of the command request is a geojson
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}
    
    # Example how to use object:
    #metadata["bbox"] = [coor0, coor1, coor2, coor3]
    metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]

    if fileFormat == 'geojson' or fileFormat == 'json': 
            gjson = open(filePath, "rb")
            #print ("gjson open filePath: " + str(gjson))            
            gjsonContent = json.load(gjson)
            gjson.close()
            ##print ('gjson: ' + str(gjsonContent))

            ##validate geojson
            ##gjsonContent.is_valid
            ##gjsonContent.errors()
            gjsonContent = json.dumps(gjsonContent, sort_keys=False, indent=4)
    else:
        print("\nError: The searched .geojson file was not found under " + str(gjson) + "\n")
    
    gjson1=str(gjsonContent)
    ##print ('gjson as a string' + str(gjson1))

    gjson1=str(gjsonContent)
    ##print ('gjson as a string' + str(gjson1))

    ##extract filename and fileformatGeo
    if whatMetadata != 's':
        metadata["filename"] = filePath[filePath.rfind("/")+1:]
        metadata["fileformat"] = fileFormat
        #metadata["type"] = gjson["type"]


    ## create bbox
    ## extract geometry
    print ('before createGeometry')
    geomJson = ogr.CreateGeometryFromJson(gjson1)
    metadata["geometry"] = geomJson
    print ('after createGeometry: ' + str(geomJson))
    print ("%d,%d" % (geomJson.GetX(), geomJson.GetY()))
    # Get Envelope returns a tuple (minX, maxX, minY, maxY)
    print ('before GetEnvelope')
    bbox = geomJson.GetEnvelope()
    print ("after GetEnvelope: %r" %(bbox))
    print ("minX: %d, minY: %d, maxX: %d, maxY: %d" (bbox[0],bbox[2],bbox[1],bbox[3]))
    metadata["bbox"] = bbox
    
    #if whatMetadata != 's':
     #   metadata["shapetype"] =  ourFile.shapeTypeName
      #  metadata["shape_elements"] = len(ourFile)

    # time extraction


    return metadata
