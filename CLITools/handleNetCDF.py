import datetime, xarray, gdal
from datetime import datetime as dtime
from netCDF4 import Dataset as NCDataset
import helpfunctions as hf

# abstract the geometry of the file with a polygon
# first: collects all the points of the file
# then: call the function that computes the polygon of it
# returns the polygon as an array of points
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
        # TO DO: call function that computes polygon
    raise Exception("The vector representaton could not be extracted from the file")

# returns the bounding box of the file: an array with len(array) = 4 
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

    raise Exception("The bounding box could not be extracted from the file")

# returns the bounding box of the netcdf file
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
                        # HERE: CRS is in a different format
    return "No CRS found"

# extracts the temporal extent of the netCDF file
# the returned values is an array with the schema [ startpoint, endpoint ]
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
                        print("temporal extent of " + path + " is not valid! (" + str(temporal_extent) + ")")
                    else:
                        return temporal_extent
    # raises exception when 1) no time variable could be found OR 2) no time unit could be found

    raise Exception("The temporal extent could not be extracted from the file")

