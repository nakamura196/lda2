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

files = glob.glob("data/metadata/*.json")

# ChromeのDriverオブジェクト生成時にオプションに引数を追加して渡す。
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)

for i in range(len(files)):
    print(str(i+1)+"/"+str(len(files)))

    file = files[i]

    # jsonファイルを読み込む
    f = open(file)
    # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
    data = json.load(f)
    # ファイルを閉じる
    f.close()


    id = data["id"]

    url2 = data["url"]

    filename = "data/images/"+id+".json"

    if os.path.exists(filename):
        continue

    print(url2)

    main = {}
    array = []
    main["array"] = array

    driver.get(url2)

    r = requests.get(url2)  # requestsを使って、webから取得

    soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

    try:
        driver.find_element_by_id(
            "originalImage").click()
    except:
        print("Init Error: 拡大ボタンを押せませんでした。")
        continue

    next_flg = True

    first_flg = True

    error_flg = False

    while(next_flg):

        time.sleep(1)

        try:

            if first_flg:
                img_url = driver.find_element_by_id(
                    "sdw_image").get_attribute("src").replace("=view", "=org")

            else:
                img_url = driver.find_element_by_class_name(
                    "cboxPhoto").get_attribute("src").replace("=view", "=org")

            print(img_url)

            thumb_url = img_url.replace("=org", "=thumb")

            image = Image.open(urllib.request.urlopen(img_url))
            width, height = image.size

            obj = {
                "img_url": img_url,
                "thumb_url": thumb_url,
                "width": width,
                "height": height
            }
            array.append(obj)

            if "thumbnail" not in main:
                main["thumbnail"] = thumb_url

            first_flg = False

            try:
                cboxNext = driver.find_element_by_id(
                    "cboxNext").get_attribute("style")
            except:
                next_flg = False

            if "float: left;" == cboxNext:

                driver.find_element_by_id(
                    "cboxNext").click()
            else:

                next_flg = False

  
        except:
            print("Second Error")
            error_flg = True
            next_flg = False

        

    if not error_flg:
        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                    sort_keys=True, separators=(',', ': '))


driver.quit()
