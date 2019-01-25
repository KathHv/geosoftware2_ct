# geosoftware2_ct

This is the Geosoftware project written by [@bennidietz](https://github.com/bennidietz), [@ipleis](https://github.com/ipleis), [@NiklasAsselmann](https://github.com/NiklasAsselmann), [@carojw](https://github.com/carojw) and [@KathHv](https://github.com/KathHv).

To install our CLI-Tools the required packages to install are [pip](https://pip.pypa.io/en/stable/) and [python](https://www.python.org).



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
  
`git clone https://github.com/KathHv/geosoftware2_ct.git && cd geosoftware2_ct && pip install -r requirements.txt && cd CLITools && python3 extract_metadata.py -h`

All CLITool impelementations can be found in the folder [CLITools](https://github.com/bennidietz/geosoftware2_ct/tree/master/CLITools). The [extract_metadata.py-file](https://github.com/bennidietz/geosoftware2_ct/blob/master/CLITools/extract_metadata.py) is the only file that is intended to be executed.

Tests can be found in the folder [Tests](https://github.com/bennidietz/geosoftware2_ct/tree/master/Tests) and can be executed with pytest


Our pycsw repository: [https://github.com/KathHv/pycsw](https://github.com/KathHv/pycsw)