#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import pandas as pd

from sklearn.model_selection import KFold
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split

import argparse

def main(csvfile, dest_dir, k, **args):

    kf = KFold(n_splits=k, shuffle=True, random_state=2)
    speech_corpus_df = pd.read_csv(csvfile, encoding='utf-8')

    fold_num = 0
    for train_indexes, test_indexes in kf.split(speech_corpus_df):
        fold_num+=1

        train_file = os.path.join(dest_dir, 'train_' + str(fold_num) + '.csv')
        train_df = pd.DataFrame(speech_corpus_df.ix[train_indexes])
        train_df.to_csv(train_file, sep=',', encoding='utf-8')
        
        test_file = os.path.join(dest_dir, 'test_' + str(fold_num) + '.csv')
        test_df = pd.DataFrame(speech_corpus_df.ix[test_indexes])
        test_df.to_csv(test_file, sep=',', encoding='utf-8')

        print ('train: %s, test %s' % (train_indexes, test_indexes))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='k-fold')

    parser.add_argument('--k', 
                        dest="k",
                        default=10,
                        help='k')

    parser.add_argument('--csv', 
                        dest='csvfile',
                        default='/data/paldaruo/deepspeech.csv',
                        help='DeepSpeech CSV file.')

    parser.add_argument('--dest_dir',
                        dest='dest_dir',
                        default='/data/paldaruo',
                        help='dest dir')

    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))

