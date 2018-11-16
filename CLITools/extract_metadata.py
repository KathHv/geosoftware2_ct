import sys, os, platform, datetime, math, shapefile, nio
from six.moves import configparser
from netCDF4 import Dataset
import netCDF4
import getopt
from os import walk

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

#output of metadata object
def printObject(object):
    print("\n")
    for a,b in object.items():
        print(a,b)
    print("\n")

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


            Possible metadata for formats:

                .shp and .dbf    :   bbox, shapetype, number of shape elements
                .csv             : 
                .nc              :
                .geojson | .json :
                .gpkg            :
                .geotiff | .tif  :
                .gml             :
            
            Available temporal metadata:
            
                ?
            
            Available spatial metadata:

                bbox

'''

#does a file with the relative path 'filename' exist locally?
def exists(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False

def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())

if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'e:s:t:')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    sys.exit(2)

if len(OPTS) == 0:
    errorFunction()

#gets called when the argument of the command request is a csv-file
def extractMetadataFromCSV(filePath, whatMetadata):
    metadata = {}
    # Example how to use object:
    #metadata["bbox"] = [coor0, coor1, coor2, coor3]
    metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
    file = Dataset(filePath)
    print(file.variables["latitude"][:])

    # TO DO

    return metadata

#gets called when the argument of the command request is a NetCDF
def extractMetadataFromNetCDF(fileFormat, filePath, whatMetadata):
    # file format can be either .nc or .cdf
    metadata = {}
    # Example how to use object:
    #metadata["bbox"] = [coor0, coor1, coor2, coor3]
    metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
    

    # TO DO

    return metadata

#gets called when the argument of the command request is a geopackage
def extractMetadataFromGeopackage(filePath, whatMetadata):
    metadata = {}
    # Example how to use object:
    #metadata["bbox"] = [coor0, coor1, coor2, coor3]
    metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]


    # TO DO
    
    return metadata

#gets called when the argument of the command request is a geojson
def extractMetadataFromGeoJSON(fileFormat, filePath, whatMetadata):
    metadata = {}
    # Example how to use object:
    #metadata["bbox"] = [coor0, coor1, coor2, coor3]
    metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]

    # TO DO

    return metadata

#gets called when the argument of the command request is a ISOxxx
def extractMetadataFromISO(fileFormat, filePath, whatMetadata):
    metadata = {}
    # Example how to use object:
    #metadata["bbox"] = [coor0, coor1, coor2, coor3]
    metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]

    # TO DO
    
    return metadata

#gets called when the argument of the command request is a GeoTIFF
def extractMetadataFromGeoTIFF(fileFormat, filePath, whatMetadata):
    metadata = {}
    # Example how to use object:
    #metadata["bbox"] = [coor0, coor1, coor2, coor3]
    metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]

    # TO DO

    return metadata

#gets called when the argument of the command request is a shape-file
def extractMetadataFromShapefile(fileFormat, filePath, whatMetadata):
    if fileFormat == 'shp':
        myshp = open(filePath, "rb")
        dbfPath = filePath[:filePath.rfind(".")] + ".dbf"
        if exists(dbfPath):
            mydbf = open(dbfPath, "rb")
            ourFile = shapefile.Reader(shp=myshp, dbf=mydbf)
        else:
            print("\nError: There searched .dbf file was not found under " + dbfPath + "\n")
    else:
        mydbf = open(filePath, "rb")
        shpPath = filePath[:filePath.rfind(".")] + ".shp"
        if exists(shpPath):
            myshp = open(shpPath, "rb")
            ourFile = shapefile.Reader(shp=myshp, dbf=mydbf)
        else: 
            print("\nError: There searched .shp file was not found under " + shpPath + "\n")
    metadata = {}
    if whatMetadata != 's':
        metadata["filename"] = filePath[filePath.rfind("/")+1:]
        metadata["fileformat"] = fileFormat
    metadata["bbox"] = ourFile.bbox
    if whatMetadata != 's':
        metadata["shapetype"] =  ourFile.shapeTypeName
        metadata["shape_elements"] = len(ourFile)
    return metadata

# function is called when filePath is included in commanline (with tag 'e', 't' or 's')
# how this is done depends on the file format - the function calls the extractMetadataFrom<format>() - function
# returns False if the format is not supported, else returns True 
def extractMetadataFromFile(filePath, whatMetadata):
    fileFormat = a[a.rfind('.')+1:]
    if fileFormat == 'shp' or fileFormat == 'dbf':
        metadata = extractMetadataFromShapefile(fileFormat, filePath, whatMetadata)
    elif fileFormat == 'csv':
        metadata = extractMetadataFromCSV(filePath, whatMetadata)
    elif fileFormat == 'nc':
        metadata = extractMetadataFromNetCDF(fileFormat, filePath, whatMetadata)
    elif fileFormat == 'geojson' or fileFormat == 'json':
        metadata = extractMetadataFromGeoJSON(fileFormat, filePath, whatMetadata)
    elif fileFormat == 'gpkg':
        metadata = extractMetadataFromGeopackage(filePath, whatMetadata)
    elif fileFormat == 'geotiff' or fileFormat == 'tif':
        metadata = extractMetadataFromGeoTIFF(fileFormat, filePath, whatMetadata)
    else: return False
    printObject(metadata)
    return True

#compute an overall bbox from an array of bounding boxes
def computeBboxOfMultiple(bboxes):
    coordinate0 = 200
    coordinate1 = 200
    coordinate2 = -200
    coordinate3 = -200
    for x in bboxes:
        if x[0] < coordinate0:
            coordinate0 = x[0]
        if x[1] < coordinate1:
            coordinate1 = x[1]
        if x[2] > coordinate2:
            coordinate2 = x[2]
        if x[3] > coordinate3:
            coordinate3 = x[3]
    return [coordinate0, coordinate1, coordinate2, coordinate3]

#return the occurancies of all values in the array
def countElements(array):
    list = []
    for x in array:
            if [x, array.count(x)] not in list:
                list.append([x, array.count(x)])
    return list

def extractCommonMetaDataOfMultiple(metadataElements, whatMetadata):
    numberHavingAttribute = []
    numberHavingAttribute.extend((0, 0, 0, 0))
    bbox = []
    shapetypes = []
    shapeElements = 0.0
     # looking for common attributes
    for metadataObject in metadataElements:
        if "bbox" in metadataObject:
            #print(metadataObject["bbox"])
            numberHavingAttribute[0] += 1
            bbox.append(metadataObject["bbox"])
        if "shapetype" in metadataObject:
            shapetypes.append(metadataObject["shapetype"])
            numberHavingAttribute[1] += 1
        if "shape_elements" in metadataObject:
            shapeElements += float(metadataObject["shape_elements"])
            numberHavingAttribute[2] += 1
    output = {}

    if whatMetadata != 's' and whatMetadata != 't':
        # only taken into accound when ALL metadata is required
        output["number_files"] =  len(metadataElements)

        if not numberHavingAttribute[2] == 0:
            # shape elemnts
            output["average_number_shape_elements"] = str(shapeElements/float(numberHavingAttribute[2]))
            if numberHavingAttribute[2] != len(metadataElements):
                output["average_number_shape_elements"] += " WARNING: Only " + str(numberHavingAttribute[2]) + " Element(s) have this attribute"
        # shape types
        output["occurancy_shape_elements"] = str(countElements(shapetypes))
        if numberHavingAttribute[1] != len(metadataElements):
            output["occurancy_shape_elements"] += " WARNING: Only " + str(numberHavingAttribute[1]) + " Element(s) have this attribute"
    
    # bounding box
    if numberHavingAttribute[0] == 0:
        if whatMetadata == "s": raise Exception("The system could not compute spatial metadata of files")
    elif whatMetadata != 't': 
        # not taken into account when temporal metadata is required
        output["bbox"] =  str(computeBboxOfMultiple(bbox))
        if numberHavingAttribute[0] != len(metadataElements):
            output["bbox"] += " WARNING: Only " + str(numberHavingAttribute[0]) + " Element(s) have this attribute"
    return output


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
        if fileFormat == 'shp': #here not 'dbf' so that it doesn take the object twice into account
            metadataElements.append(extractMetadataFromShapefile("shp", x, whatMetadata))
        elif fileFormat == 'csv':
            metadataElements.append(extractMetadataFromCSV(x, whatMetadata))
        elif fileFormat == 'nc':
            metadataElements.append(extractMetadataFromNetCDF(fileFormat, x, whatMetadata))
        elif fileFormat == 'geojson' or fileFormat == 'json': #here both because it is either geojson OR json
            metadataElements.append(extractMetadataFromGeoJSON(fileFormat, x, whatMetadata))
        elif fileFormat == 'gpkg':
            metadataElements.append(extractMetadataFromGeopackage(x, whatMetadata))
        elif fileFormat == 'geotiff' or fileFormat == 'tif': #here both because it is either geotiff OR tif
            metadataElements.append(extractMetadataFromGeoTIFF(fileFormat, x, whatMetadata))
        elif not (fileFormat == 'shp' or fileFormat == 'dbf'): 
            filesSkiped += 1
    if filesSkiped != 0: 
        print(str(filesSkiped) + ' file(s) has been skipped as its format is not suppoted; to see the suppoted formats look at -help')
    if len(metadataElements):
        printObject(extractCommonMetaDataOfMultiple(metadataElements, whatMetadata))
    else: print("No file in directory with metadata")

# tells the program what to do with certain tags and their attributes that are
# inserted over the command line
for o, a in OPTS:
    if o == '-e':
        COMMAND = a
        print("Extract all metadata:\n")
        if exists(a):
            print("File exists")
            extractMetadataFromFile(a, 'e')
        elif os.path.isdir(a):
            #the input is a valid folder 
            extractMetadataFromFolder(a, 'e')
        else: print("\nFile or folder does not exist\n")
    elif o == '-t':
        print("\n")
        print("Extract Temporal metadata only:\n")
    elif o == '-s':
        print("\n")
        print("Extract Spatial metadata only:\n")
        COMMAND = a
        if exists(a):
            extractMetadataFromFile(a, 's')
        elif os.path.isdir(a):
            #the input is a valid folder 
            extractMetadataFromFolder(a, 's')
        else: print("\nFile or folder does not exist\n")
    elif o == '-help':
        print("\n")
        print(usage())
        print("\n")