#!/bin/bash

in_dir="$1"
out_dir="$2"

if [[ ! -d "$in_dir" ]]
then
    echo >&2 "'$in_dir' should exist!!!"
    exit 1
fi

if [[ -d "$out_dir" ]]
then
    echo >&2 "'$out_dir' should not exist!!!"
    exit 1
fi

geval --init --expected-directory $out_dir --metric 'CER' --precision 3 -%

out_images_dir=$out_dir/images
mkdir -p $out_images_dir

in_images_dir=$in_dir/images

for t in train dev-0 test-A
do
    paste $in_dir/$t/{in.tsv,expected.tsv} | ./ocr2bareocr.py $in_images_dir $out_images_dir | tee >(cut -f 1 > $out_dir/$t/in.tsv) | cut -f 2- > $out_dir/$t/expected.tsv
done
