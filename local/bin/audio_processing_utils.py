#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import os
import shutil

import wave
from sox import Transformer

import pandas as pd
import numpy as np
import scipy.io.wavfile as wav

from python_speech_features import mfcc

N_CONTEXT=9


def downsample_wavfile(wavfile):
    temp_48kHz_wavfile = wavfile.replace(".wav","_48kHz.wav")
    shutil.move(wavfile, temp_48kHz_wavfile)
    transform_audio(temp_48kHz_wavfile, wavfile)
    os.remove(temp_48kHz_wavfile)
    return True


def convert_mp3(mp3file):
    wavfile = mp3file.replace(".mp3",".wav")
    try:
        transform_audio(mp3file, wavfile)
        return True
    except:
        return False



def transform_audio(old_file, new_file):
    tf = Transformer()
    tf.convert(samplerate=16000, n_channels=1)
    tf.build(old_file, new_file)

def get_duration_wav(wavfile):
    f = wave.open(wavfile, 'r')
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    f.close()
    return duration


def audiofile_to_input_vector(audio_filename, numcep, numcontext):
    r"""
    Given a WAV audio file at ``audio_filename``, calculates ``numcep`` MFCC features
    at every 0.01s time step with a window length of 0.025s. Appends ``numcontext``
    context frames to the left and right of each time step, and returns this data
    in a numpy array.
    """
    # Load wav files
    fs, audio = wav.read(audio_filename)

    # Get mfcc coefficients
    features = mfcc(audio, samplerate=fs, numcep=numcep, winlen=0.032, winstep=0.02, winfunc=np.hamming)

    # Add empty initial and final contexts
    empty_context = np.zeros((numcontext, numcep), dtype=features.dtype)
    features = np.concatenate((empty_context, features, empty_context))

    return features


def is_feasible_transcription(wavfile, transcription):
    try:
        aftiv_length=audiofile_to_input_vector(wavfile, 26, N_CONTEXT).shape[0] - 2*N_CONTEXT
    except:
        return False

    return aftiv_length > len(transcription)


