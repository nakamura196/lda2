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


df = pd.read_excel("data/metadata_bk.xlsx", sheet_name=0,
                   header=None, index_col=None)

map = {}

r_count = len(df.index)
c_count = len(df.columns)

map = {}

description_index = None
logo_index = None

for i in range(0, c_count):
    label = df.iloc[0, i]
    uri = df.iloc[1, i]
    # type = df.iloc[2, i]
    target = df.iloc[3, i]

    if target == "metadata":
        obj = {}
        map[i] = obj
        obj["label"] = label

    if uri == "http://purl.org/dc/terms/rights":
        license_index = i
    if uri == "http://purl.org/dc/terms/title":
        title_index = i
    if uri == "http://purl.org/dc/terms/description":
        description_index = i
    if uri == "http://www.w3.org/2000/01/rdf-schema#seeAlso":
        seeAlso_index = i
    if uri == "http://purl.org/dc/terms/identifier":
        identifier_index = i
    if label == "logo":
        logo_index = i
    if label == "attribution":
        attribution_index = i
    if label == "within":
        within_index = i
    if label == "viewingDirection":
        viewingDirection_index = i
    if uri == "http://purl.org/dc/terms/relation":
        related_index = i

for j in range(4, r_count):

    print(str(j)+"/"+str(r_count))

    # id = df.iloc[j, identifier_index]

    

    # manifest_uri = prefix+"/"+dir_name+"/manifest/"+filename

    relation = df.iloc[j, related_index]

    title = df.iloc[j, title_index]

    url = df.iloc[j, related_index]
    id = url.split("=")[1]

    filename = "data/metadata/"+id+".json"

    obj = {
        "attribution": df.iloc[j, attribution_index],
        "id": id,
        "license": df.iloc[j, license_index],
        "metadata": {},
        "title": df.iloc[j, title_index],
        "url": url,
        "within": df.iloc[j, within_index]
    }

    for index in map:
        value = df.iloc[j, index]
        if not pd.isnull(value) and value != 0:
            values = str(value).split(",")
            for value in values:
                obj["metadata"][map[index]["label"]] = value.strip()

    f2 = open(filename, 'w')
    json.dump(obj, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))


'''

for j in range(1, r_count):

    id = df.iloc[j, 0]
    image = df.iloc[j, 1]
    thumbnail = df.iloc[j, 2]
    width = int(df.iloc[j, 3])
    height = int(df.iloc[j, 4])

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

'''
