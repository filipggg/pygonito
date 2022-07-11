#!/usr/bin/env python3

"""coco2gonito

This script reformat coco annotations into gonito format, split them into
train/dev/test with stable md5 split. It can also sorts data inside
train/dev/test with stable md5 sort. It is assumed that the challenge dir has
been initialized.
This tool accepts coco .json files.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * sorter - sorts data inside train/dev/test with stable md5 sort
    * merge_annotations - formats all annotations into gonito format and merges
    them into dict
    * split_to_dirs - splits annotation into train/dev/test with stable md5
    split and writes them into .tsv
    * main - the main function of the script
"""

import json
import argparse
from utils.hashutils import assign_item_to_set, hash_without_salt_on_string

parser = argparse.ArgumentParser(
    description='Convert object-dection data set in the Coco format into the Gonito format')
parser.add_argument('path', metavar='CHALLENGE_PATH', type=str,
                    help='path to challenge dir')
parser.add_argument('coco_file', metavar='COCO_JSON_FILE', type=str, nargs='+',
                    help='JSON file with annotations')
parser.add_argument('--rename', metavar='DICT_OF_NEW_CLASSES', nargs='?',
                    type=json.loads, help='string with dict of new names to rename classes')

parser.add_argument('--file', metavar='FILE_WITH_NEW_CLASSES', nargs='?', type=str,
                    const = 'classes_out.json', help='file with new names to rename classes')

parser.add_argument('-s', '--sort', action='store_false',
                    help='sort inside of train/dev/test with md5 stable sort')
parser.add_argument('-r', '--round', action='store_true',
                    help='convert bbox coordinates into ints')


def sorter(in_file: str, expected_file: str) -> None:
    """Sort piars of (value-from-in, value-from-expected) with stable md5 sort
    inside in and expected file

    Parameters
    ----------
    in_file : str
        Input .tsv with file names like:
        p02_TOTBIB_BCUMCS_4010641.jpg
        if you want to use diffrent names change hashable_feature to something like datatime
    expected_file : str
        Expected .tsv file

    Returns
    -------
    None
    """
    values = []
    with open(in_file, 'r') as dir_in, \
         open(expected_file, 'r') as dir_expected:
        for input, output in zip(dir_in, dir_expected):
            values.append([input, output])

    def hashable_feature(x):
        #extract '4010641' from 'p02_TOTBIB_BCUMCS_4010641.jpg'
        return x[0].split('\t')[0].split('_')[3].replace('.jpg', '')
    values = sorted(values, key=lambda x: hash_without_salt_on_string(hashable_feature(x)))

    with open(in_file, 'w') as dir_in, \
         open(expected_file, 'w') as dir_expected:
        for input, output in values:
            dir_in.write(input)
            dir_expected.write(output)

def merge_annotations(filenames: "list of strings", rename_dict: dict = dict(),
                    rename_file: str = None, round: bool = False) -> dict:
    """Formats all annotations into gonito format and merges them into dict
    optionally it can also rename categories of annotation classes and/or
    round bbox coordinates

    Parameters
    ----------
    filenames : list of strings
        List of coco files
    rename_dict: dict of str:str, optional
        Dict for renaming categories of annotation classes
        {old_class_name: new_class_name}
    rename_file: str, optional
        filepath to .json file with output of coco2classes.py containing
        dict for renaming categories of annotation classes
        !this argument supress rename_dict
    round: bool, optional
        A flag used to convert bbox coordinates into ints (default is
        False)

    Returns
    -------
    dict
        Dict containing all annotations in format:
        file_name: [width, height, 'category:coord,coord,coord,coord ...']
    """
    merged = {}
    for file in filenames:
        annotations = {}
        json_data = json.loads(open(file).read())

        categories = {}
        for item in json_data['categories']:
            categories[item['id']] = item['name']
        if rename_file:
            rename_dict = json.loads(open(rename_file).read())
        if rename_dict:
            for key, value in categories.items():
                if value in rename_dict.keys():
                    categories[key] = rename_dict[value]

        # Add bbox with class_id to image_id
        # "category": "class_id:coord,coord,coord,coord"
        for item in json_data['annotations']:
            if round:
                formated = f"{categories[item['category_id']]}:{','.join(str(int(x)) for x in item['bbox'])}"
            else:
                formated = f"{categories[item['category_id']]}:{','.join(str(x) for x in item['bbox'])}"
            if item['image_id'] in annotations :
                annotations[item['image_id']] = annotations.pop(item['image_id']) + ' ' + formated
            else:
                annotations[item['image_id']] = formated

        # Replace image_id with file_name, add width, height
        # file_name: [width, height, 'category:topLeftX,topLeftY,bottomRightX,bottomRightY  x N]
        for item in json_data['images']:
            if item['id'] in annotations :
                annotations[item['file_name']] = [annotations.pop(item['id'])]
            else:
                annotations[item['file_name']] = ['']

        #check for duplicates
        for item in merged.keys():
            if item in annotations.keys():
                print(f"Warning file was twice (or more) annotated: {item}")

        merged.update(annotations)
    return merged

def split_to_dirs(dir: str, merged: dict) -> None:
    """Splits annotation into train/dev/test with stable md5 split and writes them into .tsv
    in: file_name   width   height
    expected: category1:topLeftX,topLeftY,bottomRightX,bottomRightY   categoryN:topLeftX,topLeftY,bottomRightX,bottomRightY

    Parameters
    ----------
    dir : str
        Drectory of initialized challenge
    merged : dict
        Dict containing annotations to be splited and writen in files
        with keys like p02_TOTBIB_BCUMCS_4010641.jpg
        if you want to use diffrent keys change hashable_feature to something else

    Returns
    -------
    None
    """
    with open(f'{dir}dev-0/in.tsv', 'w') as dev_in, \
         open(f'{dir}dev-0/expected.tsv', 'w') as dev_expected, \
         open(f'{dir}test-A/in.tsv', 'w') as test_in, \
         open(f'{dir}test-A/expected.tsv', 'w') as test_expected, \
         open(f'{dir}train/in.tsv', 'w') as train_in, \
         open(f'{dir}train/expected.tsv', 'w') as train_expected:
            for key, value in merged.items():
                #extract 'BCUMCS' from 'p02_TOTBIB_BCUMCS_4010641.jpg'
                hashable_feature = key.split('_')[2]
                if assign_item_to_set(hashable_feature) == 'dev-0':
                    dev_in.write(f'{key}\n')
                    dev_expected.write(f'{value[-1]}\n')
                elif assign_item_to_set(hashable_feature) == 'test-A':
                    test_in.write(f'{key}\n')
                    test_expected.write(f'{value[-1]}\n')
                elif assign_item_to_set(hashable_feature) == 'train':
                    train_in.write(f'{key}\n')
                    train_expected.write(f'{value[-1]}\n')

def main(path: str, coco_files: "list of strings", rename_dict: dict = dict(),
        rename_file: str = None, sort: bool = True, round: bool = False) -> None:
    merged = merge_annotations(coco_files, rename_dict, rename_file, round)
    split_to_dirs(path, merged)

    if sort:
        files = [[f'{path}dev-0/in.tsv', f'{path}dev-0/expected.tsv'],
                [f'{path}test-A/in.tsv', f'{path}test-A/expected.tsv'],
                [f'{path}train/in.tsv', f'{path}train/expected.tsv']]
        for in_file, expected_file in files:
            sorter(in_file, expected_file)

if __name__ == '__main__':
    args = parser.parse_args()
    path = args.path
    coco_files = args.coco_file
    rename_dict = args.rename
    rename_file = args.file
    sort = args.sort
    round = args.round
    print(rename_file)
    main(path, coco_files, rename_dict, rename_file, sort, round)
