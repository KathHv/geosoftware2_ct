import fiona, gdal, xarray, sqlite3
import helpfunctions as hf


#gets called when the argument of the command request is a geopackage
def extractMetadata(filePath, whatMetadata):
    metadata = {}
    # gdal.Open not working
    try:
        with fiona.open(filePath) as datasetFiona:
            if whatMetadata == "e":
                metadata["filename"] = filePath[filePath.rfind("/")+1:filePath.rfind(".")]
                if datasetFiona.meta["driver"] is not None:
                    metadata["format"] = "application/" + str(datasetFiona.meta["driver"])
                else: metadata["format"] = "application/gpkg"
                metadata["shape_elements"] = len(datasetFiona)
                metadata["projection"] = datasetFiona.meta["crs"]["proj"]
                metadata["crs"] = str(datasetFiona.meta["crs"])
                metadata["encoding"] = datasetFiona.encoding
                metadata["used_ellipsoid"] = datasetFiona.crs["ellps"]
                geoTypes = []
                for shapeElement in datasetFiona:
                    geoTypes.append(shapeElement["geometry"]["type"])
                metadata["occurancy_shapetypes"] = hf.countElements(geoTypes)
                metadata["shapetype"] = datasetFiona.meta["schema"]["geometry"]
            if whatMetadata != "t":
                metadata["bbox"] = [datasetFiona.bounds[0], datasetFiona.bounds[1], datasetFiona.bounds[2], datasetFiona.bounds[3]]
    except:
        print("Exeption")
        pass
    
    
    sqliteConnection = sqlite3.connect(filePath)
    if sqliteConnection is not None:
        c = sqliteConnection.cursor()
    if c is not None:
        if 'crs' in metadata:
            crs = []
            for row in c.execute('SELECT table_name, srs_name, definition FROM gpkg_geometry_columns, gpkg_spatial_ref_sys where gpkg_spatial_ref_sys.srs_id ==  gpkg_geometry_columns.srs_id'):
                dict = {row[0]: {"crs_name": row[1], "description": row[2]}}
                crs.append(dict)
            if len(crs) > 0:
                metadata["crs"] = crs
        description = ""
        lats = []
        longs = []
        last_change = []
        for row in c.execute('SELECT table_name, description, last_change, min_x, min_y, max_x, max_y FROM gpkg_contents'):
            longs.extend([row[3], row[5]])
            lats.extend([row[4], row[6]])
            description += row[1] + " "
            last_change.append(row[2])
        if 'bbox' not in metadata:
            metadata["bbox"] = [min(longs), min(lats), max(longs), max(lats)]
        if 'description' not in metadata:
            if len(description) > 4:
                metadata["description"] = description
        if 'last_changed' not in metadata:
            metadata["last_changed"] = str(max(last_change))[:10]
        
    
    # TO DO: bbox in wgs84 + temporal extent
    
    return metadata

