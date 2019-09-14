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

categories = ["千葉県デジタルアーカイブ"]

prefix = "http://e-library.gprime.jp/lib_pref_chiba/da/"

for category in categories:

    flg = True
    p = 0

    while(flg):

        url = prefix+"result_sd?qf=&q=&start=" + \
            str(p*10) + \
            "&sort=タイトル_STRING asc, METADATA_ID asc&dispStyle=&fifq=&tilcod=&mode=result_sd&cond[item1_andOr]=and&cond[item1_cond]=in&cond[item2_andOr]=and&cond[item2_cond]=in&cond[item5_andOr]=and&cond[item5_cond]=in&category="+category

        p += 1

        print(str(p)+"\t"+category)

        r = requests.get(url)  # requestsを使って、webから取得
        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        divs = soup.find_all(class_="sdw_search_resultListLink")

        if len(divs) == 0:
            flg = False

        for div in divs:
            id = div.get("onclick").split("'")[1]

            url2 = prefix+"detail?tilcod="+id

            filename = "data/metadata/"+id+".json"

            if os.path.exists(filename):
                continue

            print(url2)

            obj = {}
            metadata = {}
            obj["metadata"] = metadata

            obj["url"] = url2
            obj["id"] = id
            obj["within"] = prefix+"top"
            obj["attribution"] = "千葉県デジタルアーカイブ"
            obj["license"] = prefix+"top"

            time.sleep(1)

            r = requests.get(url2)  # requestsを使って、webから取得

            soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

            
            trs = soup.find(class_="sdw_detailTable").find_all("tr")

            for tr in trs:
                if len(tr.find_all("th")) > 0:
                    th = tr.find("th").text.strip()
                    td = tr.find("td")

                    metadata[th] = []

                    if len(td.find_all("table")) == 0:
                        value = td.text.strip()
                        metadata[th].append(value)

                        if th == "書名" and len(metadata[th]) == 1:
                            obj["title"] = value
                    else:
                        tds = td.find_all("td")

                        for td in tds:
                            value = td.text.strip()
                            metadata[th].append(value)

                            if th == "書名" and len(metadata[th]) == 1:
                                obj["title"] = value
            

            f2 = open(filename, 'w')
            json.dump(obj, f2, ensure_ascii=False, indent=4,
                      sort_keys=True, separators=(',', ': '))