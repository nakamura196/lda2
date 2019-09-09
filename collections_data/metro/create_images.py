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

categories = ["絵葉書・写真帖"]

# ChromeのDriverオブジェクト生成時にオプションに引数を追加して渡す。
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

for category in categories:

    

    

    flg = True
    p = 0

    while(flg):

        url = "http://archive.library.metro.tokyo.jp/da/result_sd?qf=&q=&start=" + \
            str(10*p)+"&sort=タイトル_STRING asc, METADATA_ID asc&dispStyle=&tilcod=&mode=result_sd&cond[item0_andOr]=and&cond[item0_cond]=in&cond[item10_andOr]=and&cond[item10_cond]=in&cond[item11_andOr]=and&cond[item11_cond]=in&cond[item12_andOr]=and&cond[item12_cond]=in&cond[item13_andOr]=and&cond[item13_cond]=in&cond[item14_andOr]=and&cond[item14_cond]=in&cond[item15_andOr]=and&cond[item15_cond]=in&cond[item16_andOr]=and&cond[item16_cond]=in&cond[item17_andOr]=and&cond[item17_cond]=in&cond[item18_andOr]=and&cond[item18_cond]=in&cond[item19_andOr]=and&cond[item19_cond]=in&cond[item20_andOr]=and&cond[item20_cond]=eq&cond[item2_andOr]=and&cond[item2_cond]=in&cond[item3_andOr]=and&cond[item3_cond]=in&cond[item4_andOr]=and&cond[item4_cond]=in&cond[item8_andOr]=and&cond[item8_cond]=in&cond[item9_andOr]=and&cond[item9_cond]=in&category=江戸城"

        p += 1

        r = requests.get(url)  # requestsを使って、webから取得
        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        divs = soup.find_all(class_="sdw_search_resultListLink")

        for div in divs:
            id = div.get("onclick").split("'")[1]

            url2 = "http://archive.library.metro.tokyo.jp/da/detail?tilcod="+id

            print(url2)


            filename = "data/images/"+id+".json"

            if os.path.exists(filename):
                continue

            main = {}
            array = []
            main["array"] = array

            driver.get(url2)

            time.sleep(1)

            img_url = driver.find_element_by_id(
                "sdw_image").get_attribute("src").replace("=view", "=org")
            thumb_url = img_url.replace("=org", "=thumb")
            print(img_url)

            max = int(driver.find_element_by_id(
                "thumbTotalCount").text)

            main["thumbnail"] = thumb_url

            r = requests.get(url2)  # requestsを使って、webから取得

            soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

            '''
            trs = soup.find(class_="sdw_detailTable").find_all("tr")

            # print(trs)

            for tr in trs:
                if len(tr.find_all("th")) > 0:
                    th = tr.find("th").text.strip()
                    td = tr.find("td").text.strip()

                    print(th+"\t"+td)

            time.sleep(1)
            '''

            

            if max != 1:
                continue

            image = Image.open(urllib.request.urlopen(img_url))
            width, height = image.size

            obj = {
                "img_url": img_url,
                "thumb_url": thumb_url,
                "width": width,
                "height": height
            }
            array.append(obj)

            f2 = open(filename, 'w')
            json.dump(main, f2, ensure_ascii=False, indent=4,
                      sort_keys=True, separators=(',', ': '))


            
driver.quit()
