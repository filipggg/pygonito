#!/usr/bin/env python3

from typing import List, Tuple
import re
import sys
from PIL import Image

in_image_dir = sys.argv[1]
out_image_dir = sys.argv[2]

parse_ocr_re = re.compile(r'^([^:]+):(\d+),(\d+),(\d+),(\d+):(.*)$')


def parse_ocr_item(item: str) -> Tuple[str, Tuple[int, int, int, int], str]:
    m = parse_ocr_re.search(item)

    if m:
        return (m.group(1), (int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))), m.group(6))
    else:
        raise "???"


def parse_ocr(line: str) -> List[Tuple[str, Tuple[int, int, int, int], str]]:
    if line == '':
        return []

    return [parse_ocr_item(item) for item in line.split()]


def process_file(png_file, expected):
    exp = parse_ocr(expected)

    doc_id = png_file
    doc_id = re.sub(r'\.png$', '', doc_id)

    bbox_id = 1

    img = Image.open(f'{in_image_dir}/{png_file}')
    width, height = img.size

    for _, area, content in exp:
        if area[2] > width:
            area[2] = width
        if area[3] > height:
            area[3] = height

        cropped_img = img.crop(area)
        out_png = f'{out_image_dir}/{doc_id}-{bbox_id}.png'
        cropped_img.save(out_png)
        bbox_id += 1

        print('\t'.join([out_png, content]))


for line in sys.stdin:
    line = line.rstrip('\n')
    png_file, expected = line.split('\t')
    process_file(png_file, expected)
