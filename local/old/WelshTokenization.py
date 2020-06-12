#!/usr/bin/env python3
#coding: utf-8
import re
import datetime

VALID_LETTERS_LOWER = 'aáàâäbcdeéèêëfghiíìîïjlmnoóòôöprstuúùûüwẃẁŵẅyýỳŷÿ'

REGEX_SEPARATOR = r"[\\,\.\?!()\";/\\|`]"
REGEX_CLITICS = r"'CH |'ch |'I |'i |'M |'m |'N |'n |'R |'r |'TH |'th |'U |'u |'W |'w "


class WelshTokenization(object):

    def __init__(self):
        self.initialise_regular_expressions(VALID_LETTERS_LOWER)
        pass

       
    def load_alphabet(self, alphabet_file_path):
        alpha = set()
        alpha.add(' ')
        with open(alphabet_file_path, 'r', encoding='utf-8') as alphabet_file:
            for letter in alphabet_file:
                alpha.add(letter.strip().lower())

            self.initialise_regular_expressions(''.join(alpha)) 
            

    def initialise_regular_expressions(self, valid_letters):
        self.valid_letters_lower = valid_letters
        self.valid_alphabet = set(self.valid_letters_lower)

        self.regex_letter_number = r"[" + self.valid_letters_lower + r"0-9]"
        self.regex_not_letter_number = r"[^" + self.valid_letters_lower + r"0-9]"


    def detokenize(self, string):
        s = string
        s = ' '.join(s)
        s = re.sub(r' (' + REGEX_CLITICS + ')', r"\g<1>", s)
        s = re.sub(r' (' + REGEX_SEPARATOR + ')', r"\g<1>", s)
        return s.strip()


    def tokenize(self, string):
        s = string
        s = re.sub('\t', " ", s)
        s = re.sub(r"(" + REGEX_SEPARATOR + ")", r" \g<1> ", s)
        s = re.sub(r"(" + self.regex_not_letter_number + r")'", r"\g<1> '", s)
        s = re.sub(r"(" + REGEX_CLITICS + ")", r" \g<1>", s)
        s = re.sub(r"(" + REGEX_CLITICS + ")(" + self.regex_not_letter_number + ")", r" \g<1> \g<2>", s)

        return s.strip().split()


    def remove_seperators(self, string):
        tokens = self.tokenize(string)
        new_tokens = []
        for tok in tokens:
            s = re.sub(REGEX_SEPARATOR,"", tok)
            if len(s) > 0:
                new_tokens.append(tok)

        return self.detokenize(new_tokens)


    def out_of_alphabet(self, string):
        return set(string) - self.valid_alphabet


    def get_alphabet(self):
        return self.valid_alphabet


if __name__ == "__main__":

    t = WelshTokenization()
    toks = t.tokenize("Beth yw'r tywydd ym Mangor?")    
    print(toks)
    print(' '.join(toks))
    print(t.detokenize(toks))

