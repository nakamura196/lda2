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

import requests
import shutil


rows = []
row = ["id", "img_url", "thumb_url", "width", "height"]
rows.append(row)

rows2 = []
row2 = ["id", "thumb_url"]
rows2.append(row2)

page = 1

flg = True

all = []

while(flg):
    url = "http://jmapps.ne.jp/adachitokyo/list.html?page=" + \
        str(page)+"&list_count=100"

    r = requests.get(url)  # requestsを使って、webから取得

    soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

    imgs = soup.find_all("a")

    for img in imgs:

        src = img.get("href")

        if "det.html" in src:

            id = src.split("=")[1]

            src = "http://jmapps.ne.jp/adachitokyo/"+src.replace("./", "")

            print(src)

            time.sleep(1)

            r2 = requests.get(src)  # requestsを使って、webから取得

            soup2 = BeautifulSoup(r2.text, 'lxml')  # 要素を抽出

            blockData = soup2.find(id="blockData")
            print(blockData)

            obj = {}
            obj["metadata"] = {}

            title = blockData.find("strong").text
            obj["title"] = title

            obj["url"] = src
            obj["id"] = id
            obj["within"] = "http://jmapps.ne.jp/adachitokyo/index.html"
            obj["attribution"] = "足立区立郷土博物館"
            obj["license"] = "http://creativecommons.org/publicdomain/mark/1.0/"

            trs = blockData.find_all("tr")

            for tr in trs:
                obj["metadata"][tr.find("th").text] = tr.find("td").text

            print(obj)

            all.append(obj)



    page += 1

    if len(imgs) == 0:
        flg = False

fields = []

for obj in all:
    for key in obj["metadata"]:
        if key not in fields:
            fields.append(key) 

rows = []
row0 = ["title", "thumbnail", "relation", "logo", "within", "attribution", "license", "uuid"]
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
    row = [obj["title"], "", obj["url"], "", obj["within"], obj["attribution"], obj["license"], ""]

    for key in fields:
        value = ""
        if key in obj["metadata"]:
            value = obj["metadata"][key]
        row.append(value)

    rows.append(row)

df = pd.DataFrame(rows)
writer = pd.ExcelWriter('data/metadata.xlsx', options={'strings_to_urls': False})

df.to_excel(writer, index=False, header=False)

writer.close()
