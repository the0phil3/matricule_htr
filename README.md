# Maurin's matricule processor
Here is the working library for a bash script using `python`, `yolo` `kraken` models to automatically transcribe French "fiches matricules" from 1887 to 1921.

The models present have been trained on a sample of documents from the Paris municipal archives. The pipeline includes three models :
- `Yolov8` segmentation model
- `Kraken` baseline segmentation model
- `Kraken` text recognition model

All of these models are implemented after each other thanks to Thibault Clérice's `YALTAi` [library](https://github.com/PonteIneptique/YALTAi).

To use this repository, clone it. Then create a Python3.9 virtual environment with `venv` like this : `python3.9 -m venv venv`. Once the environment is made, you may enter it by ´source venv/bin/activate´ and download all the required libraries by doing `pip install -r requirements.txt`.

Then simply put the `.jpg`s of matricules that you have in the input folder of the cloned repository and run `bash processeur2maurin.sh`.
