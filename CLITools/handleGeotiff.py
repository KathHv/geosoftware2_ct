import helpfunctions as hf
import gdal, gdalconst
import os
import osgeo.osr as osr


#returns boundin box of submitted geotiff
def getBoundingBox(gtiffContent):
    boundingBox = []

    geoTransform = gtiffContent.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * gtiffContent.RasterXSize
    miny = maxy + geoTransform[5] * gtiffContent.RasterYSize

    boundingBox= [miny, minx, maxy, maxx]



    return boundingBox

def getCRS(gtiffContent):
    crsId = None
    crsId = format(gtiffContent.GetProjection())
    return crsId



#returns vector representation of submitted geotiff
def getVectorRepresentation(gtiffContent):
    vectorRepresentation = []
    
    geoTransform = gtiffContent.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * gtiffContent.RasterXSize
    miny = maxy + geoTransform[5] * gtiffContent.RasterYSize

    vectorRepresentation= [miny, minx, maxy, maxx]



    return vectorRepresentation

#returns temporal extent of submitted geotiff
def getTemporalExtent(gtiffContent):
    temporalExtent = []
    
    return temporalExtent

#returns addditional metadata of submitted geotiff
def getAdditionalMetadata(gtiffContent, fileFormat, filePath):
    additionalMetadata = {}
    # extract other metadata
        
    #additionalMetadata["crs"] = gtiffContent.GetAttrValue("AUTHORITY", 1)
    additionalMetadata["driver"] =  format(gtiffContent.GetDriver().LongName)
    
    additionalMetadata["description"] = gtiffContent.GetDescription()

    additionalMetadata["fileformat"] = "text/" + fileFormat
    additionalMetadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
 
    return additionalMetadata





#gets called when the argument of the command request is a GeoTIFF
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}
    
    gdal.UseExceptions()
    
    #zip https://rasterio.readthedocs.io/en/latest/quickstart.html
    #GDAL error handler
    #from: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#get-raster-metadata
    try:
        gtiffContent = gdal.Open(filePath)
        #if gtiffContent is None:
            #raise FileNotFoundError, e
    

        #extract bbox and geometry
        if whatMetadata == 's':
            metadata["bbox"] = getBoundingBox(gtiffContent)   
            metadata["crs"] = getCRS(gtiffContent)
            metadata["coordinates"] = metadata["bbox"]
        #extract temporal extend
        if whatMetadata == 't':
            metadata["temporal_extent"] = getTemporalExtent(gtiffContent)
        #extract bbox, temporal extend and additional metadata
        if whatMetadata == 'e':
            #extract bbox and geometry
            metadata["bbox"] = getBoundingBox(gtiffContent)
            metadata["crs"] = getCRS(gtiffContent)
            #extract time extent
            metadata["temporal_extent"] = getTemporalExtent(gtiffContent)
            #extract other metadata
            addMetadata = getAdditionalMetadata(gtiffContent, fileFormat, filePath)       
            for key, value in addMetadata.items():
                metadata[key] = value


    #except FileNotFoundError, e:
    #    print("Could not open " + filePath)
    #    print e

    except Exception as e:
        print ('RuntimeError')
        print (e)
    print (metadata)
    return metadata

