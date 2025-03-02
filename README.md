# SAPS_merge
Python code to merge SAPS geometry, attribute, and data files for 2011, 2016, and 2022.

This code outputs two merged datasets per boundary type per year: a merge of data and attributes and a merge of geometry and data. Note that the attribute file is just all the non-geometry columns included in the geometry file.

At the moment, this code only applies to 2016 and 2022 small areas. 2011 will be added once I find the ungeneralised small area geometry files - the files available on the CSO website appear to be generalised to 20m. Other geometries may be added as I need them, although hopefully the process is the same for each.

The attribute file (CSV) and geometry file (GeoJSON) for both years is downloaded from the Tailte Éireann Open Data Portal. I have named these 'sa_xx_geo' and 'sa_xx_attr'. 

The data file (CSV) is downloaded from the CSO SAPS website for the relevant year. See links to the relevant pages below:

[Attributes and Geometry 2022](https://data-osi.opendata.arcgis.com/datasets/osi::cso-small-areas-national-statistical-boundaries-2022-ungeneralised/about)

[Attributes and Geometry 2016](https://data-osi.opendata.arcgis.com/datasets/osi::small-areas-ungeneralised-national-statistical-boundaries-2015/about)

[Data 2022](https://www.cso.ie/en/census/census2022/census2022smallareapopulationstatistics/)

[Data 2016](https://www.cso.ie/en/census/census2016reports/census2016smallareapopulationstatistics/) 
