import helpfunctions as hf
import json, gdal
from osgeo import ogr
import sys
from datetime import datetime
import datetime
from django.utils.dateparse import parse_datetime
import django, pytz
import unicodedata

# all extracted metadata are saved to the dict metadata


foundCoordsX = []
foundCoordsY = []

coordinates = []      
metadataList = []

#extract geometry
def extractGeometry (json): 
    try:
        jsonGeometry = None
        jsonGeometry = ogr.CreateGeometryFromJson(json)
        #metadata["geometry"] = jsonGeometry
        return jsonGeometry
        
    except AttributeError as e:
        print('Warning: missing metadata. Could not extract geometry')
        print(e)
        return jsonGeometry 

    except TypeError as e:
        print('Warning: missing metadata. Could not extract geometry')
        print(e)
        return jsonGeometry 
        




# extract Coordinates from coordinate Arrays
def extractCoordinatesForBbox(coordinateArray):
    #further arrays with coordinates
    if type(coordinateArray) == list and len(coordinateArray) == 2 and type(coordinateArray[0]) == float and type(coordinateArray[1]):
        global foundCoordsX
        global foundCoordsY
        foundCoordsX.append(format(float(coordinateArray[1]), '.2f'))
        foundCoordsY.append(format(float(coordinateArray[0]), '.2f'))
    else :
        if coordinateArray == list and len(coordinateArray) != 0:
            for value in coordinateArray:
                extractCoordinatesForBbox(value)
                        
#search in Json for Lists or Dicts of coordinates
def searchForCoordinates (gjsonContent):
    if type(gjsonContent) == dict:
        for key, value in gjsonContent.items():           
            if key == "coordinates":
                extractCoordinatesForBbox(value)
                if type(value) == dict or type(value) == list:
                    searchForCoordinates(value)
            else:
                searchForCoordinates(value)
    if type(gjsonContent) == list:
        for element in gjsonContent:
            searchForCoordinates(element)


# extract bounding box
def getBoundingBox (contentString, content, geometry):
    try:
        bbox = None
        if not geometry:
      
            searchForCoordinates(content)
            global foundCoordsX 
            global foundCoordsY
            foundCoordsX= sorted(foundCoordsX)
            foundCoordsY = sorted(foundCoordsY)
            bbox=[foundCoordsY[0], foundCoordsX[0], foundCoordsY[len(foundCoordsY)-1], foundCoordsX[len(foundCoordsX)-1]]
        else:
            bbox = geometry.GetEnvelope()
        return bbox
        
    except AttributeError as e:
        print('Warning: missing metadata. Could not extract bounding box')
        print (e)
        return bbox



def getCRS(gjsonContent):
    crs= {}
    
    searchParam = ["crs", "coordinate_system", "coordinate_reference_system", "coordinateSystem", "CRS", "coordianteReferenceSystem"]    
    fillIfAvailable(searchParam, gjsonContent, crs)


    return crs


ignore = ["created_at", "closed_at", "created", "closed", "initilize", "init", "last_viewed", "last_change", "change", "last_Change", "lastChange"]    
#ignore = []

#searches for time elements in a json
def searchForTimeElements(gjsonContent, dateArray):
    if type(gjsonContent) == dict:
        for key, value in gjsonContent.items():     
            if key not in ignore:
                   searchForTimeElements(value, dateArray)    
    else: 
        if type(gjsonContent) == list:
            for element in gjsonContent:
                searchForTimeElements(element, dateArray)
        else:
            if type(gjsonContent) == bytes:
                datetime_object = parse_datetime(unicodedata.normalize('NFKD', gjsonContent).encode('ascii', 'ignore') )
                if type(datetime_object) ==datetime.datetime: #date
                    dateArray.append(gjsonContent)



#extract timeextend from json string
def getTemporalExtent (gjsonContent):
    try:
        dateArray = []
        timeExtent = []

        searchForTimeElements(gjsonContent,dateArray)
        if len(dateArray)!= 0:
            dateArray = sorted(dateArray)
            timeExtent.append(dateArray[0])
            timeExtent.append(dateArray[len(dateArray)-1])
        else:
            raise AttributeError
        return timeExtent
        

    except AttributeError as e:
        print('Warning: missing metadata. Could not extract timestamps')
        print (e)
      






#extract coordinates as tuples for metadata keyword 'coordinate', 'coord', 'coordinates' or 'coords'
def extractCoordinatesForMetadata(coordinateArray):
    global coordinates
    #further arrays with coordinates
    if type(coordinateArray) == list and len(coordinateArray) == 2 and type(coordinateArray[0]) == float and type(coordinateArray[1]):
        coordinates.append(coordinateArray)
    else :  
        if coordinateArray == list and len(coordinateArray) != 0:
            for value in coordinateArray:
                extractCoordinatesForMetadata(value)

#extracts values and keys from a dict and saves them in a list
def extractFromDict(content):
    global metadataList
    for key, value in content.items():
        metadataList.append(key)
        if type(value) == dict:
            extractFromDict(value)
        elif type(value) == list:
            extractFromList(value)
        else:
            metadataList.append(value)

#extracts all values from a list (also from list inside the list) and saves them in a one dimensional list
def extractFromList(content):
    global metadataList

    for value in content:
        if type(value) == dict:
            extractFromDict(value)
        elif type(value) == list:
            extractFromList(value)
        else:
            if value not in metadataList:
                metadataList.append(value)

#fill metadata for keywords if possible
def fillIfAvailable(searchParam, gjsonContent, metadata):
    global metadataList

    if type(gjsonContent) == dict:
        for key, value in gjsonContent.items():
            for x in searchParam:
                if key == x:
                    metadataList = []
                    if key == 'coord' or key == 'coords' or key == 'coordinates' or key == 'coordinate':
                            extractCoordinatesForMetadata(value)
                            print("coordinates:")
                            print(coordinates)
                            value = coordinates
                    elif type(value) == dict:
                        extractFromDict(value) 
                        metadata[x] = metadataList   
                    elif type(value) == list:
                        extractFromList(value)
                        metadata[x] = metadataList   
                    else:
                        if not x in metadata:
                            metadata[x] = value 
                        else:
                            if type(metadata[x]) == list:
                                metadata[x].append(value)
                            else:
                                arrayContent = metadata[x]
                                metadata[x] = []
                                metadata[x].append(arrayContent)
                                metadata[x].append(value)
            if type(value) == dict or type(value) == list:
                fillIfAvailable(searchParam, value, metadata)
    if type(gjsonContent) == list:
        for element in gjsonContent:
            fillIfAvailable(searchParam, element, metadata)
       

#extracts additional metadata
def getAdditionalMetadata(gjsonContent, fileFormat, filePath):
            metadataDict = {}

            # extract other metadata
            searchParams = ['format', 'source', 'crs', 'srs', 'language', 'publisher', 'creator', 'resourcelanguage', 'contributor',
            'organization', 'securityconstraints', 'servicetype', 'servicetypeversion', 'links', 'degree', 'conditionapplyingtoaccessanduse',
            'title_alternate', 'abstract', 'keywords', 'keywordstype', 'relation', 'wkt_geometry', 'date_revision', 'date_creation', 'date_publication',
            'date_modified', 'specificationtitle', 'specificationdate', 'specificationdatetype' , 'otherconstraints', 'type', 'comments', 'tags', 'comment', 'created_by', 'description']

            metadataDict["fileformat"] = "text/" + fileFormat
            metadataDict["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
           
            fillIfAvailable(searchParams, gjsonContent, metadataDict)

            return metadataDict

#extracts vector representation
def getVectorRepresentation(gjsonContent):
    global metadataList
    coordDict = {}
    searchParams = ['coordinates', 'coords', 'coord', 'coordinate']
    fillIfAvailable(searchParams, gjsonContent, coordDict)
    print("coordinates")
    print(coordinates)
    for key, value in metadataList:
        coordinates.append(value)
    return coordinates

#gets called when the argument of the command request is a geojson
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}

    #reading file content and validate (geo)json
    try :   
        gjson = open(filePath, "rb")
        gjsonContent = json.load(gjson)
        gjsonContentString = json.dumps(gjsonContent, sort_keys=False, indent=4)
        #gjsonContentString = json.loads(gjson) #throws ValueError if content is invalid json
        gjson.close()

    except ValueError(json) as e:
        print ('The geojson file from ' + filePath + ' is not valid.') 
        print (e)
        sys.exit(1)

    except RuntimeError as e:
        print ('Error: (geo)json file cannot be opened or read.')
        print (e)
        sys.exit(1)

    try: 
        if not gjsonContent:
            raise RuntimeError('The geojson file from ' + filePath + ' is empty')
    except RuntimeError as e:
        print ('Error')
        print (e)
        raise


    #metadata extraction    
    try:
        #extracting bbox and crs
        if whatMetadata == 's':
            metadata["crs"] = getCRS(gjsonContent)
            metadata["bbox"] = getBoundingBox(gjsonContentString, gjsonContent, extractGeometry(gjsonContentString))   
            metadata["coordinates"] = getVectorRepresentation(gjsonContent)      
        # time extraction
        if whatMetadata == 't':
            metadata["temporal_extent"] = getTemporalExtent(gjsonContent)
        #extract bbox, time and other metadata
        if whatMetadata == 'e':
            #extract bbox and crs
            metadata["bbox"] = getBoundingBox(gjsonContentString, gjsonContent, extractGeometry(gjsonContentString))
            metadata["crs"] = getCRS(gjsonContent)
            #extract time extent
            metadata["temporal_extent"] = getTemporalExtent(gjsonContent)
            #extract other metadata
            addMetadata = getAdditionalMetadata(gjsonContent, fileFormat, filePath)       
            for key, value in addMetadata.items():
                metadata[key] = value
            #extract coordinates for vector representation
            metadata["coordinates"] = getVectorRepresentation(gjsonContent)       
            
            
    except AttributeError as e:
        print('Warning: missing metadata. Could not extract all metadata')
        print (e)

    print (metadata)
    return metadata


extractMetadata("geojson", "/home/ilka/Desktop/Geosoftware2_old/MetadatenExtrahieren/Geojson/testdata1.geojson", "e")