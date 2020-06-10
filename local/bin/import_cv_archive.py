#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import pathlib
import tarfile

import shlex
import subprocess

from argparse import ArgumentParser, RawTextHelpFormatter

DESCRIPTION = """

"""

def extract(source_tar_gz, target_dir):
    print ("Extracting: %s" % source_tar_gz)
    tar = tarfile.open(source_tar_gz, "r:gz")
    tar.extractall(target_dir)
    tar.close()


def main(cv_archive_file_path, **args):

    cv_root_dir = pathlib.Path(cv_archive_file_path).parent
    extract(cv_archive_file_path, cv_root_dir)
    
    cmd = "python3 /DeepSpeech/bin/import_cv2.py %s" % (cv_root_dir)

    import_process = subprocess.Popen(shlex.split(cmd))
    import_process.wait()

   
if __name__ == "__main__": 

    parser = ArgumentParser(description=DESCRIPTION, formatter_class=RawTextHelpFormatter) 

    parser.add_argument("--archive", dest="cv_archive_file_path", required=True, help="path to downloaded CommonVoice tar.gz file")
   
    parser.set_defaults(func=main)
    args = parser.parse_args()
    args.func(**vars(args))
