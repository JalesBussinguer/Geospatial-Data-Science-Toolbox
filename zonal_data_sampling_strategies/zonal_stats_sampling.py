import numpy as np
import geopandas as gpd
import pandas as pd
import os

from rasterstats import zonal_stats

import argparse

def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--json',
    help='The input json file containing the preprocessing settings',
    type=str)

    args = parser.parse_args()

    return args

def sample_from_shape(shape, images_path, target_band_list, target_stats, outpath):

    image_list = os.listdir(images_path)

    for id, band in enumerate(target_band_list, start=1):

        df_stats = pd.DataFrame()

        for index, image in enumerate(image_list):

            date = image_list[index].split('T')[0] # Must be changed to match the raster's name pattern

            stats = zonal_stats(shape, images_path + image, band=id, nodata=np.nan, stats=target_stats)

            stats_df = pd.DataFrame(stats)
            stats_df['date'] = pd.to_datetime(int(date), format='%Y%m%d')
            df_stats = pd.concat([df_stats, stats_df])

            print(f'{band} - {date} data collected')

        df_stats = df_stats.reindex(index=df_stats.index[::-1])
        df_stats.reset_index(inplace=True, drop=True)
        df_stats.to_csv(outpath + band + '.csv', sep=',', index=False)

        print(f'{band} csv file saved!')

        return 0

def main(params):

    # Import the target shapes for sampling individually
    shape_to_sample = gpd.read_file(params['shape_to_sample'])

    images_path = params['images_path']

    target_band_list = params['target_band_list'] # Must be the exact same order as the bands in the raster

    target_stats = params['target_stats']

    outpath = params['outpath']

    sample_from_shape(shape_to_sample, images_path, target_band_list, target_stats, outpath)

    print('Sampling completed')

    return 0

if __name__ == "__main__":

    import json

    args = get_args()

    file = open('settings.json')

    params = json.load(file)

    main(params)
    
    
