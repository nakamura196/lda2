import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import glob
import sys
import argparse

def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'collection_uri',
        action='store',
        type=str,
        help='collection uri.')

    parser.add_argument(
        'output_file_path',
        action='store',
        type=str,
        help='output file path.')

    return parser.parse_args(args)


args = parse_args()

collection_uri = args.collection_uri

opath = args.output_file_path

size = 10

local_flg = True

if local_flg:
    f = open(collection_uri)
    # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
    collection = json.load(f)
    # ファイルを閉じる
    f.close()
else:
    response = urllib.request.urlopen(collection_uri)
    collection = json.loads(response.read().decode('utf8'))

manifests = collection["manifests"]
result = {}
aggregations = {}
aggregations2 = {}

data = []

for i in range(len(manifests)):

    manifest_uri = manifests[i]["@id"]

    print(str(i+1)+"/"+str(len(manifests)))

    if local_flg:
        manifest_path = os.path.split(opath)[0]+"/manifest/"+os.path.split(manifest_uri)[1]
        f = open(manifest_path)
        # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
        manifest = json.load(f)
        # ファイルを閉じる
        f.close()
    else:
        response = urllib.request.urlopen(manifest_uri)
        manifest = json.loads(response.read().decode('utf8'))

    thumbnail = None
    if "thumbnail" in manifest:
        if "@id" in manifest["thumbnail"]:
            thumbnail = manifest["thumbnail"]["@id"]
        else:
            thumbnail = manifest["thumbnail"]

    fulltext = ""

    obj = {
        "label": manifest["label"],
        "manifest": manifest["@id"]
    }

    obj["thumbnail"] = thumbnail

    if "related" in manifest:
        obj["related"] = manifest["related"]

    if "description" in manifest:
        obj["description"] = manifest["description"]

    if "attribution" in manifest:
        obj["attribution"] = manifest["attribution"]

    if "license" in manifest:
        license = manifest["license"]
        if license == "http://creativecommons.org/publicdomain/mark/1.0/":
            license = "Public Domain Marked"
        elif license == "http://creativecommons.org/licenses/by/4.0/":
            license = "CC BY"
        obj["license"] = license

    if "metadata" in manifest:
        for metadata in manifest["metadata"]:
            label = metadata["label"]
            value = metadata["value"]

            if label == "description":
                label = "description_"

            if isinstance(value, list):
                values = value
            else:
                values = [value]

            for value in values:

                if "http" not in value:

                    fulltext += " "+value

    obj["fulltext"] = fulltext
    data.append(obj)

f2 = open(opath, 'w')
json.dump(data, f2, ensure_ascii = False, indent = 4,
            sort_keys = True, separators = (',', ': '))
