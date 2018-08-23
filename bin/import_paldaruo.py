#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import codecs
import csv

import shlex
import shutil
import zipfile
import subprocess

import wave
from sox import Transformer

from argparse import ArgumentParser, RawTextHelpFormatter


DESCRIPTION = """

Llwytho i lawr Corpws Paldaruo a'i addasu ar gyfer DeepSpeech

Download Paldaruo Speech Corpus and make it available for DeepSpeech

© Prifysgol Bangor University

"""

#UTF8Writer = codecs.getwriter('utf8')
#sys.stdout = UTF8Writer(sys.stdout)

PALDARUO_DATA_URL="https://git.techiaith.bangor.ac.uk/Data-Porth-Technolegau-Iaith/Corpws-Paldaruo"
PALDARUO_DATA_VERSION="v4.0"

prompts = {}

def git_lfs_clone_paldaruo(corpus_dir):

    if not os.path.exists(corpus_dir):
        git_lfs_clone_cmd = "git -c http.sslVerify=false lfs clone --branch %s --depth 1 %s %s" % (PALDARUO_DATA_VERSION, PALDARUO_DATA_URL, corpus_dir)
	print git_lfs_clone_cmd
        o = subprocess.Popen(shlex.split(git_lfs_clone_cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in o.stdout:
            print line,  
       
    wav_zips_root = os.path.join(corpus_dir, 'audio', 'wav')
    if os.path.exists(wav_zips_root): 
        for file in os.listdir(os.path.join(wav_zips_root)):
            if file.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(wav_zips_root,file)) as paldaruo_zipfile:
                    print file
                    paldaruo_zipfile.extractall(corpus_dir)
        
        shutil.rmtree(wav_zips_root) 


def get_directory_structure(rootdir):
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir, followlinks=True):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir

    topdirname = dir.iterkeys().next()
    return dir[topdirname]


def get_prompts(sourcefile):
    with codecs.open(sourcefile,'r', encoding='utf-8') as prompts_file:
        for line in prompts_file:
            elements = line.rstrip().split(' ',1)
            key = elements[0].replace('*/','')
            prompts[key]=elements[1]

    return prompts


def get_duration_wav(wavfile):
    f = wave.open(wavfile, 'r')
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    f.close()
    return duration


def get_alphabet(transcript):
    return set(transcript)


def process_transcript(orig_transcript):
    transcript = orig_transcript.replace("_"," ")
    transcript = transcript.replace("-"," ")
    transcript = transcript.lower()

    return transcript 


def downsample_wavfile(wavfile):
    temp_48kHz_wavfile = wavfile.replace(".wav","_48kHz.wav")
    shutil.move(wavfile, temp_48kHz_wavfile)

    tf = Transformer()
    tf.convert(samplerate=16000, n_channels=1)
    tf.build(temp_48kHz_wavfile, wavfile)
    os.remove(temp_48kHz_wavfile)

    return True


def main(paldaruo_root_dir, csv_file, alphabet_file, **args):

    git_lfs_clone_paldaruo(paldaruo_root_dir)

    paldaruo_files = get_directory_structure(paldaruo_root_dir)
    paldaruo_metadata = csv.DictReader(codecs.open(os.path.join(paldaruo_root_dir,'metadata.csv'), 'r', encoding='utf-8'))
    get_prompts(os.path.join(paldaruo_root_dir, 'samples.txt'))
   
    moz_fieldnames = ['wav_filename','wav_filesize', 'transcript']
    csv_file_out = csv.DictWriter(codecs.open(csv_file, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()

    alphabet = set()

    for row in paldaruo_metadata:
        uid=row['uid']
        if os.path.isdir(os.path.join(paldaruo_root_dir, uid)):
            for wavfile in paldaruo_files[uid]:
                filepath=os.path.join(paldaruo_root_dir, uid, wavfile)
                if not os.path.isfile(filepath): continue
                if wavfile.startswith("silence"): continue
                if get_duration_wav(filepath) < 5 : continue
                transcript = process_transcript(prompts[wavfile.replace(".wav","")])
                alphabet = alphabet.union(get_alphabet(transcript)) 
                if downsample_wavfile(filepath):
                    print filepath, os.path.getsize(filepath), transcript.encode('utf-8') 
                    csv_file_out.writerow({'wav_filename':filepath, 'wav_filesize':os.path.getsize(filepath), 'transcript':transcript.encode('utf-8')})

    with codecs.open(alphabet_file, "w", encoding='utf-8') as alphabet_file_out:
        for c in sorted(alphabet):
            alphabet_file_out.write('%s\n' % c) 
     
           
if __name__ == "__main__":

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)

    parser.add_argument("-i", dest="paldaruo_root_dir", required=True)
    parser.add_argument("-a", dest="alphabet_file", required=True)
    parser.add_argument("-o", dest="csv_file", required=True)
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

