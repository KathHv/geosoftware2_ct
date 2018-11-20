import sys, os, platform, datetime, math, shapefile, fiona, gdal, nio
from datetime import datetime as dtime
from six.moves import configparser
from netCDF4 import Dataset as NCDataset
import netCDF4
import getopt
from os import walk

#output of metadata object
def printObject(object):
    print("\n")
    for a,b in object.items():
        print(str(a) + ": " + str(b))
    print("\n")

#does a file with the relative path 'filename' exist locally?
def exists(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False

#compute an overall bbox from an array of bounding boxes
def computeBboxOfMultiple(bboxes):
    coordinate0 = 200
    coordinate1 = 200
    coordinate2 = -200
    coordinate3 = -200
    for x in bboxes:
        if x[0] < coordinate0:
            coordinate0 = x[0]
        if x[1] < coordinate1:
            coordinate1 = x[1]
        if x[2] > coordinate2:
            coordinate2 = x[2]
        if x[3] > coordinate3:
            coordinate3 = x[3]
    return [coordinate0, coordinate1, coordinate2, coordinate3]

#return the occurancies of all values in the array
def countElements(array):
    list = []
    for x in array:
            if [x, array.count(x)] not in list:
                list.append([x, array.count(x)])
    return list
     # looking for common attributes
    for metadataObject in metadataElements:
        if "bbox" in metadataObject:
            numberHavingAttribute[0] += 1
            bbox.append(metadataObject["bbox"])
        if "shapetype" in metadataObject:
            shapetypes.append(metadataObject["shapetype"])
            numberHavingAttribute[1] += 1
        if "shape_elements" in metadataObject:
            shapeElements += float(metadataObject["shape_elements"])
            numberHavingAttribute[2] += 1
        if "fileformat" in metadataObject:
            fileFormats.append(metadataObject["fileformat"])

    output = {}
    output["filetypes"] = countElements(fileFormats)
    if whatMetadata != 's' and whatMetadata != 't':
        # only taken into accound when ALL metadata is required
        output["number_files"] =  len(metadataElements)

        if not numberHavingAttribute[2] == 0:
            # shape elemnts
            output["average_number_shape_elements"] = str(shapeElements/float(numberHavingAttribute[2]))
            if numberHavingAttribute[2] != len(metadataElements):
                output["average_number_shape_elements"] += " WARNING: Only " + str(numberHavingAttribute[2]) + " Element(s) have this attribute"
        # shape types
        if numberHavingAttribute[1]: #ignore if no element has attribute
            output["occurancy_shapetypes"] = str(countElements(shapetypes))
            if numberHavingAttribute[1] != len(metadataElements):
                output["occurancy_shape_elements"] += " WARNING: Only " + str(numberHavingAttribute[1]) + " Element(s) have this attribute"
    
    # bounding box
    if numberHavingAttribute[0] == 0:
        if whatMetadata == "s": raise Exception("The system could not compute spatial metadata of files")
    elif whatMetadata != 't': 
        # not taken into account when temporal metadata is required
        output["bbox"] =  str(computeBboxOfMultiple(bbox))
        if numberHavingAttribute[0] != len(metadataElements):
            output["bbox"] += " WARNING: Only " + str(numberHavingAttribute[0]) + " Element(s) have this attribute"
    return output

#help-function to get all row elements for a specific string
def getAllRowElements(rowname,elements):
    for idx, val in enumerate(elements[0]):
        if  rowname in val:
            indexOf = idx
            values = []
            for x in elements:
                if x[indexOf] != rowname:
                    values.append(x[indexOf])
            return values

def searchForParameters(elements, paramArray):
    for x in paramArray:
        for row in elements[0]:
            if x in row:
                return getAllRowElements(x,elements)