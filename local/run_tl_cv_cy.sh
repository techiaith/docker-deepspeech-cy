#!/bin/bash
set -xe

train_files=/data/commonvoice-cy-v4-20191210/deepspeech.validated.csv,/data/commonvoice-cy-v4-20191210/deepspeech.other.csv

alphabet_cy_file=/DeepSpeech/bin/bangor_welsh/alphabet.txt
lm_scorer_path=/data/texts/oscar_commonvoice/kenlm.scorer

checkpoint_dir=/checkpoints
export_dir=/export/cv-tl-cy
summary_dir=/keep/transfer/summaries

# Force UTF-8 output
export PYTHONIOENCODING=utf-8

checkpoint_en_dir="${checkpoint_dir}/en"
checkpoint_cy_dir="${checkpoint_dir}/cy"

rm -rf ${checkpoint_en_dir}
rm -rf ${checkpoint_cy_dir}
rm -rf $export_dir
rm -rf $summary_dir

mkdir -p ${checkpoint_en_dir}
mkdir -p ${checkpoint_cy_dir}

cp -rv /checkpoints/mozilla/deepspeech-en-checkpoint/ $checkpoint_en_dir

set +x
echo "####################################################################################"
echo "#### Transfer to WELSH model with --save_checkpoint_dir --load_checkpoint_dir   ####"
echo "####################################################################################"
set -x
python -u DeepSpeech.py \
	--train_files "${train_files}" --train_batch_size 64 \
	--drop_source_layers 2 \
	--epochs 10 \
	--alphabet_config_path "${alphabet_cy_file}" \
	--load_checkpoint_dir "${checkpoint_en_dir}" \
	--save_checkpoint_dir "${checkpoint_cy_dir}"
	