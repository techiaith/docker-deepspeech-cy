#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re
import pathlib 

from utils.clean_transcript import clean_transcript

from tqdm import tqdm
from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

"""

def main(source_text_file_path, output_text_file_path, alphabet_file_path, **args):
    
    source_text_file_extension = pathlib.Path(source_text_file_path).suffix
    ooa_text_file_path = source_text_file_path.replace(source_text_file_extension, ".ooa" + source_text_file_extension)
    clean = clean_transcript(alphabet_file_path, ooa_text_file_path)

    with open(output_text_file_path, 'w', encoding='utf-8') as out_file:
        with open(source_text_file_path, 'r', encoding='utf-8') as in_file:
            for i, transcript in enumerate(tqdm(in_file)):
                cleaned, transcript = clean.clean(transcript)
                if cleaned:
                    out_file.write(transcript.lower() + "\n")


if __name__ == "__main__":
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 
    parser.add_argument("-s", dest="source_text_file_path", required=True, help="location of source text file")
    parser.add_argument("-o", dest="output_text_file_path", required=True, help="location of output text file")
    parser.add_argument("-a", dest="alphabet_file_path", default='/DeepSpeech/bin/bangor_welsh/alphabet.txt', help="location of alphabet file")

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
