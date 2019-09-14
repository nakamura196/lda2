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


url = "https://www.lib.pref.ibaraki.jp/guide/shiryou/digital_lib/digital_lib_main.html#sonota"

r = requests.get(url)  # requestsを使って、webから取得

soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

aas = soup.find_all("a")

for j in range(len(aas)):
    a = aas[j]

    if a.get("href") != None and "valuable_m" in a.get("href"):

        url = "https://www.lib.pref.ibaraki.jp/guide/shiryou/digital_lib/"+a.get("href")

        print(url)

        id = url.split("/")[-2]

        filename = "data/images/"+id+".json"

        if os.path.exists(filename):
            continue

        main = {}
        array = []
        main["array"] = array

        time.sleep(1)

        r = requests.get(url)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        imgs = soup.find_all("a")

        if len(imgs) != 0:

            for img in imgs:
                src = img.get("href")

                if ".png" in src or ".jpg" in src:

                    last = url.split("/")[-1]

                    thumb_url = url.replace("/"+last, "/")+src
                    print(thumb_url)

                    img_url = thumb_url

                    image = Image.open(urllib.request.urlopen(img_url))
                    width, height = image.size

                    obj = {
                        "img_url": img_url,
                        "thumb_url": thumb_url,
                        "width": width,
                        "height": height
                    }
                    array.append(obj)

                    if "thumbnail" not in main:

                        main["thumbnail"] = thumb_url
                else:
                    continue

        

        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
