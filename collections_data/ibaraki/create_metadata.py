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

rows = []
row = ["id", "img_url", "thumb_url", "width", "height"]
rows.append(row)

rows2 = []
row2 = ["id", "thumb_url"]
rows2.append(row2)

f = open("data/data.html")
html = f.read()
f.close()

soup = BeautifulSoup(html)

aas = soup.find_all("a")

urls = []

for j in range(len(aas)):
    a = aas[j]
    if "mkey" in a.get("href"):

        url = "https://archives.nishi.or.jp/"+a.get("href")

        if url in urls:
            continue

        urls.append(url)

        print(url)

        id = url.split("=")[-1]

        filename = "data/metadata/"+id+".json"

        if os.path.exists(filename):
            continue

        time.sleep(1)

        r = requests.get(url)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出


        obj = {}
        obj["metadata"] = {}

        obj["title"] = soup.find(class_="detail").find("header").text.strip()

        obj["url"] = url
        obj["id"] = id
        obj["within"] = "https://archives.nishi.or.jp/index.php"
        obj["attribution"] = "にしのみやデジタルアーカイブ"
        obj["license"] = "http://creativecommons.org/licenses/by/4.0/"

        obj["description"] = soup.find(class_="summary").text.strip()

        trs = soup.find(class_="data").find_all("tr")

        for tr in trs:

            obj["metadata"][tr.find("th").text.strip()
                            ] = tr.find("td").text.strip()

                

        f2 = open(filename, 'w')
        json.dump(obj, f2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
