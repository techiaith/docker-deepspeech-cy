#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import wave
import time
import hashlib
import wget
import shutil

from text_preprocessor import TextPreProcessor
import audio_processing_utils
import language_modelling_utils

from pathlib import Path
from functools import reduce
from collections import Counter
from argparse import ArgumentParser, RawTextHelpFormatter


DESCRIPTION = """

Mewnforio a pharatoi casgliad o ffeiliau wav gyda ffeiliau txt sy'n cynnwys eu trasgrifiad i 
gorpws addas ar gyfer hyfforddi gyda Kaldi.

Hawlfraint / Copyright Prifysgol Bangor University

"""

corpus = set()


def get_directory_structure(rootdir):
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir, followlinks=True):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir

    # get name of parent directory
    top_dir_name = os.path.basename(rootdir)
    print (rootdir, top_dir_name)
    return dir[top_dir_name]


def get_duration_wav(wavfile):
    f = wave.open(wavfile, 'r')
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    f.close()
    return duration


def process_corpus_files(current_dir, current_files, alphabet_file_path, csv_file_out, rejected_csv_file_out):
    global corpus

    text_preprocessor = TextPreProcessor(alphabet_file_path)

    for wavfile in current_files:

        wavfile_path = os.path.join(current_dir, wavfile)

        if os.path.isdir(wavfile_path):
            process_corpus_files(current_dir, current_files[wavfile], alphabet_file_path, csv_file_out, rejected_csv_file_out)

        if wavfile.endswith(".wav"):
            txtfile_path = wavfile_path.replace(".wav", ".txt")

            if not os.path.isfile(txtfile_path):
                continue

            print ("\t%s" % wavfile)

            with open(txtfile_path, "r", encoding='utf-8') as txtfile:
                hashed_wavfile_path = hashlib.md5(wavfile_path.encode('utf-8')).hexdigest()
                tagged_transcript = txtfile.read()

                if text_preprocessor.has_background(tagged_transcript):
                    rejected_csv_file_out.writerow({
                        'wav_filename':wavfile_path,
                        'transcript': tagged_transcript,
                        'reason': "Tagged as having background music/noise"})
                    continue

                success, reason, transcript = text_preprocessor.clean(tagged_transcript)

                if success is False:
                    rejected_csv_file_out.writerow({
                        'wav_filename':wavfile_path,
                        'transcript':transcript,
                        'reason':reason})
                    continue

                if not audio_processing_utils.is_feasible_transcription(wavfile_path, transcript):
                    rejected_csv_file_out.writerow({
                        'wav_filename':wavfile_path,
                        'transcript':transcript,
                        'reason':'Not feasible transcript'})
                    continue
             
                corpus.add(transcript)

                csv_file_out.writerow({
                    'wav_filename':wavfile_path,
                    'wav_filesize':os.path.getsize(wavfile_path),
                    'wav_date':os.path.getmtime(wavfile_path),
                    'transcript': transcript,
                    'wav_fileid':hashed_wavfile_path,
                    'speakerid':text_preprocessor.get_speaker_id(tagged_transcript),
                    'duration': get_duration_wav(wavfile_path),
                    'accent': text_preprocessor.get_accent(tagged_transcript),
                    'gender': text_preprocessor.get_gender(tagged_transcript),
                    'age': text_preprocessor.get_age(tagged_transcript),
                    })


def main(corpus_root_dir, csv_file_path, alphabet_file_path, text_file_path, **args):

    corpus_files = get_directory_structure(corpus_root_dir)

    csv_fieldnames = ['wav_filename', 'wav_filesize', 'wav_date', 'transcript', 'wav_fileid', 'speakerid', 'duration', 'accent', 'gender', 'age', 'valid']
    csv_file_out = csv.DictWriter(open(csv_file_path, 'w', encoding='utf-8'), fieldnames=csv_fieldnames)
    csv_file_out.writeheader()

    rejected_csv_fieldnames = ['wav_filename', 'transcript', 'reason']
    rejected_csv_file_path = csv_file_path.replace(".csv",".rejected.csv")
    rejected_csv_file_out = csv.DictWriter(open(rejected_csv_file_path, 'w', encoding='utf-8'), fieldnames=rejected_csv_fieldnames)
    rejected_csv_file_out.writeheader()

    corpus_file_out = open(text_file_path, "w", encoding='utf-8')

    process_corpus_files(corpus_root_dir, corpus_files, alphabet_file_path, csv_file_out, rejected_csv_file_out)

    corpus_file_out.close()

    language_modelling_utils.save_corpus(corpus, text_file_path)

    lm_root_dir = os.path.dirname(text_file_path) 
    lm_binary_file_path = os.path.join(lm_root_dir, "lm.binary")
    trie_file_path = os.path.join(lm_root_dir, "trie")

    language_modelling_utils.create_binary_language_model(lm_binary_file_path, text_file_path)
    language_modelling_utils.create_trie(trie_file_path, alphabet_file_path, lm_binary_file_path)

 
if __name__ == "__main__":
    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("-d", dest="corpus_root_dir", required=True, help="directory location of wavs and txt files that constitutes the corpus")
    parser.add_argument("-a", dest="alphabet_file_path", required=True, help="location of alphabet file")
    parser.add_argument("-o", dest="csv_file_path", required=True, help="full file path for the csv this script will output")
    parser.add_argument("-t", dest="text_file_path", required=True, help="full file path for the output text file containing all corpus file texts")

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

