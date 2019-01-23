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
sys.path.insert(1, os.path.join(sys.path[0], '..')) 
import extract_metadata as extrMetad

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
        print(source)
    elif o == '-i':
        uuid = a
        print(uuid)
    elif o == '-p':
        port = a
        print(port)
    else: raise Exception("The argument " + o + " is not known. Please use -s \"[sourceOfFolderOrFile]\" and -i \"[idOfEntryInDB]\"")

if not source:
    raise Exception("The argument -s is missing. Please give a source of the used file. Format: -s \"[sourceOfFile]\"")
if not uuid:
    raise Exception("The argument -i is missing. Please give a uuid for the database entry that should be updated. Format: -i \"[uuid]\" ")

#metadata = extrMetad.extractMetadataFromFile(source, 'e')
metadata = subprocess.call("python3 ../extract_metadata.py -e " + source, shell=True) 
print("metadata")
print(metadata)
#metadata = CLITool ausführen


transactionTree = '''<?xml version="1.0" encoding="UTF-8"?>
  <csw:Transaction xmlns:ogc="http://www.opengis.net/ogc" xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:ows="http://www.opengis.net/ows" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-publication.xsd" service="CSW" version="2.0.2">
    <csw:Update>
        <csw:RecordProperty>
            <csw:Name>apiso:Time_begin</csw:Name>
            <csw:Value>''' + metadata["temp_extent"][0] + '''</csw:Value>
        </csw:RecordProperty>
        <csw:RecordProperty>
            <csw:Name>apiso:Time_end</csw:Name>
            <csw:Value>''' + metadata["temp_extent"][1] + '''</csw:Value>
        </csw:RecordProperty>

        <csw:RecordProperty>
            <csw:Name>apiso:Vector_rep</csw:Name>
            <csw:Value>''' + metadata["vector_rep"] + '''</csw:Value>
        </csw:RecordProperty>

        <csw:RecordProperty>
            <csw:Name>apiso:BoundingBox</csw:Name>
            <csw:Value>''' + metadata["bbox"] + '''</csw:Value>
        </csw:RecordProperty>

        <csw:Constraint version="1.1.0">
            <ogc:Filter>
                <ogc:PropertyIsEqualTo>
                    <ogc:PropertyName>apiso:Identifier</ogc:PropertyName>
                   <ogc:Literal>''' + str(uuid) + '''</ogc:Literal>
                </ogc:PropertyIsEqualTo>
            </ogc:Filter>
        </csw:Constraint>
    </csw:Update>
   </csw:Transaction>
'''

print("xmltree")
print(transactionTree)
r = requests.post(port, data = transactionTree)
#r = requests.post('http://localhost:8000/csw', data = xmltree)
print(r.content)
