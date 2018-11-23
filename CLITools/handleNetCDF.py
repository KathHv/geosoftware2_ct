import gdal, datetime
from datetime import datetime as dtime
from netCDF4 import Dataset as NCDataset
import helpfunctions as hf


#gets called when the argument of the command request is a NetCDF
def extractMetadata(fileFormat, filePath, whatMetadata):
    # file format can be either .nc or .cdf
    metadata = {}
    datasetGDAL = gdal.Open(filePath)
    geotransformGDAL = datasetGDAL.GetGeoTransform()
    metadataGDAL = datasetGDAL.GetMetadata()
    dimensions = []
    if whatMetadata == "e":
        for key in metadataGDAL:
            if 'axis' in key:
                dimensions.append(key[:key.rfind("#")])
            if 'NC_GLOBAL' in key:
                metadata[key[key.rfind("#")+1:]] = metadataGDAL[key]
        metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
        metadata["format"] = datasetGDAL.GetDriver().ShortName
        metadata["size"] = [datasetGDAL.RasterXSize, datasetGDAL.RasterYSize, datasetGDAL.RasterCount] # [raster width in pixels, raster height in pixels, number raster bands]
        metadata["pixel_size"] = [geotransformGDAL[1], geotransformGDAL[5]]
        metadata["origin"] = [geotransformGDAL[0], geotransformGDAL[3]]

        # get metadata beginning with "tos" if they are available
        for key in metadataGDAL:
            if 'tos' == key[:3]:
                metadata["subject"] = metadataGDAL["tos#long_name"]
                metadata["original_units"] = metadataGDAL["tos#original_units"]
                metadata["units"] = metadataGDAL["tos#units"]

        # get standard_name for each dimension of available
        if dimensions:
            counter = 0
            for dim in dimensions:
                mdataOfDimension = []
                for key in metadataGDAL:
                    if key[:len(dim)] == dim:
                        mdataOfDimension.append([key[len(dim)+1:], metadataGDAL[key]])
                if str(dim) + "#standard_name" in metadataGDAL:
                    dimensions[counter] = metadataGDAL[str(dim) + "#standard_name"]
                metadata[dim] = mdataOfDimension
                counter += 1
            metadata["dimensions"] = dimensions

    ncDataset = NCDataset(filePath)
    if 'latitude' in ncDataset.variables:
        lats = ncDataset.variables["latitude"][:]
        if 'longitude' in ncDataset.variables:
            lngs = ncDataset.variables["longitude"][:]
            metadata["bbox"] =  [min(lngs), min(lats), max(lngs), max(lats)]
        elif whatMetadata == "s": raise Exception("No spatial data found")
    elif whatMetadata == "s": raise Exception("No spatial data found")
    if not whatMetadata == "s":
        if 'time' in ncDataset.variables:
            times = ncDataset.variables["time"][:]
            metadata["temporalExtent"] = str([min(times), max(times)]) + " Warning: Unit not absolute"
            if "time#units" in metadataGDAL:
                    unit = metadataGDAL["time#units"]
                    steps = unit[:unit.rfind(" since")]
                    origin = unit[unit.rfind("since ")+6:]
                    originDate = dtime.strptime(origin ,'%Y-%m-%d')
                    def getAbsoulteTimestamp(timeValue):
                        if "days" in steps:
                            return originDate + datetime.timedelta(days=timeValue)
                        elif "hours" in steps:
                            return originDate + datetime.timedelta(hours=timeValue)
                        elif "minutes" in steps:
                            return originDate + datetime.timedelta(minutes=timeValue)
                        elif "seconds" in steps:
                            return originDate + datetime.timedelta(seconds=timeValue)
                    #metadata["temporalExtent"] = [getAbsoulteTimestamp(min(times)) , getAbsoulteTimestamp(max(times))]
                    metadata["temporalExtent"] = [str(getAbsoulteTimestamp(min(times))) , str(getAbsoulteTimestamp(max(times)))]

    '''
        # shows what metadata is available
        for a,b in metadataGDAL.items():
        print(str(a) + ": " + b)    '''

    # get survey 
    for a,b in metadata.items():
        if len(b) > 150:
            metadata[a] = " { ... } "

    # filename, format, size, pixel_size, origin, subject, original_units, units, dimensions
    # NC_GLOBAL: title, source, dimensions, references, realization, project_id, institution, history, experiment_id, Conventions(of metadata!), contact, comment, cmor_version
    return metadata
