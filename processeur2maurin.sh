#!/bin/bash

INPUT='input/'
OUTPUT='output/'
LINE='------------------------------------------------------'

echo Here are all the files that the programme will run on :
echo $INPUT*.jpg
echo $LINE

for file in $INPUT*.jpg; do
	echo "$file"
	yaltai kraken --device cpu -I "$file" --suffix ".xml" segment --yolo /Users/Theo/Desktop/seg_models/big_seg_model_v2/weights/best.pt -i line_seg.mlmodel
	kraken -a -I "$file" -o _ocr.xml -f xml ocr -m kraken_htrtrained.mlmodel
done
#python csv_converter.py
