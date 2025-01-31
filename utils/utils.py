import argparse

def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--json',
    help='The input json file containing the preprocessing settings',
    type=str)

    args = parser.parse_args()

    return args