import csv
import os
from os.path import exists
import json


DIRECTORIES = ['train', 'dev-0', 'test-A']
coco_file = 'instances_default.json'


for dir in DIRECTORIES:
    file_path = f'{dir}/in.tsv'


    # adapt in.tsv files

    images = []

    file = open(file_path)
    read_tsv = csv.reader(file, delimiter="\t")
    for row in read_tsv:
        images.append(row[0])
    file.close()

    os.remove(file_path)
    
    file = open(file_path, "a")
    file.write('\n'.join(images) + '\n')
    file.close()


    # create expected.tsv files

    expected_file_path = f'{dir}/expected.tsv'

    if exists(expected_file_path):
        os.remove(expected_file_path)

    json_data = json.loads(open(coco_file).read())

    imgs, annotations = {}, {}
    for image in json_data["images"]:
        imgs[image["id"]] = image["file_name"]
        annotations[image["file_name"]] = []
    for annotation in json_data["annotations"]:
        annotations[imgs[annotation["image_id"]]] += [annotation]

    expected_result = ''
    for i in images:
        tmp = annotations[i]
        res = []
        for j in tmp:
            bbox = [int(k) for k in j['bbox']]
            res.append(f'hwr_line:{bbox[0]},{bbox[1]},{bbox[0] + bbox[2]},{bbox[1] + bbox[3]}')
        expected_result += ' '.join(res) + '\n'

    file = open(expected_file_path, "a")
    file.write(expected_result)
    file.close()