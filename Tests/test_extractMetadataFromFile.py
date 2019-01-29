#!/usr/bin/env python
# coding: utf8
import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..') + "/CLITools/metadataExtraction")
import dateutil.parser
import extractFromFolderOrFile as extract
import math
import configparser

# testfiles
geojsons = ['https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fgeojson%20-%20Cerca%20Trova&files=testdata1.geojson',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fgeojson%20-%20Cerca%20Trova&files=testdata2.geojson',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FgeoJSON-die%20Gruppe%201&files=Abgrabungen_Kreis_Kleve.geojson',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FgeoJSON-die%20Gruppe%201&files=Baumf%C3%A4llungen_D%C3%BCsseldorf.geojson',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FgeoJSON-die%20Gruppe%201&files=Behindertenparkpl%C3%A4tze_D%C3%BCsseldorf.geojson',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FgeoJSON-die%20Gruppe%201&files=schutzhuetten_aachen.json']
csv = ['https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fcsv-die%20Gruppe1&files=Adressen_Kreis_Viersen_CSV.csv',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fcsv-die%20Gruppe1&files=Baudenkmale_Bielefeld.csv',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fcsv-die%20Gruppe1&files=Baumf%C3%A4llungen%202018%20geocodiert_D%C3%BCsseldofr.csv',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fcsv-die%20Gruppe1&files=Behindertenparkpl%C3%A4tze_D%C3%BCsseldorf.csv',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fcsv-die%20Gruppe1&files=Bewegungen_Juelich.csv',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fcsv-die%20Gruppe1&files=schutzhuetten_Aachen.csv',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FTestdaten-A%C2%B2HL%C2%B2%2Fcsv&files=kalterherberg_zeitreihe.csv',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FTestdaten-A%C2%B2HL%C2%B2%2Fcsv&files=kalterherberg_zeitreihe_fehler.csv',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FTestdaten-A%C2%B2HL%C2%B2%2Fcsv&files=schlangenberg_zeitreihe.csv']
geopackages = ['https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FGeopackage-die%20Gruppe%201%2FGeopackage_Queensland_Children&files=census2016_cca_qld_short.gpkg']
netcdf = ['https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FnetCDF%20-%20Cerca%20Trova&files=cami_0000-09-01_64x128_L26_c030918.nc',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FnetCDF%20-%20Cerca%20Trova&files=sresa1b_ncar_ccsm3-example.nc',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2FnetCDF%20-%20Cerca%20Trova&files=tos_O1_2001-2002.nc']
shapefile = ['https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fshapefiles%20-%20Cerca%20Trova%2Fpol&files=simplified_land_polygons.shp',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fshapefile-die%20Gruppe%201%2FAbgrabungen_Kreis_Kleve&files=Abgrabungen_Kreis_Kleve_Shape.shp',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fshapefile-die%20Gruppe%201%2FJagdbezirke_Viersen&files=JAGDBEZIRKSKARTE.shp',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fshapefile-die%20Gruppe%201%2FMittlWindgeschw-100m&files=wf_100m.shp',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Fshapefile-die%20Gruppe%201%2FStadtbezirke_Aachen&files=stadtbezirkePolygon.shx']
goetiff = ['https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Ftif-die%20Gruppe%201%2Fdigitale_Verwaltungsgrenzen_tiff&files=dvg2bld_geo_nw.tif',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Ftif-die%20Gruppe%201%2Fdigitale_Verwaltungsgrenzen_tiff&files=dvg2gem_namen_nw.tif',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Ftif-die%20Gruppe%201%2Fdigitale_Verwaltungsgrenzen_tiff&files=dvg2rbz_namen_nw.tif',
'https://uni-muenster.sciebo.de/s/QFj5pzm7AzxAh1f/download?path=%2Ftif-die%20Gruppe%201%2FMittlWindgeschw-100m_GeoTIFF&files=wf_100m_klas.tif']

TESTED_FILE = geojsons[0]

'''configParser = configparser.RawConfigParser()
configFilePath = 'testdata.cfg'
configParser.read(configFilePath)
TESTED_FILE = configParser.get('testdata', 'testfile')'''

print(TESTED_FILE)



def test_bbox():
    try:
        bbox = extract.extractMetadataFromFile(TESTED_FILE, "s")
        bbox = bbox["bbox"]
    except:
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
        temp_extent = extract.extractMetadataFromFile(TESTED_FILE, "t")
        temp_extent = temp_extent["temporal_extent"] 
    except:
        assert False # temporal extent could not be extracted
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
        vector_rep = extract.extractMetadataFromFile(TESTED_FILE, "s")
        vector_rep = vector_rep["vector_rep"]
    except:
        assert False # vector representation could not be extracted
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




