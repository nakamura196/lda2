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

categories = ["名古屋市史編纂資料【和装本】", "名古屋市史編纂資料【地図】", "名古屋市史資料写真集",
              "名古屋の絵葉書集", "鶴舞公園にあった動物園", "特別集書資料", "郷土検索データベース", "市政資料館資料検索"]

# ChromeのDriverオブジェクト生成時にオプションに引数を追加して渡す。
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

for category in categories:
    
    flg = True
    p = 0

    while(flg):

        url = "http://e-library2.gprime.jp/lib_city_nagoya/da/result?qf=&q=&start=" + \
            str(p*10)+"&sort=%E3%82%BF%E3%82%A4%E3%83%88%E3%83%AB_STRING+asc%2C+METADATA_ID+asc&dispStyle=&fifq=%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA%3A%E5%90%8D%E5%8F%A4%E5%B1%8B%E5%B8%82%E5%8F%B2%E7%B7%A8%E7%BA%82%E8%B3%87%E6%96%99%E3%80%90%E5%92%8C%E8%A3%85%E6%9C%AC%E3%80%91&tilcod=&mode=result&category="+category
            
        p += 1

        r = requests.get(url)  # requestsを使って、webから取得
        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        divs = soup.find_all(class_="sdw_search_resultListLink")

        if len(divs) == 0:
            flg = False

        for div in divs:
            id = div.get("onclick").split("'")[1]

            url2 = "http://e-library2.gprime.jp/lib_city_nagoya/da/detail?tilcod="+id

            

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

            time.sleep(2)

            check = []

            while(next_flg):

                soup = BeautifulSoup(driver.page_source, 'lxml')  # 要素を抽出

                imgs = soup.find(class_="sdw_detailViewLinkThumb").find_all("img")

                for img in imgs:
                    src = img.get("src")

                    thumb_url = "http://e-library2.gprime.jp/lib_city_nagoya/da/"+src

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
