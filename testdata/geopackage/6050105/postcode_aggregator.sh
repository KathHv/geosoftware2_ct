# GRASS commands for making postcode areas

v.voronoi input=postcodes@postcode output=pc_voronoi@postcode

v.dissolve input=pc_voronoi@postcode column=str_9 output=pc_area
v.dissolve input=pc_voronoi@postcode column=str_8 output=pc_district

v.overlay ainput=pc_area@postcode binput=GB_coast@postcode operator=and output=pc_area_clip
v.overlay ainput=pc_district@postcode binput=GB_coast@postcode operator=and output=pc_district_clip

v.db.renamecolumn map=pc_district_clip@postcode column=a_str_8,pc_district
v.db.renamecolumn map=pc_area_clip@postcode column=a_str_9,pc_area

db.dropcolumn -f table=pc_area_clip column=a_cat
db.dropcolumn -f table=pc_area_clip column=b_cat
db.dropcolumn -f table=pc_area_clip column=b_ID
db.dropcolumn -f table=pc_area_clip column=b_AREA
db.dropcolumn -f table=pc_area_clip column=b_PERIMETER
db.dropcolumn -f table=pc_area_clip column=b_ACRES
db.dropcolumn -f table=pc_district_clip column=a_cat
db.dropcolumn -f table=pc_district_clip column=b_cat
db.dropcolumn -f table=pc_district_clip column=b_ID
db.dropcolumn -f table=pc_district_clip column=b_AREA
db.dropcolumn -f table=pc_district_clip column=b_PERIMETER
db.dropcolumn -f table=pc_district_clip column=b_ACRES

