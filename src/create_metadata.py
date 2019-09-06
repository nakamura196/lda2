import urllib.request  # ライブラリを取り込む
import csv
import json
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os
import glob
from lxml import etree
import sys
import requests
import hashlib
import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
import time
from PIL import Image
import yaml

config_path = "/Users/nakamura/git/min_a/lda2/src/data/nishinomiya/data/config.yml"
f = open(config_path, "r+")
config = yaml.load(f)

data_dir = config["data_dir"]
output_dir = config["output_dir"]
prefix = config["prefix"]

dir_name = output_dir.split("/")[-1]


all = []

# -------

files = glob.glob(data_dir+"/metadata/*.json")

for file in files:
    # jsonファイルを読み込む
    f = open(file)
    # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
    data = json.load(f)
    # ファイルを閉じる
    f.close()

    all.append(data)

# --------

images = {}

files = glob.glob(data_dir+"/images/*.json")

for file in files:
    try:
        # jsonファイルを読み込む
        f = open(file)
        # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
        data = json.load(f)
        # ファイルを閉じる
        f.close()

        filename = os.path.split(file)[1].split(".")[0]

        images[filename] = data
    except:
        print("error 1")

# ---------


fields = []

for obj in all:
    for key in obj["metadata"]:
        if key not in fields:
            fields.append(key)

rows = []
row0 = ["title", "thumbnail", "relation", "logo",
        "within", "attribution", "license", "uuid"]
row1 = ["http://purl.org/dc/terms/title", "http://xmlns.com/foaf/0.1/thumbnail", "http://purl.org/dc/terms/relation", "logo",
        "within", "attribution", "http://purl.org/dc/terms/rights", "http://purl.org/dc/terms/identifier"]
row2 = []
row3 = []

for e in row0:
    row3.append("")

for key in fields:
    row0.append(key)
    row3.append("metadata")

rows.append(row0)
rows.append(row1)
rows.append(row2)
rows.append(row3)

for obj in all:

    id = obj["id"]
    url = obj["url"]
    uuid = hashlib.md5(url.encode('utf-8')).hexdigest()
    thumbnail = ""
    if id in images:
        thumbnail = images[id]["thumbnail"]

    row = [obj["title"], thumbnail, url, "", obj["within"],
           obj["attribution"], obj["license"], uuid]

    for key in fields:
        value = ""
        if key in obj["metadata"]:
            value = obj["metadata"][key]
        row.append(value)

    rows.append(row)

df = pd.DataFrame(rows)
writer = pd.ExcelWriter(data_dir+'/metadata.xlsx',
                        options={'strings_to_urls': False})

df.to_excel(writer, index=False, header=False)

writer.close()