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

check = []

odir = "data/metadata"

with open('data/html.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:

        url = row[0]

        print("********\t"+url)

        id = url.split("_")[-1]

        filename = odir+"/"+id+".json"

        if os.path.exists(filename):
            continue

        time.sleep(1)

        r = requests.get(url)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        main = {}
        main["metadata"] = {}

        main["title"] = soup.find(class_="infolib_section").text.strip()
        main["url"] = url
        main["id"] = id
        main["within"] = "http://www.i-repository.net/il/meta_pub/G0000307library"
        main["attribution"] = "県立長野図書館"
        main["license"] = "http://creativecommons.org/publicdomain/mark/1.0/"

        trs = soup.find(class_="detail_tbl").find_all("tr")

        for tr in trs:

            tds = tr.find_all("td")

            if tds != None and len(tds) == 2:

                main["metadata"][tds[0].text.strip()
                                ] = tds[1].text.strip()

        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

