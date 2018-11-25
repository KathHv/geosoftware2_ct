import helpfunctions as hf
import json, gdal
from osgeo import ogr
import sys


#extract geometry
def extractGeometry (json, metadata): 
    try:
        jsonGeometry = None
        jsonGeometry = ogr.CreateGeometryFromJson(json)
        metadata["geometry"] = jsonGeometry
        return jsonGeometry
        
    except AttributeError, e:
        print('Warning: missing metadata. Could not extract geometry')
        print e
        return jsonGeometry

    except TypeError, e:
        print('Warning: missing metadata. Could not extract geometry')
        print e
        return jsonGeometry

        


# extract bounding box
def extractBbox (properties, geometry, metadata):
    try:
        bbox = None
        if not geometry:
            if not properties["bboxes"]:
                raise AttributeError("geometry is empty.")
            else: bbox = properties["bbox"]
        else:
            #Get Envelope returns a tuple (minX, maxX, minY, maxY)
            bbox = geometry.GetEnvelope()
        metadata["bbox"] = bbox
        return bbox
        
    except AttributeError, e:
        print('Warning: missing metadata. Could not extract bounding box')
        print e
        return bbox

    


#extract timeextend from json string
def extractTimeExtend (properties, metadata):
    try:
        metadata["start"] = properties["created_at"]
        metadata["end"] =  properties["closed_at"]
        

    except AttributeError, e:
        print('Warning: missing metadata. Could not extract timestamps')
        print e
      



#gets called when the argument of the command request is a geojson
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}
    #emptyContentError = Error
    #ValidityError = Error

    #reading file content and validate (geo)json
    try :    
        gjson = open(filePath, "rb")
        gjsonContent = json.load(gjson)
        #gjsonContentString = json.loads(gjson) #throws ValueError if content is invalid json
        gjson.close()

    except ValueError(json), e:
        print ('The geojson file from ' + filePath + ' is not valid.') 
        print e
        sys.exit(1)

    except RuntimeError, e:
        print ('Error: (geo)json file cannot be opened or read.')
        print e
        sys.exit(1)
    


    try: 
        if not gjsonContent:
            raise RuntimeError('The geojson file from ' + filePath + ' is empty')
    except RuntimeError, e:
        print ('Error')
        print e
        raise





    #metadata extraction    
    try:
        #gjsonContentString = json.dumps(gjsonContent, sort_keys=False, indent=4)
        features = gjsonContent["features"]
        properties = features[0]["properties"]

        #extracting bbox and geometry
        if whatMetadata != 't':
            bboxes = extractBbox(properties, extractGeometry(properties, metadata), metadata)
            if bboxes:
                hf.computeBboxOfMultiple(bboxes)
           
        
        # time extraction
        if whatMetadata != 's':
            extractTimeExtend(properties, metadata)


        # extract other metadata
        metadata["fileformat"] = fileFormat
        metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
        #metadata["type"] = gjson["type"]

    except AttributeError, e:
        print('Warning: missing metadata. Could not extract all metadata')
        print e


    return metadata

