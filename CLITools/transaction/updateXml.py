'''
@author: Katharina Hovestadt
'''
from osgeo import ogr
from datetime import datetime as dtime

def createXmlTree(metadata, uuid):
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
                if len(metadata["temporal_extent"])>1:
                    try:

                        startPoint = dtime.strptime(metadata["temporal_extent"][0] ,'%Y-%m-%dT%H:%M:%SZ')
                        endPoint = dtime.strptime(metadata["temporal_extent"][1] ,'%Y-%m-%dT%H:%M:%SZ')
                    
                        tempextent = '''<csw:RecordProperty>
                                        <csw:Name>apiso:TempExtent_begin</csw:Name>
                                        <csw:Value>''' + startPoint + '''</csw:Value>
                                    </csw:RecordProperty>
                                    <csw:RecordProperty>
                                        <csw:Name>apiso:TempExtent_end</csw:Name>
                                        <csw:Value>''' + endPoint + '''</csw:Value>
                                    </csw:RecordProperty>'''
                    except:
                        tempextent = ""
            if key == "vector_rep":
                if metadata["vector_rep"]:
                    #create wkt polygon by parsing coordinates to wkb 
                    wkbLineVecRep = ogr.Geometry(ogr.wkbLinearRing)
                    for elem in metadata["vector_rep"]:
                        wkbLineVecRep.AddPoint(elem[0], elem[1])
                    wkbLineVecRep.AddPoint(metadata["vector_rep"][0][0], metadata["vector_rep"][0][1])

                    wkbPolyVecRep = ogr.Geometry(ogr.wkbPolygon)
                    wkbPolyVecRep.AddGeometry(wkbLineVecRep)

                    wktVecRep = wkbPolyVecRep.ExportToWkt()

                    vectorrep = '''<csw:RecordProperty>
                                        <csw:Name>apiso:Vector_rep</csw:Name>
                                        <csw:Value>''' + wktVecRep + '''</csw:Value>
                                    </csw:RecordProperty>'''

            if key == "bbox":
                if metadata["bbox"]:
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
            <csw:Update>''' + tempextent + vectorrep + bbox + '''<csw:Constraint version="1.1.0">
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
