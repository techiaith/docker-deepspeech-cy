#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from clean_transcript import clean_transcript

ALPHABET_FILE_PATH = "/DeepSpeech/bin/bangor_welsh/alphabet.txt"

def validate_label(label):

    clean = clean_transcript(ALPHABET_FILE_PATH)
    cleaned, transcript = clean.clean(label)
    if cleaned:
        return transcript.lower()
    return None
