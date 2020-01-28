#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import argparse
import pandas as pd
from tqdm import tqdm

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

print ("Checking alphabet....")
for index, row in tqdm(concatenated_df.iterrows(), total=concatenated_df.shape[0]):
    if not pd.isnull(row["transcript"]) :
        success, reason, transcript = text_preprocessor.clean(row["transcript"])
        if success==False:
            print (transcript, reason)
            continue
          
        alphabet = alphabet.union(set(transcript))
   
alpha_diff = text_preprocessor.get_alphabet() - alphabet
if len(alpha_diff) > 0:
    print ("WARNING! Characters in alphabet, but not in datasets")
    print (alpha_diff)

