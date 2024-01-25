import xml.etree.ElementTree as ET
import os
import pandas as pd
from lxml import etree


directory = "input/"
output = pd.DataFrame()

for filename in os.listdir(directory):
    if filename.endswith('.xml'):
        # Load the XML file into an ElementTree object
        tree = ET.parse(os.path.join(directory, filename))
        region_list = []
        region_value = []
        for region in tree.findall(".//{http://www.loc.gov/standards/alto/ns-v4#}OtherTag"):
            if region.attrib['LABEL'] != 'default':
                region_list.append(region.attrib['LABEL'])
                region_value.append(region.attrib['ID'])

        regions_dict = {region_list[i]: region_value[i] for i in range(len(region_list))}

        result = {}
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

order = ['nom', 'prenom', 'date_naissance', 'num_mat', 'classe', 'signalement', 'taille',
         'instruction', 'instruction_militaire', 'details', 'affectation', 'adresse',
         'dates', 'etat_civil', 'decision', 'cassier', 'campagnes', 'blessures']

output = output[order]
output.to_csv('output/output.tsv', sep='\t', index=False)
