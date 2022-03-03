#!/usr/bin/python3

import cv2
from bounding_box import bounding_box as bb
import sys
import re

if len(sys.argv) != 3:
    print('Script for visualizing bboxes in Gonito challenges', file=sys.stderr)
    print('For example, to visualize 10 first images from the train set:', file=sys.stderr)
    print('   paste train/in.tsv train/expected.tsv| head -n 10 | ./visualize-bboxes.py images out', file=sys.stderr)
    exit(1)

in_dir = sys.argv[1]
out_dir = sys.argv[2]

bbox_re = re.compile(r'^([^:]+):(\d+),(\d+),(\d+),(\d+)(:.*)?$')


def parse_bbox(b):
    m = bbox_re.match(b)
    if m:
        return [int(m.group(2)), int(m.group(3)),
                int(m.group(4)), int(m.group(5)),
                m.group(1)]
    else:
        raise f'WRONG BBOX {b}'


def parse_bboxes(s):
    return [parse_bbox(b) for b in s.split()]


def process_file(in_file, bboxes, out_file):
    image = cv2.imread(in_file)
    for bbox in bboxes:
        bb.add(image, bbox[0], bbox[1], bbox[2], bbox[3], bbox[4])

    cv2.imwrite(out_file, image)


for line in sys.stdin:
    line = line.rstrip()
    img_file, annotations = line.split('\t')
    bboxes = parse_bboxes(annotations)
    process_file(f'{in_dir}/{img_file}', bboxes, f'{out_dir}/{img_file}')
