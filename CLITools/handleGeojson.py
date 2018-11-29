import helpfunctions as hf
import json, gdal
from osgeo import ogr
import sys
from datetime import datetime
import datetime
from django.utils.dateparse import parse_datetime
import django, pytz
import unicodedata


#extract geometry
def extractGeometry (json, metadata): 
    try:
        jsonGeometry = None
        jsonGeometry = ogr.CreateGeometryFromJson(json)
        metadata["geometry"] = jsonGeometry
        raise Exception("abc")
        return jsonGeometry
        
    except AttributeError, e:
        print('Warning: missing metadata. Could not extract geometry')
        print e
        return jsonGeometry 

    except TypeError, e:
        print('Warning: missing metadata. Could not extract geometry')
        print e
        return jsonGeometry 
        






foundCoordsX = []
foundCoordsY = []
# extract Coordinates from coordinate Arrays
def extractCoordinates(coordinateArray):
    #further arrays with coordinates
    print(coordinateArray)
    if type(coordinateArray) == list and len(coordinateArray) == 2 and type(coordinateArray[0]) == float and type(coordinateArray[1]):
        global foundCoordsX
        global foundCoordsY
        foundCoordsX.append(format(float(coordinateArray[1]), '.2f'))
        foundCoordsY.append(format(float(coordinateArray[0]), '.2f'))
    else :
        if coordinateArray == list and len(coordinateArray) != 0:
            for value in coordinateArray:
                extractCoordinates(value)
                        
#search in Json File for Coordinate Lists or Dicts
def searchForCoordinates (gjsonContent):
    if type(gjsonContent) == dict:
        for key, value in gjsonContent.items():           
            if key == "coordinates":
                extractCoordinates(value)
                if type(value) == dict or type(value) == list:
                    searchForCoordinates(value)
            else:
                searchForCoordinates(value)
    if type(gjsonContent) == list:
        for element in gjsonContent:
            searchForCoordinates(element)


# extract bounding box
def extractBbox (contentString, content, geometry, metadata):
    try:
        bbox = None
        if not geometry:
      
            searchForCoordinates(content)
            global foundCoordsX 
            global foundCoordsY
            foundCoordsX= sorted(foundCoordsX)
            foundCoordsY = sorted(foundCoordsY)
            print(foundCoordsX)
            bbox=[foundCoordsY[0], foundCoordsX[0], foundCoordsY[len(foundCoordsY)-1], foundCoordsX[len(foundCoordsX)-1]]
        else:
            bbox = geometry.GetEnvelope()
        metadata["bbox"] = bbox
        return bbox
        
    except AttributeError, e:
        print('Warning: missing metadata. Could not extract bounding box')
        print e
        return bbox

    
ignore = ["created_at", "closed_at", "created", "closed", "initilize", "init", "last_viewed", "last_change", "change", "last_Change", "lastChange"]    
#ignore = []

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
            if type(gjsonContent) == unicode :
                datetime_object = parse_datetime(unicodedata.normalize('NFKD', gjsonContent).encode('ascii', 'ignore') )
                if type(datetime_object) ==datetime.datetime: #date
                    dateArray.append(gjsonContent)



#extract timeextend from json string
def extractTimeExtend (gjsonContent, metadata):
    try:
        dateArray = []
        searchForTimeElements(gjsonContent,dateArray)
        if len(dateArray)!= 0:
            dateArray = sorted(dateArray)
            timeExtent = []
            timeExtent.append(dateArray[0])
            timeExtent.append(dateArray[len(dateArray)-1])
            metadata["time_extent"] = timeExtent
        else:
            raise AttributeError
        

    except AttributeError, e:
        print('Warning: missing metadata. Could not extract timestamps')
        print e
      



#gets called when the argument of the command request is a geojson
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}
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
        gjsonContentString = json.dumps(gjsonContent, sort_keys=False, indent=4)

        #extracting bbox and geometry
        if whatMetadata == 's':
            bbox = extractBbox(gjsonContentString, gjsonContent, extractGeometry(gjsonContentString, metadata), metadata)  
        
           
        
        # time extraction
        if whatMetadata == 't':
            extractTimeExtend(gjsonContent, metadata)
        #extracting bbox, time and other metadata
        if whatMetadata == 'e':
            #extracting bbox and geometry
            bbox = extractBbox(gjsonContentString, gjsonContent, extractGeometry(gjsonContentString, metadata), metadata)
            # time extraction
            extractTimeExtend(gjsonContent, metadata)

            
            # extract other metadata
            searchParams = ['format', 'source', 'crs', 'language', 'publisher', 'creator', 'resourcelanguage', 'contributor',
            'organization', 'securityconstraints', 'servicetype', 'servicetypeversion', 'links', 'degree', 'conditionapplyingtoaccessanduse',
            'title_alternate', 'abstract', 'keywords', 'keywordstype', 'relation', 'wkt_geometry', 'date_revision', 'date_creation', 'date_publication',
            'date_modified', 'specificationtitle', 'specificationdate', 'specificationdatetype' , 'otherconstraints', 'type', 'comments', 'tags', 'comment', 'created_by', 'description']
            
            def fillIfAvailable(searchParam, gjsonContent):
                if type(gjsonContent) == dict:
                    for key, value in gjsonContent.items():
                        for x in searchParams:
                            if key == x:
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
                            fillIfAvailable(searchParam, value)
                if type(gjsonContent) == list:
                    for element in gjsonContent:
                        fillIfAvailable(searchParam, element)
      
            metadata["fileformat"] = "text/" + fileFormat
            metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
           
            fillIfAvailable(searchParams, gjsonContent)
    except AttributeError, e:
        print('Warning: missing metadata. Could not extract all metadata')
        print e


    return metadata

