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

path = "data/omlDAdataset.xlsx"

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

    if j < 821:
        continue

    id = df.iloc[j, 0]
    num = df.iloc[j, 87]

    print(j)

    if not pd.isnull(num) and num != 0:
        for k in range(0, num):
            url = "http://image.oml.city.osaka.lg.jp/archive/detail.do?id="+str(id)
            # print(url)

            time.sleep(1)

            r = requests.get(url)  # requestsを使って、webから取得

            soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

            imgs = soup.find_all("img")

            thumb_flg = True

            for img in imgs:
                src = img.get("src")
                

                if "data_no" in src and "get-large" in src:
                    # print(src)
                    data_no = src.split("data_no=")[1].split("&")[0]
                    img_url = "http://image.oml.city.osaka.lg.jp/archive/get-media?data_no="+data_no
                    thumb_url = "http://image.oml.city.osaka.lg.jp/archive/get-thumbnail?data_no="+data_no

                    image = Image.open(urllib.request.urlopen(img_url))
                    width, height = image.size

                    row = [id, img_url, thumb_url, width, height]
                    rows.append(row)

                    if thumb_flg:
                        
                        row2 = [id, thumb_url]
                        rows2.append(row2)

                        thumb_flg = False

                    

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


