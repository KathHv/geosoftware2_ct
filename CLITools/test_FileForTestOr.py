import helpfunctions
import pytest
import FileForTestOr
from handleCSV import extractMetadataFromCSV
from handleGeopackage import extractMetadataGeopackage
from handleGeojson import extractMetadataGeojson


#testet, ob die Datei nicht existiert
def test_exists_FileNotFound():
    ans = helpfunctions.exists("du")
    assert ans == False

#testet, ob die Datei existiert
def test_exists_FileFound():
    ans = helpfunctions.exists("/home/ilka/Desktop/postcode_polygons.gpkg")
    ans2 = helpfunctions.exists("/home/ilka/Desktop/test.csv")
    ans3 = helpfunctions.exists("/home/ilka/Desktop/geojson.json")
    assert ans == True
    assert ans2 == True
    assert ans3 == True

#testet, ob in der aufgerufene CSV-Datei keine Metadaten enthalten sind
def test_extractMetadataCSV_ValueError():
    ans = extractMetadataFromCSV("/home/ilka/Desktop/testempty.csv")
    assert ans == {'elements': []}

#testet, ob die aufgerufene GeoJSON-Datei leer ist
#def test_extractMetadataGeoJson_ValueError():
#    ans = extractMetadataGeojson("json","/home/ilka/Desktop/geojsonempty.json", "e")
#    assert ans == {'elements': []}

#testet, ob die aufgerufene Gpkg-Datei leer ist
#def test_extractMetadataGpkg_ValueError():
#    ans = extractMetadataGeopackage("/home/ilka/Desktop/postcode_polygonsempty.gpkg", "e")
#    assert ans == {'elements': []}

#testet, ob das FileFormat unterstützt wird
def test_extractMetadataFromFile_FiletypeNotValid():
    with pytest.raises(Exception) as ans:
        FileForTestOr.extractMetadataFromFile("/home/ilka/Desktop/bild.jpg","e")
    assert "This file format is not supported" in str(ans.value)

#testet, ob shp mit shx existiert
def test_extractMetadataFromFile_shpWithoutShx():
    path = "/home/ilka/Desktop/shape"
    shpPath = path+".shp"
    shxPath = path+".shx"
    shxPath2 = path+".SHX"
    with pytest.raises(Exception) as ans:
        FileForTestOr.extractMetadataFromFile(shpPath, "e")
    errorString = "Unable to open "+shxPath+" or "+shxPath2+". Set SHAPE_RESTORE_SHX config option to YES to restore or create it."
    
    assert errorString in str(ans.value)

#testet, ob dbf mit "Nonetype" existiert
def test_extractMetadataFromFile_shpWithoutDbf():
    path = "/home/ilka/Desktop/sample"
    dbfPath = path+".dbf"
    with pytest.raises(Exception) as ans:
        FileForTestOr.extractMetadataFromFile(dbfPath, "e")
    errorString = "'NoneType' object is not subscriptable"
    
    assert errorString in str(ans.value)

#testet, ob die Metadaten eine BB besitzen
def test_extractMetadataFromFile_hasBoundingBox():
    ans = FileForTestOr.extractMetadataFromFile("/home/ilka/Desktop/test.csv", "e")
    print(ans)
    assert [] != ans["BoundingBox"]

#testet, ob die BoundingBox mindestens die Länge ein hat
def test_extractMetadataFromFile_hasBoundingBoxGrEins():
    ans = FileForTestOr.extractMetadataFromFile("/home/ilka/Desktop/test.csv", "e")
    assert len(ans["BoundingBox"]) >= 1
    ans2 = False
    if type(ans["BoundingBox"]) is list: 
        ans2 = True
    assert ans2 == True

#testet, ob der temporal extend extrahiert werden kann
def test_extractMetadataFromFile_hasBoundingBoxGrEins():
    ans = FileForTestOr.extractMetadataFromFile("/home/ilka/Desktop/test.csv", "t")
    print(ans)
    assert len(ans["Temporal Extent"]) >= 1
    ans2 = False
    if type(ans["Temporal Extent"]) is list: 
        ans2 = True
    assert ans2 == True

#testet, ob Tag -t funktioniert
def test_extractMetadataFromFile_TagT():
    ans = FileForTestOr.extractMetadataFromFile("/home/ilka/Desktop/test.csv", "t")
    print(ans)
    ans3 = False
    if len(ans["Temporal Extent"]) == 2:
        ans3 = True
    ans2 = False
    ans4 = False
    ans5 = True
    if len(ans) >0:
        ans4 = True
    if ans["Temporal Extent"]:
        ans2 = True
    if "bbox" in ans or "BoundingBox" in ans:
        ans5 = False
    assert ans2 == True
    assert ans3 == True
    assert ans4 == True
    assert ans5 == True

#testet, ob Tag -s funktioniert
def test_extractMetadataFromFile_TagS():
    ans = FileForTestOr.extractMetadataFromFile("/home/ilka/Desktop/test.csv", "s")
    print (ans)
    ans3 = False
    if len(ans["Spatial Extent"]) == 4:
        ans3 = True
    ans2 = False
    ans4 = False
    ans5 = True
    if len(ans) > 0:
        ans4 = True
    if ans ["Spatial Extent"]:
        ans2 = True
    if "bbox" in ans or "BoundingBox" in ans:
        ans5 = False
    assert ans2 == True
    assert ans3 == True
    assert ans4 == True
    assert ans5 == True

#testet, ob Tag -e funktioniert
def test_extractMetadataFromFile_TagE():
    ans = FileForTestOr.extractMetadataFromFile("/home/ilka/Desktop/test.csv", "e")
    ans2 = False
    print(ans)
    if len(ans)>= 1:
        ans2 = True
    ans3 = False
    ans4 = False
    for key, value in ans.items():
        if key == "StartTime-EndTime":
            if len(ans["StartTime-EndTime"]) == 2:
                ans3 = True
        if key == "BoundingBox":
            if len(ans["BoundingBox"]) == 4:
                ans4 = True    
    assert ans2 == True
    assert ans3 == True
    assert ans4 == True

#testet, ob die BoundingBox ein Koordinatensystem mit sich bringt

def test_extractMetadataFromFile_BoundingBoxExists():
    ans = FileForTestOr.extractMetadataFromFile("/home/ilka/Desktop/test.csv", "e")
    ans2 = False
    print (ans)
    if len(ans) > 0:
        ans2 = True
    assert ans == 5
