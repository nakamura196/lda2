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

odir = "data/metadata"

flg = True
p = 0

while(flg):
    url = "https://iss.ndl.go.jp/api/opensearch?cnt=500&dpid=nwec-womens-da&idx=" + \
        str(p*500+1)
    # url = "https://iss.ndl.go.jp/api/opensearch?cnt=18106&dpid=nwec-womens-da"

    print(url)

    p += 1

    r = requests.get(url)  # requestsを使って、webから取得
    soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

    items = soup.find_all("item")

    print(len(items))

    if len(items) == 0:
        break

    for item in items:

        url = item.find("rdfs:seealso").get("rdf:resource")
       

        id = url.split("/")[-1]

        filename = odir+"/"+id+".json"

        if os.path.exists(filename):
            continue

        print(url)

        obj = {}
        metadata = {}
        obj["metadata"] = metadata

        obj["url"] = url
        obj["id"] = id
        obj["within"] = "http://www.i-repository.net/il/meta_pub/G0000337warchive"
        obj["attribution"] = "国立女性教育会館女性デジタルアーカイブシステム"
        obj["license"] = "http://www.i-repository.net/il/meta_pub/G0000337warchive"


        els = item.findChildren()
        for el in els:
            field = el.name.strip()
            value = el.text.strip()

            if ":" not in field or value == "":
                continue
            

            if field not in metadata:
                metadata[field] = []
            
            if value not in metadata[field]:
                metadata[field].append(value)

        f2 = open(filename, 'w')
        json.dump(obj, f2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

 

