#!/bin/bash -e

in_gonito_dir="$1"
in_images_dir="$2"
out_dir="$3"

docker build -t gonito2coco --build-arg INPUT_GONITO_DIR=${in_gonito_dir} --build-arg INPUT_IMAGES_DIR=${in_images_dir} .

docker run gonito2coco 
docker cp `docker ps -l -q`:/opt/results ${out_dir}