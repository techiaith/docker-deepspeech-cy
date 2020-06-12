#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re
import pathlib 

from tqdm import tqdm
from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

"""

def load_alphabet(alphabet_file_path):
    alpha = set()
    alpha.add(' ')
    alpha.add("'")
    with open(alphabet_file_path, 'r', encoding='utf-8') as alphabet_file:
        for letter in alphabet_file:
            alpha.add(letter.strip().lower())

    return alpha


def remove_seperators(transcript):    
    transcript = re.sub(r"[\\,\.\?!()\";/\\|`]", '', transcript)
    return transcript


def replace(transcript):
    transcript = transcript.strip()

    transcript = transcript.replace(":","")
    transcript = transcript.replace("-","")
    
    transcript = transcript.replace("\u2019","'")
    transcript = transcript.replace("\u2018","'")
    transcript = transcript.replace("\u2010","")
    transcript = transcript.replace("\u2011","")
    transcript = transcript.replace("\u2012","")
    transcript = transcript.replace("\u2013","")
    transcript = transcript.replace("\u2014","")
    transcript = transcript.replace("\u201C","")
    transcript = transcript.replace("\u201D","")
    
    return transcript


def out_of_alphabet(transcript, valid_alphabet):
    transcript = transcript.lower()
    return set(transcript) - valid_alphabet


def main(source_text_file_path, output_text_file_path, alphabet_file_path, **args):
    valid_alphabet = load_alphabet(alphabet_file_path)    
    with open(output_text_file_path, 'w', encoding='utf-8') as out_file:
        with open(source_text_file_path, 'r', encoding='utf-8') as in_file:
            source_text_file_extension = pathlib.Path(source_text_file_path).suffix
            ooa_text_file_path = source_text_file_path.replace(source_text_file_extension, ".ooa" + source_text_file_extension)
            with open(ooa_text_file_path, 'w', encoding='utf-8') as ooa_out_file:
                for i, transcript in enumerate(tqdm(in_file)):                    
                    transcript = replace(transcript)
                    transcript = remove_seperators(transcript)
                    ooa = out_of_alphabet(transcript, valid_alphabet)
                    if (len(ooa) > 0):
                        ooa_out_file.write("%s\t%s\t%s\n" % (i, ooa, transcript))
                        continue

                    out_file.write(transcript +"\n")


if __name__ == "__main__":
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 
    parser.add_argument("-s", dest="source_text_file_path", required=True, help="location of source text file")
    parser.add_argument("-o", dest="output_text_file_path", required=True, help="location of output text file")
    parser.add_argument("-a", dest="alphabet_file_path", required=True, help="location of alphabet file")

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
