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

flg = True
p = 0

while(flg):
    url = "https://iss.ndl.go.jp/api/opensearch?cnt=500&dpid=nwec-womens-da&idx="+str(p*500+1)

    p += 1

    r = requests.get(url)  # requestsを使って、webから取得
    soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

    items = soup.find_all("item")

    if len(items) == 0:
        break

    for item in items:

        url = item.find("rdfs:seealso").get("rdf:resource")

        filename = odir+"/"+url.split("/")[-1]+".json"

        if os.path.exists(filename):
            continue

        print("********\t"+url)

        main = {}
        array = []
        main["array"] = array

        driver.get(url)

        els = driver.find_elements_by_class_name(
            "xinfolib_bt_span")

        try:
            els[3].click()
        except:
            print("画像なし？")
            continue

        time.sleep(2)

        text = driver.find_element_by_id(
            "contviewer_url").text

        if len(text) == 0:
            print("空？")
            continue

        img_url = text.split("URL:")[1]

        check = []

        if img_url != "" and img_url not in check:

            check.append(img_url)

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
                "contviewer_url").text.split("URL:")

            img_url = tmp[1]
            

            if img_url in check:
                break

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

            check.append(img_url)
            driver.find_element_by_id("toolbar_xpanelcont_next").click()

        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                    sort_keys=True, separators=(',', ': '))


driver.quit()
