#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import wget
import columnize

import tarfile
import functools
from urllib.parse import urlparse

import utils.kfold as kfold
import utils.audio as audio


from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """
Llwytho i lawr set data Macsen ar gyfer DeepSpeech o fewn yr ap Macsen 

Mae angen rhoid lleoliad i ffeil alphabet.txt

© Prifysgol Bangor University

"""

alphabet = set()

MACSEN_DATASET_URL ="http://techiaith.cymru/deepspeech/macsen/datasets/macsen_200121.tar.gz"


def wget_macsen_dataset(data_root_dir):

    if not os.path.exists(data_root_dir):
        os.makedirs(data_root_dir)
        wget.download(MACSEN_DATASET_URL, data_root_dir)

        tarfile_url_path = urlparse(MACSEN_DATASET_URL)
        tarfile_filename = os.path.basename(tarfile_url_path.path)
      
        with tarfile.open(os.path.join(data_root_dir, tarfile_filename), "r:gz") as macsen_tarfile:
            print ("\nExtracting.....")
            macsen_tarfile.extractall(data_root_dir)

        os.remove(os.path.join(data_root_dir, tarfile_filename))



def get_directory_structure(rootdir):
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir, followlinks=True):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = functools.reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir

    return dir


def main(target_data_root_dir, **args):

    #wget_macsen_dataset(target_data_root_dir)
    csv_file_path = os.path.join(target_data_root_dir, "deepspeech.csv")

    macsen_files = get_directory_structure(target_data_root_dir)
    macsen_files_root = list(macsen_files)[0]

    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
    csv_file_out = csv.DictWriter(open(csv_file_path, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()
    
    clips_root = macsen_files[macsen_files_root]['clips']
    for user in clips_root:
        for wavfile in clips_root[user]:
            if wavfile.endswith(".wav"):
                wavfilepath = os.path.join(target_data_root_dir, 'clips', user, wavfile)
                txtfilepath = wavfilepath.replace(".wav",".txt")
                with open(txtfilepath, "r", encoding='utf-8') as txtfile:
                    transcript = txtfile.read()                                     
                    if audio.downsample_wavfile(wavfilepath):
                        print (wavfilepath)
                        csv_file_out.writerow({
                            'wav_filename':wavfilepath, 
                            'wav_filesize':os.path.getsize(wavfilepath), 
                            'transcript':transcript
                        }) 
    
    kfold.create_kfolds(csv_file_path, target_data_root_dir, 10)
    
    print ("Import Macsen data to %s finished." % (target_data_root_dir))
    print ("%s contents: " % (target_data_root_dir))
    macsen_dir = sorted(os.listdir(target_data_root_dir))      
    print (columnize.columnize(macsen_dir, displaywidth=80))



if __name__ == "__main__":
    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-t", dest="target_data_root_dir", required=True, default="/data/macsen")    
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
