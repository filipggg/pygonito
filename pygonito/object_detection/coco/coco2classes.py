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
parser.add_argument('-o', '--output', metavar='OUTPUT', type=str, nargs='?',
                    help='run in interactive renaming mode to output rename file',
                    const='classes_out')


def find_categories(filenames: "list of strings") -> "list of strings":
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

def rename(old_names: "list of strings") -> dict:
    new_names = {}
    for item in old_names:
        name = ''
        name = input(f'rename: {item}\n')
        if name == '':
            new_names[item] = item
        else:
            new_names[item] = name
    return new_names

def json_output(dictionary, output):
    # json_object = json.dumps(dictionary, indent = 4)
    with open(f"{output}.json", "w", encoding="UTF-8") as f:
    #     f.write(json_object)
        json.dump(dictionary, f, ensure_ascii=False, indent = 4)


def main(coco_files: "list of strings", output: str = None) -> None:
    merged = find_categories(coco_files)
    print(*merged, sep='\n')
    if output:
        dict = rename(merged)
        json_output(dict, output)

if __name__ == '__main__':
    args = parser.parse_args()
    coco_files = args.coco_file
    output = args.output
    print(output)
    main(coco_files, output)
