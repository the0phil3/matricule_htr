# Maurin's matricule processor
Here is the working library for a bash shell using `python`, `yolo` `kraken` models to automatically transcribe French "fiches matricules" from 1887 to 1921.

The models present have been trained on a sample of documents from the Paris municipal archives. The pipeline includes three models :
- `Yolov8` segmentation model
- `Kraken` baseline segmentation model
- `Kraken` text recognition model

All of these models are implemented after each other thanks to Thibault Clérice's `YALTAi` [library](https://github.com/PonteIneptique/YALTAi).

## Installation
To use this repository, clone it. Then create a Python3.9 virtual environment with `venv` like this : `python3.9 -m venv venv`. Once the environment is made, you may enter it by `source venv/bin/activate` and download all the required libraries by doing `pip install -r requirements.txt`.

If you use `conda` then you can simply run this line of code `conda env create -f environment.yml` to create and run the environment.

## Using the shell

Put `.jpg`s of the matricules that you have in the input folder of the cloned repository and run `bash processeur2maurin.sh`.

The shell will ask you whether you want to extract or extract and process the different matricules.

If you decide to extract without processing :
- An ouput folder will be created with all the different alto files corresponding to each image as well as a `.tsv` file that can be opened with microsoft excel or any other spreadsheet programme.

If you decide to extract and process :
- An ouput folder will be created with all the different alto files corresponding to each image as well as a `.tsv` file that has been cleaned and has some prelimnary information extracted.
