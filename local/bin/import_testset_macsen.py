#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import csv
import wget
import codecs
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

MACSEN_TESTSET_BASE_URL = "http://techiaith.cymru/deepspeech/testsets"
MACSEN_TESTSET_TARFILE = "macsen_v1.1.tar.gz"


def wget_macsen_testset(testset_root_dir):

    if not os.path.exists(testset_root_dir):
        os.makedirs(testset_root_dir)
        macsen_url = os.path.join(MACSEN_TESTSET_BASE_URL, MACSEN_TESTSET_TARFILE)
        wget.download(macsen_url, testset_root_dir)
       
        with tarfile.open(os.path.join(testset_root_dir, MACSEN_TESTSET_TARFILE), "r:gz") as macsen_tarfile:
            print ("\nExtracting.....")
            macsen_tarfile.extractall(testset_root_dir)

        os.remove(os.path.join(testset_root_dir, MACSEN_TESTSET_TARFILE))


def simple_tokenizer(raw_text):
    result = raw_text.replace('?','')
    result = result.replace("'",'')
    return result


def main(testset_root_dir, csv_file, alphabet_file_path, **args):

    wget_macsen_testset(testset_root_dir)

    macsen_files = import_paldaruo.get_directory_structure(testset_root_dir)
    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
    csv_file_out = csv.DictWriter(codecs.open(csv_file, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()

    # open alphabet file 
    with codecs.open(alphabet_file_path, 'r', encoding='utf-8') as alphabet_file:
        for c in alphabet_file:
            c = c.rstrip()
            if len(c) == 0:
                c = ' '   
            alphabet.add(c)
    
    print (alphabet)
    for recs in macsen_files:
        print (recs)
        for wavfile in macsen_files[recs]:
            if wavfile.endswith(".wav"):
                wavfilepath = os.path.join(testset_root_dir, recs, wavfile)
                txtfilepath = wavfilepath.replace(".wav",".txt")
                with codecs.open(txtfilepath, "r", encoding='utf-8') as txtfile:
                    transcript = txtfile.read()
                    transcript = language_modelling_utils.process_transcript(transcript)
               
                duration = audio_processing_utils.get_duration_wav(wavfilepath)
                if audio_processing_utils.downsample_wavfile(wavfilepath):
                    tokenized_transcript = simple_tokenizer(transcript)
                    if set(tokenized_transcript).issubset(alphabet):
                        corpus.add(tokenized_transcript) 
                        vocab.update(tokenized_transcript.split()) 
                        csv_file_out.writerow({'wav_filename':wavfilepath, 'wav_filesize':os.path.getsize(wavfilepath), 'transcript':tokenized_transcript.encode('utf-8')}) 
                        # print (wavfilepath, os.path.getsize(wavfilepath), tokenized_transcript.encode('utf-8'))
                    else:
                        print ('### %s contains non-alphabet characters: %s' % (tokenized_transcript, alphabet - set(tokenized_transcript)))

    corpus_file_path = os.path.join(testset_root_dir, "corpus.txt")
    language_modelling_utils.save_corpus(corpus, corpus_file_path)

    lm_binary_file_path = language_modelling_utils.create_binary_language_model(corpus_file_path)
    trie_file_path = language_modelling_utils.create_trie(os.path.join(testset_root_dir, 'trie'), alphabet_file_path, lm_binary_file_path)

    print ("Import Macsen testset to %s finished. Associated lm and trie files at %s and %s" % (testset_root_dir, lm_binary_file_path, trie_file_path))

 
if __name__ == "__main__":
    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("-i", dest="testset_root_dir", default="/data/testsets/macsen")
    parser.add_argument("-a", dest="alphabet_file_path", required=True)
    parser.add_argument("-o", dest="csv_file", default="/data/testsets/macsen/deepspeech.csv")
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

