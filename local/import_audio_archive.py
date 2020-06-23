#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import pathlib
import tarfile
import pandas
import csv
import shlex
import subprocess

from utils.clean_transcript import clean_transcript
from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

"""

ALPHABET_FILE_PATH = "/DeepSpeech/bin/bangor_welsh/alphabet.txt"


def extract(source_tar_gz, target_dir):
    print ("Extracting: %s" % source_tar_gz)
    tar = tarfile.open(source_tar_gz, "r:gz")
    tar.extractall(target_dir)
    tar.close()


def main(cv_archive_file_path, cv_root_dir, **args):

    extract(cv_archive_file_path, cv_root_dir)
    
    cmd = "python3 /DeepSpeech/bin/import_cv2.py %s" % (cv_root_dir)

    import_process = subprocess.Popen(shlex.split(cmd))
    import_process.wait()

    #
    csv_files = pathlib.Path(os.path.join(cv_root_dir,'clips')).glob("*.csv")
    clean = clean_transcript(ALPHABET_FILE_PATH)

    for csv_file_path in csv_files:
        print ("Clean and Check %s transcripts against alphabet" % csv_file_path)
        df = pandas.read_csv(csv_file_path, encoding='utf-8')
        
        moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
        csv_file_out = csv.DictWriter(open(str(csv_file_path).replace(".csv",".clean.csv"), 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
        csv_file_out.writeheader()

        for index, row in df.iterrows():
            transcript=row["transcript"]
            cleaned, transcript = clean.clean(transcript)
            if cleaned:
                csv_file_out.writerow({
                    'wav_filename':row["wav_filename"], 
                    'wav_filesize':row["wav_filesize"], 
                    'transcript':transcript.lower()
                }) 
            else:                
                print ("Dropped %s\n" % transcript)            


if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--archive", dest="cv_archive_file_path", required=True, help="path to downloaded tar.gz containing speech corpus in CommonVoice v2.0 format")
    parser.add_argument("--target_dir", dest="cv_root_dir", required=True, help="target directory for extracted archive, also root directory for training data")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
