import igraph as ig
import helpfunctions as hf

# Function name: extractMetadata
# Function purpose: gets called when the argument of the command request is a ISOxxx
# Input: whatMetadata, filePath
# Output: object metadata
def extractMetadata(filePath, whatMetadata):
        if whatMetadata=="s":
            metadaten = {}
            metadaten["Spatial Extent"] = extractSpatialExtentFromGML(filePath)
            return metadaten
        if whatMetadata=="t":
            metadaten = {}
            metadaten["Temporal Extent"] = extractTemporalExtentFromGML(filePath)
            return metadaten
        if whatMetadata=="e":
            metadaten = {}
            metadaten["BoundingBox"] = extractSpatialExtentFromGML(filePath)
            metadaten["StartTime-EndTime"] = extractTemporalExtentFromGML(filePath)
            metadaten["Shapetypes"] = extractShapeTypeFromGML(filePath)
            return metadaten
        else:
            metadaten = {}
            return metadaten

# Function name: extractSpatialExtentFromGML
# Function purpose: extracting the spatial extent from a gml-file
# Input: filePath
# Output: object g
def extractSpatialExtentFromGML(filePath):
    with open(filePath) as gml_file:
        g = {}
        Graph = ig.Graph.Read_GML(gml_file)
        g["Graph"] = Graph
        print(g)
        return g

# Function name: extractTemporalExtentFromGML
# Function purpose: extracting the temporal extent from a gml-file
# Input: filePath
# Output: 
def extractTemporalExtentFromGML(filePath):
    #todo
    return ""

# Function name: extractShapeTypeFromGML
# Function purpose: extracting the shape type from a gml-file
# Input: filePath
# Output:
def extractShapeTypeFromGML(filePath):
    #todo
    return ""

