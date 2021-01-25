#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import hashlib
import gzip
import pandas
import requests
import json

from enum import Enum

import tarfile
import gzip
import shutil
import functools

from urllib.parse import urlparse

from praatio import tgio

from pathlib import Path
from git import Repo
from pydub import AudioSegment

import utils.kfold as kfold
import utils.audio as audio

from tqdm import tqdm

from utils.clean_transcript import clean_transcript

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """
Llwytho i lawr set data Macsen ar gyfer DeepSpeech o fewn yr ap Macsen 

Mae angen rhoid lleoliad i ffeil alphabet.txt

© Prifysgol Bangor University

"""

ALPHABET_FILE_PATH = "/DeepSpeech/bin/bangor_welsh/alphabet.txt"

TESTSET_URL = "https://git.techiaith.bangor.ac.uk/data-corpws-mewnol/corpws-profi-deepspeech"



def clone_testset(target_testset_dir):
    Repo.clone_from(TESTSET_URL, target_testset_dir)


def get_commonvoice_textcorpus(commonvoice_validated_csv_file_path, lm_data_root_dir):
    
    print ("Extracting texts from CommonVoice: %s " % commonvoice_validated_csv_file_path)
    if not os.path.isfile(commonvoice_validated_csv_file_path):
        print ("Proceeding with missing file %s " % commonvoice_validated_csv_file_path)

    target_dir = os.path.join(lm_data_root_dir, 'commonvoice')
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    corpus_file_path = os.path.join(target_dir, "corpus.txt")

    df = pandas.read_csv(commonvoice_validated_csv_file_path, encoding='utf-8', sep='\t', header=0, dtype={'sentence':str})
    sentences = df['sentence']

    with open(corpus_file_path, 'w', encoding='utf-8') as corpus_file:
        for t in sentences:
            corpus_file.write(t + "\n")

    return clean_text_corpus(target_dir)       



def get_oscar_textcorpus(oscar_archive_file_path, lm_data_root_dir):

    print ("Extracting: %s" % oscar_archive_file_path)

    target_dir = os.path.join(lm_data_root_dir, 'oscar')
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    oscar_corpus_file_path = oscar_archive_file_path.replace('.gz','')
    corpus_file_path = os.path.join(target_dir, "corpus.txt")

    with gzip.open(oscar_archive_file_path, 'rb') as oscar_archive_file:
        with open(oscar_corpus_file_path, 'wb') as oscar_file:
            shutil.copyfileobj(oscar_archive_file, oscar_file)
    
    shutil.move(oscar_corpus_file_path, corpus_file_path)

    return clean_text_corpus(target_dir)




def get_macsen_textcorpus(lm_data_root_dir):

    target_dir = os.path.join(lm_data_root_dir, 'macsen')
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    json_data = json.loads(requests.get("https://api.techiaith.org/assistant/get_all_sentences").text)
    with open(os.path.join(target_dir, "corpus.txt"), 'w', encoding='utf-8') as macsen_file_out: 
        for s in json_data["result"]:
            macsen_file_out.write(s[0] + "\n")

    return clean_text_corpus(target_dir)



def clean_text_corpus(lm_data_root_dir):

    print ("Cleaning corpus files in %s " % lm_data_root_dir)
    
    source_text_file_path = os.path.join(lm_data_root_dir, "corpus.txt")
    output_text_file_path = os.path.join(lm_data_root_dir, "corpus.clean.txt")

    ooa_text_file_path = source_text_file_path.replace(".txt", ".ooa.txt")
    clean = clean_transcript(ALPHABET_FILE_PATH, ooa_text_file_path)
    
    with open(output_text_file_path, 'w', encoding='utf-8') as out_file:
        with open(source_text_file_path, 'r', encoding='utf-8') as in_file:
            for i, transcript in enumerate(tqdm(in_file)):
                cleaned, transcript = clean.clean(transcript)
                if cleaned:
                    out_file.write(transcript.lower() + "\n")

    return output_text_file_path


def get_directory_structure(rootdir):
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir, followlinks=True):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = functools.reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir

    return dir


def join_corpus_files(corpus_files, target_languagemodel_data_root_dir):
    
    print ("Join corpus text files %s " % corpus_files)

    corpus_file_path = os.path.join(target_languagemodel_data_root_dir, "corpus.txt")

    with open(corpus_file_path, 'w', encoding='utf-8') as corpus_outfile:
        for fname in corpus_files:
            with open(fname, 'r', encoding='utf-8') as corpus_infile:
                for line in corpus_infile:
                    corpus_outfile.write(line)

    return clean_text_corpus(target_languagemodel_data_root_dir)


def import_textgrid_test(target_data_root_dir):

    print ("Importing transcripts from files in %s " % target_data_root_dir)

    target_clips_dir = os.path.join(target_data_root_dir, "clips")
    Path(target_clips_dir).mkdir(parents=True, exist_ok=True)

    csv_file_path = os.path.join(target_data_root_dir, 'deepspeech.csv')
    textgrid_file_path = os.path.join(target_data_root_dir, 'sain.TextGrid')
    audio_file = AudioSegment.from_wav(os.path.join(target_data_root_dir, 'sain.wav'))

    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
    with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
    
        csv_file_out = csv.DictWriter(csv_file, fieldnames=moz_fieldnames)
        csv_file_out.writeheader()

        ooa_text_file_path = os.path.join(target_data_root_dir, 'deepspeech.ooa.txt')
        clean = clean_transcript(ALPHABET_FILE_PATH, ooa_text_file_path)

        tg = tgio.openTextgrid(textgrid_file_path)
        entryList = tg.tierDict["utterance"].entryList

        for interval in entryList:
            text = interval.label        
            cleaned, transcript = clean.clean(text)
            
            if cleaned and len(transcript)>0:
                transcript = transcript.lower()
                
                start = float(interval.start) * 1000
                end = float(interval.end) * 1000

                #print (start, end, transcript)

                split_audio = audio_file[start:end]  
                hashId = hashlib.md5(transcript.encode('utf-8')).hexdigest()
                wav_segment_filepath = os.path.join(target_clips_dir, hashId + ".wav")   
                split_audio.export(wav_segment_filepath, format="wav")

                csv_file_out.writerow({
                                    'wav_filename':wav_segment_filepath, 
                                    'wav_filesize':os.path.getsize(wav_segment_filepath), 
                                    'transcript':transcript
                                })
    
    return pandas.read_csv(csv_file_path, delimiter=',', encoding='utf-8')

   
def import_textgrid_test(target_data_root_dir):

    print ("Importing transcripts from files in %s " % target_data_root_dir)

    target_clips_dir = os.path.join(target_data_root_dir, "clips")
    Path(target_clips_dir).mkdir(parents=True, exist_ok=True)

    csv_file_path = os.path.join(target_data_root_dir, 'deepspeech.csv')
    textgrid_file_path = os.path.join(target_data_root_dir, 'sain.TextGrid')
    audio_file = AudioSegment.from_wav(os.path.join(target_data_root_dir, 'sain.wav'))

    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
    with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
    
        csv_file_out = csv.DictWriter(csv_file, fieldnames=moz_fieldnames)
        csv_file_out.writeheader()

        ooa_text_file_path = os.path.join(target_data_root_dir, 'deepspeech.ooa.txt')
        clean = clean_transcript(ALPHABET_FILE_PATH, ooa_text_file_path)

        tg = tgio.openTextgrid(textgrid_file_path)
        entryList = tg.tierDict["utterance"].entryList

        for interval in entryList:
            text = interval.label        
            cleaned, transcript = clean.clean(text)
            
            if cleaned and len(transcript)>0:
                transcript = transcript.lower()
                
                start = float(interval.start) * 1000
                end = float(interval.end) * 1000

                #print (start, end, transcript)

                split_audio = audio_file[start:end]  
                hashId = hashlib.md5(transcript.encode('utf-8')).hexdigest()
                wav_segment_filepath = os.path.join(target_clips_dir, hashId + ".wav")   
                split_audio.export(wav_segment_filepath, format="wav")

                csv_file_out.writerow({
                                    'wav_filename':wav_segment_filepath, 
                                    'wav_filesize':os.path.getsize(wav_segment_filepath), 
                                    'transcript':transcript
                                })
    
    return pandas.read_csv(csv_file_path, delimiter=',', encoding='utf-8')


def import_clips_dir(target_testset_dir, **args):

    print ("Importing clips dir in %s " % target_testset_dir)

    arddweud_root_dir = get_directory_structure(os.path.join(target_testset_dir, "clips"))
    
    csv_file_path = os.path.join(target_testset_dir, 'deepspeech.csv')
    print (csv_file_path)

    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
    csv_file_out = csv.DictWriter(open(csv_file_path, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()

    ooa_text_file_path = os.path.join(target_testset_dir, 'deepspeech.ooa.txt')
    clean = clean_transcript(ALPHABET_FILE_PATH, ooa_text_file_path)

    for filename in arddweud_root_dir["clips"]:
        if filename.endswith(".wav"):
            wavfilepath = os.path.join(target_testset_dir, "clips", filename)
            txtfilepath = wavfilepath.replace(".wav", ".txt")
            with open(txtfilepath, "r", encoding='utf-8') as txtfile:
                transcript = txtfile.read()
                cleaned, transcript = clean.clean(transcript)
                if cleaned:
                    transcript = transcript.lower()
                    if audio.downsample_wavfile(wavfilepath):                        
                        # print (wavfilepath)
                        csv_file_out.writerow({
                            'wav_filename':wavfilepath, 
                            'wav_filesize':os.path.getsize(wavfilepath), 
                            'transcript':transcript
                        })
    
    return pandas.read_csv(csv_file_path, delimiter=',', encoding='utf-8')                                         
    

def import_macsen_testset(target_testset_dir, **args):

    print ("Importing Macsen test sets")

    macsen_root_dir = get_directory_structure(target_testset_dir)
    
    csv_file_path = os.path.join(target_testset_dir, 'deepspeech.csv')

    moz_fieldnames = ['wav_filename', 'wav_filesize', 'transcript']
    csv_file_out = csv.DictWriter(open(csv_file_path, 'w', encoding='utf-8'), fieldnames=moz_fieldnames)
    csv_file_out.writeheader()

    ooa_text_file_path = os.path.join(target_testset_dir, 'deepspeech.ooa.txt')
    clean = clean_transcript(ALPHABET_FILE_PATH, ooa_text_file_path)

    for userid in macsen_root_dir["macsen"]["clips"]:                
        for filename in macsen_root_dir["macsen"]["clips"][userid]:                        
            if filename.endswith(".wav"):
                wavfilepath = os.path.join(target_testset_dir, "clips", userid, filename)
                txtfilepath = wavfilepath.replace(".wav", ".txt")
                with open(txtfilepath, "r", encoding='utf-8') as txtfile:
                    transcript = txtfile.read()
                    cleaned, transcript = clean.clean(transcript)
                    if cleaned:
                        transcript = transcript.lower()
                        if audio.downsample_wavfile(wavfilepath):                        
                            #print (wavfilepath)
                            csv_file_out.writerow({
                                'wav_filename':wavfilepath, 
                                'wav_filesize':os.path.getsize(wavfilepath), 
                                'transcript':transcript
                            })
                                                
    kfold.create_kfolds(csv_file_path, target_testset_dir, 10)
   



def main(target_bangor_root_dir, oscar_archive_file_path, commonvoice_validated_csv_file_path, **args):

    #
    target_testset_root_dir = os.path.join(target_bangor_root_dir, "testsets")
    target_languagemodel_data_root_dir = os.path.join(target_bangor_root_dir, "lm-data")

    clone_testset(target_testset_root_dir)

    # import audio and transcripts    
    df_csvs=[]
    df_csvs.append(import_textgrid_test(os.path.join(target_testset_root_dir, "data", "trawsgrifio", "OpiwHxPPqRI")))
    df_csvs.append(import_clips_dir(os.path.join(target_testset_root_dir, "data", "trawsgrifio", "arddweud_200617")))
    
    
    ##
    df_all_transcript_csvs = pandas.concat(df_csvs)
    df_all_transcript_csvs.to_csv(os.path.join(target_testset_root_dir, "data", "trawsgrifio", "deepspeech.csv"), encoding='utf-8', index=False)


    #
    import_macsen_testset(os.path.join(target_testset_root_dir, "data", "macsen"))

    #
    get_macsen_textcorpus(target_languagemodel_data_root_dir)

    #
    corpus_files = []
    corpus_files.append(get_oscar_textcorpus(oscar_archive_file_path, target_languagemodel_data_root_dir))        
    corpus_files.append(get_commonvoice_textcorpus(commonvoice_validated_csv_file_path, target_languagemodel_data_root_dir))

    #
    corpus_file_path = join_corpus_files(corpus_files, target_languagemodel_data_root_dir)
    print ("Text corpus ready at %s " % corpus_file_path )


    #
    print ("Import Bangor data to %s finished." % (target_testset_root_dir))



if __name__ == "__main__":
    
    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter)    
    parser.add_argument("-b", dest="target_bangor_root_dir", default="/data/bangor")        
    parser.add_argument("-o", dest="oscar_archive_file_path", required=True)
    parser.add_argument("-c", dest="commonvoice_validated_csv_file_path", required=True)
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
