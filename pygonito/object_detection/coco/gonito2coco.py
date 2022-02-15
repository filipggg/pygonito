#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
    description='Convert object-dection data set in the Gonito format into the Coco format')
parser.add_argument('gonito_input_dir', metavar='GONITO_DIR', type=str,
                    help='Input dir with Gonito data')
parser.add_argument('coco_output_dir', metavar='COCO_DIR', type=str,
                    help='Output dir with Coco data')
args = parser.parse_args()
