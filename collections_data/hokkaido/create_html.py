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

check = []


# ChromeのDriverオブジェクト生成時にオプションに引数を追加して渡す。
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

url = "http://www3.library.pref.hokkaido.jp/digitallibrary/dsearch/da/fwsearch.php?name%5B%5D=%E3%83%95%E3%83%AA%E3%83%BC%E3%83%AF%E3%83%BC%E3%83%89"

driver.get(url)

flg = True

page = 0

while(flg):

    page += 1

    print(page)

    path = "data/html/"+str(page).zfill(6)+".html"

    time.sleep(2)

    if not os.path.exists(path):

        

        source = driver.page_source
        
        with open(path, mode='w') as f:
            f.write(source)

    try:
        driver.find_element_by_class_name("next").click()
    except:
        print("No next")
        flg = False

'''

odir = "data/images"

with open('data/html.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:

        url = row[0]

        filename = odir+"/"+url.split("_")[-1]+".json"

        if os.path.exists(filename):
            continue

        print("********\t"+url)

        main = {}
        array = []
        main["array"] = array

        driver.get(url)
        time.sleep(5)

        text = driver.find_element_by_id(
            "contviewer_url").text

        if len(text) == 0:
            print("空？")
            continue

        img_url = text.split("のURL:")[1]

        if img_url != "":

            print(img_url)

            thumb_url = img_url.replace(".jpg", "_ls.jpg")

            main["thumbnail"] = thumb_url

            image = Image.open(urllib.request.urlopen(img_url))
            width, height = image.size

            obj = {
                "img_url": img_url,
                "thumb_url": thumb_url,
                "width": width,
                "height": height
            }
            array.append(obj)
        else:
            print("空？")
            continue

        driver.find_element_by_id("toolbar_xpanelcont_next").click()

        flg = True

        while(flg):

            tmp = driver.find_element_by_id(
                "contviewer_url").text.split("のURL:")

            img_url = tmp[1]
            print(img_url)

            thumb_url = img_url.replace(".jpg", "_ls.jpg")

            image = Image.open(urllib.request.urlopen(img_url))
            width, height = image.size

            obj = {
                "img_url": img_url,
                "thumb_url": thumb_url,
                "width": width,
                "height": height
            }
            array.append(obj)

            if img_url in check:
                flg = False
            else:

                check.append(img_url)
                driver.find_element_by_id("toolbar_xpanelcont_next").click()

        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

'''

driver.quit()
