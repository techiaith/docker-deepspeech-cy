#!/usr/bin/env python3
#coding: utf-8
import re

valid_letters_lower = 'aáàâäbcdeéèêëfghiíìîïjlmnoóòôöprstuúùûüwẃẁŵẅyýỳŷÿ'
valid_letters_upper = valid_letters_lower.upper()

regex_letter_number = r"[" + valid_letters_lower + valid_letters_upper + r"0-9]"
regex_not_letter_number = r"[^" + valid_letters_lower + valid_letters_upper + r"0-9]"
regex_separator = r"[\\?!()\";/\\|`]"

regex_clitics = r"'|:|-|'CH|'ch|'I|'i|'M|'m|'N|'n|'R|'r|'TH|'th|'U|'u|'W|'w"


class Tokenization(object):

    def __init__(self):
        pass

        
    def detokenize(self, string):
        s = string
        s = ' '.join(s)
        s = re.sub(r' (' + regex_clitics + ')', r"\g<1>", s)
        s = re.sub(r' (' + regex_separator + ')', r"\g<1>", s)
        return s.strip()


    def tokenize(self, string):
        s = string
        s = re.sub('\t', " ", s)
        s = re.sub("(" + regex_separator + ")", " \g<1> ", s)
        s = re.sub("(" + regex_not_letter_number + ")'", "\g<1> '", s)
        s = re.sub("(" + regex_clitics + ")$", " \g<1>", s)
        s = re.sub("(" + regex_clitics + ")(" + regex_not_letter_number + ")", " \g<1> \g<2>", s)

        return s.strip().split()


if __name__ == "__main__":

    t = Tokenizer()
    toks = t.tokenize("Beth yw'r tywydd ym Mangor?")    
    print(toks)
    print(t.detokenize(toks))


