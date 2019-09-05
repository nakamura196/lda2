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

files = glob.glob("data/images/*.csv")

rows = []
rows.append(["id", "img_url", "thumb_url", "width", "height"])

for file in sorted(files):
    print(file)

    f = open(file, 'r')

    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        rows.append(row)

    f.close()

df = pd.DataFrame(rows)

df.to_excel("data/images.xlsx", index=False, header=False)
