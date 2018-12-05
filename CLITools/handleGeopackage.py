import fiona, xarray, sqlite3
import helpfunctions as hf


#gets called when the argument of the command request is a geopackage
def extractMetadata(filePath, whatMetadata):
    metadata = {}
    # gdal.Open not working
    metadata = {}
    if whatMetadata == "e":
        addictionalMetadata = getAddictionalMetadata(filePath)
        for x in addictionalMetadata:
            metadata[x] = addictionalMetadata[x]

    if whatMetadata == "e" or whatMetadata == "s":
        metadata["bbox"] = getBoundingBox(filePath)
        metadata["crs"] = getCRS(filePath)
        metadata["vector_representation"] = getVectorRepresentation(filePath)

    return metadata
    
def getBoundingBox(path):
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
        for row in c.execute('SELECT min_x, min_y, max_x, max_y FROM gpkg_contents'):
            if not None in row:
                longs.extend([row[0], row[2]])
                lats.extend([row[1], row[3]])
        if len(longs) > 1 and len(lats) > 1:
            return [min(longs), min(lats), max(longs), max(lats)]

def getAddictionalMetadata(path):
    metadata = {}
    metadata["filename"] = path[path.rfind("/")+1:path.rfind(".")]
    metadata["path"] = path
    with fiona.open(path) as datasetFiona:
        if 'driver' in datasetFiona.meta:
            metadata["format"] = "application/" + str(datasetFiona.meta["driver"])
        else: metadata["format"] = "application/gpkg"
        metadata["shape_elements"] = len(datasetFiona)
        if 'crs' in datasetFiona.meta:
            if 'proj' in datasetFiona.meta["crs"]:
                metadata["projection"] = datasetFiona.meta["crs"]["proj"]
        metadata["encoding"] = datasetFiona.encoding
        if 'ellps' in datasetFiona.crs:
            metadata["used_ellipsoid"] = datasetFiona.crs["ellps"]
        geoTypes = []
        for shapeElement in datasetFiona:
            if 'geometry' in shapeElement:
                if shapeElement["geometry"] is not None:
                    if 'type' in shapeElement["geometry"]:
                        geoTypes.append(shapeElement["geometry"]["type"])
        metadata["occurancy_shapetypes"] = hf.countElements(geoTypes)
        if 'schema' in datasetFiona.meta:
            if 'geometry' in datasetFiona.meta["schema"]:
                metadata["shapetype"] = datasetFiona.meta["schema"]["geometry"]
    return metadata

def getVectorRepresentation(path):
    with fiona.open(path) as datasetFiona:
        coordinates = []
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
    return coordinates


def getCRS(path):
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
                return crsid
    with fiona.open(path) as datasetFiona:
        if 'crs' in datasetFiona.meta:
            if 'init' in datasetFiona.meta["crs"]:
               if ':' in  datasetFiona.meta["crs"]["init"]:
                    init = datasetFiona.meta["crs"]["init"]
                    return init[init.rfind(":")+1:]
