#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import os
import shutil

import json
from praatio import tgio

def convert_json_to_textgrid(json_filepath, textgrid_filepath):
    with open (json_filepath, 'r', encoding='utf-8') as jsonfile:
        json_transcription = json.load(jsonfile)
        print (json_transcription)