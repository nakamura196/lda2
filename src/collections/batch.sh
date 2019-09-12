echo ' --- 01 ---'
python 01_create_metadata.py ../../collections_data/nagoya/data/config.yml
echo ' ---- 02 ----'
python 02_create_images.py ../../collections_data/nagoya/data/config.yml
echo ' ---- 12 ----'
python 12_create_manifest.py ../../collections_data/nagoya/data/config.yml
echo ' ---- 13 ----'
python 13_create_collection.py ../../collections_data/nagoya/data/config.yml
echo ' ---- 20 ----'
python 20_collection_converter.py /Users/nakamura/git/min_a/lda2/docs/nagoya/collection.json /Users/nakamura/git/min_a/lda2/docs/nagoya/items.json
