import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import glob
import hashlib
import yaml

path = "data/adachi/data/md5.csv"

f = open(path, 'r')
rows = []
reader = csv.reader(f)

for row in reader:
    hash = hashlib.md5(row[0].encode('utf-8')).hexdigest()
    row2 = [row[0], hash]
    rows.append(row2)

f = open(path+".csv", 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()
