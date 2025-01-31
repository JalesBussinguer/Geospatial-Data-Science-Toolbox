import numpy as np
import pandas as pd
import os
import argparse

from utils.utils import get_args

def jm_distances_normal(set_1, set_2):
    """
    Implements the Jeffries-Matusita distance between two normal distributions.

    Inputs:
        set_1: a list or array of numbers
        set_2: a list or array of numbers

    Outputs:
        jm_dist: the Jeffries-Matusita distance between set_1 and set_2
    """

    # The mean and standard deviation of the two sets
    set_1_mean = np.mean(set_1)
    set_2_mean = np.mean(set_2)
    
    set_1_std = np.std(set_1)
    set_2_std = np.std(set_2)

    # The variance of the two sets (sigma^2)
    sigma_1 = np.power(set_1_std, 2)
    sigma_2 = np.power(set_2_std, 2)

    # The Bhattacharyya distance between two normal distributions
    b_dist = 0.25 * np.log(0.25 * (sigma_1/sigma_2) + (sigma_1/sigma_2) + 2) + 0.25 * ((set_1_mean-set_2_mean)**2 / sigma_1 + sigma_2)

    # Jeffries-Matusita distance
    jm_dist = np.sqrt(2 * (1 - np.exp(-b_dist)))
    
    return jm_dist

def main(params):
        
    class1_path = params['class1_path']
    class2_path = params['class2_path']
    output_path = params['output_path']

    class1_name = class1_path.split('/')[-1]
    class2_name = class1_path.split('/')[-1]

    class1_list = os.listdir(class1_path)
    class2_list = os.listdir(class2_path)
        
    index_list = ['DpRVI', 'PRVI','DPSVI', 'DPSVIm', 'RVI']

    data = {}

    for i in range(len(class1_list)):

        class1_df = pd.read_csv(class1_path + class1_list[i])
        class2_df = pd.read_csv(class2_path + class2_list[i])

        for index in index_list:
            
            class1 = class1_df.filter(regex=f'^{index}', axis=1).values
            class2 = class2_df.filter(regex=f'^{index}', axis=1).values

            if index not in data:
                data[index] = []

            jm_dist = jm_distances_normal(class1, class2)

            data[index].append(jm_dist)
        
        print(f'test {i} done!')

    result = pd.DataFrame(data)

    result.to_csv(output_path + f'{class1_name}_{class2_name}_jm_dists.csv', sep=',', index=False)

    return 0

if __name__ == "__main__":

    import json

    args = get_args()

    file = open('settings.json')

    params = json.load(file)

    main(params)
