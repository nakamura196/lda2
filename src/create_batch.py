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
import argparse
import sys


def parse_args(args=sys.argv[1:]):
    """ Get the parsed arguments specified on this script.
    """
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        'config_path',
        action='store',
        type=str,
        help='config path.')

    return parser.parse_args(args)


args = parse_args()

config_path = args.config_path

f = open(config_path, "r+")
config = yaml.load(f)

data_dir = config["data_dir"]
output_dir = config["output_dir"]
prefix = config["prefix"]
label = config["label"]

collection_path = output_dir+"/collection.json"

rows = [
    ["python create_metadata.py "+config_path],
    ["python create_images.py "+config_path],
    ["python 12_create_manifest.py "+config_path],
    ["python 13_create_collection.py "+config_path],
    ["python collection_converter.py "+collection_path+" "+output_dir+"/items.json"],
    ["python collection_converter4es.py "+collection_path +
        " "+output_dir+"/rows.json"],
    ["python create_uni.py"]
]


f = open("batch.sh", 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()
