import os
from pathlib import Path
import pandas as pd
import geopandas as gpd

# Set up directory path
dirname = Path(__file__).parent

# Input Paths
data_22_path = "SAPS_data/sa_22_data.csv"
data_16_path = "SAPS_data/sa_16_data.csv"

attr_22_path = "SAPS_data/sa_22_attributes.csv"
attr_16_path = "SAPS_data/sa_16_attributes.csv"

geo_22_path = "SAPS_data/sa_22_geo.geojson"
geo_16_path = "SAPS_data/sa_16_geo.geojson"

# Output paths
merged_22_path = "SAPS_output/sa_22_merged.csv"
merged_16_path = "SAPS_output/sa_16_merged.csv"

geo_merged_22_path = "SAPS_output/sa_22_geo_merged.geojson"
geo_merged_16_path = "SAPS_output/sa_16_geo_merged.geojson"

# Create /SAPS_output/
if not os.path.exists(os.path.join(dirname, "SAPS_output/")):
    # if the demo_folder directory is not present
    # then create it.
    os.makedirs(os.path.join(dirname, "SAPS_output/"))

###################
# Preparing merge #
###################

# Read in data
data_22 = pd.read_csv(os.path.join(dirname, data_22_path))
data_16 = pd.read_csv(os.path.join(dirname, data_16_path))

attr_22 = pd.read_csv(os.path.join(dirname, attr_22_path))
attr_16 = pd.read_csv(os.path.join(dirname, attr_16_path))

geo_22 = gpd.read_file(os.path.join(dirname, geo_22_path))
geo_16 = gpd.read_file(os.path.join(dirname, geo_16_path))

print("Data read in.")

# Remove the prefix "SA2017_" from all GEOGID in data 16
data_16['GEOGID'] = data_16['GEOGID'].str.replace('SA2017_', '')

## Remove A prefix from GEOGID in geomety and attribute files
datasets = [
    (attr_22, 'SA_GEOGID_2022'),
    (geo_22, 'SA_GEOGID_2022'),
    (geo_16, 'GEOGID'),
    (attr_16, 'GEOGID')
]

for df, field in datasets:
    df[field] = df[field].str.replace('A', '', regex=False)

print("Files prepared for merge.")

#######################
# Merge Data with Attributes #
#######################
# This merge provides with CSVs that have geometry attributes (all the non-geometry columns  included in the boundary
# data, such as codes and names) and data. We merge on GEOGID as it is the only unique identifier - the 'Small Area'
# codes have exceptions for some reason.

# Merge data with attributes 2022
merged_22 = attr_22.merge(data_22, how='inner', left_on='SA_GEOGID_2022', right_on='GEOGID')

print(f"Attributes 2022 rows and columns: {attr_22.shape}")
print(f"Data 2022 rows and columns: {data_22.shape}")
print(f"Merged 2022 rows and columns: {merged_22.shape}")

# 1-1 Merge of attr_16 to data_22
merged_16 = attr_16.merge(data_16, how='inner', left_on='GUID', right_on='GUID')

print(f"Attributes 2016 rows and columns: {attr_16.shape}")
print(f"Data 2016 rows and columns: {data_16.shape}")
print(f"Merged 2016 rows and columns: {merged_16.shape}")

print("Data files merged with attribute files")

#######################
# Merge Geo with Data #
#######################
# This merge provides us with geojson files that have boundaries and data on each small area. All merges are 1-1, i.e.
# inner. We merge on GEOGID as it is the only unique identifier - the 'Small Area' codes have exceptions for some
# reason.

print("Merging geometry files with data files.")

# Merge geometry with data - 2022
geo_merged_22 = geo_22.merge(data_22, how='inner', left_on='SA_GEOGID_2022', right_on='GEOGID', suffixes=('_g','_d'))

print(f"Geometry 2022 rows and columns: {geo_22.shape}")
print(f"Data 2022 rows and columns: {data_22.shape}")
print(f"Merged Geometry 2022 rows and columns: {geo_merged_22.shape}")

# Merge geometry with data - 2016
geo_merged_16 = geo_16.merge(data_16, how='inner', left_on='GEOGID', right_on='GEOGID', suffixes=('_g','_d'))

print(f"Geometry 2016 rows and columns: {geo_16.shape}")
print(f"Data 2016 rows and columns: {data_16.shape}")
print(f"Merged Geometry 2016 rows and columns: {geo_merged_16.shape}")

print("Geometry files merged with data files.")

#######################
# Save output #
#######################
merged_16.to_csv(os.path.join(dirname, merged_16_path))
merged_22.to_csv(os.path.join(dirname, merged_22_path))

geo_merged_16.to_file(os.path.join(dirname, geo_merged_16_path), driver='GeoJSON')
geo_merged_22.to_file(os.path.join(dirname, geo_merged_22_path), driver='GeoJSON')

print(f"Merged files saved to {os.path.join(dirname,"/SAPS_output/")}")