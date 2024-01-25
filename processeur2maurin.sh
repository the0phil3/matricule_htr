#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# Constants
INPUT='input/'
OUTPUT='output/'
LINE='--------------------------------------------------------------------------------------------------------'
files=("models/kraken_htrtrained.mlmodel" "models/line_seg.mlmodel" "models/best.pt")

# General checks before running
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}Error:${NC} This script must be run within a virtual environment."
    exit 1
fi

# Check if the required libraries are installed
if ! pip check requirements.txt; then
     echo -e "${RED}Error:${NC} Some or all required libraries are not installed. Please install them using 'pip install -r requirements.txt'."
    exit 1
fi

for file in "${files[@]}"; do
    if [ ! -e "$file" ]; then
        echo -e "${RED}Error:${NC} File $file is not present in the directory."
        exit 1  # Exit with an error code
    fi
done

# Create input and output directories if they don't exist
mkdir -p "$INPUT"
mkdir -p "$OUTPUT"

# Pre-running messages
echo -e "${GREEN}Success:${NC} Script is running in a virtual environment with the required libraries installed."
echo -e "${GREEN}Success:${NC} All models are present in the directory."
echo Here are all the files that the programme will run on :
echo $INPUT*.jpg
echo $LINE

# Starts treatment
cd $INPUT
yaltai kraken --device cpu -I "*.jpg" --suffix ".xml" segment --yolo ../models/best.pt -i ../models/line_seg.mlmodel
kraken -a -I '*.xml' -o _ocr.xml -f xml ocr -m ../models/kraken_htrtrained.mlmodel
cd ..
find $INPUT -type f -name "*ocr*" -exec mv {} $OUTPUT \;
echo -e "${GREEN}Success:${NC} Finished predicitions! All completed Altos are in the output folder."
echo $OUTPUT*.xml

# Converts Alto to CSV
echo $LINE
python3 csv_converter.py $OUTPUT
echo -e "${GREEN}Success:${NC} Converted Altos into one tsv file called sample_table.tsv"
