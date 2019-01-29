'''
@author: Katharina Hovestadt, Niklas Asselmann, Benjamin Dietz
'''
import sys, os, getopt, datetime, errno, sqlite3, subprocess, uuid # important
from six.moves import configparser
from os import walk
import helpfunctions as hf
import threading 
import convex_hull

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
    if 'crs' in locals() and crs and bbox_in_orig_crs:
        bbox_transformed = hf.transformingArrayIntoWGS84(crs, bbox_in_orig_crs)
        return bbox_transformed
    else:
        raise Exception("The bounding box could not be related to a CRS")

def computeVectorRepresentationInWGS84(module, path):
    ''' input "module": type module, module from which methods shall be used \n
    input "path": type string, path to file \n
    returns a vector representation, type list, schema = [[lon1, lon2], [lon2, lon2], ...], that is in its original crs.
    '''
    crs = None
    vector_rep_in_orig_crs = module.getVectorRepresentation(path)
    try:
        crs = module.getCRS(path)
    except Exception as e:
        print("Exception in module.getCRS(path) in computeVectorRepresentationInWGS84(%s, %s): %s" % (module, path, e))

    if crs and vector_rep_in_orig_crs:
        vector_rep_transformed = hf.transformingArrayIntoWGS84(crs, vector_rep_in_orig_crs)
        return vector_rep_transformed
    else:
        raise Exception("The vector representation could not be related to a CRS.")




def extractMetadataFromFile(filePath, whatMetadata):
    ''' function is called when filePath is included in commanline (with tag 'e', 't' or 's')
    how this is done depends on the file format - the function calls the extractMetadataFrom<format>()-function \n
    input "filePath": type string, path to file from which the metadata shall be extracted \n
    input "whatMetadata": type string, specifices which metadata should be extracted  \n
    returns None if the format is not supported, else returns the metadata of the file as a dict 
    (possible) keys of the dict: 'temporal_extent', 'bbox', 'vector_reps', 'crs'
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
    elif fileFormat == 'xml':
        import handleXML
        usedModule = handleXML
    elif fileFormat == 'kml':
        import handleKML
        usedModule = handleKML
    else: 
        # file format is not supported
        return None
    #only extracts metadata if the file content is valid
    try:
        valid = usedModule.isValid(filePath)
    except Exception as e:
        print("Error for " + filePath + ": " + str(e))
        valid = False 
    #get Bbox, Temporal Extent, Vector representation and crs parallel with threads
    class thread(threading.Thread): 
        def __init__(self, thread_ID): 
            threading.Thread.__init__(self) 
            self.thread_ID = thread_ID
        def run(self):
            metadata["format"] = usedModule.DATATYPE
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
                    metadata["vector_rep"] = computeVectorRepresentationInWGS84(usedModule, filePath)
                except Exception as e:
                    print("Warning for " + filePath + ": " + str(e))
            
            elif self.thread_ID == 200:
                metadata["bbox"] = computeBboxInWGS84(usedModule, filePath)
            elif self.thread_ID == 201:
                metadata["temporal_extent"] = usedModule.getTemporalExtent(filePath)
            elif self.thread_ID == 202:
                metadata["vector_rep"] = computeVectorRepresentationInWGS84(usedModule, filePath)
            
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
    
    if valid:
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
    else:
                raise Exception("The file " + str(filePath) + " could not be validated")
        
    return metadata




def extractMetadataFromFolder(folderPath, whatMetadata):
    '''function is called when path of directory is included in commanline (with tag 'e', 't' or 's') \n
    calls the extractMetadataFromFile-function and computes the average for the metadata fields
    (possible) keys of the returning dict: 'temporal_extent', 'bbox', 'vector_reps' \n
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
        metadataElements = []
        fullPaths = []

        for x in files_in_folder:
            fullPaths.append(str(os.path.join(folderPath, x)))
        
        filesSkiped = 0
        bboxes = []
        temporal_extents = []
        vector_reps = []

        # handle each of the files in the folder seperately
        # get metadata fields 'bbox', 'vector_rep', 'temporal_extent' of all supported files
        for x in fullPaths:
            try:
                metadataOfFile = extractMetadataFromFile(x, "e")
                if metadataOfFile is not None:
                    metadataElements.append(metadataOfFile)
                    if 'bbox' in metadataOfFile:
                        if metadataOfFile["bbox"] is not None:
                            bboxes.append(metadataOfFile["bbox"])
                    if 'vector_rep' in metadataOfFile:
                        if metadataOfFile["vector_rep"] is not None:
                            vector_reps.append(metadataOfFile["vector_rep"]) # TO DO: here all the coors should be appended later
                    if 'temporal_extent' in metadataOfFile:
                        if metadataOfFile["temporal_extent"] is not None:
                            temporal_extents.append(metadataOfFile["temporal_extent"]) 
                else:
                    # fileformat is not supported
                    filesSkiped = filesSkiped + 1            
            except Exception as e:
                print("Warning for " + str(x) + ": "+ str(e))
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
        print("There are " + str(len(mult_vec_rep)) + " extracted coordinate pairs out of " + str(len(fullPaths)-filesSkiped) + " file(s).")
        if type(mult_vec_rep) == list:
            if len(mult_vec_rep) > 0:
                return convex_hull.graham_scan(mult_vec_rep)

        return None

    bbox = getBboxFromFolder(bboxes)
    if(type(vector_reps) == list):
        if(len(vector_reps) is not 0):    
            if type(vector_reps[0] == list):
                if type(vector_reps[0][0] == list):
                    vector_reps_help = []
                    for elem1 in vector_reps:
                        for elem2 in elem1:
                            vector_reps_help.append(elem2)
                    vector_reps = vector_reps_help
    vector_rep = getVectorRepFromFolder(vector_reps)
    temp_ext = getTemporalExtentFromFolder(temporal_extents)

    if whatMetadata == "e":
        
        if bbox is not None:
            metadata["bbox"] = bbox
        
        if vector_rep is not None:
            metadata["vector_rep"] = vector_rep
        
        if temp_ext is not None:
            metadata["temporal_extent"] = temp_ext

    
    if whatMetadata == "s":
        # raise exception if one of the metadata fields 'bbox' or 'vector_represenation' could not be extracted from the folder    
        if bbox is not None and vector_rep is not None:
            metadata["bbox"] = bbox
            metadata["vector_rep"] = vector_rep

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
