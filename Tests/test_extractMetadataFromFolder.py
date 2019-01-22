import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..') + "/CLITools")
import dateutil.parser
import helpfunctions
import pytest
from extract_metadata import extractMetadataFromFolder
import handleCSV, handleGeopackage, handleNetCDF, handleShapefile
import math

# path to our abosulte folder 'testdata'; dive link: https://drive.google.com/drive/u/0/folders/1IWoqpba4xT5kIX0FhNOKfXA5EIJDqj5I
# when the folder is downloaded as in drive, the other pathes depend only on the path
ABSOULTE_PATH = "/Users/benjamindietz/Desktop/vpycsw/testdata/"

# Folders only with data of one certain file format
onlyCSV = ABSOULTE_PATH + "csv/"
onlyGeopackage = ABSOULTE_PATH + "geopackage/"
onlyNetCDF = ABSOULTE_PATH + "netcdf/"
onlyShapefile1 = ABSOULTE_PATH + "shapefile/antarctica-latest-free/"
onlyShapefile2 = ABSOULTE_PATH + "shapefile/antarctica-latest-free2/"
testfolder1 = ABSOULTE_PATH + "/TestFolder/Testfolder1"
all_testfolders = [onlyCSV, onlyGeopackage, onlyNetCDF, onlyShapefile1, onlyShapefile2, testfolder1]

def test_bbox():
    metadata = extractMetadataFromFolder(testfolder1, "e") 
    if 'bbox' in metadata:
        if len(metadata["bbox"]) == 4:
            print(metadata["bbox"])
            for index, x in enumerate(metadata["bbox"]):
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
        else: assert len(metadata["bbox"]) == 4
    else: assert 'bbox' in metadata

test_bbox()

def test_temporalextent():
    metadata = extractMetadataFromFolder(testfolder1, "e") 
    if 'temporal_extent' in metadata:
        if len(metadata["temporal_extent"]) == 2:
            for x in metadata["temporal_extent"]:
                try:
                    dateutil.parser.parse(x)
                except Exception as e:
                    print(e)
                    assert False
                    return
            if dateutil.parser.parse(metadata["temporal_extent"][0]) > dateutil.parser.parse(metadata["temporal_extent"][1]): 
                assert False
                return
            assert True
            return
    assert False

def test_vectorrepresentation():
    metadata = extractMetadataFromFolder(testfolder1, "e") 
    if 'vector_rep' in metadata:
        if len(metadata["vector_rep"]) < 1:
            for x in metadata["vector_rep"]:
                try:
                    float(x)
                except Exception as e:
                    print(e)
                    assert False
                    return
            assert True
            return
    assert False




