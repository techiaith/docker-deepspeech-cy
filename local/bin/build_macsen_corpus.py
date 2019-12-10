#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import requests

TEXT_CORPUS_URL="https://api.techiaith.org/assistant/dev/get_all_sentences"
TEXT_CORPUS_FILE="/data/macsen-prepare/corpus.txt"

DESCRIPTION = """

"""

def fetch_corpus(corpus_url, corpus_file_path):
    r = requests.get(corpus_url)
    data = r.json()

    if data["success"]:

        with open(corpus_file_path, 'a+', encoding='utf-8') as corpus_file:
            for r in data["result"]:
                line = process_transcript(r[0])
                corpus_file.write(line + '\n')


def process_transcript(orig_transcript):
    transcript = orig_transcript.replace("_"," ")
    transcript = transcript.replace("-"," ")
    transcript = transcript.lower()
    return transcript


def main():
    fetch_corpus(TEXT_CORPUS_URL, TEXT_CORPUS_FILE)

    

if __name__ == "__main__":
    main()
