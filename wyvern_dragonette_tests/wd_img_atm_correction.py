import json
import rasterio
import dateutil.parser
import numpy as np

input_img_path = 'E:/wyvern_dragonette-003_20241229T165203_12324bcb/wyvern_dragonette-003_20241229T165203_12324bcb.tiff'
metadata_path = 'E:/wyvern_dragonette-003_20241229T165203_12324bcb/wyvern_dragonette-003_20241229T165203_12324bcb_metadata.json'

output_img_path = 'E:/wyvern_dragonette-003_20241229T165203_12324bcb/wyvern_dragonette-003_20241229T165203_12324bcb_TOA.tiff'

# Open the Dragonette image
with rasterio.open(input_img_path) as src:
    image_toa_radiance = src.read()
    nodata_value = src.nodata
    profile = src.meta.copy()

image_toa_radiance[image_toa_radiance == nodata_value] = np.nan

# Open metadata.json file
try:
    with open(metadata_path, 'r') as file:
        metadata = json.load(file)
    print(f"Image {input_img_path} metadata loaded succesfully!")
except FileNotFoundError:
    print(f"Error: File '{metadata_path}' not found.")
except json.JSONDecodeError:
    print(f"Error: File '{metadata_path}' content is not a valid JSON.")
except Exception as e:
    print(f"A unnexpected error occurred: {str(e)}")

properties = metadata['properties']
band_data = metadata['assets']['Cloud optimized GeoTiff']['eo:bands']
collection_datetime = dateutil.parser.parse(properties['datetime'])
collection_day_of_year = int(collection_datetime.strftime("%j"))

sun_earth_distance = 1 - (0.01672 * np.cos(np.deg2rad(0.9856 * (collection_day_of_year - 4))))

sun_elevation = properties['view:sun_elevation']

# Prepare arrays for vectorized operations
solar_illumination = np.array([band['solar_illumination'] for band in band_data])
sin_sun_elevation = np.sin(np.deg2rad(sun_elevation))

# Calculate the scaling factor
scaling_factor = np.pi * (sun_earth_distance ** 2) / (solar_illumination[:, None, None] * sin_sun_elevation)

# Apply the scaling factor to each band using vectorized operation
image_toa_reflectance = image_toa_radiance * scaling_factor

print('TOA reflection image calculated! Writing...')

band_names = [band['name'] for band in band_data]

# Write the output image
with rasterio.open(output_img_path,'w',**profile) as dst:
    for i in range(image_toa_reflectance.shape[0]):
        dst.write(image_toa_reflectance[i, :, :], i + 1)
        dst.set_band_description(i+1, band_names[i])

    dst.nodata = nodata_value
    dst.close()

print(f"Image TOA Reflectance saved successfully at: {output_img_path}")