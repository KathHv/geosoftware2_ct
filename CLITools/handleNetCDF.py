'''
@author: Benjamin Dietz
'''

import datetime, xarray
import gdal
from datetime import datetime as dtime
from netCDF4 import Dataset as NCDataset
import helpfunctions as hf
import convex_hull

DATATYPE = "application/x-netcdf"

def isValid(path):
    '''Checks whether it is valid netCDF or not. \n
    input "path": type string, path to file which shall be extracted \n
    output true if file is valid, false if not
    '''
    try:
        file = xarray.open_dataset(path)
        ncDataset = NCDataset(path)
        datasetGDAL = gdal.Open(path)
        if file is None or ncDataset is None or datasetGDAL is None:
            return False
    except:
        return False
    return True

def getVectorRepresentation(path):
    ''' abstracts the geometry of the file with a polygon
    first: collects all the points of the file
    then: call the function that computes the polygon of it \n
    input "path": type string, path to file which shall be extracted \n
    returns extracted coordinates of content: type list, list of lists with length = 2: type list
    '''
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
        coordinates = { 'lat': lats, 'lon': lons }
        if len(lats) == len(lons):
            referenced_coordinates = []
            for index, val in enumerate(lats):
                referenced_coordinates.append([lons[index], val])
                coordinates = convex_hull.graham_scan(coordinates)
        else: 
            raise Exception("The numer auf lat-points and lon-points is not equal, thus a  vector representation cannot be computed.")
        return coordinates
    raise Exception("The vector representaton could not be extracted from the file")




def getBoundingBox(path):
    ''' extracts bounding box from NetCDF \n
    input "path": type string, path to file which shall be extracted \n
    returns bounding box: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
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




def getCRS(path):
    ''' gets the coordinate reference systems from the NetCDF file \n
    input "path": type string, path to file which shall be extracted \n
    returns epsg code of the used coordiante reference system: type list, list with two elements: 1. Crs of lats and 2. Crs of lons
    '''
    return hf.WGS84_EPSG_ID




def getTemporalExtent(path):
    ''' extracts the temporal extent of the netCDF file \n
    input "path": type string, path to file which shall be extracted \n
    reutrns temporal  extent of the file: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
    '''
    ncDataset = NCDataset(path)
    datasetGDAL = gdal.Open(path)
    metadataGDAL = datasetGDAL.GetMetadata()
    try:
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
    except:
        raise Exception("The temporal extent could not be extracted from the file")
    
    # raises exception when 1) no time variable could be found OR 2) no time unit could be found

    raise Exception("The temporal extent could not be extracted from the file")
