#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import shutil

import wave
from sox import Transformer

def downsample_wavfile(wavfile):
    temp_48kHz_wavfile = wavfile.replace(".wav","_48kHz.wav")
    shutil.move(wavfile, temp_48kHz_wavfile)
    transform_audio(temp_48kHz_wavfile, wavfile)
    os.remove(temp_48kHz_wavfile)
    return True


def convert_mp3(mp3file):
    wavfile = mp3file.replace(".mp3",".wav")
    transform_audio(mp3file, wavfile) 
    return True


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
