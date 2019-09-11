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
# options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

odir = "data/images"

page = 0

flg = True

while(flg):

    page += 1

    time.sleep(1)

    url = "http://open-imagedata.city.kanazawa.ishikawa.jp/search/detail?dts=&dte=&q=&p="+str(page)

    filename = odir+"/"+url.split("_")[-1]+".json"

    if os.path.exists(filename):
        continue

    print("********\t"+url)

    main = {}
    array = []
    main["array"] = array

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'lxml')  # 要素を抽出

    thumbs = soup.find_all(class_="thumb")

    for i in range(len(thumbs)):

        main = {}
        array = []
        main["array"] = array

        id = thumbs[i].find("a").get("href").split("/")[-2]

        filename = "data/images/"+id+".json"

        if os.path.exists(filename):
            continue

        thumb_url = "http://open-imagedata.city.kanazawa.ishikawa.jp/image/thumbnail/"+thumbs[i].find("script").text.split("(")[1].split(", ")[0]
        img_url = thumb_url.replace("thumbnail", "regular")

        print(img_url)

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

            main["thumbnail"] = thumb_url

            f2 = open(filename, 'w')
            json.dump(main, f2, ensure_ascii=False, indent=4,
                    sort_keys=True, separators=(',', ': '))
        except:
            print("Error")
