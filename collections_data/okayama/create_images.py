from flickrapi import FlickrAPI
from urllib.request import urlretrieve
import os
import time
import sys
import json

# 「事前準備」で取得したAPI KeyとSecret Keyを設定
key = "a66ab3613dca3151a1f91c94d435f917"
secret = "d86ef83022cd8573"

# 接続クライアントの作成とサーチの実行
flickr = FlickrAPI(key, secret, format='parsed-json')

page = 1

flg = True

while(flg):


    result = flickr.photos.search(
        user_id="162440869@N03",           # 検索キーワード
        page=page
    )

    pages = result["photos"]["pages"]

    if page == pages:
        flg = False
    page += 1

    # 結果の取り出しと格納
    photos = result['photos']


    for i, photo in enumerate(photos['photo']):

        print(i)

        main = {}
        array = []
        main["array"] = array

        photo_id = photo["id"]
        id = photo_id

        filename = "data/images/"+id+".json"
        

        if os.path.exists(filename):
                continue

        result = flickr.photos.getSizes(
            photo_id=photo_id
        )    

        sizes = result["sizes"]["size"]

        medium = sizes[5]

        original = sizes[7]

        obj = {
            "img_url": original["source"],
            "thumb_url": medium["source"],
            "width": int(original["width"]),
            "height": int(original["height"])
        }

        main["thumbnail"] = medium["source"]
        array.append(obj)

        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
        