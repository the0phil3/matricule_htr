import xml.etree.ElementTree as ET
import os
import pandas as pd
from lxml import etree
import sys

def run(directory):
    output = pd.DataFrame()
    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            tree = ET.parse(os.path.join(directory, filename))
            region_list = []
            region_value = []
            for region in tree.findall(".//{http://www.loc.gov/standards/alto/ns-v4#}OtherTag"):
                if region.attrib['LABEL'] != 'default':
                    region_list.append(region.attrib['LABEL'])
                    region_value.append(region.attrib['ID'])

            regions_dict = {region_list[i]: region_value[i] for i in range(len(region_list))}
            result = {}
            result['filename'] = filename

            for key, value in regions_dict.items():
                line1 = ".//{http://www.loc.gov/standards/alto/ns-v4#}"
                line2 = f"TextBlock[@TAGREFS='{value}']/"
                line3 = "{http://www.loc.gov/standards/alto/ns-v4#}TextLine/"
                lines = tree.findall(line1 + line2 + line3 + "{http://www.loc.gov/standards/alto/ns-v4#}String")

                cat = []

                for content in lines:
                    cat.append(content.attrib['CONTENT'])

                result[f'{key}'] = cat
                df_dictionary = pd.DataFrame([result])

            output = pd.concat([output, df_dictionary], ignore_index=True)

    return (output)

def main():
    # Check if a directory is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Error: Please provide a directory as a command-line argument.")
        sys.exit(1)

    directory = sys.argv[1]
    output = run(directory)
    output.to_csv('output/sample_table.tsv', sep='\t', index=False)

if __name__ == "__main__":
    main()
