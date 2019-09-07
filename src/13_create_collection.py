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
config = yaml.load(f, Loader=yaml.SafeLoader)

data_dir = config["data_dir"]
output_dir = config["output_dir"]
prefix = config["prefix"]
label = config["label"]

collection_uri = prefix+"/"+output_dir.split("/")[-1]+"/collection.json"

files = glob.glob(output_dir+"/manifest/*.json")

manifests = []

for file in files:

    try:

        with open(file) as f:
            df = json.load(f)

        manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": df["@id"],
            "@type": "sc:Manifest",
            "label": df["label"]
        }

        if "thumbnail" in df:
            manifest["thumbnail"] = df["thumbnail"]["@id"]

        manifests.append(manifest)
    except:
        print("Error: "+file)

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": collection_uri,
    "@type": "sc:Collection",
    "label": label,
    "vhint": "use-thumb",
    "manifests": manifests
}


f2 = open(output_dir+"/collection.json", 'w')
json.dump(collection, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
