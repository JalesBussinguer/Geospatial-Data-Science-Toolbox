"""
Script that downloads Wyvern Dragonette data from its open data portal.

It also downloads the metadata on a json file.
"""

import requests
import time
import json
import os

stac_item = "https://wyvern-prod-public-open-data-program.s3.ca-central-1.amazonaws.com/product-type/extended/wyvern_dragonette-003_20241229T165203_12324bcb/wyvern_dragonette-003_20241229T165203_12324bcb.json"

root_path = 'E:/'

stac_item_response = requests.get(stac_item)
stac_item_response.raise_for_status()  # Will raise an error if we have any issues getting the STAC item
stac_item = stac_item_response.json()
print(f"Successfully loaded STAC Item!\nSTAC Item ID: {stac_item['id']}")

download_url = stac_item["assets"]["Cloud optimized GeoTiff"]["href"]
local_file_name = download_url.split("/")[-1]

local_folder_name = local_file_name.split('.')[0] # naming the folder as the same name of the file (minus the file extension)

local_metadata_name = f'{local_folder_name}_metadata.json'

# Check if the folder exists 
if not os.path.exists(root_path + local_folder_name):
    os.makedirs(root_path + local_folder_name)
    # The existence of the folder means that the image was already targeted to download before, but somthing happened and the download was not completed

# Check if the image metadata already exists

if not os.path.exists(f'{root_path}{local_folder_name}/{local_metadata_name}'):
    with open(f'{root_path}{local_folder_name}/{local_metadata_name}', 'w') as file:
        json.dump(stac_item, file, indent=4, sort_keys=True)

# Check if the image data was already downloaded
if not os.path.exists(f'{root_path}{local_folder_name}/{local_file_name}'):
    
    download_path = f'{root_path}{local_folder_name}/{local_file_name}'

    print(f'Downloading {local_file_name} bands...')

    t1 = time.time()

    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(download_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    t2 = time.time()

    print(f'Downloaded {local_file_name} bands in {round(t2-t1, 2)} seconds')

else:

    print(f'File: {local_file_name} already exists!')