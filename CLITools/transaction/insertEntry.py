'''
@author: Katharina Hovestadt
'''
import lxml.etree as etree
from owslib.util import http_post
import requests
from owslib.csw import CatalogueServiceWeb
import sys
import getopt
import subprocess
from urllib.request import urlopen
import os
from osgeo import ogr
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
            insertEntry.py 

        SYNOPSIS
            insertEntry.py -m </absoulte/path/to/metadataxml/of/record(s)> -s </absoulte/path/to/record>|</absoulte/path/to/directory/of/records> -p <url to server>

            p is optional - if it is not defined in the command, then the default value in the cunfiguration file (default_url.cfg) is taken as the url
'''


def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())

if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 's:m:p:h:ho:')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    #sys.exit(2)

if 'OPTS' in globals(): 
    if len(OPTS) == 0:
        errorFunction()


if 'OPTS' not in globals():
        raise Exception("The arguments -s \"[sourceOfFolderOrFile]\" and-m \"[sourceOfInserXMLFile]\" and -p \"[portOfServer]\" are required.")

source = None
insertXml = None
port = None

for o, a in OPTS:

    if o == '-s':
        source = a
        print(source)
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
    elif o == '-m':
        insertXml = a
        print(insertXml)
    elif o == '-p':
        port = a
        print(port)
    elif o == '-h':
        print(usage())
    else: raise Exception("The argument " + o + " is not known. Please use -s \"[sourceOfFolderOrFile]\" and-m \"[sourceOfInsertXMLFile]\" and and -r \"[portOfServer]\".")

if not source:
    raise Exception("The argument -s is missing. Please give a source path of the used file/folder. Format: -s \"[sourceOfFileOrFolder]\"")
if not port:
    try:
        configParser = configparser.RawConfigParser()
        configFilePath = 'default_url.cfg'
        configParser.read(configFilePath)
        port = configParser.get('server', 'url')
    except:
        raise Exception("The argument -p is missing. Please give a url to the server. Format: -p \"[urlOfServer]\"")
if not insertXml:
    raise Exception("The argument -m is missing. Please give a source path to the insert xml file. Format:-m \"[sourceOfInsertXMLFile]\"  ")



xmlContent = open(insertXml)
tree = etree.parse(xmlContent)
root = tree.getroot()
#insert with typename "md:MD_Metadata"
if(root.tag == "{http://www.opengis.net/cat/csw/2.0.2}Transaction"):
    uuid = root[0][0][0][0].text
    try:
        #sends transaction-insert request as xml to pycsw server
        insert = requests.post(port, data = open(insertXml))
        print(insert.content)
    except Exception as e:
        print("Error while inserting db entry. "+ str(e))

#insert Record with typename csw:Record
else:
    uuid = root[0].text
    try:
        # sends transaction-insert request as xml to pycsw server
        csw = CatalogueServiceWeb(port)
        csw.transaction(ttype='insert', typename='csw:Record', record = xmlContent)
        insert = requests.post(port, data = open(insertXml))
        print(insert.content)
    except Exception as e:
        print("Error while inserting db entry. "+ str(e))

try:
    # sends transaction-update request as xml to pycsw server 
    update = requests.post(port, data = updateXml.createXmlTree(metadata, uuid))
    print(update.content)
except Exception as e:
    print("Error while updating db entry with id "+ uuid +". "+ str(e))



