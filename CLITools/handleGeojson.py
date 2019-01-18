import helpfunctions as hf
import json, gdal
from osgeo import ogr
import sys
from datetime import datetime
import datetime
from django.utils.dateparse import parse_datetime
import django, pytz
import unicodedata
import convex_hull
import pygeoj





def extractContentFromPath(filePath):
    ''' method to extract geojson content from a file by using its filepath \n
    input "filepath": type string, path to file which shall be extracted \n
    returns geojson content of the filePath: type string,  returns  geojson content of filepath 
    '''
    try :   
        gjson = open(filePath, "rb")
        gjsonContent = json.load(gjson)
        #gjsonContentString = json.loads(gjson) #throws ValueError if content is invalid json
        gjson.close()
        return gjsonContent

    except ValueError(json) as e:
        print ('The geojson file from ' + filePath + ' is not valid.' + str(e)) 
        print (e)
        sys.exit(1)

    except RuntimeError as e:
        print ('(geo)json file cannot be opened or read.' + str(e))
        sys.exit(1)

    try: 
        if not gjsonContent:
            raise Exception('The geojson file from ' + filePath + ' is empty' + str(e))
    
    except Exception as e:
        print ('Error: ' + str(e))
        sys.exit(1)




def getBoundingBox (filePath):
    ''' extract bounding box from geojson content \n
    input "filePath": type string, file path to geojson File \n
    returns bounding box: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
    bbox = None
    
    #gjsonContent is a FeatureCollection
    try:
        gjsonContent = pygeoj.load(filepath = filePath)
        bbox = gjsonContent.bbox
    #gjsonContent is a single file and has to be converted to a FeatureCollection
    except ValueError:
        gjson = open(filePath, "rb")
        gjsonContent = extractContentFromPath(filePath)

        gjsonFeatureCollection = {"type": "FeatureCollection", "features": []}
        gjsonFeatureCollection.get("features").append(gjsonContent)
        gjsonContent_FeatureColl = pygeoj.load(data=gjsonFeatureCollection)
        bbox = gjsonContent_FeatureColl.bbox
    
    if not bbox:
        raise Exception("Bounding box could not be extracted")
    return bbox




def getCRS(filePath):
    ''' extracts EPSG number of the taken coordinate reference system (short: crs), as standard the crs WGS84 is used. \n
    input "filePath": type string, file path to geojson File \n
    returns the epsg code of the used coordinate reference system: type int, EPSG number of taken crs
    '''    
    gjsonContent = pygeoj.load(filePath)
    crsCode = gjsonContent.crs
    if not crsCode:
        return hf.WGS84_EPSG_ID
    else:
        return crsCode



 
def getVectorRepresentation(filePath):
    ''' extracts coordinates from geojson File (for vector representation) \n
    input "filePath": type string, file path to geojson File \n
    returns extracted coordinates of content: type list, list of lists with length = 2
    '''
    #type list, contains all coordinates as tuples
    coordinates = []

    #type list, contains everything extracted
    extracted = []




    def extractAfterKeyword(searchParam, gjsonContent):
        ''' searches for the value fo the dict entry with keyword which is given as input \n
        input "searchParam": type string, keyword for which is searched in the dict \n
        input "gjsonContent": type dict, Content of geojson File
        '''
        if type(gjsonContent) == dict:
            for keyContent, valueContent in gjsonContent.items():
                if keyContent == searchParam:   
                    extracted.append(valueContent)
                if type(valueContent) == dict or type(valueContent) == list:
                    extractAfterKeyword(searchParam, valueContent)
        if type(gjsonContent) == list:
            for element in gjsonContent:
                extractAfterKeyword(searchParam, element)




    def extractCoordinates(coordsList):
        ''' extract coordinates as tuples out of a some more lists (e.g. with Multipolygons) \n
        input "coordsList": type list, value of dict entry with key "coordinates"
        '''
        if type(coordsList) == list and len(coordsList) == 2 and (type(coordsList[0]) == float or type(coordsList[0]) == int) and (type(coordsList[1]) == float or type(coordsList[1]) == int):
            coordinates.append(coordsList)
        elif type(coordsList) == list and len(coordsList) != 0:
            for value in coordsList:
                extractCoordinates(value)




    gjsonContent = extractContentFromPath(filePath)
    extracted = []
    extractAfterKeyword("coordinates", gjsonContent)
    extractCoordinates(extracted)
    if not coordinates:
        raise Exception("No coordinates found in File. Vector Representation could not be extracted.")
    coordinates = convex_hull.graham_scan(coordinates)
    return coordinates

    


def getTemporalExtent (filePath):
    ''' extract time extent from json string \n
    input "filePath": type string, file path to geojson File \n
    returns the temporal extent of the file: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
    '''
    #type list, contains all dates
    dateArray = []
    
    
    def searchForTimeElements(gjsonContent):
        ''' searches for time elements in a json \n
        input "gjsonContent": type dict, Content of geojson File
        '''
        
        ignore = ["created_at", "closed_at", "created", "closed", "initialize", "init", "last_viewed", "last_change", "change", "last_Change", "lastChange"] 
       

        if type(gjsonContent) == dict:
            for key, value in gjsonContent.items():     
                if key not in ignore:
                    searchForTimeElements(value)    
        elif type(gjsonContent) == list:
            for element in gjsonContent:
                searchForTimeElements(element)
        elif type(gjsonContent) == str:
            datetime_object = None
            datetime_object = parse_datetime(gjsonContent)
            if type(datetime_object) == datetime.datetime:
                dateArray.append(gjsonContent)



    gjsonContent = extractContentFromPath(filePath)
    temporalExtent = []

    searchForTimeElements(gjsonContent)
    if len(dateArray)!= 0:
        dateArray = sorted(dateArray)
        temporalExtent.append(dateArray[0])
        temporalExtent.append(dateArray[len(dateArray)-1])
    else:
        raise Exception("Could not extract timestamp.")
    return temporalExtent
