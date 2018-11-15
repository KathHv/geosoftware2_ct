# ----------------------------
# ----------------------------
# Postcode aggregator
# ----------------------------
# ----------------------------

library(tidyverse)

df = read_csv("~/GIS/OS/postcode.csv")

df = df %>% 
   mutate(pc_district = str_sub(Postcode, 1, nchar(Postcode)-3)) %>% 
   mutate(pc_district = trimws(pc_district)) %>% 
   mutate(pc_area = gsub('[0-9]+', '', pc_district)) %>% 
   mutate(pc_area = str_sub(pc_area, 1, 2))

write_csv(df, "~/GIS/OS/postcode_extra.csv")

