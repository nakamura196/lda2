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

files = glob.glob("data/html/*.html")

# ChromeのDriverオブジェクト生成時にオプションに引数を追加して渡す。
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

for i in range(len(files)):
    file = files[i]

    print(str(i+1)+"/"+str(len(files)))

    soup = BeautifulSoup(open(file), "lxml")

    aas = soup.find_all(class_="thumnailLinkImg")

    for j in range(len(aas)):
        a = aas[j]

        url = "http://www3.library.pref.hokkaido.jp"+a.get("href")

        print(str(j+1)+"/"+str(len(aas))+"\t"+url)

        id = url.split("=")[-1]

        filename = "data/html2/"+id+".html"

        if os.path.exists(filename):
            continue

        driver.get(url)

        filename2 = "data/metadata2/"+id+".html"

        source2 = driver.page_source

        try:
            driver.find_element_by_id("ui-id-2").click()

            time.sleep(1)

            source = driver.page_source

            if "thumbnailImg" in source:

                with open(filename2, mode='w') as f:
                    f.write(source2)

                with open(filename, mode='w') as f:
                    f.write(source)

            elif "dataIcon" in source:

                with open(filename2, mode='w') as f:
                    f.write("")

                with open(filename, mode='w') as f:
                    f.write("")

            else:
                print("None")
        except:
            continue

driver.quit()
