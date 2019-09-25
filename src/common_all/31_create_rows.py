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

import yaml
import hashlib
import argparse
import sys
import requests
import time

path = "data/data.json"

data = []

total = 0

def exec(manifest):
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
    return obj


with open(path) as f:
    df = json.load(f)

for config in df:

    print(config["collection_uri"])

    r = requests.get(config["collection_uri"])
    collection = r.json()

    for manifest_obj in collection["manifests"]:

        manifest_uri = manifest_obj["@id"]
        print(manifest_uri)

        if config["local_flg"]:
            filepath = config["path"]+"/"+manifest_uri.split("/")[-1]

            try:
                with open(filepath) as f:
                    manifest = json.load(f)
                    data.append(exec(manifest))
            except:
                print("Error: "+path)

        else:
            uuid = hashlib.md5(manifest_uri.encode('utf-8')).hexdigest()
            filepath = config["path"]+"/"+uuid+".json"

            if not os.path.exists(filepath):
                r = requests.get(manifest_uri)
                tmp = r.json()
                f2 = open(filepath, 'w')
                json.dump(tmp, f2, ensure_ascii=False, indent=4,
                          sort_keys=True, separators=(',', ': '))

                data.append(exec(tmp))
            else:
                with open(filepath) as f:
                    manifest = json.load(f)
                    data.append(exec(manifest))


f2 = open("data/rows.json", 'w')
json.dump(data, f2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
