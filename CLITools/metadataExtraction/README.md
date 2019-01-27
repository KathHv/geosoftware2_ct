# CLI Tool to extract metadata
This CLI Tool is to extract metadata from different file formats. The supported file formats are:
      .dbf .shp  .csv  .nc  .geojson .json .gpkg  .geotiff .tif .gml

The CLI Tool extracts the bounding box, the temporal extent, the vector representation and CRS of a file or of many files.
It transforms the bounding box and the vector representation to WGS84.

The temporal extent is given by two datetime objects in the format of YYYY-MM-DDTHH:MM:SS.ssZ after the iso-standard.


To get more information about the methods type in the command line 
`` python extract_metadata.py -h ``

1. extract_metadata.py covers all the CLI operations

2. helpfunctions.py include all helpfunctions for all python files assumed it could be useful for other python files as well

3. handle[Format].py files have the method extractMetadata and handle the extraction for the file format for all metadata (whatMetadata = "e"), the temporal Extent (whatMetadata = "t") and the spatial extent (whatMetadata = "s")


Using local (without installation)

In folder wih extract_metadata.py file:
`` python extract_metadata.py -e /path/to/file/or/folder``


Installation via pip
(coming soon)