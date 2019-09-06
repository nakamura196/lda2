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

map = {}

rows = []
row = ["id", "img_url", "thumb_url", "width", "height"]
rows.append(row)

rows2 = []
row2 = ["id", "thumb_url"]
rows2.append(row2)

for j in range(1, r_count):

    if j < 3391:
        continue

    id = df.iloc[j, 0]
    num = df.iloc[j, 87]

    print(str(j)+"/"+str(r_count))

    if not pd.isnull(num) and num != 0:
        url = "http://image.oml.city.osaka.lg.jp/archive/detail.do?id="+str(id)
        print(url)

        time.sleep(1)

        r = requests.get(url)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        imgs = soup.find_all("img")

        print("画像数: "+str(len(imgs)-11))

        thumb_flg = True

        thumb_url = "http://image.oml.city.osaka.lg.jp/archive/get-thumbnail?data_no="+str(id)
                    
        row2 = [id, thumb_url]
        rows2.append(row2)

        for img in imgs:
            src = img.get("src")
            

            if "data_no" in src and "get-large" in src:
                # print(src)
                data_no = src.split("data_no=")[1].split("&")[0]
                img_url = "http://image.oml.city.osaka.lg.jp/archive/get-media?data_no="+data_no
                thumb_url = "http://image.oml.city.osaka.lg.jp/archive/get-middle?data_no="+data_no

                print(img_url)

                image = Image.open(urllib.request.urlopen(img_url))
                width, height = image.size

                row = [id, img_url, thumb_url, width, height]
                rows.append(row)

                    

                    

    # break

    if j % 10 == 0:

        f = open("data/images/images_"+str(j).zfill(5)+".csv", 'w')

        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(rows)

        f.close()

        f = open("data/thumbnails/thumbnails_"+str(j).zfill(5)+".csv", 'w')

        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(rows2)

        f.close()

        rows = []
        row = ["id", "img_url"]
        rows.append(row)

        rows2 = []
        row2 = ["id", "thumb_url"]
        rows2.append(row2)


