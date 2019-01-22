'''
@author: Katharina Hovestadt, Niklas Asselmann, Benjamin Dietz
'''

import sys, os, getopt, datetime, errno, sqlite3, subprocess, uuid # important
from six.moves import configparser
from os import walk
import helpfunctions as hf
import dicttoxml, xml, subprocess
import threading 
import convex_hull


COMMAND = None
XML_DIRPATH = None
CFG = None
RECURSIVE = False
OUTPUT_FILE = None
CSW_URL = None
XML = None
XSD = None
TIMEOUT = 30
FORCE_CONFIRM = False

# the capabilities of our CLI
def usage():
    """Provide usage instructions"""
    return '''
        NAME
            cli.py 

        SYNOPSIS
            cli.py -e </absoulte/path/to/record>|</absoulte/path/to/directory>
            cli.py -s </absoulte/path/to/record>|</absoulte/path/to/directory>
            cli.py -t </absoulte/path/to/record>|</absoulte/path/to/directory>

            Supported formats:

                    .dbf     |
                    .shp     | temporal extent is not available
                    .csv     |
                    .nc      |
                    .geojson |
                    .json    |
                    .gpkg    | temporal extent is not vaialable
                    .geotiff |
                    .tif     |
                    .gml     |


            Available options:

            -e    Extract all metadata of a geospatial file
            -s    Extract all spatial metadata of a geospatial file
            -t    Extract all temporal metadata of a geospatial file
  
            
            Available temporal metadata:
            
                [starting point, endpoint]
            
            Available spatial metadata:

                bbox
'''

def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())

if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)

try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'e:s:t:ho:')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    #sys.exit(2)

if 'OPTS' in globals(): 
    if len(OPTS) == 0:
        errorFunction()




def computeBboxInWGS84(module, path):
    ''' input "module": type module, module from which methods shall be used \n
    input "path": type string, path to file \n
    returns a bounding box, type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)], the boudning box has either its original crs or WGS84 (transformed).
    '''
    
    bbox_in_orig_crs = module.getBoundingBox(path)
    try:
        crs = module.getCRS(path)
    except:
        pass
    if 'crs' in locals() and crs is not None:
        print(bbox_in_orig_crs)

        bbox_transformed = hf.transformingArrayIntoWGS84(crs, bbox_in_orig_crs)
        return bbox_transformed
    else:
        raise Exception("The bounding box could not be related to a CRS")

def computeVectorRepresentationInWGS84(module, path):
    ''' input "module": type module, module from which methods shall be used \n
    input "path": type string, path to file \n
    returns a vector representation, type list, schema = [[lon1, lon2], [lon2, lon2], ...], that is in its original crs.
    '''
    
    vector_rep_in_orig_crs = module.getVectorRepresentation(path)
    try:
        crs = module.getCRS(path)
    except Exception as e:
        print("Exception in module.getCRS(path) in computeVectorRepresentationInWGS84(%s, %s): %s" % (module, path, e))
    if 'crs' in locals() and crs is not None:
        for x in vector_rep_in_orig_crs:
            print(crs, vector_rep_in_orig_crs)
            vector_rep_transformed = hf.transformingArrayIntoWGS84(crs, vector_rep_in_orig_crs)
            return vector_rep_transformed
    else:
        raise Exception("The vector representation could not be related to a CRS")




def extractMetadataFromFile(filePath, whatMetadata):
    ''' function is called when filePath is included in commanline (with tag 'e', 't' or 's')
    how this is done depends on the file format - the function calls the extractMetadataFrom<format>()-function \n
    input "filePath": type string, path to file from which the metadata shall be extracted \n
    input "whatMetadata": type string, specifices which metadata should be extracted  \n
    returns None if the format is not supported, else returns the metadata of the file as a dict 
    (possible) keys of the dict: 'temporal_extent', 'bbox', 'vector_representations', 'crs'
    '''
    
    fileFormat = filePath[filePath.rfind('.')+1:]
    usedModule = None

    # initialization of later output dict
    metadata = {}

    # first get the module that will be called (depending on the format of the file)
    if fileFormat == 'shp' or fileFormat == 'dbf':
        import handleShapefile
        usedModule = handleShapefile
    elif fileFormat == 'csv':
        import handleCSV
        usedModule = handleCSV
    elif fileFormat == 'nc':
        import handleNetCDF
        usedModule = handleNetCDF
    elif fileFormat == 'geojson' or fileFormat == 'json':
        import handleGeojson
        usedModule = handleGeojson
    elif fileFormat == 'gpkg':
        import handleGeopackage
        usedModule = handleGeopackage
    elif fileFormat == 'geotiff' or fileFormat == 'tif':
        import handleGeotiff
        usedModule = handleGeotiff
    elif fileFormat == 'gml':
        import handleGML
        usedModule = handleGML
    elif fileFormat =='xml':
        import handleXML
        usedModule = handleXML
    elif fileFormat == 'kml':
        import handleKML
        usedModule = handleKML
    else: 
        # file format is not supported
        return None
    #get Bbox, Temporal Extent, Vector representation and crs parallel with threads
    class thread(threading.Thread): 
        def __init__(self, thread_ID): 
            threading.Thread.__init__(self) 
            self.thread_ID = thread_ID
        def run(self):
          
            #only extracts metadata if the file content is valid
            try:
                valid = usedModule.isValid(filePath)
            except Exception as e:
                print("Error for " + filePath + ": " + str(e))
                valid = False 
            if valid:
                print("Thread with Thread_ID " +  str(self.thread_ID) + " now running...")
                #metadata[self.thread_ID] = self.thread_ID
                if self.thread_ID == 100:
                    try:
                        metadata["bbox"] = computeBboxInWGS84(usedModule, filePath)
                    except Exception as e:
                        print("Warning for " + filePath + ": " + str(e)) 
                elif self.thread_ID == 101:
                    try:
                        metadata["temporal_extent"] = usedModule.getTemporalExtent(filePath)
                    except Exception as e:
                        print("Warning for " + filePath + ": " + str(e))
                elif self.thread_ID == 102:
                    try:
                        metadata["vector_representation"] = computeVectorRepresentationInWGS84(usedModule, filePath)
                    except Exception as e:
                        print("Warning for " + filePath + ": " + str(e))
                elif self.thread_ID == 200:
                    metadata["bbox"] = computeBboxInWGS84(usedModule, filePath)
                elif self.thread_ID == 201:
                    metadata["temporal_extent"] = usedModule.getTemporalExtent(filePath)
                elif self.thread_ID == 202:
                    metadata["vector_representation"] = usedModule.getVectorRepresentation(filePath)
                elif self.thread_ID == 103:
                    try:
                        # the CRS is not neccessarily required
                        if hasattr(usedModule, 'getCRS'):
                            metadata["crs"] = usedModule.getCRS(filePath)
                        else: print ("Warning: The CRS cannot be extracted from the file")
                    except Exception as e:
                        print("Warning for " + filePath + ": " + str(e))      
            try:
                barrier.wait()
            except Exception as e:
                print("Warning for " + filePath + ": " + str(e))
                barrier.abort()

            
    #thread id 100+ -> metadata extraction with exceptions from methods (raise Exception)
    #thread id 200+ -> metadata extraction without exceptions from methods ( only standard exceptions are raised (e.g. ValueError, AttributeError))
    thread_bbox_except = thread(100) 
    thread_temp_except = thread(101) 
    thread_vector_except = thread(102)
    thread_crs_except = thread(103)
    thread_bbox = thread(200) 
    thread_temp = thread(201) 
    thread_vector = thread(202) 

    if whatMetadata == "e":
        # none of the metadata field is required 
        # so the system does not crash even if it does not find anything
        barrier = threading.Barrier(5)
        thread_bbox_except.start() 
        thread_temp_except.start() 
        thread_vector_except.start() 
        thread_crs_except.start()
        barrier.wait() 
        barrier.reset() 
        barrier.abort() 
        
    if whatMetadata == "s":
        # only spatial extent is required
        # if one of the metadata field could not be extrated, the system crashes
        barrier = threading.Barrier(4)
        thread_bbox.start()
        thread_vector.start()
        thread_crs_except.start()
        barrier.wait()
        barrier.reset() 
        barrier.abort() 

    if whatMetadata == "t":
        # only temporal extent is required
        # if one of the metadata field could not be extracted, the system crashes
        barrier = threading.Barrier(2)
        thread_temp.start()
        barrier.wait()
        barrier.reset() 
        barrier.abort() 
    
    return metadata




def extractMetadataFromFolder(folderPath, whatMetadata):
    '''function is called when path of directory is included in commanline (with tag 'e', 't' or 's') \n
    calls the extractMetadataFromFile-function and computes the average for the metadata fields
    (possible) keys of the returning dict: 'temporal_extent', 'bbox', 'vector_representations' \n
    input "folderPath": type string, path to folder from which the metadata shall be extracted \n
    input "whatMetadata": type string, specifices which metadata should be extracted  \n
    returns the metadata of the folder as a dict \n
    '''
    if not os.path.isdir(folderPath):
        raise FileNotFoundError("This directory could not be found")
    else:
        # initialization of later output dict
        metadata = {}

        files_in_folder = []

        # get all files from the folder
        for (dirpath, dirnames, filenames) in walk(folderPath):
            files_in_folder.extend(filenames)
        # for shapefile: ignore all .prj-, .dbf-, .shx- and cpg-files where a related .shp-file exists
        # so that the same shapefile is only executed once
        i = 0
        while (i < len(files_in_folder)):
            pathWithoutEnding = files_in_folder[i][:len(files_in_folder[i])-4]
            if '.cpg' in files_in_folder[i] or '.prj' in files_in_folder[i] \
                or '.shx' in files_in_folder[i] or '.dbf' in files_in_folder[i]:
                if pathWithoutEnding + ".shp" in files_in_folder:
                    files_in_folder.remove(files_in_folder[i])
                else:
                    i += 1
            else:
                i += 1
        print(files_in_folder)
        metadataElements = []
        fullPaths = []

        for x in files_in_folder:
            fullPaths.append(str(os.path.join(folderPath, x)))
        
        filesSkiped = 0
        bboxes = []
        temporal_extents = []
        vector_representations = []

        # handle each of the files in the folder seperately
        # get metadata fields 'bbox', 'vector_representation', 'temporal_extent' of all supported files
        for x in fullPaths:
            metadataOfFile = extractMetadataFromFile(x, "e")
            if metadataOfFile is not None:
                metadataElements.append(metadataOfFile)
                if 'bbox' in metadataOfFile:
                    if metadataOfFile["bbox"] is not None:
                        bboxes.append(metadataOfFile["bbox"])
                if 'vector_representation' in metadataOfFile:
                    if metadataOfFile["vector_representation"] is not None:
                        vector_representations.append(len(metadataOfFile["vector_representation"])) # TO DO: here all the coors should be appended later
                if 'temporal_extent' in metadataOfFile:
                    if metadataOfFile["temporal_extent"] is not None:
                        temporal_extents.append(metadataOfFile["temporal_extent"]) 
            else:
                # fileformat is not supported
                filesSkiped += 1


    def getTemporalExtentFromFolder(mult_temp_extents):
        ''' computes temporal extent from multiple temporal extents stored in the array 'mult_temp_extents' (uses helpfunction) \n
        input "mult_temp_extents": type list, list of list with temporal extent with length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1] \n
        returns temporal extent of all files, type list with two datetime
        '''
        print(str(len(mult_temp_extents)) + " of " + str(len(fullPaths)-filesSkiped) + " supported Files have a temporal extent.")

        if len(mult_temp_extents) > 0 and hf.computeTempExtentOfMultiple(mult_temp_extents) is not None:
            return hf.computeTempExtentOfMultiple(mult_temp_extents)

        else: return None

    def getBboxFromFolder(mult_bboxes):
        ''' computes boundingbox from multiple bounding boxes stored in the array 'mult_bboxes' (uses helpfunction) \n
        input "mult_bboxes": type list, list with bounding boxes, one bbox has the following format:  length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] \n
        returns bounding box of the files in the folder, type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)], the boudning box has either its original crs or WGS84 (transformed).
        '''
        print(str(len(mult_bboxes)) + " of " + str(len(fullPaths)-filesSkiped) + " supported Files have a bbox.")
        
        if len(mult_bboxes) > 0 and hf.computeBboxOfMultiple(mult_bboxes) is not None:
            return hf.computeBboxOfMultiple(mult_bboxes)

        else: return None

    def getVectorRepFromFolder(mult_vec_rep):
        '''
        computes vector representation from multiple vector representations stored in the array 'mult_vec_rep' (uses helpfunction) \n
        input "mult_vec_rep": type list, all vector representations from the files in the folder \n
        returns the vector representation of the files in the folder: type list, one vector representation of the files from folder
        '''
        print(str(len(mult_vec_rep)) + " of " + str(len(fullPaths)-filesSkiped) + " supported Files have a vector representation.")
        if type(mult_vec_rep) == list:
            if len(mult_vec_rep) > 0:
                return convex_hull.graham_scan(mult_vec_rep)

        return None

    bbox = getBboxFromFolder(bboxes)
    vector_rep = getVectorRepFromFolder(vector_representations)
    temp_ext = getTemporalExtentFromFolder(temporal_extents)

    if whatMetadata == "e":
        
        if bbox is not None:
            metadata["bbox"] = bbox
        
        if vector_rep is not None:
            metadata["vector_representation"] = vector_rep
        
        if temp_ext is not None:
            metadata["temporal_extent"] = temp_ext
    

    
    if whatMetadata == "s":
        # raise exception if one of the metadata fields 'bbox' or 'vector_represenation' could not be extracted from the folder    
        if bbox is not None and vector_rep is not None:
            metadata["bbox"] = bbox
            metadata["vector_representation"] = vector_rep

        else: raise Exception("A spatial extent cannot be computed out of any file in this folder")

    if whatMetadata == "t":
        # raise exception if the temporal extent could not be extracted from the folder
        if temp_ext is not None:
            metadata["temporal_extent"] = temp_ext

        else: raise Exception("A temporal extent cannot be computed out of any file in this folder")
        
    if filesSkiped != 0: 
        print(str(filesSkiped) + ' file(s) has been skipped as its format is not supported; to see the supported formats look at -help')
    if len(fullPaths) - filesSkiped == 0:
        raise Exception("None of the files in the dictionary are supported.")
    
    return metadata



#process arguemnts from command line
if 'OPTS' not in globals():
    raise Exception("An Argument is required")

for o, a in OPTS:
    '''
    tells the program what to do with certain tags and their attributes that are
    inserted over the command line
    '''
    ending = a
    if "/" in a:
        ending = a[a.rfind("/")+1:]
    

    #extracts spatial and temporal metadata and also the vector representation
    if o == '-e':
        COMMAND = a
        print("Extract all metadata:\n")
        if '.' in ending:
            # handle it as a file
            output = extractMetadataFromFile(a, 'e')
            if output is None:
                raise Exception("This file format is not supported")
        else:
            # handle it as a folder
            output = extractMetadataFromFolder(a, 'e')


    #extract only temporal metadata
    elif o == '-t':
        print("\n")
        print("Extract Temporal metadata only:\n")
        COMMAND = a
        if '.' in ending:
            # handle it as a file
            output = extractMetadataFromFile(a, 't')
            if output is None:
                raise Exception("This file format is not supported")
        else:
            # handle it as a folder
            output = extractMetadataFromFolder(a, 't')


    #extract only spatial metadata    
    elif o == '-s':
        print("\n")
        print("Extract Spatial metadata only:\n")
        COMMAND = a
        if '.' in ending:
            # handle it as a file
            output = extractMetadataFromFile(a, 's')
            if output is None:
                raise Exception("This file format is not supported")
        else:
            # handle it as a folder
            if os.path.isdir(a):
                output = extractMetadataFromFolder(a, 's')
            else:
                raise Exception("The path is not a valid folder or file")

    elif o == '-h':  # dump help and exit
        print(usage())
        sys.exit(3)
        
    # print output differently depending on the outputs type
    if 'output' in globals():
        if type(output) == list or type(output) == dict:
            hf.printObject(output)
        else: print(output)
