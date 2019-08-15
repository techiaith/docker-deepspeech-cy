import pandas as pd
import numpy as np
import scipy.io.wavfile as wav

from python_speech_features import mfcc

N_CONTEXT=9

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

df = pd.read_csv('/data/corpws_s4c/test_1.csv')

def aftiv_length(row):
    return audiofile_to_input_vector(row['wav_filename'], 26, N_CONTEXT).shape[0] - 2*N_CONTEXT

def trans_length(row):
    return len(row['transcript'])

df['aftiv_len'] = df.apply(aftiv_length, axis=1)
df['trans_len'] = df.apply(trans_length, axis=1)
df['good_flag'] = df.aftiv_len > df.trans_len

df.to_csv('/data/corpws_s4c/test_validation_1.csv', index=False, sep=',', encoding='utf-8')

