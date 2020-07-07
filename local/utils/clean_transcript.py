#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re
import pathlib 


class clean_transcript(object):


    def __init__(self, alphabet_file_path, ooa_file_path=''):
        self.valid_alphabet = self.load_alphabet(alphabet_file_path)
        self.ooa_file_path=ooa_file_path
        if len(ooa_file_path) > 0:
            # reset content
            open(ooa_file_path, 'w').close()
        

    def clean(self, transcript):
        transcript = self.replace(transcript)
        transcript = self.remove_seperators(transcript)
        
        ooa = self.out_of_alphabet(transcript)
        if (len(ooa) > 0):
            #print (ooa, transcript)
            if len(self.ooa_file_path) > 0:
                with open(self.ooa_file_path, 'w+', encoding='utf-8') as ooa_out_file:
                    ooa_out_file.write("%s\t%s\n" % (ooa, transcript))
            return False, transcript
            
        return True, transcript


    def load_alphabet(self, alphabet_file_path):
        alpha = set()
        alpha.add(' ')
        alpha.add("'")
        with open(alphabet_file_path, 'r', encoding='utf-8') as alphabet_file:
            for letter in alphabet_file:
                alpha.add(letter.strip().lower())

        return alpha


    def remove_seperators(self, transcript):    
        transcript = re.sub(r"[\\,\.\?!()\";/\\|`]", '', transcript)
        return transcript


    def replace(self, transcript):
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


    def out_of_alphabet(self, transcript):
        transcript = transcript.lower()
        return set(transcript) - self.valid_alphabet

