'''
@author: Katharina Hovestadt
'''

import helpfunctions as hf
import gdal, gdalconst
import os
import osgeo.osr as osr
import convex_hull


DATATYPE = "image/tiff"

def extractContentFromPath(filePath):
    ''' method to extract geotiff content from a file by using its filepath \n
    input "filepath": type string, path to file which shall be extracted \n
    returns geotiff content of the filepath: type string
    '''
    gdal.UseExceptions()
    #zip https://rasterio.readthedocs.io/en/latest/quickstart.html
    #GDAL error handler
    #from: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#get-raster-metadata
    gtiffContent = gdal.Open(filePath)
    return gtiffContent




def isValid(filePath):
    '''Checks whether it is valid geotiff or not.
    input filepath: type string, path to file which shall be extracted
    output true if file is valid, false if not
    '''
    gdal.UseExceptions()
    
    #zip https://rasterio.readthedocs.io/en/latest/quickstart.html
    #GDAL error handler
    #from: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#get-raster-metadata
    gtiffContent = gdal.Open(filePath)
    if not gtiffContent:
        raise Exception("geotiff file cannot be opened, read or is empty.")
    return gtiffContent




def getBoundingBox(filePath):
    ''' extracts bounding box from geotiff \n
    input "filepath": type string, file path to geotiff file \n
    returns bounding box of the file: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
    gtiffContent = extractContentFromPath(filePath)
    boundingBox = []
    geoTransform = gtiffContent.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]        
    maxx = minx + geoTransform[1] * gtiffContent.RasterXSize
    miny = maxy + geoTransform[5] * gtiffContent.RasterYSize
     
    minx = float(minx)
    maxy = float(maxy)
    maxx = float(maxx)
    miny = float(miny)

    boundingBox= [miny, minx, maxy, maxx]
    if not boundingBox:
        raise Exception("Bounding box could not be extracted")
    return boundingBox



def getCRS(filePath):
    ''' gets the coordinate reference systems from the geotiff file \n
    input "filepath": type string, file path to geotiff file \n
    return epsg code of the used coordiante reference system: type int
    '''

    gtiffContent = extractContentFromPath(filePath)
    crsCode = None
    proj = osr.SpatialReference(wkt=gtiffContent.GetProjection())
    crsCode = proj.GetAttrValue('AUTHORITY',1)
    if not crsCode :
        raise Exception("Crs could not be extracted. WGS84 will be taken as standard.")
    return crsCode




def getVectorRepresentation(filePath):
    ''' extracts coordinates from geotiff File (for vector representation) \n
    input "filepath": type string, file path to geotiff file \n
    returns extracted coordinates of content: type list, list of lists with length = 2
    See bbox (doubled for threading (getBoundingBox is locked))
    '''
    gtiffContent = extractContentFromPath(filePath)
    vectorRepresentation = []
    geoTransform = gtiffContent.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]        
    maxx = minx + geoTransform[1] * gtiffContent.RasterXSize
    miny = maxy + geoTransform[5] * gtiffContent.RasterYSize
     
    minx = float(minx)
    maxy = float(maxy)
    maxx = float(maxx)
    miny = float(miny)

    vectorRepresentation= [[minx, miny], [maxx, maxy]]
    if not vectorRepresentation:
        raise Exception("Bounding box could not be extracted")
    return vectorRepresentation



def getTemporalExtent(filePath):
    ''' extracts temporal extent of the geotiff \n
    input "filepath": type string, file path to geotiff file \n
    returns the temporal extent of the file: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
    '''

    gtiffContent = extractContentFromPath(filePath)

    temporalExtent = []
    temporalExtent = gtiffContent.GetMetadataItem("TIFFTAG_DATETIME")

    if not temporalExtent:
        raise Exception("Geotiff has no temporal extent")

    temporalExtent = [temporalExtent, temporalExtent]
    return temporalExtent

