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
import language_modelling_utils

from argparse import ArgumentParser, RawTextHelpFormatter


DESCRIPTION = """

"""



def build_corpus(source_text_file_path, alphabet_file_path):

    corpus=set() 

    text_preprocessor = TextPreProcessor(alphabet_file_path)

    print ("Processing sentences....")
    num_lines = sum(1 for line in open(source_text_file_path, 'r', encoding='utf-8'))
    with open(source_text_file_path, 'r', encoding='utf-8') as source_text_file:
        for line in tqdm(source_text_file, total=num_lines):
            success, reason, transcript = text_preprocessor.clean(line)
            if success:
                corpus.add(transcript)

    return corpus


def main(source_text_file_path, alphabet_file_path, **args):

    corpus = build_corpus(source_text_file_path, alphabet_file_path)
    corpus_text_file_path = source_text_file_path + ".corpus"
    language_modelling_utils.save_corpus(corpus, corpus_text_file_path)

    lm_root_dir = os.path.dirname(source_text_file_path)
    lm_binary_file_path = os.path.join(lm_root_dir, "lm.binary")
    trie_file_path = os.path.join(lm_root_dir, "trie")

    language_modelling_utils.create_binary_language_model(lm_binary_file_path, corpus_text_file_path)
    language_modelling_utils.create_trie(trie_file_path, alphabet_file_path, lm_binary_file_path)



if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 
    parser.add_argument("-s", dest="source_text_file_path", required=True, help="location of source text file")
    parser.add_argument("-a", dest="alphabet_file_path", required=True, help="location of alphabet file")

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))


