#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import argparse
import numpy as np
import shlex
import subprocess
import wave
import codecs
import csv

from deepspeech import Model, printVersions
from timeit import default_timer as timer

from wer import wer

try:
    from shhlex import quote
except ImportError:
    from pipes import quote

# These constants control the beam search decoder

# Beam width used in the CTC decoder when building candidate transcriptions
BEAM_WIDTH = 500

# The alpha hyperparameter of the CTC decoder. Language Model weight
LM_ALPHA = 20

# The beta hyperparameter of the CTC decoder. Word insertion bonus.
LM_BETA = 1.85


# These constants are tied to the shape of the graph used (changing them changes
# the geometry of the first layer), so make sure you use the same constants that
# were used during training

# Number of MFCC features to use
N_FEATURES = 26

# Size of the context window used for producing timesteps in the input vector
N_CONTEXT = 9

def convert_samplerate(audio_path):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate 16000 - '.format(quote(audio_path))
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use 16kHz files or install it: {}'.format(e.strerror))

    return 16000, np.frombuffer(output, np.int16)


class VersionAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        super(VersionAction, self).__init__(nargs=0, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        printVersions()
        exit(0)

def main(model, alphabet, lm, trie, testset_csv, **args):

    print('Loading model from file {}'.format(model), file=sys.stderr)
    model_load_start = timer()
    ds = Model(model, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s.'.format(model_load_end), file=sys.stderr)

    print('Loading language model from files {} {}'.format(lm, trie), file=sys.stderr)
    lm_load_start = timer()
    ds.enableDecoderWithLM(alphabet, lm, trie, LM_ALPHA, LM_BETA)
    lm_load_end = timer() - lm_load_start
    print('Loaded language model in {:.3}s.'.format(lm_load_end), file=sys.stderr)

    result_file = codecs.open('testresults.txt', 'w', encoding='utf-8')

    with codecs.open(testset_csv, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            fin = wave.open(row["wav_filename"], 'rb')
            fs = fin.getframerate()
            if fs != 16000:
                print('Warning: original sample rate ({}) is different than 16kHz. Resampling might produce erratic speech recognition.'.format(fs), file=sys.stderr)
                fs, audio = convert_samplerate(args.audio)
            else:
                audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

            audio_length = fin.getnframes() * (1/16000)
            fin.close()

            #print('Running inference.', file=sys.stderr)
            inference_start = timer()
            hypothesis = ds.stt(audio, fs)
            inference_end = timer() - inference_start

            result_file.write('%s\t%s\t%s\n' % (hypothesis, row["transcript"], wer(row["transcript"].split(), hypothesis.split())))

            print('%s , %s. Inference took %0.3fs for %0.3fs audio file.' % (hypothesis, row["transcript"], inference_end, audio_length), file=sys.stderr)

    result_file.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Running DeepSpeech inference.')
    parser.add_argument('--model', 
                        dest="model",
                        default='/data/output/output_graph.pb',
                        help='Path to the model (protocol buffer binary file)')
    parser.add_argument('--alphabet', 
                        dest='alphabet',
                        default='/data/output/alphabet.txt',
                        help='Path to the configuration file specifying the alphabet used by the network')
    parser.add_argument('--lm', nargs='?',
                        dest='lm',
                        default='/data/output/lm.binary',
                        help='Path to the language model binary file')
    parser.add_argument('--trie', nargs='?',
                        dest='trie',
                        default='/data/output/trie',
                        help='Path to the language model trie file created with native_client/generate_trie')
    parser.add_argument('--csv',
                        dest='testset_csv',
                        default='/data/testsets/macsen/deepspeech.csv',
                        help='Path to test set csv file')
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

