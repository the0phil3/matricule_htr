#!/bin/bash

# Constants
INPUT='input/'
OUTPUT='output/'
LINE='--------------------------------------------------------------------------------------------------------'
files=("models/kraken_htrtrained.mlmodel" "models/line_seg.mlmodel" "models/best.pt")

# Check if all files are present
for file in "${files[@]}"; do
    if [ ! -e "$file" ]; then
        echo "Error: File $file is not present in the directory."
        exit 1  # Exit with an error code
    fi
done

# Pre-running messages
echo "All models are present in the directory."
echo Here are all the files that the programme will run on :
echo $INPUT*.jpg
echo $LINE

# Starts treatment
cd $INPUT
yaltai kraken --device cpu -I "*.jpg" --suffix ".xml" segment --yolo ../models/best.pt -i ../models/line_seg.mlmodel
kraken -a -I '*.xml' -o _ocr.xml -f xml ocr -m ../models/kraken_htrtrained.mlmodel
cd ..
find $INPUT -type f -name "*ocr*" -exec mv {} $OUTPUT \;

