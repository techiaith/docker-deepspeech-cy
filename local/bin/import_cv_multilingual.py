#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import wget
import codecs
import zipfile
import csv

import pandas as pd
import numpy as np

import audio_processing_utils
import language_modelling_utils

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


def get_common_voice_artefact(data_root_dir, artefact):
    url = os.path.join(COMMONVOICE_DOWNLOAD_URL_BASE, artefact)
    print ("Downloading %s" % url)
    wget.download(url, data_root_dir)
    unzip(os.path.join(data_root_dir, artefact), data_root_dir) 


def get_data(data_root_dir, locale):
    if not os.path.exists(data_root_dir):
         os.makedirs(data_root_dir)

    # download cy.zip audio data
    get_common_voice_artefact(data_root_dir, locale + '.zip') 

    # download clips.tsv.zip
    get_common_voice_artefact(data_root_dir, 'clips.tsv.zip')


def convert_audio(data_root_dir):
    # convert each mp3 to wav
    for mp3file in os.listdir(data_root_dir):
        if mp3file.endswith(".mp3"):
            print (mp3file)
            audio_processing_utils.convert_mp3(os.path.join(data_root_dir, mp3file))


def dataframe_to_deepspeech_csv(df, data_root_dir, csv_file):
    global alphabet
    global corpus

    # deepspeech fieldnames
    deepspeech_fieldnames = ['wav_filename', 'wav_filesize', 'transcript', 'age', 'gender', 'accent', 'dataset']
    csv_file_out = csv.DictWriter(codecs.open(csv_file, 'w', encoding='utf-8'), fieldnames=deepspeech_fieldnames)
    csv_file_out.writeheader()
    for index, row in df.iterrows():
        wav_filepath = os.path.join(data_root_dir, row["path"].replace(".mp3",".wav")) 
        transcript = language_modelling_utils.process_transcript(row["sentence"])
        corpus.add(transcript)
        alphabet = alphabet.union(language_modelling_utils.get_alphabet(transcript)) 
        output_entry = {
            'wav_filename': wav_filepath,
            'wav_filesize': os.path.getsize(wav_filepath),
            'transcript': transcript,
            'age': row["age"],
            'gender':row["gender"],
            'accent':row["accent"],
            'dataset':row["bucket"]
        }
        csv_file_out.writerow(output_entry) 


def main(data_root_dir, deepspeech_csv_file, alphabet_file_path, locale, **args):

    get_data(data_root_dir, locale)

    convert_audio(data_root_dir)

    # commonvoice fieldnames
    # client_id, path, sentence, up_votes, down_votes, age, gender, accent, locale, bucket
    commonvoice_df = pd.read_csv(os.path.join(data_root_dir, 'clips.tsv'), delimiter='\t', encoding='utf-8')

    print ("all datasets")
    commonvoice_df_locale = commonvoice_df.loc[commonvoice_df['locale'] == locale] 
    dataframe_to_deepspeech_csv(commonvoice_df_locale, data_root_dir, deepspeech_csv_file)

    print ("train")
    commonvoice_df_locale_train = commonvoice_df_locale.loc[commonvoice_df_locale['bucket'] == 'train']
    dataframe_to_deepspeech_csv(commonvoice_df_locale_train, data_root_dir, deepspeech_csv_file.replace('.csv','.train.csv'))

    print ("dev") 
    commonvoice_df_locale_dev = commonvoice_df_locale.loc[commonvoice_df_locale['bucket'] == 'dev']
    dataframe_to_deepspeech_csv(commonvoice_df_locale_dev, data_root_dir, deepspeech_csv_file.replace('.csv','.dev.csv'))

    print ("test")
    commonvoice_df_locale_test = commonvoice_df_locale.loc[commonvoice_df_locale['bucket'] == 'test']
    dataframe_to_deepspeech_csv(commonvoice_df_locale_test, data_root_dir, deepspeech_csv_file.replace('.csv','.test.csv'))

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

