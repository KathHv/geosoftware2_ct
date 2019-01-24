#!/usr/bin/env python
# coding: utf8

#import pip
#from pycsw.core.etree import etree
import lxml.etree as etree
from owslib.util import http_post
import requests
from owslib.csw import CatalogueServiceWeb
import sys
import getopt
import subprocess
import os
from osgeo import ogr
sys.path.insert(1, os.path.join(sys.path[0], '..')+"/metadataExtraction") 
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
            cli.py 

        SYNOPSIS
            cli.py -e </absoulte/path/to/record>|</absoulte/path/to/directory>
            cli.py -s </absoulte/path/to/record>|</absoulte/path/to/directory>
            cli.py -t </absoulte/path/to/record>|</absoulte/path/to/directory>
'''


def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())

if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 's:i:p:ho:')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    #sys.exit(2)

if 'OPTS' in globals(): 
    if len(OPTS) == 0:
        errorFunction()


#command in commandline: python3 update-recordproperty.py -s testdata.json -i id
if 'OPTS' not in globals():
        raise Exception("The arguments -s \"[sourceOfFolderOrFile]\" and -i \"[idOfEntryInDB]\" -r \"[portOfServer]\" are required.")
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
    elif o == '-i':
        uuid = a
    elif o == '-p':
        port = a
    else: raise Exception("The argument " + o + " is not known. Please use -s \"[sourceOfFolderOrFile]\" and -i \"[idOfEntryInDB]\"")

if not source:
    raise Exception("The argument -s is missing. Please give a source of the used file. Format: -s \"[sourceOfFile]\"")
if not uuid:
    raise Exception("The argument -i is missing. Please give a uuid for the database entry that should be updated. Format: -i \"[uuid]\" ")




def creatXmlTree(metadata, uuid):
    '''
    input "metadata": type list, contains values for metadata that shall be updated
    input "uuid": type string, id from entry that shall be updated
    returns a xml string that is send as a post request to the server to update the entry in the database
    '''

    tempextent = ""
    vectorrep = ""
    bbox = ""
    #creating xml parts
    for key, value in metadata.items():
        if value:
            if key == "temporal_extent":
                tempextent = '''<csw:RecordProperty>
                                    <csw:Name>apiso:Time_begin</csw:Name>
                                    <csw:Value>''' + metadata["temporal_extent"][0] + '''</csw:Value>
                                </csw:RecordProperty>
                                <csw:RecordProperty>
                                    <csw:Name>apiso:Time_end</csw:Name>
                                    <csw:Value>''' + metadata["temporal_extent"][1] + '''</csw:Value>
                                </csw:RecordProperty>'''
            
            if key == "vector_rep":
                wkbLineVecRep = ogr.Geometry(ogr.wkbLinearRing)
                for elem in metadata["vector_rep"]:
                    wkbLineVecRep.AddPoint(elem[0], elem[1])
                
                wkbPolyVecRep = ogr.Geometry(ogr.wkbPolygon)
                wkbPolyVecRep.AddGeometry(wkbLineVecRep)

                wktVecRep = wkbPolyVecRep.ExportToWkt()

                vectorrep = '''<csw:RecordProperty>
                                    <csw:Name>apiso:VectorRepresentation</csw:Name>
                                    <csw:Value>''' + wktVecRep + '''</csw:Value>
                                </csw:RecordProperty>'''

            if key == "bbox":
                wkbLineBbox = ogr.Geometry(ogr.wkbLinearRing)
                wkbLineBbox.AddPoint(metadata["bbox"][0],metadata["bbox"][1])
                wkbLineBbox.AddPoint(metadata["bbox"][2],metadata["bbox"][3])
                
                wkbPolyBbox = ogr.Geometry(ogr.wkbPolygon)
                wkbPolyBbox.AddGeometry(wkbLineBbox)

                wktBbox = wkbPolyBbox.ExportToWkt()

                bbox = '''<csw:RecordProperty>
                            <csw:Name>apiso:BoundingBox</csw:Name>
                            <csw:Value>''' + wktBbox + '''</csw:Value>
                        </csw:RecordProperty>'''

    # if there is nothing to update                   
    if tempextent == "" and vectorrep == "" and bbox == "":
        raise Exception("The given entry has no temporal extent, vector representation and bounding box. The file could not be updated.")

    
    return '''<?xml version="1.0" encoding="UTF-8"?>
        <csw:Transaction xmlns:ogc="http://www.opengis.net/ogc" xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ows="http://www.opengis.net/ows" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd" service="CSW" version="2.0.2">
            <csw:Insert>''' + tempextent + vectorrep + bbox + '''<csw:Constraint version="1.1.0">
                    <ogc:Filter>
                        <ogc:PropertyIsEqualTo>
                            <ogc:PropertyName>apiso:Identifier</ogc:PropertyName>
                        <ogc:Literal>''' + uuid + '''</ogc:Literal>
                        </ogc:PropertyIsEqualTo>
                    </ogc:Filter>
                </csw:Constraint>
            </csw:Update>
        </csw:Transaction>
        '''



try:
    # sends update request as xml to pycsw server 
    r = requests.post(port, data = creatXmlTree(metadata, uuid))
    print(r.content)
except Exception as e:
    print("Error while updating db entry with id "+ uuid +". "+ str(e))



