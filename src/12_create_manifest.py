import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import yaml
import requests

import argparse
import sys

def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'config_path',
        action='store',
        type=str,
        help='config path.')

    return parser.parse_args(args)


args = parse_args()

config_path = args.config_path

f = open(config_path, "r+")
config = yaml.load(f)

data_dir = config["data_dir"]
output_dir = config["output_dir"]
prefix = config["prefix"]

dir_name = output_dir.split("/")[-1]

path_metadata = data_dir+"/metadata.xlsx"
path_image = data_dir+"/images.xlsx"

manifest_dir = output_dir +"/manifest"
os.makedirs(manifest_dir, exist_ok=True)

def get_id_image_map():
    df = pd.read_excel(path_image, sheet_name=0,
                       header=None, index_col=None)

    map = {}

    r_count = len(df.index)

    for j in range(1, r_count):

        id = df.iloc[j, 0]
        image = df.iloc[j, 1]
        thumbnail = df.iloc[j, 2]
        width = int(df.iloc[j, 3])
        height = int(df.iloc[j, 4])

        if id not in map:
            map[id] = []

        map[id].append({
            "original" : image,
            "thumbnail": thumbnail,
            "width": width,
            "height": height
        })

    return map

df = pd.read_excel(path_metadata, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

id_image_map = get_id_image_map()

map = {}

description_index = None
logo_index = None

for i in range(0, c_count):
    label = df.iloc[0, i]
    uri = df.iloc[1, i]
    # type = df.iloc[2, i]
    target=df.iloc[3,i]

    if target == "metadata":
        obj = {}
        map[i] = obj
        obj["label"] = label

    if uri == "http://purl.org/dc/terms/rights":
        license_index = i
    if uri == "http://purl.org/dc/terms/title":
        title_index = i
    if uri == "http://purl.org/dc/terms/description":
        description_index = i
    if uri == "http://www.w3.org/2000/01/rdf-schema#seeAlso":
        seeAlso_index = i
    if uri == "http://purl.org/dc/terms/identifier":
        identifier_index = i
    if label == "logo":
        logo_index = i
    if label == "attribution":
        attribution_index = i
    if label == "within":
        within_index = i
    if label == "viewingDirection":
        viewingDirection_index = i
    if uri == "http://purl.org/dc/terms/relation":
        related_index = i

for j in range(4, r_count):

    print(str(j)+"/"+str(r_count))

    id = df.iloc[j, identifier_index]

    filename = id+".json"

    manifest_uri = prefix+"/"+dir_name+"/manifest/"+filename

    relation = df.iloc[j, related_index]

    title = df.iloc[j, title_index]

    metadata = []
    for index in map:
        value = df.iloc[j, index]
        if not pd.isnull(value) and value != 0:
            values = str(value).split(",")
            for value in values:
                metadata.append({
                    "label": map[index]["label"],
                    "value" : value.strip()
                })

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "@id": manifest_uri,
        "license": df.iloc[j, license_index],
        "attribution": df.iloc[j, attribution_index],
        "label": title,
        # "logo": df.iloc[j, logo_index],
        "within": df.iloc[j, within_index],
        # "viewingDirection": df.iloc[j, viewingDirection_index],
        # "seeAlso": seeAlso,
        "related": relation,
        "sequences": [
            {
                "@type": "sc:Sequence",
                "@id": manifest_uri+"/sequence/normal",
                "label": "Current Page Order",
                "viewingHint": "non-paged",
                "canvases": []
            }
        ]
    }

    if len(metadata) > 0:
        manifest["metadata"] = metadata

    if description_index != None:
        value = df.iloc[j, description_index]
        if not pd.isnull(value) and value != 0:
            manifest["description"] = value

    if logo_index != None:
        value = df.iloc[j, logo_index]
        if not pd.isnull(value) and value != 0:
            manifest["logo"] = value

    canvases = manifest["sequences"][0]["canvases"]

    if id not in id_image_map:
        continue

    images = id_image_map[id]
    for i in range(len(images)):

        img = images[i]

        img_url = img["original"]

        if "info.json" in img_url:

            r = requests.get(img_url)
            info = r.json()

            image_api = img_url.replace("/info.json", "")

            thumbnail = image_api+"/full/"+str(info["sizes"][0]["width"])+",/0/default.jpg"

            width = info["width"]
            height = info["height"]

            service = {
                "@context": info["@context"],
                "@id": image_api,
                "profile": info["profile"][0]
            }

            img_id = image_api+"/full/full/0/default.jpg"

        else:
            thumbnail = img["thumbnail"]

            width = img["width"]
            height = img["height"]

            img_id = img_url

        canvas_id = manifest_uri+"/canvas/p"+str(i+1)

        canvas_label = "["+str(i+1)+"]"

        canvas = {
            "@type": "sc:Canvas",
            "@id": canvas_id,
            "label": canvas_label,
            "thumbnail": {
                "@id": thumbnail
            },
            "images": [
                {
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "@id": manifest_uri + "/annotation/p"+str(i+1)+"-image",
                    "resource": {
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                        "width" : width,
                        "height" : height,
                        "@id": img_id
                    },
                    "on": canvas_id
                }
            ],
            "width": width,
            "height": height
        }

        if i == 0:
            manifest["thumbnail"] = {
                "@id" : thumbnail
            }

        if "info.json" in img_url:
            canvas["thumbnail"]["service"] = service
            canvas["images"][0]["resource"]["service"] = service

        canvases.append(canvas)



    f2 = open(manifest_dir+"/"+filename, 'w')
    json.dump(manifest, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
