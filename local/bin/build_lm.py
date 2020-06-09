#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(1, '/DeepSpeech/data/lm')
import generate_lm
import generate_package

from argparse import ArgumentParser, RawTextHelpFormatter


DESCRIPTION = """

"""

class generate_lm_args(object):

    def __init__(self, input_txt, output_dir, top_k, kenlm_bins, arpa_order, max_arpa_memory,
                 arpa_prune, binary_a_bits, binary_q_bits, binary_type, discount_fallback=True):         
        self.input_txt = input_txt
        self.output_dir = output_dir
        self.top_k = top_k
        self.kenlm_bins = kenlm_bins
        self.arpa_order = arpa_order
        self.max_arpa_memory = max_arpa_memory
        self.arpa_prune = arpa_prune
        self.binary_a_bits = binary_a_bits
        self.binary_q_bits = binary_q_bits
        self.binary_type = binary_type
        self.discount_fallback=discount_fallback     
    

def main(source_text_file_path, alphabet_file_path, **args):

    output_dir = os.path.dirname(source_text_file_path)

    lm_args = generate_lm_args(input_txt=source_text_file_path, 
                               output_dir=output_dir,
                               top_k=50000,
                               kenlm_bins='/DeepSpeech/native_client/kenlm/build/bin/',
                               arpa_order=5,
                               max_arpa_memory='85%',
                               arpa_prune="0|0|1",
                               binary_a_bits=255,
                               binary_q_bits=8,
                               binary_type='trie')

    data_lower, vocab_str = generate_lm.convert_and_filter_topk(lm_args)
    generate_lm.build_lm(lm_args, data_lower, vocab_str)

    generate_package.create_bundle(alphabet_file_path,
                                   os.path.join(output_dir, "lm.binary"),
                                   os.path.join(output_dir, "vocab-50000.txt"),
                                   os.path.join(output_dir, "kenlm.scorer"),
                                   generate_package.Tristate(True), 0.9, 1.2)

if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 
    parser.add_argument("-s", dest="source_text_file_path", required=True, help="location of source text file")
    parser.add_argument("-a", dest="alphabet_file_path", required=True, help="location of alphabet file")

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))


