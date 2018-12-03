import helpfunctions as hf
import gdal

#gets called when the argument of the command request is a GeoTIFF
def extractMetadata(fileFormat, filePath, whatMetadata):
    metadata = {}
    
    gdal.UseExceptions()
    
    #zip https://rasterio.readthedocs.io/en/latest/quickstart.html
    #GDAL error handler
    #from: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#get-raster-metadata
    try:
        # Example how to use object:
        #metadata["bbox"] = [coor0, coor1, coor2, coor3]
        metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]

        gtiff = gdal.Open(filePath)
        print (gtiff)
        #print(gtiff.GeoTIFF.GetEnvelope)
        #print(gtiff.GetEnvelope)
        #print(gtiff.getRasterBand(1))
        rasterBand = gtiff.getRasterBand(1)
        print (rasterBand.GetMaximum())
        print (rasterBand.GetScale())
        #metadata["name"] = gtiff.name
        #metadata["NumberOfBands"] = gtiff.count
        #metadata["BandsWidth"] = gtiff.width
        #metadata["BandsHeight"] = gtiff.height
        #metadata["bbox"] = gtiff.bounds()
        #metadata["transform"] = gtiff.transform
        #metadata["crs"] =gtiff.crs
        metadata = gtiff.GetMetadata()
        #print(gtiff.whatMetadata)
        print(gdal.GDAL_GCP_GCPY_get)
        #metadata["GCPInfo"] = gdal.GDAL_GCP_Info_get
        #metadata["GCPX"] = gdal.GDAL_GCP_GCPX_get
        #metadata["GCPY"] = gdal.GDAL_GCP_GCPY_get
        #print(gtiff.GetMetadata())
        print (metadata)
    except RuntimeError, e:
        print ('Unable to open: ' + filePath)
        print e
        
     
    


    return metadata