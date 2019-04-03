#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import wget
import tarfile

import import_paldaruo
import audio_processing_utils
import language_modelling_utils

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

© Prifysgol Bangor University

"""

alphabet = set()
corpus = set()
vocab = set() 

MACSEN_DEVSET_BASE_URL = "http://techiaith.cymru/deepspeech/devsets"
MACSEN_DEVSET_TARFILE = "macsen_v1.1.tar.gz"
MACSEN_TESTSET_BASE_URL = "http://techiaith.cymru/deepspeech/testsets"
MACSEN_TESTSET_TARFILE = "macsen_v0.1.tar.gz"


def wget_macsen_dataset(dataset_root_dir, dataset_url, dataset_tarfile):

    if not os.path.exists(dataset_root_dir):
        os.makedirs(dataset_root_dir)
        macsen_url = os.path.join(dataset_url, dataset_tarfile)
        wget.download(macsen_url, dataset_root_dir)
       
        with tarfile.open(os.path.join(dataset_root_dir, dataset_tarfile), "r:gz") as macsen_tarfile:
            print ("\nExtracting.....")
            macsen_tarfile.extractall(dataset_root_dir)

        os.remove(os.path.join(dataset_root_dir, dataset_tarfile))


def simple_tokenizer(raw_text):
    result = raw_text.replace('?','')
    result = result.replace("'",'')
    return result


def create_csv(dataset_root_dir, dataset_url, dataset_tarfile, alphabet_file_path):

    wget_macsen_dataset(dataset_root_dir, dataset_url, dataset_tarfile)
    csv_file_path = os.path.join(dataset_root_dir, "deepspeech.csv")

    macsen_files = import_paldaruo.get_directory_structure(dataset_root_dir)
    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
    csv_file_out = csv.DictWriter(open(csv_file_path, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()

    # open alphabet file 
    with open(alphabet_file_path, 'r', encoding='utf-8') as alphabet_file:
        for c in alphabet_file:
            c = c.rstrip()
            if len(c) == 0:
                c = ' '   
            alphabet.add(c)
    
    print (alphabet)
    for top in macsen_files:
        for recs in macsen_files[top]:
            recs_file_path=os.path.join(dataset_root_dir, recs)
            print (recs_file_path)
            if os.path.isfile(recs_file_path):
                continue
            for wavfile in macsen_files[top][recs]:
                if wavfile.endswith(".wav"):
                    wavfilepath = os.path.join(dataset_root_dir, recs, wavfile)
                    txtfilepath = wavfilepath.replace(".wav",".txt")
                    with open(txtfilepath, "r", encoding='utf-8') as txtfile:
                        transcript = txtfile.read()
                        transcript = language_modelling_utils.process_transcript(transcript)
               
                    duration = audio_processing_utils.get_duration_wav(wavfilepath)
                    if audio_processing_utils.downsample_wavfile(wavfilepath):
                        tokenized_transcript = simple_tokenizer(transcript)
                        if set(tokenized_transcript).issubset(alphabet):
                            corpus.add(tokenized_transcript) 
                            vocab.update(tokenized_transcript.split()) 
                            csv_file_out.writerow({
                                'wav_filename':wavfilepath, 
                                'wav_filesize':os.path.getsize(wavfilepath), 
                                'transcript':tokenized_transcript
                            }) 
                        else:
                            print ('### %s contains non-alphabet characters: %s' % (tokenized_transcript, alphabet - set(tokenized_transcript)))

    corpus_file_path = os.path.join(dataset_root_dir, "corpus.txt")
    lm_binary_file_path = os.path.join(dataset_root_dir, "lm.binary")
    trie_file_path = os.path.join(dataset_root_dir, "trie")

    language_modelling_utils.save_corpus(corpus, corpus_file_path)
    language_modelling_utils.create_binary_language_model(lm_binary_file_path, corpus_file_path)
    language_modelling_utils.create_trie(trie_file_path, alphabet_file_path, lm_binary_file_path)

    print ("Import Macsen dataset to %s finished. Associated lm and trie files at %s and %s" % (dataset_root_dir, lm_binary_file_path, trie_file_path))


def main(testset_root_dir, devset_root_dir, alphabet_file_path, **args):
    create_csv(testset_root_dir, MACSEN_TESTSET_BASE_URL, MACSEN_TESTSET_TARFILE, alphabet_file_path)
    create_csv(devset_root_dir, MACSEN_DEVSET_BASE_URL, MACSEN_DEVSET_TARFILE, alphabet_file_path)


if __name__ == "__main__":
    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("-i", dest="devset_root_dir", default="/data/devsets/macsen")
    parser.add_argument("-t", dest="testset_root_dir", default="/data/testsets/macsen")
    parser.add_argument("-a", dest="alphabet_file_path", required=True)
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

