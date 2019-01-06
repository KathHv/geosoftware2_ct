import helpfunctions as hf
import gdal, gdalconst
import os
import osgeo.osr as osr




#method to extract geotiff content from a file by using its filepath
#input filepath: type string, path to file which shall be extracted
#output gtiffContent: type string,  returns  geojson content of filepath 
def extractContentFromPath(filePath):
    gdal.UseExceptions()
    
    #zip https://rasterio.readthedocs.io/en/latest/quickstart.html
    #GDAL error handler
    #from: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#get-raster-metadata
    gtiffContent = gdal.Open(filePath)
    if not gtiffContent:
        raise Exception("geotiff file cannot be opened, read or is empty.")
    return gtiffContent


#extract bounding box from geotiff
#input filepath: type string, file path to geotiff file
#output bbox: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
def getBoundingBox(filePath):
        gtiffContent = extractContentFromPath(filePath)
        boundingBox = []
        geoTransform = gtiffContent.GetGeoTransform()
        minx = geoTransform[0]
        maxy = geoTransform[3]        
        maxx = minx + geoTransform[1] * gtiffContent.RasterXSize
        miny = maxy + geoTransform[5] * gtiffContent.RasterYSize
        
        minx = format(float(minx), '.2f')
        maxy = format(float(maxy), '.2f')
        maxx = format(float(maxx), '.2f')
        miny = format(float(miny), '.2f')

        boundingBox= [miny, minx, maxy, maxx]
        if not boundingBox:
            raise Exception("Bounding box could not be extracted")
        return boundingBox



#extracts EPSG number of the taken coordinate reference system (short: crs)
#input filepath: type string, file path to geotiff file
#output crsCode: type int, EPSG number of taken crs
def getCRS(filePath):

    gtiffContent = extractContentFromPath(filePath)
    crsCode = None
    proj = osr.SpatialReference(wkt=gtiffContent.GetProjection())
    crsCode = proj.GetAttrValue('AUTHORITY',1)
    if not crsCode :
        raise Exception("Crs could not be extracted.")
    return crsCode




#extracts coordinates from geojson File (for vector representation)
#input filepath: type string, file path to geotiff file
#output coordinates: type list, list of lists with length = 2, contains extracted coordinates of content from geotiff file
def getVectorRepresentation(filePath):
    gtiffContent = extractContentFromPath(filePath)
    vectorRepresentation = []
    geoTransform = gtiffContent.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * gtiffContent.RasterXSize
    miny = maxy + geoTransform[5] * gtiffContent.RasterYSize
    vectorRepresentation = [miny, minx, maxy, maxx]

    #raise Exception("Vector representation could not be extracted" + str(e))
    if not vectorRepresentation:
        raise Exception("No coordinates found in file. Vector Representation could not be extracted.")
    return vectorRepresentation




#extracts temporal extent of the geotiff
#input filepath: type string, file path to geotiff file
#output timeExtent: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
def getTemporalExtent(filePath):
    gtiffContent = extractContentFromPath(filePath)

    temporalExtent = []
    temporalExtent = gtiffContent.GetMetadataItem("TIFFTAG_DATETIME")

    if not temporalExtent:
        raise Exception("Geotiff has no temporal extent")

    temporalExtent = [temporalExtent, temporalExtent]
    return temporalExtent

