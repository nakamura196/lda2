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

driver = webdriver.Chrome()
driver.get('http://www.i-repository.net/il/meta_pub/G0000307library')
time.sleep(1)

driver.find_element_by_xpath(("//*[text()=\"画像\"]")).click()

time.sleep(1)


driver.find_element_by_id("image_list").click()

flg = True

check = []
rows = []
rows.append(["url"])

while(flg):

    url = driver.find_element_by_id("infolib_permalink").text

    if url in check:
        flg = False
    else:

        rows.append([url])
        check.append(url)


        driver.find_element_by_class_name("fa-angle-right").click()


driver.quit()

f = open("data/html.csv", 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()
