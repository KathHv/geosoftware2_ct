import datetime, xarray, gdal
from datetime import datetime as dtime
from netCDF4 import Dataset as NCDataset
import helpfunctions as hf


#gets called when the argument of the command request is a NetCDF
def extractMetadata(fileFormat, filePath, whatMetadata):
    # file format can be either .nc or .cdf
    metadata = {}

    if whatMetadata == "e":
        addictionalMetadata = getAddictionalMetadata(filePath)
        for x in addictionalMetadata:
            metadata[x] = addictionalMetadata[x]

    if whatMetadata == "s" or whatMetadata == "e":
        metadata["bbox"] = getBoundingBox(filePath)
        metadata["vector_representation"] = getVectorRepresentation(filePath)

        # not yet complete (does not found correct CRS -> always WGS 84?)
        metadata["crs"] = getCRS(filePath)
    
    if whatMetadata == "t" or whatMetadata == "e":
        metadata["temporal_extent"] = getTemporalExtent(filePath)
    
    return metadata
        

def getAddictionalMetadata(path):
    ncDataset = NCDataset(path)
    datasetGDAL = gdal.Open(path)
    geotransformGDAL = datasetGDAL.GetGeoTransform()
    metadataGDAL = datasetGDAL.GetMetadata()
    dimensions = []
    metadataGDAL = datasetGDAL.GetMetadata()
    metadata = {}
    for key in metadataGDAL:
        if 'axis' in key:
            dimensions.append(key[:key.rfind("#")])
        if 'NC_GLOBAL' in key:
            metadata[key[key.rfind("#")+1:]] = metadataGDAL[key]
    metadata["filename"] = path[path.rfind("/")+1:path.rfind(".")]
    metadata["format"] = "application/" + str(datasetGDAL.GetDriver().ShortName)
    metadata["size"] = [datasetGDAL.RasterXSize, datasetGDAL.RasterYSize, datasetGDAL.RasterCount] # [raster width in pixels, raster height in pixels, number raster bands]
    metadata["pixel_size"] = [geotransformGDAL[1], geotransformGDAL[5]]
    metadata["origin"] = [geotransformGDAL[0], geotransformGDAL[3]]
    return metadata

def getVectorRepresentation(path):
    file = xarray.open_dataset(path)
    if file is not None:
        if 'coords' in file.to_dict():
            if all (x in file.to_dict()["coords"] for x in ['lat', 'lon']):
                if 'data' in file.to_dict()["coords"]["lat"] and 'data' in file.to_dict()["coords"]["lon"]:
                    lats = file.to_dict()["coords"]["lat"]["data"]
                    lons = file.to_dict()["coords"]["lon"]["data"]
    if not ('lats' in locals() and 'lons' in locals()):
        ncDataset = NCDataset(path)
        if 'latitude' in ncDataset.variables:
            latitudes = ncDataset.variables["latitude"][:]
            lats = []
            for x in latitudes:
                lats.append(x)
        if 'longitude' in ncDataset.variables:
            longitudes = ncDataset.variables["longitude"][:]
            lons = []
            for x in longitudes:
                lons.append(x)
    if 'lats' in locals()  and 'lons' in locals():
        return { 'lat': lats,
                    'lon': lons }
    else: return []

def getBoundingBox(path):
    ncDataset = NCDataset(path)
    if 'latitude' in ncDataset.variables:
        lats = ncDataset.variables["latitude"][:]
        if 'longitude' in ncDataset.variables:
            lngs = ncDataset.variables["longitude"][:]
            bbox =  [min(lngs), min(lats), max(lngs), max(lats)]
            return bbox
    if 'bbox' not in locals():
        # bbox not yet extracted
        xarrayForNetCDF = xarray.open_dataset(path)
        if xarrayForNetCDF is not None:
                if 'coords' in xarrayForNetCDF.to_dict():
                    if all (x in xarrayForNetCDF.to_dict()["coords"] for x in ['lat', 'lon']):
                        if xarrayForNetCDF.to_dict()["coords"]["lat"] is not None and xarrayForNetCDF.to_dict()["coords"]["lon"] is not None:
                            lats = xarrayForNetCDF.to_dict()["coords"]["lat"]
                            dataLats = lats["data"]
                            lons = xarrayForNetCDF.to_dict()["coords"]["lon"]
                            dataLons = lons["data"]
                            if len(dataLats) > 0 and len(dataLons) > 0:
                                bbox = [min(dataLons), min(dataLats), max(dataLons), max(dataLats)]
                            return bbox
    return []

def getCRS(path):
    xarrayForNetCDF = xarray.open_dataset(path)
    if xarrayForNetCDF is not None:
            if 'coords' in xarrayForNetCDF.to_dict():
                if all (x in xarrayForNetCDF.to_dict()["coords"] for x in ['lat', 'lon']):
                    if xarrayForNetCDF.to_dict()["coords"]["lat"] is not None and xarrayForNetCDF.to_dict()["coords"]["lon"] is not None:
                        lats = xarrayForNetCDF.to_dict()["coords"]["lat"]
                        lons = xarrayForNetCDF.to_dict()["coords"]["lon"]
                        crs = [ lats["attrs"], lons["attrs"] ]
                        return crs
    return "No CRS found"

def getTemporalExtent(path):
    ncDataset = NCDataset(path)
    datasetGDAL = gdal.Open(path)
    metadataGDAL = datasetGDAL.GetMetadata()
    if 'time' in ncDataset.variables:
        times = ncDataset.variables["time"][:]
        temporal_extent =  str([min(times), max(times)]) + " Warning: Unit not absolute" 
        def getAbsoulteTimestamp(plusdays, steps, origin):
            origin = dtime.strptime(origin ,'%Y-%m-%d %H:%M:%S')
            if "days" in steps:
                return origin + datetime.timedelta(days=plusdays)
            elif "hours" in steps:
                return origin + datetime.timedelta(hours=plusdays)
            elif "minutes" in steps:
                return origin + datetime.timedelta(minutes=plusdays)
            elif "seconds" in steps:
                return origin + datetime.timedelta(seconds=plusdays)       
        if hasattr(ncDataset.variables["time"], 'units'):
            unit = ncDataset.variables["time"].units
            steps = unit[:unit.rfind(" since")]
            origin = unit[unit.rfind("since ")+6:]
            if origin[:4] == "0000":
                origin = "2000" + origin[4:]
            if len(origin) < 11:
                origin += " 00:00:00"

        elif "time#units" in metadataGDAL:
                unit = metadataGDAL["time#units"]
                steps = unit[:unit.rfind(" since")]
                origin = unit[unit.rfind("since ")+6:]
        if times is not None:
            if len(times) > 0:
                if 'steps' in locals():
                    temporal_extent = [str(getAbsoulteTimestamp(min(times), steps, origin)), str(getAbsoulteTimestamp(max(times), steps, origin))]
                    if getAbsoulteTimestamp(min(times), steps, origin) > datetime.datetime.now() or getAbsoulteTimestamp(max(times), steps, origin) > datetime.datetime.now():
                        return "temporal extent is not valid! (" + str(temporal_extent) + ")"
                    else:
                        return temporal_extent

