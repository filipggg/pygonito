#!/bin/bash -e

in_dir="$1"
out_dir="$2"

geval --init --expected-directory $out_dir --metric 'Probabilistic-Soft2D-F1:N<F1>'

rm $out_dir/*/in.tsv
rm $out_dir/*/expected.tsv

image_dir=$out_dir/images
mkdir -p "$image_dir"

process_dir() {

dir="$1"

for in_file in $dir/*
do
    base_in_file=$(basename $in_file)

    if [[ -d "$in_file" ]]
    then
        if [[ "$base_in_file" == "annotations" ]]
        then
            process_dir $in_file
        else
            cp -p $in_file/* "$image_dir/"
        fi
    else
        if [[ "$base_in_file" == *train* ]]
        then
            test_dir=train
        elif [[ "$base_in_file" == *val* ]]
        then
            test_dir=dev-0
        elif [[ "$base_in_file" == *test* ]]
        then
            test_dir=test-A
        fi

        ./coco2gonito.py --coco-file $in_file --out-test-dir $out_dir/$test_dir
    fi
done

}

process_dir $in_dir

geval --validate --expected-directory $out_dir
