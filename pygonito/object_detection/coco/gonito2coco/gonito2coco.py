import argparse
import json
from itertools import chain
from pathlib import Path
from typing import Generator, Set
 
import pandas as pd
from PIL import Image
 
ROOT = Path(__file__).parent
 
 
# CONSTANTS
CATEGORY_REGEX = r"([a-zA-Z_-]+)"
ENTIRE_RECORD = r"([a-zA-Z_-]+:\d+,\d+,\d+,\d+)"
BBOX_VALUES = r"\d+,\d+,\d+,\d+"
 
base_dict = {
    "licenses": [{"name": "", "id": 0, "url": ""}],
    "info": {
        "contributor": "",
        "date_created": "",
        "description": "",
        "url": "",
        "version": "",
        "year": "",
    },
    "categories": [],
    "images": [],
    "annotations": [],
}
 
 
def get_all_categories(content: pd.DataFrame) -> Set[str]:
    matches = content.str.findall(CATEGORY_REGEX)
    return set(chain(*matches.agg(set).tolist()))
 
 
def get_row_record(content: pd.DataFrame) -> Generator:
    matches = content.str.findall(ENTIRE_RECORD)
    for match in matches:
        yield match
 
 
def get_images_file_name(input: str) -> Generator:
    for file_name in pd.read_csv(
        ROOT / input / "in.tsv", sep="\t", header=None, squeeze=True
    ):
        yield file_name
 
 
def update_categories(content: pd.DataFrame) -> None:
    for id_, value in enumerate(get_all_categories(content), start=1):
        category = {"id": id_, "name": value, "supercategory": ""}
        base_dict["categories"].append(category)
 
 
def update_images(input: str, dir: str = "images") -> None:
    for id_, file_name in enumerate(get_images_file_name(input), start=1):
        try:
            with Image.open((ROOT / dir / file_name).as_posix()) as img:
                width, height = img.size
            image = {
                "id": id_,
                "width": width,
                "height": height,
                "file_name": file_name,
                "license": 0,
                "flickr_url": "",
                "coco_url": "",
                "date_captured": 0,
            }
            base_dict["images"].append(image)
        except FileNotFoundError:
            print((ROOT / dir / file_name).as_posix())
 
 
def update_annotations(content: pd.DataFrame) -> None:
    categories = {
        category: id_
        for id_, category in enumerate(get_all_categories(content), start=1)
    }
    for image_id, row in enumerate(get_row_record(content), start=1):
        for record_id, record in enumerate(row, start=1):
            category, bbox_values = record.split(":")
            annotation = {
                "id": record_id,
                "image_id": image_id,
                "category_id": categories[category],
                "segmentation": [],
                "area": 0,
                "bbox": [
                    float(bbox_value) for bbox_value in bbox_values.split(",")
                ],
                "iscrowd": 0,
                "attributes": {"occluded": False},
            }
            base_dict["annotations"].append(annotation)
 
 
def main(input: str, output: str, name: str, images: str) -> None:
    content = pd.read_csv(
        (ROOT / input / "expected.tsv"), sep="\t", header=None, squeeze=True
    )
    update_categories(content)
    update_images(input, images)
    update_annotations(content)
 
    output = Path(output) / name
    with open(output, "w") as fp:
        json.dump(base_dict, fp)
 
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert object-dection data set in the Gonito format into the Coco format"
    )
    parser.add_argument(
        "--input",
        metavar="GONITO_DIR",
        type=str,
        help="Input dir with Gonito data",
    )
    parser.add_argument(
        "--output",
        metavar="COCO_DIR",
        type=str,
        help="Output dir with Coco data",
    )
    parser.add_argument(
        "--name",
        default="instances_default.json",
        type=str,
        help="Output file name",
    )
    parser.add_argument(
        "--images", default="images", type=str, help="Images dir"
    )
    args = parser.parse_args()
    main(**vars(args))
