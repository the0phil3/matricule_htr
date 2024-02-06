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
files=("models/htrtrained_best.mlmodel" "models/seg_model_best.mlmodel" "models/best.pt")

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
echo -e "${GREEN}Success:${NC} Shell is running in a virtual environment with the required libraries installed."
echo -e "${GREEN}Success:${NC} All models are present in the directory."
echo Here are all the files that the programme will run on :
echo $INPUT*.jpg
echo $LINE

# Boolean questions
read -p "Do you want to proceed with the extraction of the transcribed jpgs? (y/n): " extract_response

# Check user response
if [ "$extract_response" == "y" ]; then
    extract=true
else
    echo -e "${RED}Shell aborted.${NC}"
    exit 1
fi

# If the user wants to do processing as well
if [ "$extract" == true ]; then
    read -p "Do you also want to process the transcribed jpgs? (y/n): " process_response

    # Check user response
    if [ "$process_response" == "y" ]; then
        process=true
    else
        process=false
    fi
fi

# Check if the user has a GPU
read -p "Do you have a GPU for acceleration? (y/n): " gpu_response

# Check user response
if [ "$gpu_response" == "y" ]; then
    gpu=true
else
    gpu=false
fi

# Starts treatment
cd $INPUT

# Choose device based on user response
if [ "$gpu" == true ]; then
    yaltai kraken --device cuda:0 -I "*.jpg" --suffix ".xml" segment --yolo ../models/best.pt -i ../models/seg_model_best.mlmodel
    kraken -a -I '*.xml' -o _ocr.xml -f xml ocr -m ../models/htrtrained_best.mlmodel
else
    yaltai kraken --device cpu -I "*.jpg" --suffix ".xml" segment --yolo ../models/best.pt -i ../models/seg_model_best.mlmodel
    kraken -a -I '*.xml' -o _ocr.xml -f xml ocr -m ../models/htrtrained_best.mlmodel
fi

cd ..

find $INPUT -type f -name "*ocr*" -exec mv {} $OUTPUT \;
echo -e "${GREEN}Success:${NC} Finished predicitions! All completed Altos are in the output folder."
echo $OUTPUT*.xml

# Converts Alto to CSV
if [ "$extract" == true -a "$process" == false ]; then
    echo $LINE
	python3 csv_converter.py $OUTPUT
	echo -e "${GREEN}Success:${NC} Converted Altos into one tsv file called sample_table.tsv"
fi

# Converts Alto to CSV and processes the CSV
if [ "$process" == true ]; then
    echo $LINE
	python3 csv_converter.py $OUTPUT
    python3 csv_processor.py $OUTPUT"sample_table.tsv"
    echo -e "${GREEN}Success:${NC} Converted and processed Altos into one tsv file called sample_table.tsv"
fi
