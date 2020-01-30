#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import errno
import hashlib
import shlex
import shutil
import zipfile
import subprocess
import functools

import wave
from sox import Transformer

from text_preprocessor import TextPreProcessor
from argparse import ArgumentParser, RawTextHelpFormatter

import audio_processing_utils
import language_modelling_utils


DESCRIPTION = """

Llwytho i lawr Corpws Paldaruo a'i addasu ar gyfer DeepSpeech

Download Paldaruo Speech Corpus and make it available for DeepSpeech

Usage:

   ./bin/import_paldaruo.py -i <paldaruo_root_dir> -a <alphabet file> -o <csv file>

    <paldaruo_root_dir> - destination folder for paldaruo corpus download
    <alphabet_file> - flename and path for generated alphabet file  
    <csv file> - filename and path for generated csv file

© Prifysgol Bangor University

"""

PALDARUO_DATA_URL="https://git.techiaith.bangor.ac.uk/Data-Porth-Technolegau-Iaith/Corpws-Paldaruo"
PALDARUO_DATA_VERSION="v5.0"

DEFAULT_PALDARUO_DIR = '/data/paldaruo'
DEFAULT_PALDARUO_ALPHABET = '/DeepSpeech/bin/bangor_welsh/alphabet.txt'
DEFAULT_PALDARUO_CSV = '/data/paldaruo/deepspeech.csv'

prompts = {}

corpus = set()
bad_utterances = set()

def execute_shell(cmd):
    print('$ %s' % cmd)
    o = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in o.stdout:
        print (line.rstrip())
    print ('')


def initialize_bad_utterances(paldaruo_root_dir):
    all_info_sorted_filepath = os.path.join(paldaruo_root_dir, 'all_info.sorted.txt')
    if os.path.isfile(all_info_sorted_filepath):
        with open(all_info_sorted_filepath, 'r', encoding='utf-8') as all_info_sorted_file:
            for line in all_info_sorted_file:
                # we only require the utterance-id and number of errors, seperated by space at begining of line. 
                all_info_top_fields=line.split(' ', 2)
                utterance_id=all_info_top_fields[0]
                nerrors=int(all_info_top_fields[1])
                if nerrors > 0:
                        # convert from utterance id to wav file
                        bad_utterances.add(utterance_id)


def git_lfs_clone_paldaruo(corpus_dir):

    if not os.path.exists(corpus_dir):
        git_lfs_clone_cmd = "git -c http.sslVerify=false lfs clone --branch %s --depth 1 %s %s" % (PALDARUO_DATA_VERSION, PALDARUO_DATA_URL, corpus_dir)
        execute_shell(git_lfs_clone_cmd)


def unzip_zips(corpus_dir):       
    wav_zips_root = os.path.join(corpus_dir, 'audio', 'wav')
    if os.path.exists(wav_zips_root): 
        for file in os.listdir(os.path.join(wav_zips_root)):
            if file.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(wav_zips_root,file)) as paldaruo_zipfile:
                    print (file)
                    paldaruo_zipfile.extractall(corpus_dir)
        
        shutil.rmtree(wav_zips_root) 


def get_directory_structure(rootdir):
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir, followlinks=True):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = functools.reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir

    #topdirname = dir.iterkeys().next()
    #return dir[topdirname]
    return dir


def get_prompts(sourcefile):
    with open(sourcefile,'r', encoding='utf-8') as prompts_file:
        for line in prompts_file:
            elements = line.rstrip().split(' ',1)
            key = elements[0].replace('*/','')
            prompts[key]=elements[1]

    return prompts


def main(paldaruo_root_dir, deepspeech_csv_file, alphabet_file_path, paldaruo_uid='', **args):

    git_lfs_clone_paldaruo(paldaruo_root_dir)
    unzip_zips(paldaruo_root_dir)

    initialize_bad_utterances(paldaruo_root_dir)

    paldaruo_files = get_directory_structure(paldaruo_root_dir)
    paldaruo_metadata = csv.DictReader(open(os.path.join(paldaruo_root_dir,'metadata.csv'), 'r', encoding='utf-8'))
    get_prompts(os.path.join(paldaruo_root_dir, 'samples.txt'))
   
    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript', 'amlder', 'byw', 'iaithgyntaf', 'plentyndod', 'rhanbarth', 'cyd_destun', 'rhyw', 'blwyddyngeni']
    csv_file_out = csv.DictWriter(open(deepspeech_csv_file, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()

    rejected_csv_fieldnames = ['wav_filename', 'transcript', 'reason']
    rejected_csv_file_path = deepspeech_csv_file.replace(".csv",".rejected.csv")
    rejected_csv_file_out = csv.DictWriter(open(rejected_csv_file_path, 'w', encoding='utf-8'), fieldnames=rejected_csv_fieldnames)
    rejected_csv_file_out.writeheader()

    # @todo - allbynnu metadata eraill i (ail) ffeil csv (paldaruo.csv) 
    # uid,amlder,byw,iaithgyntaf,ysgoluwchradd,plentyndod,rhanbarth,cyd_destun,rhyw,blwyddyngeni

    text_preprocessor = TextPreProcessor(alphabet_file_path)

    for row in paldaruo_metadata:
        uid=row['uid']

        print (uid)
        if os.path.isdir(os.path.join(paldaruo_root_dir, uid)):
            for top in paldaruo_files:
                for wavfile in paldaruo_files[top][uid]:
                    filepath=os.path.join(paldaruo_root_dir, uid, wavfile)
                    if not os.path.isfile(filepath): continue
                    if wavfile.startswith("silence"): continue
                    if audio_processing_utils.get_duration_wav(filepath) < 5 : continue
                    if audio_processing_utils.downsample_wavfile(filepath):
                        prompt_id=wavfile.replace(".wav","")
                        prompt = prompts[prompt_id]

                        print (prompt)
    
                        success, reason, transcript = text_preprocessor.clean(prompt)

                        if success is False:
                            rejected_csv_file_out.writerow({
                                'wav_filename':filepath,
                                'transcript':transcript,
                                'reason':reason})
                            continue

                        if not audio_processing_utils.is_feasible_transcription(filepath, transcript):
                            rejected_csv_file_out.writerow({
                                'wav_filename':filepath,
                                'transcript':transcript,
                                'reason':'Not feasible transcript'})
                            continue

                        corpus.add(transcript)

                        hashed_filename = hashlib.md5(filepath.encode('utf-8')).hexdigest()

                        if uid + '_' + hashed_filename not in bad_utterances:
                            output_entry = {
                                'wav_filename':filepath,
                                'wav_filesize':os.path.getsize(filepath),
                                'transcript':transcript.encode('utf-8'),
                                'amlder': row['amlder'],
                                'byw': row['byw'],
                                'iaithgyntaf': row['iaithgyntaf'],
                                'plentyndod': row['plentyndod'],
                                'rhanbarth': row['rhanbarth'],
                                'cyd_destun': row['cyd_destun'],
                                'rhyw': row['rhyw'],
                                'blwyddyngeni': row['blwyddyngeni']
                            }
                            print (filepath, os.path.getsize(filepath), transcript.encode('utf-8'))
                            csv_file_out.writerow(output_entry)

    #
    text_file_path=os.path.join(paldaruo_root_dir,"corpus.txt")

    language_modelling_utils.save_corpus(corpus, text_file_path)
    lm_root_dir = os.path.dirname(text_file_path)
    lm_binary_file_path = os.path.join(lm_root_dir, "lm.binary")
    trie_file_path = os.path.join(lm_root_dir, "trie")

    language_modelling_utils.create_binary_language_model(lm_binary_file_path, text_file_path)
    language_modelling_utils.create_trie(trie_file_path, alphabet_file_path, lm_binary_file_path)

    print ("Import paldaruo to %s finished. " % (paldaruo_root_dir))


             
if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("-a", dest="alphabet_file_path", default=DEFAULT_PALDARUO_ALPHABET)
    parser.add_argument("-i", dest="paldaruo_root_dir", default=DEFAULT_PALDARUO_DIR)
    parser.add_argument("-o", dest="deepspeech_csv_file", default=DEFAULT_PALDARUO_CSV)

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

