# geosoftware2_ct

This is the Geosoftware project written by Benjamin Dietz, Ilka Pleiser, Niklas Aßelmann, Carolin Wortmann and Katharina Hovestadt.

To install pip just use the Terminal and type python get-pip.py. Then Visual Studio Code can use pip to install pylint.



### **HOW TO MAKE THE CLI-TOOLS WORK:**

1. Clone repo: `git clone https://github.com/KathHv/geosoftware2_ct.git`
2. `cd geosoftware2_ct`
3. `pip install -r requirements.txt`
4. `cd CLITools`
5. install GDAL: [https://www.gdal.org](https://www.gdal.org)
6. type `python3 extract_metadata.py -h` to get all the command that are supported in our CLI-tool

Make the CLI-tools work with one command (assuming that GDAL is installed):
`git clone https://github.com/KathHv/geosoftware2_ct.git && cd geosoftware2_ct && pip install -r requirements.txt && cd CLITools && python3 extract_metadata.py -h`