#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
    description='Convert object-dection data set in the Coco format into the Gonito format')
parser.add_argument('coco_input_dir', metavar='COCO_DIR', type=str,
                    help='Input dir with Coco data')
parser.add_argument('gonito_output_dir', metavar='GONITO_DIR', type=str,
                    help='Output dir with Gonito data')
args = parser.parse_args()
