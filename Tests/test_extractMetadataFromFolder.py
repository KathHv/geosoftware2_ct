#!/usr/bin/env python
# coding: utf8
import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..') + "/CLITools/metadataExtraction")
import dateutil.parser
import extractFromFolderOrFile as extract
import math

TESTED_FOLDER = None

'''configParser = configparser.RawConfigParser()
configFilePath = 'testdata.cfg'
configParser.read(configFilePath)
TESTED_FOLDER = configParser.get('testdata', 'testfolder')'''


def test_bbox():
    try:
        bbox = extract.extractMetadataFromFolder(TESTED_FOLDER, "s")
        bbox = bbox["bbox"]
    except Exception as e:
        print(e)
        assert False # bounding could not be extracted
    if len(bbox) == 4:
        print(bbox)
        for index, x in enumerate(bbox):
            try:
                float(x)
            except Exception as e:
                print(e)
                assert type(x) == float
                return
            coordinate = float(x)
            if index == 0 or index == 2:
                print(coordinate)
                if math.ceil(coordinate) not in range(-180, 180):
                    assert math.ceil(coordinate) in range(-180, 180)
                    return
            if index == 1 or index == 3:
                if math.ceil(coordinate) not in range(-90, 90):
                    #assert coordinate in range(-90, 90)
                    assert math.ceil(coordinate) in range(-90, 90)
                    return

        assert True
        return
    else: assert len(bbox) == 4


def test_temporalextent():
    try:
        temp_extent = extract.extractMetadataFromFolder(TESTED_FOLDER, "s")
        temp_extent = temp_extent["temporal_extent"] 
    except Exception as e:
        assert False # bounding could not be extracted
    if len(temp_extent) == 2:
        for x in temp_extent:
            try:
                dateutil.parser.parse(x)
            except Exception as e:
                print(e)
                assert False
                return
        if dateutil.parser.parse(temp_extent[0]) > dateutil.parser.parse(temp_extent[1]): 
            assert False
            return
        assert True
        return

def test_vectorrepresentation():
    try:
        vector_rep = extract.extractMetadataFromFolder(TESTED_FOLDER, "s")
        vector_rep = vector_rep["vector_rep"]
    except Exception as e:
        assert False # bounding could not be extracted
    if len(vector_rep) < 1:
        for x in vector_rep:
            try:
                float(x)
            except Exception as e:
                print(e)
                assert False
                return
        assert True
        return




