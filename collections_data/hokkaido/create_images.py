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

files = glob.glob("data/html2/*.html")

for i in range(len(files)):
    file = files[i]

    print(str(i+1)+"/"+str(len(files)))

    soup = BeautifulSoup(open(file), "lxml")

    id = file.split("/")[-1].split(".")[0]

    filename = "data/images/"+id+".json"

    if os.path.exists(filename):
        continue

    main = {}
    array = []
    main["array"] = array

    top = id.split("-")[1]

    if soup.find(id="thumbnailArea_view") == None:
        continue

    aas = soup.find(id="thumbnailArea_view").find_all(class_="thumbnailImg")

    print("画像数: "+str(len(aas))+ "\t"+id)

    error_flg = False

    for i in range(len(aas)):
        a = aas[i]

        img_id = a.find("a").get("href").split("\"")[1]

        img_url = "http://www3.library.pref.hokkaido.jp/digitallibrary/dsearch/ics/viewer/iipsrv.fcgi?FIF=/" + \
            top+"/"+img_id+"/"+img_id+"_" + \
                str(i+1).zfill(7)+".jp2&WID=full&CVT=jpeg"
        print(img_url)

        thumb_url = img_url.replace("full", "300")

        if i == 0:
            main["thumbnail"] = thumb_url

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
        except:
            error_flg = True
            print("Image open Error")
            break

    if not error_flg:

        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
