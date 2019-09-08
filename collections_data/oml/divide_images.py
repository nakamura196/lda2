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

main = {}

files = glob.glob("data/images/*.csv")

for file in sorted(files):

    f = open(file, 'r')

    reader = csv.reader(f)
    header = next(reader)
    for row in reader:

        id = row[0]
        img_url = row[1]
        thumb_url = row[2]
        width = row[3]
        height = row[4]

        if id not in main:
            main[id] = {
                "thumbnail" : thumb_url,
                "array": []
            }

        main[id]["array"].append(
            {
                "img_url" : img_url,
                "thumb_url" : thumb_url,
                "width" : width,
                "height": height
            }
        )

    f.close()


for id in main:
    f2 = open("data/images/"+id+".json", 'w')
    json.dump(main[id], f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
