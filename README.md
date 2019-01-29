# geosoftware2_ct

This is the Geosoftware project written by [@bennidietz](https://github.com/bennidietz), [@ipleis](https://github.com/ipleis), [@NiklasAsselmann](https://github.com/NiklasAsselmann), [@carojw](https://github.com/carojw) and [@KathHv](https://github.com/KathHv).

To install the CLI-Tools the required packages to install are [pip](https://pip.pypa.io/en/stable/) and [python](https://www.python.org):
Pip3 can be installed via the command line: 
`sudo apt-get install python3-pip`.
Python can be installed via command line with these [instructions](http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/)

### **HOW TO MAKE THE CLI-TOOLS WORK:**

1. Write the following Code Block in your terminal:
>`git clone https://github.com/KathHv/geosoftware2_ct.git`

>`cd geosoftware2_ct`

>`pip install -r requirements.txt`

>`cd CLITools`
2. Install GDAL: [https://www.gdal.org](https://www.gdal.org)
    - Download: http at download.osgeo.org
    - Choose CURRENT/
    - Choose gdal-2.4.0.tar.gz
    - Open Terminal and write
    - `./connect`
    - `make` (may take a while)
    - `sudo make install`
3. `python3 extract_metadata.py -h` to get all the command that are supported in our CLI-tool

### **Make the CLI-tools work with one command:**
(assuming [GDAL](https://www.gdal.org) is installed):

All CLITool impelementations can be found in the subfolders of the folder [CLITools](https://github.com/KathHv/geosoftware2_ct/tree/master/CLITools). 

##### extract Metadata:
The [extract_metadata.py-file](https://github.com/KathHv/geosoftware2_ct/blob/master/CLITools/metadataExtraction/extract_metadata.py) is just for extracting the bounding box, vector representation and temporal extent. The results will be printed.
    
`git clone https://github.com/KathHv/geosoftware2_ct.git && cd geosoftware2_ct && pip3 install -r requirements.txt && cd CLITools/metadataExtraction && python3 extract_metadata.py -h`
    
##### insert Entry:
The [insert_Entry.py-file](https://github.com/KathHv/geosoftware2_ct/blob/master/CLITools/transaction/insertEntry.py) inserts a given xml file with metadata to a given server. The entry will then be updated by extracting metadata form the given source file of the metadata.
   
`git clone https://github.com/KathHv/geosoftware2_ct.git && cd geosoftware2_ct && pip3 install -r requirements.txt && cd CLITools/transaction && python3 insertEntry.py -h`


##### update Entry:
The [update_Entry.py-file](https://github.com/KathHv/geosoftware2_ct/blob/master/CLITools/transaction/updateEntry.py) updates an Entry, identified by its id, with bounding box, vector representation and temporal extent, if available.
   
`git clone https://github.com/KathHv/geosoftware2_ct.git && cd geosoftware2_ct && pip3 install -r requirements.txt && cd CLITools/transaction && python3 updateEntry.py -h`

### Tests:
Tests can be found in the folder [Tests](https://github.com/bennidietz/geosoftware2_ct/tree/master/Tests) and can be executed with pytest.


### further documentation and links:
The CLI Tool is written to insert and update Entries of the database in the [pycsw Tool](https://github.com/KathHv/pycsw). 

The documentation to the base software "pycsw" can be found [here](http://docs.pycsw.org/en/latest/)

Our pycsw repository: [https://github.com/KathHv/pycsw](https://github.com/KathHv/pycsw)
