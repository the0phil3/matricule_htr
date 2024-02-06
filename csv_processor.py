# csv_processor.py

"""This module implements custom calculations."""

# Imports
import pandas as pd
import re, os, string, ast, sys

# Constants
DATE_PATTERNS = [
        r'\b\d{1,2}\s+(?:[^\s\d]+)?\s+\d{4}\b',            # 16 novembre 1898
        r'\b\d{1,2}\s+\d{1,2}\^?bre\s+\d{4}\b',             # 5 9^bre 1872
        r'\b\d{1,2}\s+[^\s\d]+\s+\d{4}\b',                  # 31 Mai, 1895
        r'\b(?:un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze)\s+[^\s\d]+\s+\d{4}\b',  # cinq juillet 1863
        r'\b\d{1,2}(er)?\s+[^\s\d]+\s+\d{4}\b',            # 1er Décembre 1880
        r'\b\d{1,2}(e)?\s+[^\s\d]+\s+\d{4}\b',            # 1e Mai 1880
        r'\b\d{1,2}(?:\s+)?[^\d\s]\s+\d{4}\b',              # 6juillet 1875
        r'\b\d{1,2}[^\d\s]+\d{4}\b',                        # 7mars1901
        r'\b(?:un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze)\s+[IXVLC]+\^?bre\s+\d{4}\b',  # neuf X^bre 1899
        r'\b\d{1,2}[^\d\s]+\d{4}\.\b',                        # 9juin 1875.
        r'\b(\d{1,2}\s+(?:[^\s\d]+)?\s+\d{4})(?:[.,!?;:]|\b)?',
        r'\b(\d{1,2}\s*(?:[^\s\d]+)?\s+\d{4})(?:[.,!?;:]|\b)?'
    ]

DF_ORDER = [
		'filename', 'date_naissance', 'taille (cm)', 'nom', 'num_mat', 'signalement',
        'instruction', 'etat_civil', 'decision', 'details', 'affectation', 'adresse',
        'cassier', 'campagnes', 'blessures'
		]

# Functions for processing tsv
def unlist_all_rows(df):
    for column in df.columns:
        df[column] = df[column].apply(lambda x: ' '.join(ast.literal_eval(x)) if isinstance(x, str) and x.startswith('[') and x.endswith(']') else x)
    return df

def extract_birthday(df):
    df['date_naissance'] = df['etat_civil'].apply(lambda x: [re.search(pattern, x).group() for pattern in DATE_PATTERNS if re.search(pattern, x) is not None][0] if any(re.search(pattern, x) for pattern in DATE_PATTERNS) else None)
    return df

def extract_height(df):
    # Regular expression pattern to find the highest two-digit number
    pattern = r'\b(\d{2})\b'

    # Extract numbers from the "signalement" column for each row
    def extract_numbers(row):
        matches = re.findall(pattern, str(row))
        numbers = [int(match) for match in matches] if matches else []
        return max(numbers) + 100 if numbers else None

    # Apply the extraction function to each row
    df['taille (cm)'] = df['signalement'].apply(extract_numbers)

    # Convert dtype of "taille (cm)" column to int
    df['taille (cm)'] = pd.to_numeric(df['taille (cm)'], errors='coerce').astype('Int64')

    return df

def main():
    # Make sure only one arguement is given
    if len(sys.argv) != 2:
        print("Error: Please provide a directory as a command-line argument.")
        sys.exit(1)

    table = sys.argv[1]
    output = pd.read_csv(table, sep='\t')
    unlist_all_rows(output)
    extract_birthday(output)
    extract_height(output)
    output = output[DF_ORDER]
    output.to_csv('output/sample_table.tsv', sep='\t', index=False)

if __name__ == "__main__":
    main()
