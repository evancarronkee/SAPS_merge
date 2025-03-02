import os
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Set up directory path
dirname = Path(__file__).parent

# Input Paths

files = [
    # Attribute files
    ("SAPS_data/sa_22_attributes.csv", "https://stg-arcgisazurecdataprodeu1.az.arcgis.com/exportfiles-3330-45/Small_Area_National_Statistical_Boundaries_2022_Ungeneralised_view_-3668709730578654347.csv?sv=2018-03-28&sr=b&sig=p0aG8dqCLfxPKxSAHiPr7pQKrD6JJ7%2BJh5UTCr%2Fn8Y0%3D&se=2025-03-02T15%3A47%3A27Z&sp=r"),
    ("SAPS_data/sa_16_attributes.csv", "https://stg-arcgisazurecdataprodeu1.az.arcgis.com/exportfiles-2209-783/Small_Areas_Ungeneralised_9151312312590699741.csv?sv=2018-03-28&sr=b&sig=OKbQiCDviU9Irlg1GnLsssTKV54DVBwdDAzPipBSo%2BE%3D&se=2025-03-02T16%3A00%3A45Z&sp=r"),

    # Geometry files
    ("SAPS_data/sa_22_geo.geojson", "https://stg-arcgisazurecdataprodeu1.az.arcgis.com/exportfiles-3330-45/Small_Area_National_Statistical_Boundaries_2022_Ungeneralised_view_8865831477585298158.geojson?sv=2018-03-28&sr=b&sig=8rjNSU%2BBgxtDW9NUA4FxRoijLl38ENgvtxwyN8b9n8E%3D&se=2025-03-02T16%3A03%3A54Z&sp=r"),
    ("SAPS_data/sa_16_geo.geojson", "https://stg-arcgisazurecdataprodeu1.az.arcgis.com/exportfiles-2209-783/Small_Areas_Ungeneralised_-8286096441100969232.geojson?sv=2018-03-28&sr=b&sig=4pYXCnCgawjZuVevJXALT56FyXKzyLPOPDXb98XRdf8%3D&se=2025-03-02T16%3A03%3A29Z&sp=r"),

    # Data files
    ("SAPS_data/sa_22_data.csv", "https://www.cso.ie/en/media/csoie/census/census2022/SAPS_2022_Small_Area_UR_171024.csv"),
    ("SAPS_data/sa_16_data.csv", "https://www.cso.ie/en/media/csoie/census/census2016/census2016boundaryfiles/SAPS2016_SA2017.csv")
]

def download_files(url, filename):
    print(f"Attempting to download: {filename}")

    response = requests.get(url, stream=True)

    # Check if the response is successful
    if response.status_code == 200:

        # Ensure the directory exists
        file_path = os.path.join(dirname, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Log file path
        print(f"Saving file to: {file_path}")

        # Write the file in chunks to avoid memory issues with large files
        with open(file_path, mode="wb") as file:
            for chunk in response.iter_content(chunk_size=1024):  # Download in chunks
                if chunk:
                    file.write(chunk)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download {filename}. Status code: {response.status_code}")

with ThreadPoolExecutor() as executor:
    executor.map(lambda p: download_files(p[1], p[0]), files)

print("All files downloaded")