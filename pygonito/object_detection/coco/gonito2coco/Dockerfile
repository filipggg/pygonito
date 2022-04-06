FROM python:3.9

ARG INPUT_GONITO_DIR
ARG INPUT_IMAGES_DIR
ARG OUTPUT_NAME=instances_default.json

WORKDIR /opt/

RUN apt-get update

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY gonito2coco.py gonito2coco.py
COPY ${INPUT_GONITO_DIR} input_dir
COPY ${INPUT_IMAGES_DIR} images

RUN mkdir results

ENTRYPOINT python3 gonito2coco.py --input=input_dir --output=results --name=instances_default.json --images=images
