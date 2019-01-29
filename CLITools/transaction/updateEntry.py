
'''
@author: Katharina Hovestadt
'''
from owslib.util import http_post
import requests
from owslib.csw import CatalogueServiceWeb
import sys
import getopt
import subprocess
import os
import updateXml
sys.path.insert(1, os.path.join(sys.path[0], '..')+"/metadataExtraction") 
import extractFromFolderOrFile as extract
import configparser

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
            updateEntry.py 

        SYNOPSIS
            updateEntry.py -i <string or int for id> -s </absoulte/path/to/record>|</absoulte/path/to/directory/with/records> -p <url to server>

            p is optional - if it is not defined in the command, then the default value in the cunfiguration file (default_url.cfg) is taken as the url
'''


def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())

if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 's:i:p:h:ho:')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    #sys.exit(2)

if 'OPTS' in globals(): 
    if len(OPTS) == 0:
        errorFunction()

#print(globals())
if 'OPTS' not in globals():
        raise Exception("The arguments -s \"[sourceOfFolderOrFile]\" and -i \"[idOfEntryInDB]\" and -p \"[portOfServer]\" are required.")

source = None
uuid = None
port = None

for o, a in OPTS:

    if o == '-s':
        source = a
        if "/" in a:
            ending = a[a.rfind("/")+1:]
            if '.' in ending:
                # handle it as a file
                metadata = extract.extractMetadataFromFile(a, 'e')
                if metadata is None:
                    raise Exception("This file format is not supported")
            else:
                # handle it as a folder
                metadata = extract.extractMetadataFromFolder(a, 'e')
        else:
            # handle it as a folder
            metadata = extract.extractMetadataFromFolder(a, 'e')
            
    elif o == '-i':
        uuid = a
    elif o == '-p':
        port = a
    elif o == '-h':
        print(usage())
    else: raise Exception("The argument " + o + " is not known. Please use -s \"[sourceOfFolderOrFile]\" and -i \"[idOfEntryInDB]\" and -r \"[portOfServer]\".")

if not source:
    raise Exception("The argument -s is missing. Please give a source path of the used file or folder. Format: -s \"[sourceOfFileOrFolder]\"")
if not port:
    try:
        configParser = configparser.RawConfigParser()
        configFilePath = 'default_url.cfg'
        configParser.read(configFilePath)
        port = configParser.get('server', 'url')
    except:
        raise Exception("The argument -p is missing. Please give a url to the server. Format: -p \"[urlOfServer]\"")
if not uuid:
    raise Exception("The argument -i is missing. Please give a uuid for the database entry that should be updated. Format: -i \"[uuid]\" ")







try:
    # sends transaction-update request as xml to pycsw server 
    r = requests.post(port, data = updateXml.createXmlTree(metadata, uuid))
    print(r.content)
except Exception as e:
    print("Error while updating db entry with id "+ uuid +". "+ str(e))



