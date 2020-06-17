#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import wget
import columnize

from enum import Enum

import tarfile
import functools
from urllib.parse import urlparse

import utils.kfold as kfold
import utils.audio as audio
from utils.clean_transcript import clean_transcript

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """
Llwytho i lawr set data Macsen ar gyfer DeepSpeech o fewn yr ap Macsen 

Mae angen rhoid lleoliad i ffeil alphabet.txt

© Prifysgol Bangor University

"""

ALPHABET_FILE_PATH = "/DeepSpeech/bin/bangor_welsh/alphabet.txt"
MACSEN_DATASET_URL ="http://techiaith.cymru/deepspeech/macsen/datasets/macsen_200121.tar.gz"
TRANSCRIBE_DATASET_URL = "http://techiaith.cymru/deepspeech/arddweud/datasets/arddweud_testset_200617.tar.gz"


class DataSet(Enum):
    MACSEN = 'macsen'
    TRANSCRIBE = 'transcribe'

    def __str__(self):
        return self.value


def wget_dataset(dataset_name, data_root_dir):

    dataset_url = MACSEN_DATASET_URL
    print (dataset_name)
    if str(dataset_name)=="transcribe":
        dataset_url = TRANSCRIBE_DATASET_URL

    print ("Downloading: %s" % dataset_url)

    if not os.path.exists(data_root_dir):
        os.makedirs(data_root_dir)
        wget.download(dataset_url, data_root_dir)

        tarfile_url_path = urlparse(dataset_url)
        tarfile_filename = os.path.basename(tarfile_url_path.path)
      
        with tarfile.open(os.path.join(data_root_dir, tarfile_filename), "r:gz") as bangor_tarfile:
            print ("\nExtracting.....")
            bangor_tarfile.extractall(data_root_dir)

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


def main(dataset_name, target_data_root_dir,**args):

    wget_dataset(dataset_name, target_data_root_dir)
    csv_file_path = os.path.join(target_data_root_dir, "deepspeech.csv")

    bangor_files = get_directory_structure(target_data_root_dir)
    bangor_files_root = list(bangor_files)[0]

    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
    csv_file_out = csv.DictWriter(open(csv_file_path, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()

    clean = clean_transcript(ALPHABET_FILE_PATH, os.path.join(target_data_root_dir, 'ooa.txt'))
    clips_root = bangor_files[bangor_files_root]['clips']
    for user in clips_root:
        for wavfile in clips_root[user]:
            if wavfile.endswith(".wav"):
                wavfilepath = os.path.join(target_data_root_dir, 'clips', user, wavfile)
                txtfilepath = wavfilepath.replace(".wav",".txt")
                with open(txtfilepath, "r", encoding='utf-8') as txtfile:
                    transcript = txtfile.read()
                    cleaned, transcript = clean.clean(transcript)
                    if cleaned:
                        transcript = transcript.lower()
                        if audio.downsample_wavfile(wavfilepath):                        
                            #print (wavfilepath)
                            csv_file_out.writerow({
                                'wav_filename':wavfilepath, 
                                'wav_filesize':os.path.getsize(wavfilepath), 
                                'transcript':transcript
                            }) 
    
    kfold.create_kfolds(csv_file_path, target_data_root_dir, 10)
    
    print ("Import Bangor data to %s finished." % (target_data_root_dir))
    print ("%s contents: " % (target_data_root_dir))
    bangor_dir = sorted(os.listdir(target_data_root_dir))      
    print (columnize.columnize(bangor_dir, displaywidth=80))



if __name__ == "__main__":
    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-d", dest="dataset_name", type=DataSet, choices=list(DataSet), required=True, help="enw'r set ddata techiaith i'w lwytho i lawr / name of techiaith dataset to download. 'macsen' neu/or 'transcribe'")    
    parser.add_argument("-t", dest="target_data_root_dir", default="/data/techiaith_dataset")    
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))