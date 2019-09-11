cd collections

echo "metro"
python create_batch.py ../../collections_data/metro/data/config.yml
sh batch.sh

echo "nagoya"
python create_batch.py ../../collections_data/nagoya/data/config.yml
sh batch.sh

echo "hokkaido"
python create_batch.py ../../collections_data/hokkaido/data/config.yml
sh batch.sh