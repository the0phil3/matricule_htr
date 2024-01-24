import numpy as np
import os
import matplotlib.pyplot as plt
from lxml import etree
import xml.etree.ElementTree as ET
import pandas as pd
from unidecode import unidecode
import re
from datetime import datetime
import seaborn as sns

def extract_intruction_militaire(row):
    if len(row) == 2:
        # Extract the second string, uncapitalize it, and remove leading/trailing spaces
        second_string = row[1].strip().lower()
        # Remove accents
        second_string = unidecode(second_string)
        return second_string
    elif len(row) == 1 and len(row[0]) > 2 and any(c.isalpha() for c in row[0]):
        # If there's only one item, and it contains a word longer than two characters (not just numbers)
        first_string = row[0].strip().lower()
        # Remove accents
        first_string = unidecode(first_string)
        return first_string
    else:
        return None
    
def extract_digit_or_x(row):
    pattern = r'\b[0-9xX]\b'  # Regular expression pattern to match single-digit numbers or 'x' (case insensitive)

    for item in row:
        match = re.search(pattern, item, re.IGNORECASE)
        if match:
            return match.group()

    return None

def extract_first_name(row):
    if len(row) >= 2:
        # Extract the first name (second item in the list)
        first_name = row[1]
        # Unlist "nom" to keep only the last name
        last_name = row[0]
        return first_name, last_name
    elif len(row) == 0:
        return None, None  # Handle empty "nom" column
    else:
        return None, row[0]  # If only one item is present, treat it as the last name
    
def extract_height(row):
    highest_number = -1  # Initialize with a value lower than any possible two-digit number

    for item in row:
        # Use regular expressions to find all two-digit numbers in the item
        two_digit_numbers = [int(num) for num in re.findall(r'\b\d{2}\b', item) if 10 <= int(num) <= 99]

        # Find the highest two-digit number
        if two_digit_numbers:
            highest_in_item = max(two_digit_numbers)
            highest_number = max(highest_number, highest_in_item)

    if highest_number != -1:
        return (highest_number + 100)
    else:
        return None  # Return None if no two-digit number is found

def extract_date(row):
    date_patterns = [
        r'\b\d{1,2}\s+(?:[^\s\d]+)?\s+\d{4}\b',            # 16 novembre 1898
        r'\b\d{1,2}\s+\d{1,2}\^?bre\s+\d{4}\b',             # 5 9^bre 1872
        r'\b\d{1,2}\s+[^\s\d]+\s+\d{4}\b',                  # 31 Mai, 1895
        r'\b(?:un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze)\s+[^\s\d]+\s+\d{4}\b',  # cinq juillet 1863
        r'\b\d{1,2}(er)?\s+[^\s\d]+\s+\d{4}\b',            # 1er Décembre 1880
        r'\b\d{1,2}(?:\s+)?[^\d\s]\s+\d{4}\b',              # 6juillet 1875
        r'\b\d{1,2}[^\d\s]+\d{4}\b',                        # 7mars1901
        r'\b(?:un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze)\s+[IXVLC]+\^?bre\s+\d{4}\b',  # neuf X^bre 1899
        r'\b\d{1,2}[^\d\s]+\d{4}\.\b',                        # 9juin 1875.
        r'\b(\d{1,2}\s+(?:[^\s\d]+)?\s+\d{4})(?:[.,!?;:]|\b)?',
        r'\b(\d{1,2}\s*(?:[^\s\d]+)?\s+\d{4})(?:[.,!?;:]|\b)?'
        
    ]
    for pattern in date_patterns:
        date_match = re.search(pattern, ' '.join(row), re.IGNORECASE)
        if date_match:
            date_string = date_match.group()
            
            # Remove all punctuation and ensure spaces between words, numbers, and abbreviations
            cleaned_date = ' '.join(date_string.split())
            lowercased_date = cleaned_date.lower()
            formatted_date = lowercased_date.replace(r'(\d+)\s(\D+)', r'\1 \2')
            
            return formatted_date

    return None

def extract_classe(row):
    four_digit_pattern = r'\b(18[89]\d|19[01]\d)\b'
    valid_numbers = []

    for item in row:
        matches = re.findall(four_digit_pattern, item)
        valid_numbers.extend([int(match) for match in matches if 1887 <= int(match) <= 1921])

    if valid_numbers:
        # Extract and return the extracted number as an integer
        extracted_number = valid_numbers[0]
        for i in range(len(row)):
            row[i] = row[i].replace(str(extracted_number), '').strip()  # Remove the extracted number from all items
        return extracted_number

    return None


def clean_num_mat(row):
    # Unlist the column and join the items
    unlisted_text = ' '.join(row)
    
    # Remove letters and punctuation using regex
    cleaned_text = re.sub(r'[^0-9]', '', unlisted_text)
    
    return cleaned_text




