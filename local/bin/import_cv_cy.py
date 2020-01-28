#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import csv
from tqdm import tqdm

import pandas as pd
import numpy as np

from text_preprocessor import TextPreProcessor
import audio_processing_utils
import language_modelling_utils

from urllib.request import urlretrieve
from urllib.parse import urlparse

import tarfile

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

"""

corpus = set()


def convert_audio(data_root_dir):
    # convert each mp3 to wav
    all_files = os.listdir(data_root_dir)
    print ("Converting mp3 files to wav....")
    for mp3file in tqdm(all_files):
        if mp3file.endswith(".mp3"):
            audio_processing_utils.convert_mp3(os.path.join(data_root_dir, mp3file))



def dataframe_to_deepspeech_csv(df, audio_files_dir, alphabet_file_path, csv_file_out, rejected_csv_file_out):
    global corpus

    text_preprocessor = TextPreProcessor(alphabet_file_path)

    print ("Processing sentences....")
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):

        wav_file_path = os.path.join(audio_files_dir, row["path"]).replace('.mp3', ".wav") 
        if not os.path.isfile(wav_file_path):
            continue

        success, reason, transcript = text_preprocessor.clean(row["sentence"])

        if success is False:
            rejected_csv_file_out.writerow({
                'wav_filename':wav_file_path,
                'transcript':transcript,
                'reason':reason})
            continue

        if not audio_processing_utils.is_feasible_transcription(wav_file_path, transcript):
            rejected_csv_file_out.writerow({
                'wav_filename':wav_file_path,
                'transcript':transcript,
                'reason':'Not feasible transcript'})
            continue

        corpus.add(transcript)

        output_entry = {
            'wav_filename': wav_file_path,
            'wav_filesize': os.path.getsize(wav_file_path),
            'transcript': transcript,
            'age': row["age"],
            'gender':row["gender"],
            'accent':row["accent"]
        }
        csv_file_out.writerow(output_entry) 


def main(data_root_dir, csv_file_path, alphabet_file_path, text_file_path, **args):

    audio_files_dir = os.path.join(data_root_dir, 'clips') 
    convert_audio(audio_files_dir)

    deepspeech_fieldnames = ['wav_filename', 'wav_filesize', 'transcript', 'age', 'gender', 'accent', 'dataset']
    csv_file_out = csv.DictWriter(open(csv_file_path, 'w', encoding='utf-8'), fieldnames=deepspeech_fieldnames)
    csv_file_out.writeheader()

    rejected_csv_fieldnames = ['wav_filename', 'transcript', 'reason']
    rejected_csv_file_path = csv_file_path.replace(".csv",".rejected.csv")
    rejected_csv_file_out = csv.DictWriter(open(rejected_csv_file_path, 'w', encoding='utf-8'), fieldnames=rejected_csv_fieldnames)
    rejected_csv_file_out.writeheader()

    # commonvoice fieldnames
    # client_id, path, sentence, up_votes, down_votes, age, gender, accent,...
    corpus_df = pd.read_csv(os.path.join(data_root_dir, 'validated.tsv'), delimiter='\t', encoding='utf-8')
    dataframe_to_deepspeech_csv(corpus_df, audio_files_dir, alphabet_file_path, csv_file_out, rejected_csv_file_out)
   
    language_modelling_utils.save_corpus(corpus, text_file_path)

    lm_root_dir = os.path.dirname(text_file_path)
    lm_binary_file_path = os.path.join(lm_root_dir, "lm.binary")
    trie_file_path = os.path.join(lm_root_dir, "trie")

    language_modelling_utils.create_binary_language_model(lm_binary_file_path, text_file_path)
    language_modelling_utils.create_trie(trie_file_path, alphabet_file_path, lm_binary_file_path)


if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 
    parser.add_argument("-d", dest="data_root_dir", required=True, help="top directory location of the CommonVoice corpus")
    parser.add_argument("-a", dest="alphabet_file_path", required=True, help="location of alphabet file")
    parser.add_argument("-o", dest="csv_file_path", required=True, help="full file path for the csv this script will output")
    parser.add_argument("-t", dest="text_file_path", required=True, help="full file path for the output text file containing all corpus file texts")

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))


