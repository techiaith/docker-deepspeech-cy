#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import pathlib
import librosa
import pandas

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

"""

def main(csv_root_dir, **args):
    csv_files = pathlib.Path(csv_root_dir).glob("*.csv")

    for csv_file_path in csv_files:        
        df = pandas.read_csv(csv_file_path, encoding='utf-8')        
        total_duration = 0.0
        for index, row in df.iterrows(): 
            wav_file_path = os.path.join(csv_root_dir, row["wav_filename"])
            total_duration = total_duration + librosa.get_duration(filename=wav_file_path)

        print ("%s\t\t%.2f hours\t(%.2f seconds)" % (csv_file_path, total_duration/60.0/60.0, total_duration))
    
   
if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--csv_dir", dest="csv_root_dir", required=True, help="path to corpus CSV files")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
