import pandas as pd
import os
import numpy as np

from utils.utils import get_args

def overlap_coefficient(arr1, arr2, number_bins):
    """
    Calculate the overlap coefficient between two distributions.
    The overlap coefficient is defined as the area of the overlapping region divided by the area of the union.
    
    The overlap coefficient is calculated using the histogram method.
    
    Parameters
    ----------
    arr1 : array
        Array containing the first distribution.
    arr2 : array
        Array containing the second distribution.
    number_bins : int
        Number of bins to use for the histogram.
    
    Returns
    -------
    overlap_coeff : float
        Overlap coefficient between the two distributions.
    """

    # Determine the range over which the integration will occur
    min_value = min(np.min(arr1), np.min(arr2))
    max_value = max(np.max(arr1), np.max(arr2))
    
    # Calculate the histogram for each array
    hist_arr1, _ = np.histogram(arr1, bins=number_bins, range=(min_value, max_value))
    hist_arr2, _ = np.histogram(arr2, bins=number_bins, range=(min_value, max_value))

    normed_hist1 = hist_arr1 / len(arr1)
    normed_hist2 = hist_arr2 / len(arr2)
    
    # Calculate the overlap coefficient
    min_arr = np.minimum(normed_hist1, normed_hist2)
    overlap_coeff = np.sum(min_arr)
    
    return overlap_coeff

def main(params):

    class1_path = params['class1_path']
    class2_path = params['class2_path']
    output_path = params['output_path']
    index_list = params['index_list']
    n_bins = params['n_bins']

    class1_name = class1_path.split('/')[-1]
    class2_name = class1_path.split('/')[-1]

    data = {}
    
    for id, _ in enumerate(os.listdir(class1_path)):

        class1_df = pd.read_csv(class1_path + os.listdir(class1_path)[id])
        class2_df = pd.read_csv(class2_path + os.listdir(class2_path)[id])

        for index in index_list:

            class1_data = [value[0] for value in class1_df.filter(regex=f'^{index}', axis=1).values]
            class2_data = [value[0] for value in class2_df.filter(regex=f'^{index}', axis=1).values]

            if index not in data:
                data[index] = []

            results = overlap_coefficient(class1_data, class2_data, n_bins)
            
            data[index].append(results)

        print(id)
        
    out_df = pd.DataFrame(data)

    out_df.to_csv(output_path + f'{class1_name}_{class2_name}_OVL_{n_bins}_bins.csv', sep=',', index=False)

    return 0

if __name__ == '__main__':

    import json

    args = get_args()

    file = open('settings.json')

    params = json.load(file)

    main(params)