#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import pathlib
import shlex
import shutil
import subprocess
import glob

import json

import srt
from datetime import timedelta

from praatio import tgio
from utils.audio import downsample_wavfile

from utils.clean_transcript import clean_transcript
from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """
"""

ALPHABET_FILE_PATH = "/DeepSpeech/bin/bangor_welsh/alphabet.txt"
TECHIAITH_RELEASE = os.environ['TECHIAITH_RELEASE']
CHECKPOINTS_DIR = "/checkpoints/cy"
LANGUAGE_MODEL = "/models/techiaith/techiaith_bangor_transcribe_%s.scorer" % TECHIAITH_RELEASE


def convert_json_to_textgrid(wav_file_path, transcript_file_path):
    
    textgrid_file_path = transcript_file_path.replace(".tlog",".TextGrid")    

    with open(transcript_file_path) as json_file:        
        textgrid_entries_list = []
        json_data = json.load(json_file)
        for transcript in json_data:
            start_seconds = float(transcript["start"] / 1000)
            end_seconds = float(transcript["end"] / 1000)
            textgrid_entry = (start_seconds,end_seconds, transcript["transcript"])
            textgrid_entries_list.append(textgrid_entry)
            
        utterance_tier = tgio.IntervalTier('utterance', textgrid_entries_list, 0, pairedWav=wav_file_path)
        tg = tgio.Textgrid()
        tg.addTier(utterance_tier)
        tg.save(textgrid_file_path, useShortForm=False, outputFormat='textgrid')

        print ("Textgrid of transcription saved to %s" % textgrid_file_path)


def convert_json_to_srt(transcript_file_path):
    srt_file_path = transcript_file_path.replace(".tlog",".srt")
    srt_segments = []
    with open(transcript_file_path) as json_file:
        json_data = json.load(json_file)
        i=1;
        for transcript in json_data:
            start_seconds = float(transcript["start"] / 1000)
            end_seconds = float(transcript["end"] / 1000)
            start_delta=timedelta(seconds=start_seconds)
            end_delta=timedelta(seconds=end_seconds)
            srt_segments.append(srt.Subtitle(i, start=start_delta, end=end_delta, content=transcript["transcript"]))

    str_string = srt.compose(srt_segments)
    with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(str_string)

    #print(str_string)

def copy_checkpoint():
    print ("Copying checkpoint files to %s" % CHECKPOINTS_DIR)
    src_files = os.listdir("/checkpoints/techiaith")
    for f in src_files:
        full_f = os.path.join("/checkpoints/techiaith",f)
        if f.endswith(".tar.gz"): continue
        shutil.copy(full_f, CHECKPOINTS_DIR)

def ensure_checkpoint():

    if not os.path.exists(CHECKPOINTS_DIR):
        os.mkdir(CHECKPOINTS_DIR)
        copy_checkpoint()
    elif not os.listdir(CHECKPOINTS_DIR):
        # checkpoints folder is empty. Copy default techiaith cy
        copy_checkpoint()


def main(wav_file_path, **args):

    cmd = "python3 /DeepSpeech/transcribe.py --src %s --checkpoint_dir %s --alphabet_config_path %s --scorer %s --vad_aggressiveness 0 --force"
    cmd = cmd % (wav_file_path, CHECKPOINTS_DIR, ALPHABET_FILE_PATH, LANGUAGE_MODEL)

    downsample_wavfile(wav_file_path)

    ensure_checkpoint()

    import_process = subprocess.Popen(shlex.split(cmd))
    import_process.wait()

    transcript_file = wav_file_path.replace(".wav", ".tlog")

    convert_json_to_textgrid(wav_file_path, transcript_file)
    convert_json_to_srt(transcript_file)


    
if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--wavfile", dest="wav_file_path", required=True, help="path to downloaded tar.gz containing speech corpus in CommonVoice v2.0 format")
    #parser.add_argument("--target_dir", dest="cv_root_dir", required=True, help="target directory for extracted archive, also root directory for training data")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
