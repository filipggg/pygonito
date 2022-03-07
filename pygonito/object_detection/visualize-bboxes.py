#!/usr/bin/python3

import cv2
from bounding_box import bounding_box as bb
import sys
import re
import argparse
import os

parser = argparse.ArgumentParser(description='Visualize bounding boxes for the gold standard or an output for a Gonito object-detection challenge.')
parser.add_argument('indir', metavar='IN_DIR', type=str,
                    help='directory with input images')
parser.add_argument('outdir', metavar='OUR_DIR', type=str,
                    help='directory for output images (must exist)')
parser.add_argument('--resize', type=int,
                    help='optional resize factor (percent)')
args = parser.parse_args()

# For example, to visualize 10 first images from the train set:
#    paste train/in.tsv train/expected.tsv| head -n 10 | ./visualize-bboxes.py images out

in_dir = args.indir
out_dir = args.outdir

if not os.path.isdir(out_dir):
    print(f'{out_dir} does not exist!', file=sys.stderr)
    exit(1)

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

    factor = 1.0

    if args.resize is not None:
        factor = args.resize / 100

        width = int(image.shape[1] * factor)
        height = int(image.shape[0] * factor)
        dim = (width, height)

        image = cv2.resize(image, dim)

    for bbox in bboxes:
        bb.add(image,
               int(bbox[0]*factor), int(bbox[1]*factor), int(bbox[2]*factor),
               int(bbox[3]*factor), bbox[4])

    cv2.imwrite(out_file, image)


for line in sys.stdin:
    line = line.rstrip()
    img_file, annotations = line.split('\t')
    bboxes = parse_bboxes(annotations)
    process_file(f'{in_dir}/{img_file}', bboxes, f'{out_dir}/{img_file}')
