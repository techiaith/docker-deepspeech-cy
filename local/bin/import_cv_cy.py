#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import csv

import pandas as pd
import numpy as np

import corpus_creator

import audio_processing_utils
import language_modelling_utils

from urllib.request import urlretrieve
import tarfile
from argparse import ArgumentParser, RawTextHelpFormatter
from commonvoice_url import COMMONVOICE_DOWNLOAD_URL_BASE

DESCRIPTION = """

"""

DEFAULT_LOCALE = 'cy'
DEFAULT_DATA_DIR = '/data/commonvoice-%s/' % DEFAULT_LOCALE
DEFAULT_CSV = '/data/commonvoice-%s/deepspeech.csv' % DEFAULT_LOCALE
DEFAULT_ALPHABET = '/data/commonvoice-%s/alphabet.txt' % DEFAULT_LOCALE

alphabet = set()
corpus = set()


def unzip(zipfile_path, destination):
    print ("Extracting %s..." % zipfile_path)
    with open(zipfile_path, 'rb') as z:
        zf = zipfile.ZipFile(z)
        zf.extractall(destination)


def untar(targzfile_path, destination):
    print ("Extracting tar gz file %s..." % targzfile_path)
    with tarfile.open(targzfile_path) as t:
        t.extractall(destination)
     
 
def download_progress(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


def download_common_voice_artefact(data_root_dir, artefact):
    url = os.path.join(COMMONVOICE_DOWNLOAD_URL_BASE, artefact)
    print ("Downloading %s" % url)
    destination_file_path = os.path.join(data_root_dir, artefact)
    urlretrieve(url, destination_file_path, download_progress)
    if artefact.endswith('.tar.gz'):
        untar(destination_file_path, data_root_dir)
    else:
        unzip(destination_file_path, data_root_dir) 


def download_data(data_root_dir, locale):
    if not os.path.exists(data_root_dir):
         os.makedirs(data_root_dir)

    # download cy.zip audio data
    download_common_voice_artefact(data_root_dir, locale + '.tar.gz') 

    # download clips.tsv.zip
    download_common_voice_artefact(data_root_dir, 'clips.tsv.tar.gz')


def convert_audio(data_root_dir):
    # convert each mp3 to wav
    for mp3file in os.listdir(data_root_dir):
        if mp3file.endswith(".mp3"):
            print (mp3file)
            audio_processing_utils.convert_mp3(os.path.join(data_root_dir, mp3file))


def dataframe_to_deepspeech_csv(df, audio_files_dir, csv_file):
    global alphabet
    global corpus

    # deepspeech fieldnames
    deepspeech_fieldnames = ['wav_filename', 'wav_filesize', 'transcript', 'age', 'gender', 'accent', 'dataset']
    csv_file_out = csv.DictWriter(open(csv_file, 'w', encoding='utf-8'), fieldnames=deepspeech_fieldnames)
    csv_file_out.writeheader()
    for index, row in df.iterrows():
        wav_filepath = os.path.join(audio_files_dir, row["path"].replace(".mp3",".wav")) 
        transcript = language_modelling_utils.process_transcript(row["sentence"])
        corpus.add(transcript)
        alphabet = alphabet.union(language_modelling_utils.get_alphabet(transcript)) 
        output_entry = {
            'wav_filename': wav_filepath,
            'wav_filesize': os.path.getsize(wav_filepath),
            'transcript': transcript,
            'age': row["age"],
            'gender':row["gender"],
            'accent':row["accent"]
        }
        csv_file_out.writerow(output_entry) 


def main(data_root_dir, deepspeech_csv_file, alphabet_file_path, locale, **args):

    download_data(data_root_dir, locale)
    convert_audio(os.path.join(data_root_dir, 'clips'))

    clips_file_path = os.path.join(data_root_dir, 'clips.tsv')
    if not os.path.isfile(clips_file_path):
        print ("No clips file")
        return
   
    corpus_creator.execute(data_root_dir, clips_file_path, locale)

    # commonvoice fieldnames
    # client_id, path, sentence, up_votes, down_votes, age, gender, accent, locale, bucket
    corpus_df = pd.read_csv(os.path.join(data_root_dir, locale, 'validated.tsv'), delimiter='\t', encoding='utf-8')

    audio_files_dir = os.path.join(data_root_dir, 'clips') 
    dataframe_to_deepspeech_csv(corpus_df, audio_files_dir, deepspeech_csv_file)

    language_modelling_utils.save_alphabet(alphabet, alphabet_file_path)
    language_modelling_utils.save_corpus(corpus, os.path.join(data_root_dir, "corpus.txt"))


if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 
    parser.add_argument("-a", dest="alphabet_file_path", default=DEFAULT_ALPHABET)
    parser.add_argument("-i", dest="data_root_dir", default=DEFAULT_DATA_DIR)
    parser.add_argument("-o", dest="deepspeech_csv_file", default=DEFAULT_CSV)
    parser.add_argument("-l", dest="locale", default=DEFAULT_LOCALE)

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

