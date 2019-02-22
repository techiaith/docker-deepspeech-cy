#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from corporacreator import Corpora
from corporacreator import parse_args



def append(args, key, value):
    args.append(key + value)
    return args


def execute(destination, clips_file_path, locale):
    args = []
    args = append(args, '-d', destination) #'/data/commonvoice-cy')
    args = append(args, '-f', clips_file_path) # '/data/commonvoice-cy/clips.tsv')
    args = append(args, '-l', locale) # 'cy')
    args = append(args, '-v','')
    args = parse_args(args)

    corpora = Corpora(args)
    corpora.create()
    corpora.save(args.directory)

