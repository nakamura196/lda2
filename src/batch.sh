python 01_create_metadata.py data/nishinomiya/data/config.yml
python 02_create_images.py data/nishinomiya/data/config.yml
python 12_create_manifest.py data/nishinomiya/data/config.yml
python 13_create_collection.py data/nishinomiya/data/config.yml
python 20_collection_converter.py /Users/nakamura/git/min_a/lda2/docs/nishinomiya/collection.json /Users/nakamura/git/min_a/lda2/docs/nishinomiya/items.json
python 21_collection_converter4es.py /Users/nakamura/git/min_a/lda2/docs/nishinomiya/collection.json /Users/nakamura/git/min_a/lda2/docs/nishinomiya/rows.json
python 30_create_uni.py data/nishinomiya/data/config.yml
