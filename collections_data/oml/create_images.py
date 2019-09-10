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

path = "data/tmp/omlDAdataset.xlsx"

df = pd.read_excel(path, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

for j in range(1, r_count):

    num = df.iloc[j, 87]

    if not pd.isnull(num) and num != 0:

        id = df.iloc[j, 0]

        filename = "data/images/"+str(id)+".json"

        if os.path.exists(filename):
            continue

        print(str(j)+"/"+str(r_count))

        main = {}
        array = []
        main["array"] = array

        url = "http://image.oml.city.osaka.lg.jp/archive/detail.do?id="+str(id)

        r = requests.get(url)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        imgs = soup.find_all("img")

        thumb_url = "http://image.oml.city.osaka.lg.jp/archive/get-thumbnail?data_no=" + \
            str(id)

        print(len(imgs))

        error_flg = False

        for img in imgs:
            src = img.get("src")

            if "data_no" in src and "get-large" in src:

                data_no = src.split("data_no=")[1].split("&")[0]
                img_url = "http://image.oml.city.osaka.lg.jp/archive/get-media?data_no="+data_no
                thumb_url = "http://image.oml.city.osaka.lg.jp/archive/get-middle?data_no="+data_no

                try:
                    image = Image.open(urllib.request.urlopen(img_url))
                    width, height = image.size

                    obj = {
                        "img_url": img_url,
                        "thumb_url": thumb_url,
                        "width": width,
                        "height": height
                    }
                    array.append(obj)
                except:
                    print("Error Image.open")
                    error_flg = True
                    break

        if not error_flg:
            f2 = open(filename, 'w')
            json.dump(main, f2, ensure_ascii=False, indent=4,
                    sort_keys=True, separators=(',', ': '))
