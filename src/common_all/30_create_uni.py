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
import requests


path = "data/data.json"
prefix = "https://nakamura196.github.io/lda2/"

collections = []


with open(path) as f:
    df = json.load(f)

    for obj in df:
        
        print(obj["collection_uri"])

        r = requests.get(obj["collection_uri"])
        data = r.json()

        collections.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": data["@id"],
            "@type": "sc:Collection",
            "label": data["label"]+"("+str(len(data["manifests"]))+")"
        })

uni = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": prefix+"/collections_all.json",
    "@type": "sc:Collection",
    "label": "地域文化資源デジタルアーカイブ",
    "vhint": "use-thumb",
    "collections": collections
}


f2 = open("../../docs/collections_all.json", 'w')
json.dump(uni, f2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
