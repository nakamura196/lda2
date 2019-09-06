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

# -------

files = glob.glob(data_dir+"/metadata/*.json")

id_uuid_map = {}

for file in files:
    # jsonファイルを読み込む
    f = open(file)
    # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
    data = json.load(f)
    # ファイルを閉じる
    f.close()

    id_uuid_map[data["id"]] = hashlib.md5(data["url"].encode('utf-8')).hexdigest()

# --------

images = {}

files = glob.glob(data_dir+"/images/*.json")

rows = []
rows.append(["id", "img_url", "thumb_url", "width", "height"])

for file in files:
    try:
        # jsonファイルを読み込む
        f = open(file)
        # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
        data = json.load(f)
        # ファイルを閉じる
        f.close()

        id = os.path.split(file)[1].split(".")[0]
        uuid = id_uuid_map[id]



        for obj in data["array"]:
            rows.append([uuid, obj["img_url"], obj["thumb_url"], obj["width"], obj["height"]])
            
    except:
        print("error 1")

df = pd.DataFrame(rows)

df.to_excel(data_dir+"/images.xlsx", index=False, header=False)
