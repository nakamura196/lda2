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

        url = "https://www.lib.pref.ibaraki.jp/guide/shiryou/digital_lib/" + \
            a.get("href")

        print(url)

        id = url.split("/")[-2]

        filename = "data/metadata/"+id+".json"

        if os.path.exists(filename):
            continue

        r = requests.get(url)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.content, 'html.parser')

        main = {}
        main["metadata"] = {}

        # main["title"] = soup.find(id="contentHead").text.strip()
        main["url"] = url
        main["id"] = id
        main["within"] = "https://www.lib.pref.ibaraki.jp/guide/shiryou/digital_lib/digital_lib_main.html"
        main["attribution"] = "茨城県立図書館デジタルライブラリー"
        main["license"] = "https://www.lib.pref.ibaraki.jp/guide/shiryou/digital_lib/digital_lib_main.html"

        trs = soup.find_all("tr")

        for tr in trs:
            tds = tr.find_all("td")
            if len(tds) == 0:
                continue
            field = tds[0].text.strip()
            value = tds[1].text.strip()

            if field == "書名":
                main["title"] = value
            else:

                main["metadata"][field] = value

            


        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
