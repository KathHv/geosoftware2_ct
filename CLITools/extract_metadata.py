import sys, os, getopt, datetime, errno, sqlite3, subprocess, uuid # important
from six.moves import configparser
from pathlib import Path
from os import walk
import helpfunctions as hf
import handleShapefile, handleNetCDF, handleCSV, handleGeopackage, handleGeojson, handleISO, handleGeotiff
import dicttoxml, xml, subprocess
from lxml import etree


COMMAND = None
XML_DIRPATH = None
CFG = None
RECURSIVE = False
OUTPUT_FILE = None
CSW_URL = None
XML = None
XSD = None
TIMEOUT = 30
FORCE_CONFIRM = False

#the capabilities of our CLI
def usage():
    """Provide usage instructions"""
    return '''
        NAME
            cli.py 

        SYNOPSIS
            cli.py -e </absoulte/path/to/record>|</absoulte/path/to/directory>
            cli.py -s </absoulte/path/to/record>|</absoulte/path/to/directory>
            cli.py -t </absoulte/path/to/record>|</absoulte/path/to/directory>
            cli.py -l </absoulte/path/to/record>|</absoulte/path/to/directory>

            Suppoted formats:

                    .dbf     |
                    .shp     |
                    .csv     |
                    .nc      |
                    .geojson |
                    .json    |
                    .gpkg    |
                    .geotiff |
                    .tif     |
                    .gml     |


            Available options:

            -e    Extract all metadata of a geospatial file
            -s    Extract all spatial metadata of a geospatial file
            -t    Extract all temporal metadata of a geospatial file
            -l    Load metadata of file on pycsw platform


            Possible metadata for formats:

                .shp and .dbf    :   bbox, shapetype, number of shape elements
                .csv             :   
                .nc              :   bbox (with differnet ellipsoid?), temporal extent (not always given)
                .geojson | .json :   
                .gpkg            :   bbox (with different ellipsoid?), temp extent still missing
                .geotiff | .tif  :   
                .gml             :   
            
            Available temporal metadata:
            
                [starting point, endpoint]
            
            Available spatial metadata:

                bbox
'''

def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())

if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'e:s:t:l:')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    sys.exit(2)

if len(OPTS) == 0:
    errorFunction()

def getDatabaseElementFromMetadata(metadataDictionary):
    ''' 
    still missing an NOT NULL: xml, anytext
    keys required in metadataDictionary: title, temporal_extent (in ISO standard?), fileformat (image/...)'''
    databaseElement = {}
# required metadata

    # identifier NOT NULL
    databaseElement["identifier"] = "urn:uuid:" + str(uuid.uuid1())
    databaseElement["typename"] = "csw:Record" # NOT NULL
    databaseElement["schema"] = "http://www.opengis.net/cat/csw/2.0.2" # NOT NULL
    databaseElement["mdsource"] = "local" # NOT NULL
    databaseElement["insert_date"] = str(datetime.datetime.now().replace(microsecond=0).isoformat()) + "Z" # https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python NOT NULL
    if not all(x in databaseElement for x in ['typename', 'schema', "mdsource", "insert_date"]): # https://stackoverflow.com/questions/6159313/can-python-test-the-membership-of-multiple-values-in-a-list
        # metadata element cannot be saved
        raise Exception("One of the required metadata field could not be filled.")

# addictional metadata

    databaseElement["type"] = "http://purl.org/dc/dcmitype/Service" # ?

    # strict
    ''' only fills the value when search and found metadata fields are exactly the same '''
    searchStrict = ['title', 'date']
    for x in searchStrict:
        if x in metadataDictionary:
            databaseElement[x] = str(metadataDictionary[x])

    # non-strict
    ''' also fills the value if the searched parameter is part of a metadata fields in metadataDictionary '''
    searchNonStrict = ['format', 'source', 'crs', 'language', 'publisher', 'creator', 'resourcelanguage', 'contributor',
     'organization', 'securityconstraints', 'servicetype', 'servicetypeversion', 'links', 'degree', 'conditionapplyingtoaccessanduse',
     'title_alternate', 'abstract', 'keywords', 'keywordstype', 'relation', 'wkt_geometry', 'date_revision', 'date_creation', 'date_publication',
     'date_modified', 'specificationtitle', 'specificationdate', 'specificationdatetype' , 'otherconstraints']
    for x in searchNonStrict:
        if x in metadataDictionary:
            databaseElement[x] = str(metadataDictionary[x])
        else:
            for y in metadataDictionary:
                if x in y:
                    databaseElement[x] = str(metadataDictionary[y])
    
    # non-strict search for a different value as the key that gets entered in the databaseElement
    searchOtherWord = [[['constraint', 'acknowledgment'], 'otherconstraints'], [['link'], 'links'], [['src'], 'source'], [['institution'], 'organization'],
     [['comment'], 'abstract'], [['bbox'], 'wkt_geometry'] ]
    # schema of element in seachOtherWord: [[ <searchedWord1>, ... , <searchWordn> ], <keyToBeFilledInDatabase> ]
    for x in searchOtherWord:
        for key in metadataDictionary:
            for searchParam in x[0]:
                if searchParam in key:
                    if x[1] not in databaseElement:
                        databaseElement[x[1]] = str(metadataDictionary[key])

    
    # self extraction? -> many unclear metadata fields left
    # all of them (despite 'date') are already extracted when they are in the metadataDctionary. If we find better values here, 
    # we overwrite the old ones 
    if not 'links' in databaseElement:
        linksArray = []
        for a, b in metadataDictionary.items():
            def searchInString(searchedString):
                if 'http://' in searchedString:
                    indexHTTP = searchedString.find('http://')
                    endIndex = searchedString[indexHTTP:].find(" ")
                    if endIndex == -1:
                        endIndex = len(searchedString)-1
                    linksArray.append(searchedString[indexHTTP:endIndex])
                    searchInString(searchedString[endIndex:])
            if type(b) == str:
                searchInString(b)
            if len(linksArray): databaseElement['links'] = str(linksArray)[1:-1].replace("'","")
    if not 'title' in databaseElement:
        databaseElement["title"] = metadataDictionary['filename'].replace("_", " ")
    if not 'language' in databaseElement:
        databaseElement["language"] = "?" # maybe get language from texts (title, history, description, ... ?)
    databaseElement["title_alternate"] = "?" # ?
    if not 'abstract' in databaseElement:
        databaseElement["abstract"] = "?" # some text - some kind of description
    if 'keywords' not in databaseElement:
        databaseElement["keywords"] = "?" # maybe from title?
    if 'keywords' in databaseElement:
        databaseElement["keywordstype"] = "?" # ?
    databaseElement["relation"] = "?" # ? some other UUID
    databaseElement["date"] = "?" # ?
    databaseElement["wkt_geometry"] = "?" # second abstraction level?
    databaseElement["date_revision"] = "?" # ?
    if 'date_creation' in databaseElement:
        databaseElement["date_creation"] = "?" # ?
    databaseElement["date_publication"] = "?" # ?
    databaseElement["date_modified"] = "?" # ?
    databaseElement["specificationtitle"] = "?" # ?
    databaseElement["specificationdate"] = "?" # ?
    if 'specificationdate' in databaseElement:
        databaseElement["specificationdatetype"] = "?" # ?

    if 'temporal_extent' in metadataDictionary:
        if type(metadataDictionary["temporal_extent"]) == list and len(metadataDictionary["temporal_extent"]) == 2:
            databaseElement["time_begin"] = metadataDictionary["temporal_extent"][0] # in ISO standard?
            databaseElement["time_end"] = metadataDictionary["temporal_extent"][1] # in ISO standard?

    '''
        still some to come that does not really seem important
    '''
    def getXML():
        # required fileds in dataseElement: identifier, type,
        MY_NAMESPACES={'csw': 'http://www.opengis.net/cat/csw/2.0.2', 'ows': 'http://www.opengis.net/ows', 'dc': 'http://purl.org/dc/elements/1.1/', 'dct': 'http://purl.org/dc/terms/'}
        root = etree.Element("Record")
        root = etree.Element('{%s}Record' % MY_NAMESPACES['csw'], nsmap=MY_NAMESPACES)
        for x in databaseElement:
            child = etree.Element(('{%s}'+x) % MY_NAMESPACES['dc'])
            child.text = str(databaseElement[x])
            root.append(child)
        return root
    def getOnlyTextsFromXML(root):
        text = ""
        for index, child in enumerate(root):
            if child is not None:
                if index != len(root)-1:
                    text += child.text + " "
        return text
    databaseElement["xml"] = etree.tostring(getXML(), encoding='utf8', method='xml', pretty_print=True)
    databaseElement["anytext"] = getOnlyTextsFromXML(getXML())
    if not all(x in databaseElement for x in ['anytext', "xml"]):
        # metadata element cannot be saved
        raise Exception("One of the required metadata field could not be filled.")
    else: return databaseElement

# function is called when filePath is included in commanline (with tag 'e', 't' or 's')
# how this is done depends on the file format - the function calls the extractMetadataFrom<format>() - function
# returns False if the format is not supported, else returns True 
def extractMetadataFromFile(filePath, whatMetadata):
    fileFormat = a[a.rfind('.')+1:]
    if fileFormat == 'shp' or fileFormat == 'dbf':
        metadata = handleShapefile.extractMetadata(fileFormat, filePath, whatMetadata)
    elif fileFormat == 'csv':
        metadata = handleCSV.extractMetadata(filePath, whatMetadata)
    elif fileFormat == 'nc':
        metadata = handleNetCDF.extractMetadata(fileFormat, filePath, whatMetadata)
    elif fileFormat == 'geojson' or fileFormat == 'json':
        metadata = handleGeojson.extractMetadata(fileFormat, filePath, whatMetadata)
    elif fileFormat == 'gpkg':
        metadata = handleGeopackage.extractMetadata(filePath, whatMetadata)
    elif fileFormat == 'geotiff' or fileFormat == 'tif':
        metadata = handleGeotiff.extractMetadata(fileFormat, filePath, whatMetadata)
    elif fileFormat == 'gml':
        metadata = handleISO.extractMetadata(fileFormat, filePath, whatMetadata)
    else: return False
    hf.printObject(metadata)
    return True


def insertIntoDatabase(dictionary, dbpath, table):
    if hf.exists(dbpath):
        sqliteConnection = sqlite3.connect(dbpath)
        if sqliteConnection is not None:
            c = sqliteConnection.cursor()

            # save dict das databaseObject
            # https://stackoverflow.com/questions/14108162/python-sqlite3-insert-into-table-valuedictionary-goes-here
            columns = ', '.join(output.keys())
            placeholders = ':'+', :'.join(output.keys())
            query = 'INSERT INTO ' + table + ' (%s) VALUES (%s)' % (columns, placeholders)
            sqliteConnection.execute(query, output)
            sqliteConnection.commit()
            return True
    else:
        return False


# function is called when path of directory is included in commanline (with tag 'e', 't' or 's')
def extractMetadataFromFolder(folderPath, whatMetadata):
    f = []
    for (dirpath, dirnames, filenames) in walk(folderPath):
        #fullPath = os.path.join(folderPath, filenames)
        f.extend(filenames)
        break
    metadataElements = []
    fullPaths = []
    for x in f:
        fullPaths.append(str(os.path.join(folderPath, x)))
    #handle each of the files in the folder seperate
    filesSkiped = 0
    for x in fullPaths:
        fileFormat = x[x.rfind('.')+1:]
        if fileFormat == 'shp': #here not 'dbf' so that it does not take the object twice into account
            metadataElements.append(handleShapefile.extractMetadata("shp", x, whatMetadata))
        elif fileFormat == 'csv':
            metadataElements.append(handleCSV.extractMetadata(x, whatMetadata))
        elif fileFormat == 'nc':
            metadataElements.append(handleNetCDF.extractMetadata(fileFormat, x, whatMetadata))
        elif fileFormat == 'geojson' or fileFormat == 'json': #here both because it is either geojson OR json
            metadataElements.append(handleGeojson.extractMetadata(fileFormat, x, whatMetadata))
        elif fileFormat == 'gpkg':
            metadataElements.append(handleGeopackage.extractMetadata(x, whatMetadata))
        elif fileFormat == 'geotiff' or fileFormat == 'tif': #here both because it is either geotiff OR tif
            metadataElements.append(handleGeotiff.extractMetadata(fileFormat, x, whatMetadata))
        elif fileFormat == 'gml':
            metadataElements.append(handleISO.extractMetadata(fileFormat, x, whatMetadata))
        elif not (fileFormat == 'shp' or fileFormat == 'dbf'): 
            filesSkiped += 1
    if filesSkiped != 0: 
        print(str(filesSkiped) + ' file(s) has been skipped as its format is not suppoted; to see the suppoted formats look at -help')
    else: print("No file in directory with metadata")

# tells the program what to do with certain tags and their attributes that are
# inserted over the command line
for o, a in OPTS:

    if o == '-e':
        COMMAND = a
        print("Extract all metadata:\n")
        if hf.exists(a):
            print("File exists")
            output = extractMetadataFromFile(a, 'e')
        elif os.path.isdir(a):
            #the input is a valid folder 
            extractMetadataFromFolder(a, 'e')
        #else: raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), a)
    elif o == '-t':
        print("\n")
        print("Extract Temporal metadata only:\n")
        COMMAND = a
        if hf.exists(a):
            output = extractMetadataFromFile(a, 't')
        elif os.path.isdir(a):
            #the input is a valid folder 
            extractMetadataFromFolder(a, 't')
        #else: raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), a)
    elif o == '-s':
        print("\n")
        print("Extract Spatial metadata only:\n")
        COMMAND = a
        if hf.exists(a):
            output = extractMetadataFromFile(a, 's')
        elif os.path.isdir(a):
            #the input is a valid folder 
            extractMetadataFromFolder(a, 's')
        #else: raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), a)
    elif o == '-l':
        print("\n")
        print("Load metadata of file on pycsw ...\n")
        COMMAND = a
        if hf.exists(a):
            output = getDatabaseElementFromMetadata(extractMetadataFromFile(a, 'e')) 
            cp = configparser.RawConfigParser()


            dirOfThisFile = os.path.dirname(os.path.abspath(__file__))
            pycswpath = os.path.join("", '/home/niklas/Dokumente/pycsw/pycsw/pycsw')
            pathOfConfic = os.path.join(pycswpath, 'default.cfg')
            configfilePath = r'' + str(pathOfConfic)
            cp.read(configfilePath)
            sqlitepath = cp.get('repository', 'database')
            sqlitepath = sqlitepath[sqlitepath.find("sqlite:///") + 11:]
            sqlitepath = os.path.join(os.path.join("", pycswpath), sqlitepath[1:])
            if insertIntoDatabase(output, sqlitepath, 'records'):
               print("Metadata was successfully saved in the pycsw database")
            #else: raise FileNotFoundError()
            
        elif os.path.isdir(a):
            #the input is a valid folder 
            raise Exception("Only single dictionaries can be uploaded into pycsw")
        #else: raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), a)
    elif o == '-help':
        print("\n")
        print(usage())
        print("\n")
    if 'output' in globals():
        if type(output) == list or type(output) == dict:
            hf.printObject(output)
        else: print(output)

#subprocess.call(["pycsw-admin.py", "-c", "load_records", "-f", "/home/kathy/Documents/Geosoftware2/pycswDocker1/pycsw/pycsw/default.cfg", "-p", "./" + ident +".xml"])]