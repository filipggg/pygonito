#!/usr/bin/env python3

import csv
import os
from os.path import exists
import json
import argparse
import hashlib
from pathlib import Path
import sys

parser = argparse.ArgumentParser(
    description='Convert object-dection data set in the Coco format into the Gonito format')
parser.add_argument('--coco-file', metavar='COCO_JSON_FILE', type=str, default='instances_default.json',
                    help='JSON file with annotations')
parser.add_argument('--out-test-dir', metavar='TEST_NAME', type=str,
                    help='Output test dir (e.g. .../test-A)')
args = parser.parse_args()
coco_file = args.coco_file
out_test_dir = args.out_test_dir


DIRECTORIES = ['train', 'dev-0', 'test-A']


def get_md5(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()


def process_dir(dir):
    images = []

    json_data = json.loads(open(coco_file).read())

    imgs, annotations, categories = {}, {}, {}
    images_found = []
    for image in json_data["images"]:
        imgs[image["id"]] = image["file_name"]
        annotations[image["file_name"]] = []
        images_found.append(image['file_name'])
    for annotation in json_data["annotations"]:
        annotations[imgs[annotation["image_id"]]] += [annotation]
    for category in json_data["categories"]:
        categories[category['id']] = category['name']

    file_path = f'{dir}/in.tsv'

    if out_test_dir is not None:
        images = sorted(images_found, key=lambda n: get_md5(n))
    else:
        # adapt in.tsv files
        file = open(file_path)
        read_tsv = csv.reader(file, delimiter="\t")
        for row in read_tsv:
            images.append(row[0])
        file.close()
        os.remove(file_path)

    Path(dir).mkdir(exist_ok=True)
    file = open(file_path, "a")
    file.write('\n'.join(images) + '\n')
    file.close()


    # create expected.tsv files

    expected_file_path = f'{dir}/expected.tsv'

    if exists(expected_file_path):
        os.remove(expected_file_path)

    expected_result = ''
    for i in images:
        tmp = annotations[i]
        res = []
        for j in tmp:
            bbox = [int(k) for k in j['bbox']]
            category = categories[j['category_id']]
            if bbox[0] < 0 or bbox[1] < 0:
                print(f'negative coordinate {i}!!!', file=sys.stderr)
                if bbox[0] < 0:
                    bbox[0] = 0
                if bbox[1] < 0:
                    bbox[1] = 0
            res.append(f'{category}:{bbox[0]},{bbox[1]},{bbox[0] + bbox[2]},{bbox[1] + bbox[3]}')
        expected_result += ' '.join(res) + '\n'

    file = open(expected_file_path, "a")
    file.write(expected_result)
    file.close()


if out_test_dir is not None:
    process_dir(out_test_dir)
else:
    for dir in DIRECTORIES:
        process_dir(dir)
