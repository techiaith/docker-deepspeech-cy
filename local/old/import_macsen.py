#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import wget
import tarfile
import functools
from urllib.parse import urlparse

import kfold
import audio_processing_utils
import language_modelling_utils

from text_preprocessor import TextPreProcessor
from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """
Llwytho i lawr set data Macsen ar gyfer DeepSpeech o fewn yr ap Macsen 

Mae angen rhoid lleoliad i ffeil alphabet.txt

© Prifysgol Bangor University

"""

alphabet = set()

MACSEN_DATASET_URL ="http://techiaith.cymru/deepspeech/macsen/macsen_200121.tar.gz"


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


def main(data_root_dir, alphabet_file_path, **args):

    total_duration = 0.0
    text_preprocessor = TextPreProcessor(alphabet_file_path)

    wget_macsen_dataset(data_root_dir)
    csv_file_path = os.path.join(data_root_dir, "deepspeech.csv")

    macsen_files = get_directory_structure(data_root_dir)
    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript','duration']
    csv_file_out = csv.DictWriter(open(csv_file_path, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()

    for user in macsen_files['macsen']['clips']:
        for wavfile in macsen_files['macsen']['clips'][user]:
            if wavfile.endswith(".wav"):
                wavfilepath = os.path.join(data_root_dir, 'clips', user, wavfile)
                txtfilepath = wavfilepath.replace(".wav",".txt")
                with open(txtfilepath, "r", encoding='utf-8') as txtfile:
                    transcript = txtfile.read()

                success, reason, transcript = text_preprocessor.clean(transcript)

                if success: 
                    duration = audio_processing_utils.get_duration_wav(wavfilepath)
                    total_duration = total_duration + duration
                    if audio_processing_utils.downsample_wavfile(wavfilepath):
                        print (wavfilepath)
                        csv_file_out.writerow({
                            'wav_filename':wavfilepath, 
                            'wav_filesize':os.path.getsize(wavfilepath), 
                            'transcript':transcript,
                            'duration':duration
                        }) 
                else:
                    print (wavfilepath, transcript, reason)


    corpus_file_path = os.path.join(data_root_dir, "corpus.txt")
    lm_binary_file_path = os.path.join(data_root_dir, "lm.binary")
    trie_file_path = os.path.join(data_root_dir, "trie")

    language_modelling_utils.create_binary_language_model(lm_binary_file_path, corpus_file_path)
    language_modelling_utils.create_trie(trie_file_path, alphabet_file_path, lm_binary_file_path)

    kfold.create_kfolds(csv_file_path, data_root_dir, 10)

    print ("Import Macsen data to %s finished. Duration %ss . Associated lm and trie files at %s and %s" % (data_root_dir, total_duration, lm_binary_file_path, trie_file_path))




if __name__ == "__main__":
    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-d", dest="data_root_dir", default="/data/macsen")
    parser.add_argument("-a", dest="alphabet_file_path", required=True)
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
