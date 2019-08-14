#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import argparse
import pandas as pd
import language_modelling_utils

alphabet = set()
parser = argparse.ArgumentParser()

parser.add_argument("-csv", "--csv-files", help="Str. Filenames as a comma separated list", required=True)
args = parser.parse_args()
all_files = [os.path.abspath(i) for i in args.csv_files.split(",")]

df_from_each_file = (pd.read_csv(f, encoding="utf-8", usecols=["wav_filename", "wav_filesize", "transcript"]) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort=False)

for index, row in concatenated_df.iterrows():
    if not pd.isnull(row["transcript"]) :
        transcript = language_modelling_utils.process_transcript(row["transcript"])
        alphabet = alphabet.union(language_modelling_utils.get_alphabet(transcript))
    
language_modelling_utils.save_alphabet(alphabet, "/data/alphabet.txt")


