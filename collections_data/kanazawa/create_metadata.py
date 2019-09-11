from selenium.webdriver.chrome.options import Options
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

import time
from selenium import webdriver


# ChromeのDriverオブジェクト生成時にオプションに引数を追加して渡す。
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

odir = "data/images"

page = 0

flg = True

while(flg):

    page += 1

    time.sleep(1)

    url = "http://open-imagedata.city.kanazawa.ishikawa.jp/search/detail?dts=&dte=&q=&p=" + \
        str(page)

    filename = odir+"/"+url.split("_")[-1]+".json"

    if os.path.exists(filename):
        continue

    print("********\t"+url)

    

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')  # 要素を抽出

    thumbs = soup.find_all(class_="thumb")

    for i in range(len(thumbs)):

        main = {}
        array = []
        main["array"] = array

        url = thumbs[i].find("a").get("href")
        print(url)

        id = url.split("/")[-2]

        filename = "data/metadata/"+id+".json"

        if os.path.exists(filename):
            continue

        obj = {}
        metadata = {}
        obj["metadata"] = metadata

        obj["url"] = url
        obj["id"] = id
        obj["within"] = "http://open-imagedata.city.kanazawa.ishikawa.jp/"
        obj["attribution"] = "金沢市画像オープンデータ"
        # obj["license"] = "http://archive.library.metro.tokyo.jp/da/windowTokyo"

        r = requests.get(url)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        trs = soup.find(class_="table").find_all("tr")

        for tr in trs:
            field = tr.find("th").text.strip()
            if field == "ライセンス":
                value = tr.find("a").get("href").split("/jp")[0]
                obj["license"] = value
            elif field == "タイトル":
                obj["title"] = tr.find("td").text.strip()
            else:
                value = tr.find("td").text.strip()

                metadata[field] = value

        f2 = open(filename, 'w')
        json.dump(obj, f2, ensure_ascii=False, indent=4,
                    sort_keys=True, separators=(',', ': '))
