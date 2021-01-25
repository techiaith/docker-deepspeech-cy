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

    # client_id	path	sentence	up_votes	down_votes	age	gender	accent	locale	segment
    for csv_file_path in csv_files:
        
        df = pandas.read_csv(csv_file_path, encoding='utf-8')        
        #
        df_grouped = df.groupby("transcript").size().to_frame('count').reset_index()
        df_grouped = df_grouped.sort_values("count", ascending=False)

        df_grouped.to_csv(str(csv_file_path).replace(".csv",".dups.txt"))

        #        
        total_duration = 0.0
        count = 0
        for index, row in df.iterrows():
            count += 1
            wav_file_path = os.path.join(csv_root_dir, row["wav_filename"])
            total_duration = total_duration + librosa.get_duration(filename=wav_file_path)

        print ("%s\t%s recordings\t\t%.2f hours\t(%.2f seconds)" % (csv_file_path, count, total_duration/60.0/60.0, total_duration))
        print (df_grouped.nlargest(n=5, columns='count'))
        print ('\n')

    
   
if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--csv_dir", dest="csv_root_dir", required=True, help="path to audio corpus CSV files")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
