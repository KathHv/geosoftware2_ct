import sys, os, getopt # important
from os import walk
import helpfunctions as hf
import handleShapefile, handleNetCDF, handleCSV, handleGeopackage, handleGeojson, handleISO, handleGeotiff

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
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'e:s:t:')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    sys.exit(2)

if len(OPTS) == 0:
    errorFunction()

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
            metadataElements.append(handleISO.extractMetadata(x, whatMetadata))
        elif not (fileFormat == 'shp' or fileFormat == 'dbf'): 
            filesSkiped += 1
    if filesSkiped != 0: 
        print(str(filesSkiped) + ' file(s) has been skipped as its format is not suppoted; to see the suppoted formats look at -help')
    if len(metadataElements):
        hf.printObject(hf.extractCommonMetaDataOfMultiple(metadataElements, whatMetadata))
    else: print("No file in directory with metadata")

# tells the program what to do with certain tags and their attributes that are
# inserted over the command line
for o, a in OPTS:
    if o == '-e':
        COMMAND = a
        print("Extract all metadata:\n")
        if hf.exists(a):
            print("File exists")
            extractMetadataFromFile(a, 'e')
        elif os.path.isdir(a):
            #the input is a valid folder 
            extractMetadataFromFolder(a, 'e')
        else: print("\nFile or folder does not exist\n")
    elif o == '-t':
        print("\n")
        print("Extract Temporal metadata only:\n")
        COMMAND = a
        if hf.exists(a):
            extractMetadataFromFile(a, 't')
        elif os.path.isdir(a):
            #the input is a valid folder 
            extractMetadataFromFolder(a, 't')
        else: print("\nFile or folder does not exist\n")
    elif o == '-s':
        print("\n")
        print("Extract Spatial metadata only:\n")
        COMMAND = a
        if hf.exists(a):
            extractMetadataFromFile(a, 's')
        elif os.path.isdir(a):
            #the input is a valid folder 
            extractMetadataFromFolder(a, 's')
        else: print("\nFile or folder does not exist\n")
    elif o == '-help':
        print("\n")
        print(usage())
        print("\n")