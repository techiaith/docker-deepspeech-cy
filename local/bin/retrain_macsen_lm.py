#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
import WelshTokenization
import language_modelling_utils as lmutils

from argparse import ArgumentParser, RawTextHelpFormatter

DEFAULT_LOCALE='cy'
DEFAULT_ALPHABET = '/data/commonvoice-%s/alphabet.txt' % DEFAULT_LOCALE

DEFAULT_BINARY_LM='/models/macsen/lm.binary'
DEFAULT_TRIE='/models/macsen/trie'

TEXT_CORPUS_URL="https://api.techiaith.org/assistant/get_all_sentences"
TEXT_CORPUS_FILE="/data/macsen/corpus.txt"

DESCRIPTION = """

"""

def prepare_dir_structure(file_path):
    directory = os.path.abspath(os.path.join(file_path, '..'))
    if not os.path.exists(directory):
        os.makedirs(directory) 


def fetch_corpus(corpus_url, corpus_file_path):
    r = requests.get(corpus_url)
    data = r.json()

    if data["success"]:

        tokenizer = WelshTokenization.Tokenization()

        with open(corpus_file_path, 'w', encoding='utf-8') as corpus_file:
            for r in data["result"]:
                line = process_transcript(r[0])
                line = tokenizer.tokenize(line)
                line = ' '.join(line)
                corpus_file.write(line + '\n')


def process_transcript(orig_transcript):
    transcript = orig_transcript.replace("_"," ")
    transcript = transcript.replace("-"," ")
    transcript = transcript.lower()
    return transcript


def main(lm_binary_file_path, trie_file_path, alphabet_file_path, **args):

    prepare_dir_structure(lm_binary_file_path)
    prepare_dir_structure(trie_file_path)

    fetch_corpus(TEXT_CORPUS_URL, TEXT_CORPUS_FILE)

    lmutils.create_binary_language_model(lm_binary_file_path, TEXT_CORPUS_FILE)
    lmutils.create_trie(trie_file_path, alphabet_file_path, lm_binary_file_path)
    

if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 
    parser.add_argument("-a", dest="alphabet_file_path", default=DEFAULT_ALPHABET)
    parser.add_argument("-l", dest="lm_binary_file_path", default=DEFAULT_BINARY_LM)
    parser.add_argument("-t", dest="trie_file_path", default=DEFAULT_TRIE)

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

