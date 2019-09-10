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

url = "https://iss.ndl.go.jp/api/oaipmh?verb=ListRecords&metadataPrefix=dcndl_simple&set=ibaraki&from=2014-10-01"

r = requests.get(url)  # requestsを使って、webから取得

soup = BeautifulSoup(r.text, 'xml')  # 要素を抽出

metadatas = soup.find_all("metadata")

print(len(metadatas))

for metadata in metadatas:
    print(metadata)
    seeAlso = metadata.find("rdfs:seeAlso").get("rdf:resource")
    print(seeAlso)

'''



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

    if a.get("href") != None and "mkey" in a.get("href"):

        url = "https://archives.nishi.or.jp/"+a.get("href")

        if url in urls:
            continue

        urls.append(url)

        print(url)

        id = url.split("=")[-1]

        filename = "data/images/"+id+".json"

        if os.path.exists(filename):
            continue

        main = {}
        array = []
        main["array"] = array

        time.sleep(1)

        r = requests.get(url)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        imgs = soup.find(class_="group").find_all("img")

        thumb_flg = True

        if len(imgs) != 0:

            continue

            for img in imgs:
                src = img.get("src")

                if "media/thumb" in src:

                    thumb_url = "https://archives.nishi.or.jp/"+src
                    img_url = thumb_url.replace("/thumb/", "/middle/")

                    image = Image.open(urllib.request.urlopen(img_url))
                    width, height = image.size

                    obj = {
                        "img_url": img_url,
                        "thumb_url": thumb_url,
                        "width": width,
                        "height": height
                    }
                    array.append(obj)

                    if thumb_flg:

                        main["thumbnail"] = thumb_url

                        thumb_flg = False

        else:
            imgs = soup.find_all("img")

            for img in imgs:
                src = img.get("src")
                if "media/middle" in src:

                    img_url = "https://archives.nishi.or.jp/"+src
                    thumb_url = img_url.replace("/middle/", "/thumb/")

                    image = Image.open(urllib.request.urlopen(img_url))
                    width, height = image.size

                    obj = {
                        "img_url": img_url,
                        "thumb_url": thumb_url,
                        "width": width,
                        "height": height
                    }
                    array.append(obj)

                    if thumb_flg:

                        main["thumbnail"] = thumb_url

                        thumb_flg = False

        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
'''
