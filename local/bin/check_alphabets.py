#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import argparse
import pandas as pd
import unicodedata
from tqdm import tqdm
from collections import Counter
from text_preprocessor import TextPreProcessor


alphabet = set()
parser = argparse.ArgumentParser()

parser.add_argument("-csv", "--csv-files", help="Str. Filenames as a comma separated list", required=True)
parser.add_argument("-a", "--alphabet", help="Alphabet file to check")
args = parser.parse_args()

all_files = [os.path.abspath(i) for i in args.csv_files.split(",")]

text_preprocessor = TextPreProcessor(args.alphabet)

df_from_each_file = (pd.read_csv(f, encoding="utf-8", usecols=["wav_filename", "wav_filesize", "transcript"]) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort=False)

char_counter = Counter()

print ("Checking alphabet....")
for index, row in tqdm(concatenated_df.iterrows(), total=concatenated_df.shape[0]):
    if not pd.isnull(row["transcript"]) :
        success, reason, transcript = text_preprocessor.clean(row["transcript"])
        if success==False:
            print (transcript, reason)
            continue
        char_counter += Counter(transcript)          
        alphabet = alphabet.union(set(transcript))

print (char_counter)
  
alpha_diff = text_preprocessor.get_alphabet() - alphabet
if len(alpha_diff) > 0:
    print ("WARNING! Characters in alphabet, but not in datasets")
    for c in alpha_diff:
        print ('%04x' % ord(c))

alpha_diff2 = alphabet - text_preprocessor.get_alphabet()
if len(alpha_diff2) > 0:
    print ("ERROR! datasets contains characters not in alphabet")
    for c in alpha_diff2:
        print (c, '%04x' % ord(c), unicodedata.name(c))
    print ("Alphabet: ")
    for a in text_preprocessor.get_alphabet():
        print (a, '%04x' % ord(a), unicodedata.name(a))
