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

# ChromeのDriverオブジェクト生成時にオプションに引数を追加して渡す。
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

prefix = "http://e-library.gprime.jp/lib_pref_chiba/da/"

for category in categories:
    
    flg = True
    p = 0

    while(flg):

        url = prefix+"result_sd?qf=&q=&start=" + \
            str(p*10)+"&sort=%E3%82%BF%E3%82%A4%E3%83%88%E3%83%AB_STRING+asc%2C+METADATA_ID+asc&dispStyle=&fifq=&tilcod=&mode=result_sd&cond%5Bitem11_andOr%5D=and&cond%5Bitem11_cond%5D=in&cond%5Bitem12_andOr%5D=and&cond%5Bitem12_cond%5D=in&cond%5Bitem2_andOr%5D=and&cond%5Bitem2_cond%5D=in&cond%5Bitem3_andOr%5D=and&cond%5Bitem3_cond%5D=in&cond%5Bitem6_andOr%5D=and&cond%5Bitem6_cond%5D=in&cond%5Bitem8_andOr%5D=and&cond%5Bitem8_cond%5D=in&category="+category

        p += 1

        r = requests.get(url)  # requestsを使って、webから取得
        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        divs = soup.find_all(class_="sdw_search_resultListLink")

        if len(divs) == 0:
            flg = False

        for div in divs:
            id = div.get("onclick").split("'")[1]

            url2 = prefix+"detail?tilcod="+id

            

            filename = "data/images/"+id+".json"

            if os.path.exists(filename):
                continue

            print(url2)


            main = {}
            array = []
            main["array"] = array

            next_flg = True

            error_flg = False

            driver.get(url2)

            time.sleep(5)

            check = []

            while(next_flg):
                

                soup = BeautifulSoup(driver.page_source, 'lxml')  # 要素を抽出

                if soup.find(class_="sdw_detailViewLinkThumb") == None:
                    next_flg = False

                    src = soup.find(
                        class_="sdw_detailViewBaseImageContainer").find("img").get("src")

                    thumb_url = prefix+src

                    img_url = thumb_url.replace("=thumb", "=org")

                    if img_url in check:
                        continue

                    print(img_url)

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

                    if "thumbnail" not in main:
                        main["thumbnail"] = thumb_url
                    

                else:

                    imgs = soup.find(class_="sdw_detailViewLinkThumb").find_all("img")

                    for img in imgs:
                        src = img.get("src")

                        thumb_url = prefix+src

                        img_url = thumb_url.replace("=thumb", "=org")

                        if img_url in check:
                            continue

                        print(img_url)

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

                        if "thumbnail" not in main:
                            main["thumbnail"] = thumb_url

                    try:
                        driver.find_element_by_class_name(
                            "sdw_detailViewLinkButtonFwd").click()
                    except:
                        next_flg = False

            if not error_flg:
                f2 = open(filename, 'w')
                json.dump(main, f2, ensure_ascii=False, indent=4,
                        sort_keys=True, separators=(',', ': '))
          


            
driver.quit()
