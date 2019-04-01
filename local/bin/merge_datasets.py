#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import pandas as pd
import language_modelling_utils

alphabet = set()

path = '/data/training'
all_files = glob.glob(os.path.join(path, "*.csv"))

df_from_each_file = (pd.read_csv(f, encoding="utf-8", usecols=["wav_filename", "wav_filesize", "transcript"]) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True, sort=False)
concatenated_df.to_csv('/data/deepspeech.csv', encoding="utf-8", index=False)

for index, row in concatenated_df.iterrows():
    transcript = language_modelling_utils.process_transcript(row["transcript"])
    alphabet = alphabet.union(language_modelling_utils.get_alphabet(transcript))
    
language_modelling_utils.save_alphabet(alphabet, "/data/alphabet.txt")



#
# merge alphabets
all_alpha_files = glob.glob(os.path.join(path, "*.alphabet"))
for f in all_alpha_files:
    print (f)
    with open (f, 'r', encoding='utf-8') as a:
        for l in a:
            alphabet.add(l.replace('\n',''))

language_modelling_utils.save_alphabet(alphabet, '/data/alphabet.txt')

