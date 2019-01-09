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


#type list, contains all longitudes of coordinates
foundCoordsLon = []

#type list, contains all latitudes of coordinates
foundCoordsLat = []

#type list, contains all dates
dateArray = []

#type list, contains all coordinates as tuples
coordinates = []

#type list, contains everything extracted
extracted = []

'''
 method to extract geojson content from a file by using its filepath
 input filepath: type string, path to file which shall be extracted
 output gjsonContent: type string,  returns  geojson content of filepath 
'''
def extractContentFromPath(filePath):
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



'''
 extract geometry from geojson
 input gjsonContent: dict, Content of geojson File
 output gjsonGeometry: wkt, Geometry of geojson File
'''
def extractGeometry (gjsonContent): 
        gjsonContent = json.dumps(gjsonContent, sort_keys=False, indent=4)
        gjsonGeometry = None
        gjsonGeometry = ogr.CreateGeometryFromJson(gjsonContent)
        return gjsonGeometry



'''
 coordinates are extracted and divided out of the list and splitted into longitude and latitude. They are shortened to two decimal places. 
 The coordinates are written into two global lists.
 input coordsList: type list, values of key coordinates
'''
def divideCoordinatesForBbox(coordsList):
    global foundCoordsLat
    global foundCoordsLon
    if type(coordsList) == list and len(coordsList) == 2 and (type(coordsList[0]) == float or type(coordsList[0]) == int) and (type(coordsList[1]) == float or type(coordsList[1]) == int):   
        foundCoordsLat.append(format(float(coordsList[1]), '.2f'))
        foundCoordsLon.append(format(float(coordsList[0]), '.2f'))
    elif type(coordsList) == list and len(coordsList) != 0:
        for value in coordsList:
            divideCoordinatesForBbox(value)



'''
 searches for the value fo the dict entry with keyword which is given as input
 input searchParam: type string, keyword for which is searched in the dict
 input gjsonContent: type dict, Content of geojson File
'''
def extractAfterKeyword(searchParam, gjsonContent):
    global extracted
    if type(gjsonContent) == dict:
        for keyContent, valueContent in gjsonContent.items():
            if keyContent == searchParam:   
                extracted.append(valueContent)
            if type(valueContent) == dict or type(valueContent) == list:
                extractAfterKeyword(searchParam, valueContent)
    if type(gjsonContent) == list:
        for element in gjsonContent:
            extractAfterKeyword(searchParam, element)



'''
 extract bounding box from geojson content
 input filePath: type string, file path to geojson File
 output bbox: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
'''
def getBoundingBox (filePath):
        global foundCoordsLat 
        global foundCoordsLon
        global extracted

        gjsonContent = extractContentFromPath(filePath)

        geometry = extractGeometry(gjsonContent)
        bbox = None
        if not geometry:
            extracted = []
            extractAfterKeyword("coordinates", gjsonContent)
            divideCoordinatesForBbox(extracted)
            if not foundCoordsLat or not foundCoordsLon:
                raise Exception("Bounding box could not be extracted. There are no coordinates in the file.")

            # see http://wiki.geojson.org/GeoJSON_draft_version_6#Specification
            #change order of [lat,lon] if neccessary -> standard of geojson is [lon, lat]
            crs = getCRS(filePath)
            coordinate_order = extracted[0]["properties"]["coordinate_order"]
            if len(extracted) != 0 and type(extracted[0]) == dict and "coordinate_order" in extracted[0]["properties"] and coordinate_order[0] == 1 and coordinate_order[1] == 0 or (crs == 4326 and not (len(extracted) != 0 and type(extracted[0]) == dict and "coordinate_order" in extracted[0]["properties"] and coordinate_order[0] == 0 and coordinate_order[1] == 1)):
                    help = foundCoordsLat
                    foundCoordsLat = foundCoordsLon
                    foundCoordsLon = help

            foundCoordsLat = sorted(foundCoordsLat)
            foundCoordsLon = sorted(foundCoordsLon)
            bbox=[foundCoordsLon[0], foundCoordsLat[0], foundCoordsLon[len(foundCoordsLon)-1], foundCoordsLat[len(foundCoordsLat)-1]]
        else:
            envelope = geometry.GetEnvelope()
            bbox = [envelope[0], envelope[2], envelope[1], envelope[3]]
        if not bbox:
            raise Exception("Bounding box could not be extracted")
        return bbox



'''
 extract coordinates as tuples out of a some more lists (e.g. with Multipolygons)
 input coordsList: type list, value of dict entry with key "coordinates"
'''
def extractCoordinates(coordsList):
    global coordinates
    if type(coordsList) == list and len(coordsList) == 2 and (type(coordsList[0]) == float or type(coordsList[0]) == int) and (type(coordsList[1]) == float or type(coordsList[1]) == int):
        coordinates.append(coordsList)
    elif type(coordsList) == list and len(coordsList) != 0:
        for value in coordsList:
            extractCoordinates(value)



'''
 extracts EPSG number of the taken coordinate reference system (short: crs), as standard the crs WGS84 is used.
 input filePath: type string, file path to geojson File
 output crsCode: type int, EPSG number of taken crs
'''
def getCRS(filePath):
    global extracted
    
    gjsonContent = extractContentFromPath(filePath)
  
    #standard code after http://wiki.geojson.org/GeoJSON_draft_version_6#Specification
    crsCode = None
    extracted = []
    extractAfterKeyword("crs", gjsonContent)
    if len(extracted) != 0 and type(extracted[0]) == dict:
            if "properties" in extracted[0]:
                if "code" in extracted[0]["properties"]:
                    crsCode = extracted[0]["properties"]["code"]
                else: 
                    raise Exception("Crs could not be extracted key \"code\" in \"properties\" in \"crs\" is missing")
            else:
                raise Exception("Crs could not be extracted key \"properties\" in \"crs\" is missing")
    else:
        raise Exception("Crs could not be extracted. The standard WGS 84 will be taken.")
    return crsCode



'''
 extracts coordinates from geojson File (for vector representation)
 input filePath: type string, file path to geojson File
 output coordinates: type list, list of lists with length = 2, contains extracted coordinates of content from geojson file
'''
def getVectorRepresentation(filePath):
    global coordinates
    global extracted

    gjsonContent = extractContentFromPath(filePath)
    extracted = []
    extractAfterKeyword("coordinates", gjsonContent)
    extractCoordinates(extracted)
    if not coordinates:
        raise Exception("No coordinates found in File. Vector Representation could not be extracted.")
    coordinates = convex_hull.graham_scan(coordinates)
    return coordinates




   
'''
 searches for time elements in a json
 input gjsonContent: type dict, Content of geojson File
'''
def searchForTimeElements(gjsonContent):
    global dateArray
    #ignore = ["created_at", "closed_at", "created", "closed", "initialize", "init", "last_viewed", "last_change", "change", "last_Change", "lastChange"] 
    ignore = ["coordinates"]
    
    if type(gjsonContent) == dict:
        for key, value in gjsonContent.items():     
            if key not in ignore:
                searchForTimeElements(value)    
    elif type(gjsonContent) == list:
        for element in gjsonContent:
            searchForTimeElements(element)
    elif type(gjsonContent) == unicode:
        datetime_object = None
        datetime_object = parse_datetime(gjsonContent)
        #datetime_object = parse_datetime(unicodedata.normalize('NFKD', gjsonContent.encode('ascii', 'ignore') ))
        if type(datetime_object) == datetime.datetime:
            dateArray.append(gjsonContent)


'''
 extract time extent from json string
 input filePath: type string, file path to geojson File
 output temporalExtent: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
'''
def getTemporalExtent (filePath):
    global dateArray
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