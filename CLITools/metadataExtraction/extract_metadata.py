'''
@author: Katharina Hovestadt, Niklas Asselmann, Benjamin Dietz
'''

import sys, os, getopt, datetime, errno, sqlite3, subprocess, uuid # important
import helpfunctions as hf
import dicttoxml, xml
import extractFromFolderOrFile as extract


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

# the capabilities of our CLI
def usage():
    """Provide usage instructions"""
    return '''
        NAME
            extract_metadata.py 

        SYNOPSIS
            extract_metadata.py -e </absoulte/path/to/record>|</absoulte/path/to/directory>
            extract_metadata.py -s </absoulte/path/to/record>|</absoulte/path/to/directory>
            extract_metadata.py -t </absoulte/path/to/record>|</absoulte/path/to/directory>

            Supported formats:

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
                    .xml     |


            Available options:

            -e    Extract all metadata of a geospatial file (crs, vector representation, bounding box, temporal extent)
            -s    Extract all spatial metadata of a geospatial file (crs, vector representation, bounding box)
            -t    Extract all temporal metadata of a geospatial file (temporal extent)
'''

def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())

if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'e:s:t:ho:')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    #sys.exit(2)

if 'OPTS' in globals(): 
    if len(OPTS) == 0:
        errorFunction()



#process arguemnts from command line
if 'OPTS' not in globals():
    raise Exception("An Argument is required")

for o, a in OPTS:
    '''
    tells the program what to do with certain tags and their attributes that are
    inserted over the command line
    '''
    ending = a
    if "/" in a:
        ending = a[a.rfind("/")+1:]
    

    #extracts spatial and temporal metadata and also the vector representation
    if o == '-e':
        COMMAND = a
        print("Extract all metadata:\n")
        if '.' in ending:
            # handle it as a file
            output = extract.extractMetadataFromFile(a, 'e')
            if output is None:
                raise Exception("This file format is not supported")
        else:
            # handle it as a folder
            output = extract.extractMetadataFromFolder(a, 'e')


    #extract only temporal metadata
    elif o == '-t':
        print("\n")
        print("Extract Temporal metadata only:\n")
        COMMAND = a
        if '.' in ending:
            # handle it as a file
            output = extract.extractMetadataFromFile(a, 't')
            if output is None:
                raise Exception("This file format is not supported")
        else:
            # handle it as a folder
            output = extract.extractMetadataFromFolder(a, 't')


    #extract only spatial metadata    
    elif o == '-s':
        print("\n")
        print("Extract Spatial metadata only:\n")
        COMMAND = a
        if '.' in ending:
            # handle it as a file
            output = extract.extractMetadataFromFile(a, 's')
            if output is None:
                raise Exception("This file format is not supported")
        else:
            # handle it as a folder
            if os.path.isdir(a):
                output = extract.extractMetadataFromFolder(a, 's')
            else:
                raise Exception("The path is not a valid folder or file")

    elif o == '-h':  # dump help and exit
        print(usage())
        sys.exit(3)
        
    # print output differently depending on the outputs type
    if 'output' in globals():
        if type(output) == list or type(output) == dict:
            hf.printObject(output)
        else: print(output)