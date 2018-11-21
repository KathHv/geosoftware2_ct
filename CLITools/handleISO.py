import igraph as ig
import helpfunctions as hf

#gets called when the argument of the command request is a ISOxxx
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

def extractSpatialExtentFromGML(filePath):
    with open(filePath) as gml_file:
        g = {}
        Graph = ig.Graph.Read_GML(gml_file)
        g["Graph"] = Graph
        return g

def extractTemporalExtentFromGML(filePath):
    #todo
    return ""

def extractShapeTypeFromGML(filePath):
    #todo
    return ""