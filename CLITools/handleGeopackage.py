'''
@author: Benjamin Dietz
'''

import fiona, xarray, sqlite3
import helpfunctions as hf
import convex_hull
    
DATATYPE = "application/gpkg"

def isValid(path):
    '''Checks whether it is valid geopackage or not. \n
    input "path": type string, path to file which shall be extracted \n
    output: true if file is valid, false if not
    '''
    try:
        with fiona.open(path) as datasetFiona:
            sqliteConnection = sqlite3.connect(path)
            if sqliteConnection is not None:
                c = sqliteConnection.cursor()
                if c is None:
                    return False
            else:
                return False
    except:
        return False
    return True
    


def getTemporalExtent(path):
    ''' extracts temporal extent of the geopackage \n
    input "path": type string, file path to geopackage file
    '''
    raise Exception("The temporal extent cannot be extracted from geopackage files")




def getBoundingBox(path):
    ''' extract bounding box from geopackage \n
    input "path": type string, file path to geopackage file \n
    returns the bounding box of the file, type list: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''

    # try to get the bbox with fiona
    with fiona.open(path) as datasetFiona:
        bbox = [datasetFiona.bounds[0], datasetFiona.bounds[1], datasetFiona.bounds[2], datasetFiona.bounds[3]]
        return bbox
        
    # if not try the same with a database connection (sqlite)
    sqliteConnection = sqlite3.connect(path)
    if sqliteConnection is not None:
        c = sqliteConnection.cursor()
    if c is not None:
        crs = []
        for row in c.execute('SELECT table_name, srs_name, definition FROM gpkg_geometry_columns, gpkg_spatial_ref_sys where gpkg_spatial_ref_sys.srs_id ==  gpkg_geometry_columns.srs_id'):
            dict = {row[0]: {"crs_name": row[1], "description": row[2]}}
            crs.append(dict)
        lats = []
        longs = []
        crs = []
        # TO DO: transform the bbox for each row in gpkg_contents depending on its CRS and after that compute the overall bbox
        for row in c.execute('SELECT min_x, min_y, max_x, max_y FROM gpkg_contents'):
            if not None in row:
                longs.extend([row[0], row[2]])
                lats.extend([row[1], row[3]])
        if len(longs) > 1 and len(lats) > 1:
            return [min(longs), min(lats), max(longs), max(lats)]

    raise Exception("The bounding box could not be extracted from the file")




def getVectorRepresentation(path):
    ''' abstract the geometry of the file with a polygon
    first: collects all the points of the file
    then: call the function that computes the polygon of it \n
    input "path": type string, file path to geopackage file \n
    returns extracted coordinates of content: type list, list of lists with length = 2
    '''
    coordinates = []
    with fiona.open(path) as datasetFiona:
        for shapeElement in datasetFiona:
            if 'geometry' in shapeElement:
                if shapeElement["geometry"] is not None:
                    if 'coordinates' in shapeElement["geometry"]:
                        element = shapeElement["geometry"]["coordinates"]
                        def getCoordinatesFromArray(element):
                            if len(element) == 1:
                                if type(element[0]) == list:
                                    if type(element[0][0]) == list:
                                        for y in element[0][0]:
                                            coordinates.append([y[0], y[1]])
                                    elif type(element[0][0]) == tuple:
                                        coordinates.append([element[0][0][0], element[0][0][1]])
                                    else: raise Exception("Filetype could not be handled")
                            if len(element) == 2:
                                if type(element[0]) == list:
                                    if type(element[0][0]) == list:
                                        for y in element[0][0]:
                                            coordinates.append([y[0], y[1]])
                                    elif type(element[0][0]) == tuple:
                                        coordinates.append([element[0][0][0], element[0][0][1]])
                                    else: raise Exception("Filetype could not be handled")
                                if type(element[1]) == list:
                                    if type(element[0][0]) == list:
                                        for y in element[0][0]:
                                            coordinates.append([y[0], y[1]])
                                    elif type(element[0][0]) == tuple:
                                        coordinates.append([element[0][0][0], element[0][0][1]])
                                    else: raise Exception("Filetype could not be handled")
                                if type(element[0]) == float and type(element[1]) == float:
                                    coordinates.append([element[0], element[1]])
                        getCoordinatesFromArray(element)
    if len(coordinates) > 0:
        # pop the last dimension in case the coordinates are 3D
        for index, points in enumerate(coordinates):
            if type(points) == list:
                if len(points) == 3:
                    coordinates[index] = [points[0], points[1]]
        coordinates = convex_hull.graham_scan(coordinates)
        return coordinates
    else:
        raise Exception("The vector representaton could not be extracted from the file")



    
def getCRS(path):
    ''' gets all the coordinate reference systems from the geopackage (through a database connection) \n
    input "path": type string, file path to geopackage file \n
    returns the epsg code of the used coordinate reference system: type int, EPSG number of taken crs
    '''
    sqliteConnection = sqlite3.connect(path)
    if sqliteConnection is not None:
        c = sqliteConnection.cursor()

    if c is not None:
        crsid = []
        for row in c.execute('SELECT srs_name, gpkg_spatial_ref_sys.srs_id FROM gpkg_geometry_columns, gpkg_spatial_ref_sys where gpkg_spatial_ref_sys.srs_id ==  gpkg_geometry_columns.srs_id'):
            crsid.append(row[1])
        if len(crsid) > 0:
            countElements = hf.countElements(crsid)
            if len(countElements) == 1:
                return countElements[0][0]
            else:
                if len(crsid) > 0:
                    return crsid[0]
    with fiona.open(path) as datasetFiona:
        if 'crs' in datasetFiona.meta:
            if 'init' in datasetFiona.meta["crs"]:
               if ':' in  datasetFiona.meta["crs"]["init"]:
                    init = datasetFiona.meta["crs"]["init"]
                    return init[init.rfind(":")+1:]
    raise Exception("Crs could not be extracted.")
