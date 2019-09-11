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

files = glob.glob("data/metadata2/*.html")

for i in range(len(sorted(files))):
    
    file = files[i]

    soup = BeautifulSoup(open(file), "lxml")

    id = file.split("/")[-1].split(".")[0]

    print(str(i+1)+"/"+str(len(files))+"\t"+id)

    filename = "data/metadata/"+id+".json"

    if os.path.exists(filename):
        continue

    if len(soup) == 0:
        continue

    url = soup.find(class_="sanshoUrl").text.split("このページのURL：")[1].strip()

    main = {}
    main["metadata"] = {}

    main["title"] = soup.find(id="contentHead").text.strip()
    main["url"] = url
    main["id"] = id
    main["within"] = "http://www3.library.pref.hokkaido.jp/digitallibrary/"
    main["attribution"] = "北方資料デジタル・ライブラリー"
    main["license"] = "http://www3.library.pref.hokkaido.jp/digitallibrary/"

    ms = soup.find_all(class_="detail-data-set")

    for m in ms:
        field = m.find(class_="detail-title").text.strip()
        value = m.find(class_="detail-value").text.strip()
        if len(value) != 0:
            main["metadata"][field] = value


    f2 = open(filename, 'w')
    json.dump(main, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
