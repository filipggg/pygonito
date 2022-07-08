#!/usr/bin/env python3

"""coco2classes
This script helps with renaming annotation categories for gonito challenge.
It finds and prints all categories of annotation classes in coco .json files.

This file can also be imported as a module and contains the following
functions:

    * find_categories - Find all categories of annotation classes in coco files
    * main - the main function of the script
"""

import json
import argparse

parser = argparse.ArgumentParser(
    description='Find all categories of annotation classes in coco files')

parser.add_argument('coco_file', metavar='COCO_JSON_FILE', type=str, nargs='+',
                    help='JSON file with annotations')

def find_categories(filenames: "list of strings") -> dict:
    """Find all categories of annotation classes in coco files

    Parameters
    ----------
    filenames : list of strings
        List of coco files

    Returns
    -------
    list of strings
        List containing all categories of annotation classes
    """
    merged = {}
    for file in filenames:
        json_data = json.loads(open(file).read())
        categories = {}
        for item in json_data['categories']:
            categories[item['name']] = True
    merged.update(categories)
    return merged.keys()

def main(coco_files: "list of strings") -> None:
    merged = find_categories(coco_files)
    print(*merged, sep='\n')

if __name__ == '__main__':
    args = parser.parse_args()
    coco_files = args.coco_file
    main(coco_files)
