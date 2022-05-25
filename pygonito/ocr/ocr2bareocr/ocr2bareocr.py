#!/usr/bin/env python3

from typing import List, Tuple
import re
import sys
from PIL import Image
import hashlib

in_image_dir = sys.argv[1]
out_image_dir = sys.argv[2]

parse_ocr_re = re.compile(r'^([^:]+):(\d+),(\d+),(\d+),(\d+):(.*)$')

page_limit = 20


def unquote(t):
    return t.replace('_', ' ')


def clean(t):
    return t.rstrip(' ')


def parse_ocr_item(item: str) -> Tuple[str, Tuple[int, int, int, int], str]:
    m = parse_ocr_re.search(item)

    if m:
        return (m.group(1), (int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))), unquote(m.group(6)))
    else:
        raise "???"


def parse_ocr(line: str) -> List[Tuple[str, Tuple[int, int, int, int], str]]:
    if line == '':
        return []

    return [parse_ocr_item(item) for item in line.split()]


def string_hash(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def item_hash(doc_id, pair):
    ix, _ = pair
    return string_hash(f'{doc_id}-ix')


def new_tuple(t, ix, v):
    l = list(t)
    l[ix] = v
    return tuple(l)


def process_file(png_file, expected):
    exp = parse_ocr(expected)

    doc_id = png_file
    doc_id = re.sub(r'\.png$', '', doc_id)

    bbox_id = 1

    img = Image.open(f'{in_image_dir}/{png_file}')
    width, height = img.size

    if page_limit is not None:
        exp = [p[1] for p in sorted(
            (sorted(enumerate(exp), key=lambda p: item_hash(doc_id, p)))[0:page_limit],
            key=lambda p: p[0])]

    for _, area, content in exp:
        image_ok = True

        if area[2] > width:
            image_ok = False
        if area[3] > height:
            image_ok = False

        if image_ok:
            cropped_img = img.crop(area)
            out_png = f'{out_image_dir}/{doc_id}-{bbox_id}.png'
            cropped_img.save(out_png)
            bbox_id += 1

            print('\t'.join([out_png, clean(content)]))
        else:
            print(f'Something wrong with {doc_id}', file=sys.stderr)

for line in sys.stdin:
    line = line.rstrip('\n')
    png_file, expected = line.split('\t')
    process_file(png_file, expected)
