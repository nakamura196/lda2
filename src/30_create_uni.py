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

prefix = config["prefix"]

files = glob.glob("../docs/*/collection.json")

collections = []

for file in files:

   

    with open(file) as f:
        df = json.load(f)

        collections.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": df["@id"],
            "@type": "sc:Collection",
            "label": df["label"]
        })

uni = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": prefix+"/collections.json",
    "@type": "sc:Collection",
    "label": "地域文化資源デジタルアーカイブ",
    "vhint": "use-thumb",
    "collections": collections
}


f2 = open("../docs/collections.json", 'w')
json.dump(uni, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
