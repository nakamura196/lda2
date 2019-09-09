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

        filename = "data/metadata/"+id+".json"

        if os.path.exists(filename):
                continue

        result = flickr.photos.getInfo(
            photo_id=photo_id
        )

        obj = result["photo"]


        main = {}
        metadata = {}
        main["metadata"] = metadata

        main["title"] = obj["title"]["_content"]
        main["url"] = "https://www.flickr.com/photos/tsuyama-lib/"+id+"/"
        main["id"] = id
        main["within"] = "https: // www.flickr.com/photos/tsuyama-lib"
        main["attribution"] = "津山市立図書館/Public Library of Tsuyama City"
        main["license"] = "http://creativecommons.org/licenses/by/4.0/"

        tags = obj["tags"]["tag"]

        main["metadata"]["tag"] = []

        for tag in tags:
            main["metadata"]["tag"].append(tag["raw"])

        description = obj["description"]["_content"]

        objs = description.split("\n")

        for e in objs:
            # print(e)
            tmp = e.split("：")
            if len(tmp) == 1:
                continue
            field = tmp[0].strip()
            value = tmp[1].strip()

            if field not in metadata:
                metadata[field] = []

            if value not in metadata[field]:
                metadata[field].append(value)


        f2 = open(filename, 'w')
        json.dump(main, f2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

