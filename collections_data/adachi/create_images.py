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

            thumb_flg = True

            scripts = soup2.find_all('script')
            for script in scripts:
                text = script.text

                if "var pict_array = [];" in text:
                    es = text.split(";")
                    for e in es:
                        if "pict_array.push" in e:
                            es2 = e.split("'")
                            data_id = es2[3]
                            museum_id = es2[7]

                            img_url = "http://jmapps.ne.jp/adachitokyo/files/" + \
                                museum_id+"/media_files/large/"+data_id+".jpg"

                            thumb_url = img_url.replace("large", "small")

                            image = Image.open(urllib.request.urlopen(img_url))
                            width, height = image.size

                            row = [id, img_url, thumb_url, width, height]
                            rows.append(row)

                            if thumb_flg:

                                row2 = [id, thumb_url]
                                rows2.append(row2)

                                thumb_flg = False

    f = open("data/images/images_"+str(page).zfill(5)+".csv", 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(rows)

    f.close()

    f = open("data/thumbnails/thumbnails_"+str(page).zfill(5)+".csv", 'w')

    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(rows2)

    f.close()

    rows = []
    row = ["id", "img_url"]
    rows.append(row)

    rows2 = []
    row2 = ["id", "thumb_url"]
    rows2.append(row2)

    page += 1
