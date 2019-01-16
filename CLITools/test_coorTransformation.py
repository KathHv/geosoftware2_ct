import sys, os, platform, datetime, math, shapefile, fiona, gdal
from datetime import datetime as dtime
from six.moves import configparser
from netCDF4 import Dataset as NCDataset
import netCDF4
import getopt
from os import walk
import pyproj
import helpfunctions

'''
 Function purpose: testing whether function transforming SRS into WGS84
 (EPSG:4978; used by the GPS satellite navigation system) from an array
 input filepath: types array, string, point of two coordinates, proj(ektion)
 output: transformed coordinates 
'''
def test_tranformingIntoWGS84(point, proj):
    # original projection, any reference system
    p = pyproj.Proj(init=proj)
    # resulting projection, WGS84 (ESPG 4978), long, lat
    outProj =pyproj.Proj(init='epsg:4978')
    # x1,y1 = [-1902530.61073866, 3422503.38926134]    
    x1,y1 = point
    print(x1)
    print(y1)
    lon,lat,z = pyproj.transform(p,outProj,x1,y1,0)
    print(lon, lat, z)
    #(104.06918350995736, 53.539892485824495)

#>>> p1 = Proj(proj='latlong',datum='WGS84')
#>>> p2 = Proj(proj="utm",zone=10,datum='NAD27')

