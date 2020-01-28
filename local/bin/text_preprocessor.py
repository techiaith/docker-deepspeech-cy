#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from WelshTokenization import WelshTokenization


FIND_REPLACE = []

SPEAKER_START_TAG = '<SPEAKER>'
SPEAKER_END_TAG = '</SPEAKER>'

AGE_START_TAG = '<AGE>'
AGE_END_TAG = '</AGE>'

GENDER_START_TAG = '<GENDER>'
GENDER_END_TAG = '</GENDER>'

MALE_TAGS = ['<#G>','<#g>']
FEMALE_TAGS = ['<#B>','<#b>']

BACKGROUND_NOISE_TAGS = ['<#CER>','<#cer>']

ACCENT_NORTH_TAGS = ['<#ACGOG>','<#acgog>'] 
ACCENT_SOUTH_TAGS = ['<#ACDE>','<#acde>']

ALL_TAGS = MALE_TAGS + FEMALE_TAGS + BACKGROUND_NOISE_TAGS + ACCENT_NORTH_TAGS + ACCENT_SOUTH_TAGS


class TextPreProcessor(object):

    def __init__(self, alphabet_file_path=''):
        self.tokenizer=WelshTokenization()
        if len(alphabet_file_path) > 0:
            self.tokenizer.load_alphabet(alphabet_file_path)
        pass


    def clean(self, transcript):
        """
        Cleans up the given sentence removing any markup and normalizing non-alpha characters 
        """
        transcript = transcript.strip()
        transcript = self.remove_tags(transcript)
        transcript = transcript.replace("\u2019","'")
        transcript = transcript.replace("\u2018","'")
        transcript = transcript.replace("-","")
        transcript = transcript.replace("\u2010","")
        transcript = transcript.replace("\u2011","")
        transcript = transcript.replace("\u2012","")
        transcript = transcript.replace("\u2013","")
        transcript = transcript.replace("\u2014","")

        transcript = transcript.replace(":","")

        tokens = self.tokenizer.tokenize(transcript)

        new_tokens = []     

        for t in tokens:
            new_token = ' ' + t + ' '
            for find, replace in FIND_REPLACE:
                new_token = new_token.replace(find, replace)
           
            tokenized_new_tokens = self.tokenizer.tokenize(new_token.strip())
            new_tokens.extend(tokenized_new_tokens)

        new_transcript = self.tokenizer.detokenize(new_tokens)
        new_transcript = self.tokenizer.remove_seperators(new_transcript).strip()
        new_transcript = new_transcript.lower()

        ooa = ''.join(self.tokenizer.out_of_alphabet(new_transcript)).strip()
        if len(ooa)>0:
            #print ('U+%04X' % (ord(ooa),))
            return False, "Out of Alphabet (%s)" % ooa, new_transcript
        else:
            return True, "", new_transcript


    def remove_tags(self, transcript):
        for tag in ALL_TAGS:
            transcript = transcript.replace(tag, '')

        transcript = self.remove_tagged_range(SPEAKER_START_TAG, SPEAKER_END_TAG, transcript)
        transcript = self.remove_tagged_range(AGE_START_TAG, AGE_END_TAG, transcript)
        transcript = self.remove_tagged_range(GENDER_START_TAG, GENDER_END_TAG, transcript)

        return transcript.strip()


    def remove_tagged_range(self, start_tag, end_tag, transcript):
        if start_tag in transcript and end_tag in transcript:
            start = transcript.index(start_tag)
            end = transcript.index(end_tag) + len(end_tag)
            transcript = transcript[0:start:] + transcript[end::]

        return transcript


    def any_tag_in_transcript(self, tags, transcript):
        if any(tag in transcript for tag in tags):
            return True
        return False


    def get_gender(self, transcript):
        if self.any_tag_in_transcript(MALE_TAGS, transcript): return 'male'
        if self.any_tag_in_transcript(FEMALE_TAGS, transcript): return 'female'
        return self.get_tagged_value(GENDER_START_TAG, GENDER_END_TAG, transcript)


    def get_accent(self, transcript):
        if self.any_tag_in_transcript(ACCENT_NORTH_TAGS, transcript): return 'cy_north'
        if self.any_tag_in_transcript(ACCENT_SOUTH_TAGS, transcript): return 'cy_south'
        return ''


    def has_background(self, transcript):
        if self.any_tag_in_transcript(BACKGROUND_NOISE_TAGS, transcript): return True
        return False


    def get_speaker_id(self, transcript):
        return self.get_tagged_value(SPEAKER_START_TAG, SPEAKER_END_TAG, transcript)


    def get_age(self, transcript):
        return self.get_tagged_value(AGE_START_TAG, AGE_END_TAG, transcript)


    def get_tagged_value(self, start_tag, end_tag, transcript):
        if start_tag in transcript and end_tag in transcript:
            result = re.search(start_tag + '(.*)' + end_tag, transcript)
            return result.group(1)
        return 


if __name__ == "__main__":
    p=TextPreProcessor()
    print(p.clean("<SPEAKER>123</SPEAKER>Mae'n bwysig gorffen y lot i'w 'neud."))
 
