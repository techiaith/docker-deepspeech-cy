#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import wget
import columnize

import requests
import json

from enum import Enum

import tarfile
import gzip
import shutil
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



def get_oscar_textcorpus(data_root_dir):
    
    corpus_url="https://oscar-public.huma-num.fr/shuffled/cy.txt.gz"    
    dest_file = os.path.join(data_root_dir, 'cy.txt.gz')

    print ("Downloading: %s to %s" % (corpus_url, dest_file))
    
    wget.download(corpus_url, dest_file)

    file_url_path = urlparse(corpus_url)
    file_filename = os.path.basename(file_url_path.path)
    with gzip.open(os.path.join(data_root_dir, file_filename)) as oscar_gzfile:
        print ("\nExtracting.....")
        with open(os.path.join(data_root_dir, 'corpus.txt'), 'wb') as oscar_gzfile_out:
            shutil.copyfileobj(oscar_gzfile, oscar_gzfile_out)



def get_macsen_textcorpus(data_root_dir):
    json_data = json.loads(requests.get("https://api.techiaith.org/assistant/get_all_sentences").text)
    with open(os.path.join(data_root_dir, "corpus.txt"), 'w', encoding='utf-8') as macsen_file_out: 
        for s in json_data["result"]:
            macsen_file_out.write(s[0] + "\n")



def wget_dataset(dataset_name, data_root_dir):

    if not os.path.exists(data_root_dir):
        os.makedirs(data_root_dir)
    
    dataset_url = MACSEN_DATASET_URL
    if str(dataset_name)=="transcribe":
        dataset_url = TRANSCRIBE_DATASET_URL
        
    print ("Downloading: %s" % dataset_url)
    wget.download(dataset_url, data_root_dir)

    tarfile_url_path = urlparse(dataset_url)
    tarfile_filename = os.path.basename(tarfile_url_path.path)      
    with tarfile.open(os.path.join(data_root_dir, tarfile_filename), "r:gz") as bangor_tarfile:
        print ("\nExtracting.....")
        bangor_tarfile.extractall(data_root_dir)

    os.remove(os.path.join(data_root_dir, tarfile_filename))



def get_textcorpora(dataset_name, data_root_dir):
    if str(dataset_name)=="transcribe":
        get_oscar_textcorpus(data_root_dir)
    else:
        get_macsen_textcorpus(data_root_dir)



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
    get_textcorpora(dataset_name, target_data_root_dir)

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
    parser.add_argument("-t", dest="target_data_root_dir", default="/data/bangor")    
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
